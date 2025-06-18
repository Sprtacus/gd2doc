# gd2doc

`gd2doc` is a small command line tool that parses GDScript files and produces Markdown that can be fed directly into MkDocs.

## Installation

Python 3.8 or newer is required together with the libraries [click](https://palletsprojects.com/p/click/) and [Jinja2](https://jinja.palletsprojects.com/). Install them using `pip`:

```bash
pip install click jinja2
```

You can either include this repository as a submodule or copy the source code into a directory such as `tools/gd2doc`. Invoke the script from that directory, e.g. `tools/gd2doc/gd2doc`.

### Using Nix

If you have [Nix](https://nixos.org) installed, the dependencies are also
available through the provided `shell.nix`.

```bash
nix-shell
```

This drops you into a shell where `click`, `Jinja2` and `pytest` are already
available so you don't need to install anything on your local system. From that
environment run the tool exactly as shown below.

## Usage

Run the tool with the ``gd2doc`` script and pass the directory or the individual ``.gd`` file. Use ``-o`` to set the destination directory for the generated Markdown files.

```bash
gd2doc <path-to-source> -o <output-directory>
```

Add `-r/--recursive` to also search subdirectories.

Use `--clean` to delete the output directory before generating new files.

### Example

```bash
gd2doc game/src -o docs --recursive
```

## Git pre-commit hook

To automatically run `gd2doc` before each commit, create a script at `.git/hooks/pre-commit` with the following content:

```bash
#!/bin/sh
gd2doc game/src -o docs --recursive
```

Don't forget to make the script executable:

```bash
chmod +x .git/hooks/pre-commit
```

This will keep your documentation up to date with every commit.

## Tests

Run the tests with `pytest`:

```bash
pytest -q
```
