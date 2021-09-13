import fileinput
import json
import sys
from argparse import ArgumentParser
import logging

from nest import nestify
from .constants import USAGE_MESSAGE, PARAM_HELP_MESSAGE


err_handler = logging.StreamHandler(sys.stderr)
err_handler.setLevel(logging.DEBUG)

_logger = logging.getLogger(__name__)
_logger.addHandler(err_handler)


def nestify_cli():
    """Use nestify_json in cli mode"""

    parser = ArgumentParser()
    parser.usage = USAGE_MESSAGE

    _add_params(parser)

    args = parser.parse_args()

    if args.debug:
        _logger.setLevel(logging.getLevelName(args.debug.upper()))
        _logger.debug('Debug mode: ON')

    _logger.debug(args)

    file = getattr(args, 'file', None)

    if not file and sys.stdin.isatty():
        parser.print_help()
        exit(2)

    _fileinput = fileinput.input(file or ('-',))
    try:
        _input = json.loads(''.join(_fileinput))
    except (ValueError, json.JSONDecodeError, TypeError) as e:
        _logger.debug(f'INPUT: {"".join(_fileinput)}')
        _logger.debug(e)
        sys.stderr.write(f'Could not parse JSON\n')
    else:
        _logger.debug(f'INPUT LENGTH: {len(_input)}')
        try:
            nested = nestify(_input, *args.group)
        except Exception as e:
            _logger.error(e)
            sys.stderr.write(f'Could not create nested dictionary\n')
        else:
            _logger.debug(f'OUTPUT LENGTH: {len(nested)}')
            sys.stdout.write(f'{nested}\n')


def _add_params(parser: ArgumentParser):
    if sys.stdin.isatty():
        parser.add_argument('file', help=PARAM_HELP_MESSAGE.get('file', ''))

    parser.add_argument('group', help=PARAM_HELP_MESSAGE.get('group', ''), default=[], nargs='*',
                        type=str)

    parser.add_argument('--debug', help='Set logging level to debug',
                        choices=['debug'])