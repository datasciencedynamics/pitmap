# pitmap documentation source

Sphinx source for https://datasciencedynamics.github.io/pitmap/. Lives on the
`docs` branch; the package itself is on `main`. Pushing here rebuilds the site
into `gh-pages`.

Local preview:

```bash
pip install -e ../pitmap -r docs/requirements.txt   # or: pip install pitmap --pre
sphinx-build -b html docs docs/_build/html
```
