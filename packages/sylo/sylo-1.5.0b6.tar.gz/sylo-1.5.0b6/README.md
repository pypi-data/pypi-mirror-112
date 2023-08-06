# SYLO (Sort Your Life Out)
[![PyPI version](https://badge.fury.io/py/sylo.svg)](https://badge.fury.io/py/sylo)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

### A Pomodoro Timer For Your Terminal

## Install

```shell
pip install sylo
```

## Run

```shell
sylo
```

## Configure

### Optional arguments

- `-w` `--work_time` Overwrite the default time in minutes to work (default is 25 minutes)
- `-r` `--rest_time` Overwrite the default time in minutes for a rest (default is 5 minutes)
- `-a` `--audio_file` Set absolute path to an audio file to play when the timer ends.
- `-t` `--theme` Choose a different color scheme from the default

> :warning: **Keep your audio files short!**: SYLO is not sophisticated enough to shorten them yet

### Example usage

```shell
sylo -w 20 -r 10 -a ~./path/to/my/audio/file.wav -t yellow
```

### Data file

Data is persisted to disk at `~/.sylo/sessions.dat`, if you remove the file you will lose your work history.

## Acknowledgements

SYLO uses;
- [beepy](https://github.com/prabeshdhakal/beepy-v1)
- [simpleaudio](https://github.com/hamiltron/py-simple-audio)
- [Termgraph](https://github.com/mkaz/termgraph)
