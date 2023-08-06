# SYLO
[![PyPI version](https://badge.fury.io/py/sylo.svg)](https://badge.fury.io/py/sylo)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

### Sort Your Life Out with SYLO, a Pomodoro timer for your terminal!


## Install

### Mac + Linux only

```shell
pip install sylo
```


## Run

```shell
sylo
```


## Configure

### Config file

TOML Config file can be placed in the home directory `~/.sylo/sylo.cfg`.

```editorconfig
[general]
theme = "red"
audio_file = "/home/karen/Documents/my_funny_noise.wav"
time_segment_name = 'chips'

[durations]
work = 25
rest = 5


```

### Optional arguments

Arguments added through the command line will overwrite those in the config file.

- `-w` `--work_time` Overwrite the default time in minutes to work (default is 25 minutes)
- `-r` `--rest_time` Overwrite the default time in minutes for a rest (default is 5 minutes)
- `-a` `--audio_file` Set absolute path to an audio file to play when the timer ends.
- `-t` `--theme` Choose a different color scheme from the default

> :warning: **Keep your audio files short!**: SYLO is not sophisticated enough to shorten them yet

### Example usage

```shell
sylo -w 20 -r 10 -a ~./path/to/my/audio/file.wav -t yellow
```


## Data files

Data is persisted to disk at `~/.sylo/*.dat`, if you remove the files you will lose your work history.


## Acknowledgements

SYLO uses;
- [beepy](https://github.com/prabeshdhakal/beepy-v1)
- [simpleaudio](https://github.com/hamiltron/py-simple-audio)
- [Termgraph](https://github.com/mkaz/termgraph)
