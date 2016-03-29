2DPlay Tanks Unified Remote
===========================

This is a [Unified Remote][] custom remote for [2DPlay Tanks][]. Both OS X and Windows should be supported, but only OS X has currently been tested.

[Unified Remote]: https://www.unifiedremote.com/
[2DPlay Tanks]: http://www.2dplay.com/tanks/tanks-play.htm

Installation
------------

Visit the [Releases page][] to find and install the latest release. If using the OS X disk image, download the DMG and double-click the package installer. If using the zip file, follow the [Unified Remote instructions on installing a custom remote][custom-remote].

[Releases page]: https://github.com/seanfisk/2dplay-tanks-unified-remote/releases
[custom-remote]: https://www.unifiedremote.com/tutorials/how-to-install-a-custom-remote

Development
-----------

First, install [Homebrew][] and [Brew Bundle][]. Then install the Homebrew dependencies:

```
brew bundle
```

The [Waf][] build system is used to build this project. Running this Waf build system requires [Python 3.5][], so install that in your preferred way. The `waf` executable is bundled with repository and need not be installed. First, configure the build system:

```
./waf configure
```

The OS X disk image can be built with the following:

```
./waf build
```

The remote can also be installed with Waf:

```
./waf install
```

[Homebrew]: https://brew.sh/
[Brew Bundle]: https://github.com/Homebrew/homebrew-bundle#install
[Waf]: https://waf.io/
[Python 3.5]: https://www.python.org/downloads/release/python-351/
