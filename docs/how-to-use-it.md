# How to us it

## Mkdocs

Add the following to your `mkdocs.yml`:

```yaml
...
markdown_extensions:
  - pymdownx.snippets:
      url_download: True
...
```

Create a file where you want to render team members, e.g. `team.md`:

```markdown
;--8<-- "https://raw.githubusercontent.com/RoboticsBrno/Our-team/main/team.html"
```

In Github Actions, add the following to your workflow:
It will update the `team.md` file every month.

```yaml
on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 0 1 * *' # every month
jobs:
	...
```