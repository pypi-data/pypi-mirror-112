# Installation
pip install [pnu-true](https://pypi.org/project/pnu-true/)

# TRUE(1)

## NAME
true - return true value

## SYNOPSIS
**true**
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]

## DESCRIPTION
The **true** utility returns with an exit code of zero.

Some shells may provide a builtin true command which is identical to this utility.
Consult the [builtin(1)](https://www.freebsd.org/cgi/man.cgi?query=builtin) manual page.

### OPTIONS
Options | Use
------- | ---
--debug|Enable debug mode
--help\|-?|Print usage and a short help message and exit
--version|Print version and exit
--|Options processing terminator

## EXIT STATUS
The **true** utility exits 0 on success, and >0 if an error occurs.

## SEE ALSO
[builtin(1)](https://www.freebsd.org/cgi/man.cgi?query=builtin),
[csh(1)](https://www.freebsd.org/cgi/man.cgi?query=csh),
[false(1)](https://github.com/Thomas-Le-Dev/true/blob/main/FALSE.md),
[sh(1)](https://www.freebsd.org/cgi/man.cgi?query=sh)

## STANDARDS
The **true** utility is a standard UNIX/POSIX command.
It is expected to be IEEE Std 1003.2 (“[POSIX](https://en.wikipedia.org/wiki/POSIX).2”) compatible.

It tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
Tested OK under Windows.

## HISTORY
This version was made for the [PNU project](https://github.com/HubTou/PNU).

## LICENSE
This utility is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
This version was written by [Thomas Tournier](https://github.com/Thomas-Le-Dev)

The man page is derived from the [FreeBSD project's one](https://www.freebsd.org/cgi/man.cgi?query=true).
