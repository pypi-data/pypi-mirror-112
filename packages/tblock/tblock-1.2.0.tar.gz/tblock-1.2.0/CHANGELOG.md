
# Version 1.1.4

## General
* Changed remote repository locations

## Ad-Blocker
* Fixed search operation


# Version 1.1.3

## Ad-Blocker
* Fixed critical issue #25


# Version 1.1.2

## General
+ Added a clean error message when filter is a directory (#22)
- Removed a useless test

## Ad-Blocker
* TBlock now tries to get filters before marking them as `subscribed`
* Fixed conflict between operation `--sync` and option `--sync` (#21)


# Version 1.1.1

## General
* Fixed devscripts

## Ad-Blocker
* Now update remote repo before any other filter operation when '-y' flag is given


# Version 1.1.0

## General
* Changed installation method in Makefile

## Ad-Blocker
* Fixed filter info display
* Fixed real path for local filters
+ Added new features on status page


# Version 1.0.1

## Ad-Blocker
* Fixed help page
* Improved examples in man page


# Version 1.0.0

## General
+ Added support for Windows
+ Published package to Fedora Copr and Ubuntu PPA
* Code has been completely re-written
* Brand new CLI animation
* New argument parsing (closes #10, #11)

## Ad-Blocker
+ Improved status overview
+ Added a security feature to prevent hosts hijack
+ Locks the database while editing it
+ It is now possible to change the ID of a custom filter

## Converter
* Fixed redirecting rules in hosts file format (issue #15)
* Lots of improvements


# Version 0.0.6

## General
* Patched a big issue for new users


# Version 0.0.5

## General
* Changed the default Makefile installation method
* Now only binaries are available on the release page
* The database is now using primary keys in tables

## Ad-Blocker
* Improved argument parsing
* Fixed compatibility, now exits if unsupported OS

## Converter
+ Added info about converter in converted filters


# Version 0.0.4

## General
* Change arrows when executing a task
* Fixed release script

## Ad-Blocker
- Removed prompt before updating hosts file after another action
* Fixed Termux compatibility (thanks to Anter Amo, pull request #6)


# Version 0.0.3

## General
+ Added support for Opera filter syntax
+ Added a new mirror on git.disroot.org

## Ad-Blocker
+ Added an exception if downloaded repository index is not an XML file
* Changed the way that TBlock retrieves mirrors
* Fixed Termux support (issue #1)
* Improved speed when fetching ad-blocker status

## Converter
* Improved Opera filter convertion


# Version 0.0.2

## General
- Removed nosetests method from Makefile
* Changed Makefile installation method
* Fixed script to generate man pages (issue #5)
* Fixed gpg-signing in when compiling into a binary
+ Added two more tests for filters

## Ad-Blocker
* Fixed filter rule priority (issue #4)
+ Added support for Termux (issue #1)

## Converter
+ Added new option to detect filter syntax


# Version 0.0.1

## General
* Initial release

