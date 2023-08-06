from __future__ import annotations
from abc import ABC
from fileinput import FileInput

import logging
import re
from bs4 import BeautifulSoup
from subprocess import check_output
from dataclasses import dataclass, field
from pathlib import Path
from markdown import Markdown as Md
from typing import Optional


@dataclass
class Repository:
  path: Path
  glob: str
  include_path: str
  stem: bool
  deploy_branch: str
  user: str

  @property
  def url(self) -> str:
    return f"https://github.com/{self.user}/{self.path.name}/blob"

  def include_file(self):
    for markdown in File.files(self):
      line2txt = {}
      logging.info("Markdown: %s", markdown.path)
      for include in Include.includes(markdown):
        logging.info("Include: %s", include.name)
        line2txt[include.line_num] = include.to_markdown()
      with FileInput(markdown.path, inplace=True) as file:
        for i, line in enumerate(file, 1):
          if i in line2txt:
            print(line2txt[i], end="")
          else:
            print(line, end="")

  def relocate_include(self) -> None:
    logging.debug("relocate_include(%s)", self)

    files, path2include = File.files(self), {}
    logging.info("Total files %s", len(files))

    for file in files:
      for include in Include.includes(file):
        path2include[include.name] = include

    logging.debug(path2include)

    type2cnt = {}
    for child_include in IInclude.__subclasses__():
      type2cnt[child_include] = len(list(filter(lambda em: isinstance(em, child_include), path2include.values())))

    logging.info("type2cnt %s", type2cnt)

    actual = 0
    cnt = 0
    for file in files:
      for actual_path in [*file.path.parent.glob(f"{Image.OVERWRITE}/*"), *file.include_path.glob("*")]:
        actual += 1
        found_include = path2include.get(actual_path.name, None)
        if not found_include:
          continue
        correct_path = found_include.path
        if str(correct_path) != str(actual_path):
          actual_path.rename(correct_path / found_include.name)
          cnt += 1
          logging.info("Fixed %s -> %s", actual_path, correct_path / found_include.name)
          logging.info(found_include)
          logging.info(type(found_include))
          type2cnt[type(found_include)] -= 1

    logging.info("Left type2cnt %s", type2cnt)
    logging.info("%s wrong includes have been fixed", cnt)


@dataclass
class Gitbook(Repository):
  url_path: str
  summary: Optional[Markdown] = None
  toc: Optional[File] = None

  def __post_init__(self):
    logging.debug("__post_init__(%s)", self)
    if self.url_path == "":
      self.url_path = f"https://{self.user}.gitbook.io/{self.path.name}"

  def table_of_contents(self) -> str:
    logging.debug("generate_table_of_contents(%s)", self)
    assert self.summary

    lines = ["# Table of Contents"]
    for markdown in self.summary.extract_summary():
      lines.append(f"\n{'#' * (markdown.nest_count + 1)} {markdown.path.relative_to(self.path).name}\n")
      lines.append(markdown.table_of_contents(self.url_path))

    return "\n".join(lines) + "\n"


@dataclass
class File:
  repo: Repository
  path: Path
  content: str = field(repr=False, default="")

  def __post_init__(self):
    logging.debug("__post_init__(%s)", self)
    if self.content == "":
      try:
        self.content = self.path.read_text()
      except UnicodeDecodeError:
        self.content = ""

  @property
  def nest_count(self) -> int:
    return str(self.path.relative_to(self.repo.path)).count('/') + 1

  @property
  def include_path(self) -> Path:
    if self.repo.stem:
      include_path = self.path.parent / self.path.stem
    else:
      include_path = self.repo.path / self.repo.include_path
    if not include_path.is_dir():
      include_path.mkdir()
    return include_path

  @classmethod
  def files(cls, repo: Repository) -> list[File]:
    if isinstance(repo, Gitbook):
      assert repo.summary
      return [Markdown(repo, repo.path / path) for path in re.findall(Markdown.RE, repo.summary.content)]
    else:
      return [File(repo, file) for file in repo.path.glob(repo.glob) if file.is_file() and file.suffix != '.png']


