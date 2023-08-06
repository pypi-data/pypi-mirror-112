"""Perform the main functionality of the application.

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
import logging
import sys
from typing import List, Optional

from filmbuff import arguments, interface


logger = logging.getLogger(__name__)


def main(argv: Optional[List[str]] = None) -> None:
    """Handle command-line arguments and run the application.

    Parameters
    ----------
    argv
        Arguments to pass directly to the parser and QApplication.

    Returns
    -------
    None

    """
    args = arguments.parse_args(argv)
    arguments.configure_logging(args.verbose)

    logger.info("Starting filmbuff.")
    interface.main(argv)
    logger.info("Exiting filmbuff.")


if __name__ == "__main__":
    main(sys.argv[1:])
