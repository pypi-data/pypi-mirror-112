#!/usr/bin/env python
""" true - return true value
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Thomas Tournier
"""

import getopt
import logging
import os
import sys

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: true - return true value v1.1.0 (July 14, 2021) by Thomas Tournier $"


################################################################################
def display_help():
    """Displays usage and help"""
    print("usage: true|false [--debug] [--help|-?] [--version] [--]", file=sys.stderr)
    print(
        "  ------------------  -----------------------------------------------",
        file=sys.stderr,
    )
    print("  --debug             Enable debug mode", file=sys.stderr)
    print(
        "  --help|-?           Print usage and this help message and exit",
        file=sys.stderr,
    )
    print("  --version           Print version and exit", file=sys.stderr)
    print("  --                  Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def process_command_line():
    """Process command line options"""

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "?"
    string_options = [
        "debug",
        "help",
        "version",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        display_help()
        sys.exit(1)

    for option, _ in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)

    process_command_line()

    if program_name.lower() == "true":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
