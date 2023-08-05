# mnemo-assistant

![Release ID](https://img.shields.io/github/release/ggirelli/mnemo-assistant.svg?style=flat) ![Release date](https://img.shields.io/github/release-date/ggirelli/mnemo-assistant.svg?style=flat)  
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mnemo) ![PyPI - Status](https://img.shields.io/pypi/status/mnemo) ![GitHub Actions Python package status](https://github.com/ggirelli/mnemo-assistant/workflows/Python%20package/badge.svg?branch=main&event=push)  
![license](https://img.shields.io/github/license/ggirelli/mnemo-assistant.svg?style=flat) ![Code size](https://img.shields.io/github/languages/code-size/ggirelli/mnemo-assistant.svg?style=flat)  
![Watch no.](https://img.shields.io/github/watchers/ggirelli/mnemo-assistant.svg?label=Watch&style=social) ![Stars no.](https://img.shields.io/github/stars/ggirelli/mnemo-assistant.svg?style=social)

[PyPi](https://pypi.org/project/mnemo/) | [docs](https://ggirelli.github.io/mnemo-assistant/)

A Python3.8+ web framework providing tools for journaling and note taking.

## Features (in short)

* Bottle-based web framework.
* Login system (currently supports one user at a time).

## Requirements

`mnemo-assistant` has been tested with Python 3.8 and 3.9. We recommend installing it using `pipx` (see [below](https://github.com/ggirelli/mnemo-assistant#install)) to avoid dependency conflicts with other packages. The packages it depends on are listed in our [dependency graph](https://github.com/ggirelli/mnemo-assistant/network/dependencies). We use [`poetry`](https://github.com/python-poetry/poetry) to handle our dependencies.

## Install

We recommend installing `mnemo-assistant` using [`pipx`](https://github.com/pipxproject/pipx). Check how to install `pipx` [here](https://github.com/pipxproject/pipx#install-pipx) if you don't have it yet! Once you have `pipx` ready on your system, install the latest stable release of `mnemo-assistant` by running: `pipx install mnemo-assistant`. If you see the stars (✨ 🌟 ✨), then the installation went well!

## Usage

Run `mnemo` to access the barber's services. Add `-h` to see the full help page of a command! Also, run `mnemo-autocomplete -s BASH_TYPE` to activate autocompletion. `BASH_TYPE` currently supports: `bash`, `fish`, and `zsh`.

## Contributing

We welcome any contributions to `mnemo-assistant`. In short, we use [`black`](https://github.com/psf/black) to standardize code format. Any code change also needs to pass `mypy` checks. For more details, please refer to our [contribution guidelines](https://github.com/ggirelli/mnemo-assistant/blob/main/CONTRIBUTING.md) if this is your first time contributing! Also, check out our [code of conduct](https://github.com/ggirelli/mnemo-assistant/blob/main/CODE_OF_CONDUCT.md).

## License

`MIT License - Copyright (c) 2021 Gabriele Girelli`
