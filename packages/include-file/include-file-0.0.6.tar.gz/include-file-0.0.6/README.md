# Include File

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

* Managing documentation is challenging as

1. Some information ([ex] setting up git command) might come up in multiple documentation
    * put overlaped info in common areas [include](#include_overwrite)
1. Hard to edit
1. Some files are too large so it's better to put link ([ex] jupyter, data files)
    * convert link to
1. Need entire file structure or show different instructions per language ([ex] python, java)
    * convert repository into file tab [in gitbook](#repo)

## Usage

* See before and after in tests folder

```sh
make e2etest
```

### Github CI

* This pipeline will push to deploy branch

```yml
# .github/workflows/main.yml
name: Deploy to deploy branch with include_file

on:
  push:
    branches: ["main"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install include_file
      - name: Include File
        run: |
          python -m include_file -u $GITHUB_ACTOR -y SUMMARY.md -d deploy -t README.md --stem

      # For deployment add following lines
      - uses: EndBug/add-and-commit@v7
        with:
          message: "Committed by seanhwangg/include_file"
          pull_strategy: NO-PULL
          branch: deploy
          push: origin deploy --force -u
```

## Flags

### user

* -u: github user id used for [link](#link) ([ex] seanhwangg)

### glob

* -g: Which glob files to include ([ex] **"\*\*/\*"**, **/*.md)

### path

* -p: Where to look for include file ([ex] **./.include-file/**)

### stem

* -s: Use stem of markdown to overwrite path ([ex] **False**)
* includes for `REAMD.md` are stored in `README/include.txt`

### validate

* -v: Whether to fail CI in case of include error ([ex] **True**)

## Gitbook Only Flags

> Note: These are completely optional for [Gitbook](https://gitbook.com/) users

### deploy_branch

* -d: Change deploy_branch of gitbook ([ex] **"deploy"**)

### url_path

* -url: Change url of includes ([ex] **<https://seanhwangg.gitbook.io/>**)

### table_of_contents

* -toc: Create table of contents with URL ([ex] **""**, "table_of_contents.md")

### relocate_include

* -r: Relocate images and include files ([ex] **None**)

### images_overwrite

* -images: Overwrite default `images` ([ex] **images**)

### include_overwrite

* -include: Overwrite default `include` ([ex] **include**)

> Input

```md
<!-- README.md  -->

* List before include
{% include '.include.txt' %}
* List after include

<!-- include.txt  -->
* I am in include
```

> Result

```md
<!-- README.md -->
* List before include
* I am in include
* List after include
```

### link_overwrite

* -link: Overwrite default `link` ([ex] **link**)

> Example

* Input

```md
<!-- README.md -->
* List before include
{% link 'include.txt' %}
* List after include

<!-- include.txt  -->
* I am in include
```

* Result

```md
<!-- REAMD.md -->
* List before include
[include.txt](https://github.com/[user]/[repository]/blob/[deploy_branch]/local.yml)
* List after include
```

### repo_overwrite

* -repo: Overwrite default `repo`
* Default: repo

> Input

```md
<!-- README.md  -->
* List before include
{% repo 'include' %}
* List after include

<!-- include/include1.md  -->
* I am in include1

<!-- include/nested/include2.md  -->
* I am in include2
```

> Result

![Result on gitbook web](images/20210626_114700.png)

```md
<!-- README.md -->
* List before include

{% tabs %}
{% tab title='include1.md' %}

* I am in include1

{% endtab %}
{% tab title='nested/include2.md' %}

* I am in include2

{% endtab %}
{% endtabs %}

* List after include
```
