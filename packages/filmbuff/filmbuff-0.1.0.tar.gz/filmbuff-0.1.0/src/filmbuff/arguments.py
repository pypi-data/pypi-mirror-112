"""Parse the command-line arguments and configure logging.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import argparse
import logging
from typing import List, Optional

import filmbuff


def configure_logging(verbose: int) -> None:
    """Set the log handler and level.

    Parameters
    ----------
    verbose
        The level of verbosity desired.

    Returns
    -------
    None

    """
    if verbose == 0:
        filmbuff.logger.addHandler(filmbuff.null_handler)
    else:
        filmbuff.logger.addHandler(filmbuff.stream_handler)
        if verbose == 1:
            filmbuff.logger.setLevel(logging.INFO)
        else:
            filmbuff.logger.setLevel(logging.DEBUG)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Create a parser and parse command-line arguments.

    If no arguments are provided, the parser reads from `sys.argv`.

    Parameters
    ----------
    argv
        Arguments to pass directly to the parser.

    Returns
    -------
    :obj:`argparse.Namespace`
        A named-tuple like object containing the parsed arguments.

    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "filmbuff is an application for creating and managing a local\n"
            "database of film information."
            "\n\n"
            "This product uses the TMDb API but is not endorsed or certified\n"
            "by TMDb."
        ),
        epilog=(
            "filmbuff Copyright (C) 2021 emerac"
            "\n\n"
            "This program comes with ABSOLUTELY NO WARRANTY. This is free\n"
            "software, and you are welcome to redistribute it under certain\n"
            "conditions. You should have received a copy of the GNU General\n"
            "Public License along with this program. If not, see:\n"
            "<https://www.gnu.org/licenses/gpl-3.0.txt>."
        ),
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="Provide log output. This argument can be repeated.",
        action="count",
        default=0,
    )
    return parser.parse_args(argv)