class Markdown(File):
  RE = r"\((.*\.md)\)"  # * [Module](cpp/module.md) -> cpp/module.md

  @staticmethod
  def normalize(st):
    return st.lower().replace(' ', '-')

  def extract_summary(self) -> list[Markdown]:
    assert self.path.name == "SUMMARY.md"
    return [Markdown(self.repo, self.repo.path / path) for path in re.findall(Markdown.RE, self.content)]

  def extract_heading(self) -> list[tuple[int, str]]:
    logging.debug("extract_markdown()")
    text = Md(extensions=['fenced_code']).convert(self.content)
    md = BeautifulSoup(text, "html.parser")
    return [(int(str(line)[2]), str(line)[4:-5]) for line in md.find_all(re.compile('^h[1-6]$'))]

  def table_of_contents(self, url_path) -> str:
    logging.debug("table_of_contents(%s, %s)", self, url_path)
    lines = []
    for level, name in self.extract_heading():
      path = str(self.path.relative_to(self.repo.path)).replace(".md", "")
      lines.append(f"{'  ' * (level - 1)}* [{name}]({url_path}/{path}#{Markdown.normalize(name)})")
    return "\n".join(lines)


@dataclass
class IInclude(ABC):
  file: File
  name: str
  line_num: int
  txt: str

  @staticmethod
  def RE() -> str:
    pass

  @property
  def path(self) -> Path:
    return self.file.include_path / self.name

  def update_link(self, text: str) -> str:
    logging.debug("update_link(%s)", text)
    prefix = self.file.include_path.relative_to(self.file.repo.path)
    text = re.sub(r"(!\[.*\])\((.*)\)", rf'\1({prefix}/\2)', text.strip())
    return "".join(ch for i, ch in enumerate(text) if i <= 1 or not (text[i - 1] == text[i - 2] == ch == "\n")) + "\n"


@dataclass
class Include(IInclude):
  OVERWRITE = "include"

  @classmethod
  def includes(cls, file: File) -> list[IInclude]:
    includes = []
    for line_num, txt in enumerate(file.path.read_text().split("\n"), 1):
      for cls_ in IInclude.__subclasses__():
        match = re.match(cls_.RE(), txt)
        if match:
          name = match.group(1)
          include = cls_(file, name, line_num, txt)
          if "|" in name and isinstance(cls_, Repo):
            name, glob = name.split("|", 1)
            name, glob = name.strip(" '\""), glob.strip(" '\"")
            include.glob = glob
          includes.append(include)
    return includes

  @staticmethod
  def RE() -> str:
    return fr'{{% {Include.OVERWRITE} [\'"](.*)[\'"] %}}'

  def to_markdown(self):
    logging.debug("_include_to_markdown(%s)", self)
    assert self.path.is_file(), f"{self.path} is not a file"
    return self.update_link(self.path.read_text())


@dataclass
class Repo(IInclude):
  OVERWRITE = "repo"
  glob: str = "**/*"

  @staticmethod
  def RE() -> str:
    return fr'{{% {Repo.OVERWRITE} [\'"](.*)[\'"] %}}'

  def to_markdown(self):
    logging.debug("_repo_to_markdown(%s)", self.path)
    assert self.path.is_dir(), f"{self.path} is not a directory"
    lines = []
    ignored = [".gitignore"] + check_output("git ls-files --other", text=True, shell=True).splitlines()
    for file_glob in self.glob.split("|"):
      lines += ["{% tabs %}"]
      for file in self.path.glob(file_glob):
        if file.is_file() and file not in ignored:
          lines += [f"{{% tab title=\'{file.relative_to(self.path)}\' %}}\n"]
          suffix = file.suffix[1:]
          lines += [f"````{suffix if suffix else 'txt'}"]
          try:
            lines += [file.read_text()]
          except UnicodeDecodeError:
            raise Exception("Please do not include binary files")
          lines += ["````\n"]
          lines += ["{% endtab %}"]
      lines += ["{% endtabs %}\n"]
    return self.update_link("\n".join(lines))


@dataclass
class Link(IInclude):
  OVERWRITE = "link"

  @staticmethod
  def RE() -> str:
    return fr'{{% {Link.OVERWRITE} [\'"](.*)[\'"] %}}'

  def to_markdown(self):
    logging.debug("_link_to_markdown(%s)", self.path)
    repo = self.file.repo
    assert self.path.is_file(), f"{self.path} is not a file"
    return f"[{self.path.name}]({repo.url}/{repo.deploy_branch}/{self.path.relative_to(repo.path)})\n"


@dataclass
class Image(IInclude):
  OVERWRITE = "images"

  @property
  def path(self) -> Path:
    return self.file.include_path.parent / Image.OVERWRITE

  @staticmethod
  def RE() -> str:
    return rf".*!\[.*\]\(.*{Image.OVERWRITE}/(.*.png)\)"

  def to_markdown(self):
    logging.debug("_to_markdown(%s)", self)
    return self.txt
