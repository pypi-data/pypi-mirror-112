![TBlock Logo](https://tblock.codeberg.page/static/banner.png)

[![Copr build status](https://copr.fedorainfracloud.org/coprs/twann/tblock/package/tblock/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/twann/tblock/package/tblock/)
[![PyPI Version](https://img.shields.io/pypi/v/tblock)](https://pypi.org/project/tblock/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/tblock?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/tblock)
[![License](https://img.shields.io/pypi/l/tblock.svg?color=red)](https://www.gnu.org/licenses/gpl-3.0.html)
[![AUR Votes](https://img.shields.io/aur/votes/tblock)](https://aur.archlinux.org/packages/tblock/)
[![Remote repository filters count](https://img.shields.io/badge/remote%20repository-38%20filters-orange)](https://tblock.codeberg.page/repo/index.xml)
[![Syntax supported count](https://img.shields.io/badge/syntax%20supported-6-ff69b4)](https://codeberg.org/tblock/tblock/src/branch/main/docs/FILTER_SYNTAX_SUPPORTED.md)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/000327557?domain=https%3A%2F%2Ffosstodon.org&style=social)](https://fosstodon.org/@tblock)

## Summary

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Post-installation](#post-installation)
- [Usage](#usage)
- [Copyright](#copyright)
- [Libraries used](#libraries-used)
- [Contact](#contact)

## About

TBlock is a free and open-source ad-blocker, written in Python. It uses the [hosts file](https://codeberg.org/tblock/tblock/wiki/FAQ) to block advertising and tracking domains, which means it protects your whole system against these domains. TBlock is compatible [with most of filter formats](docs/FILTER_SYNTAX_SUPPORTED.md), and also has [a built-in filter converter](https://codeberg.org/tblock/tblock/wiki/How-to-use-the-converter), to help you share your custom filters with people that are using different ad-blockers. 

## Features

+ Free and open-source software
+ Easy to install
+ Does not cost any money
+ Does not track your personal data
+ Does not make you fingerprintable, unlike some ad-blocking browser extensions
+ Fast rules parsing
+ Blocks ads for your whole operating system
+ Compatible with most filter formats
+ Has an [online filter repository](https://codeberg.org/tblock/tblock/wiki/Remote-filters-repository) to help you find and subscribe to filters in an easier way
+ Has a built-in filter converter

## Installation

There are various methods to install TBlock. You need to install TBlock as root, since superuser privileges are required to edit the hosts file.

### With python

This is the fastest and easiest way to install TBlock on your machine. Simply run the following command:

```shell
$ sudo pip install tblock
```

### Other installation methods

More installation methods can be found on our website:

[![More installation methods](https://img.shields.io/badge/Install%20it-now-blue?style=for-the-badge&logo=python)](https://tblock.codeberg.page/install)

### Manually

To build TBlock manually, see [BUILDING.md](BUILDING.md).

## Post-installation

After the installation and after each update of TBlock, you should update your local version of the remote filter repository and subscribe to a blocking filter, by running:
```shell
$ sudo tblock -Sy tblock-base
```

## Usage

![Blocking a domain with TBlock](https://tblock.codeberg.page/static/tblock-animation.gif)

To show the help page of TBlock, simply run:
```shell
$ tblock -h
```
To show the help page of the built-in converter, simply run:
```shell
$ tblockc -h
```

You can find more help about usage on [TBlock's wiki](https://codeberg.org/tblock/tblock/wiki/Home).

## Copyright

TBlock and its converter are released under [GPLv3](LICENSE).

## Libraries used

TBlock uses the external libraries:

| Name | Author | License | Homepage |
| --- | --- | --- | --- |
| colorama | [Jonathan Hartley](mailto:tartley@tartley.com) | BSD | https://github.com/tartley/colorama |
| requests | [Kenneth Reitz](mailto:me@kennethreitz.org) | Apache 2.0 | https://requests.readthedocs.io |
| urllib3 | [Andrey Petrov](mailto:andrey.petrov@shazow.net) | MIT | https://urllib3.readthedocs.io/ |

## Contact

- Email: twann@ctemplar.com [[PGP key](https://tblock.codeberg.page/uploads/keys/twann.asc)]
- Mastodon: [@tblock@fosstodon.org](https://fosstodon.org/@tblock)
- Telegram: https://t.me/tblock
- Website: https://tblock.codeberg.page/
