import sys
from logging import getLogger, StreamHandler
from typing import *

from .__init__ import __version__, __title__
from .exporter import PackageWriter
from .model import HavingId
from .parser.loader import *
from .util.utils import list_pop_any

JUSTIFICATION_SIZE = 140
def get_logger(verbose: bool = False):
    logger = getLogger('openapi-parser')
    handler = StreamHandler(sys.stdout)
    logger.addHandler(handler)
    if (verbose):
        handler.setLevel('DEBUG')
        logger.setLevel('DEBUG')
    else:
        handler.setLevel('INFO')
        logger.setLevel('INFO')
    
    return logger

def run(schema_file: str, *writer_args, verbose: bool = False, dry_run: bool = False, clean: bool = True) -> int:
    logger = get_logger(verbose=verbose)
    
    parser = OpenApiParser.open(schema_file)
    parser.load_all()
    
    for path, mdl in parser.loaded_objects.items():
        msg = ('# ' + type(mdl).__name__ + (f" '{mdl.id}'" if isinstance(mdl, HavingId) else '')).ljust(JUSTIFICATION_SIZE, ' ') + f" -- '{path}'"
        logger.debug(msg)
    logger.debug('# ' + '=' * JUSTIFICATION_SIZE)
    logger.debug('')
    
    package_writer = PackageWriter(parser, *writer_args, dry_run=dry_run)
    package_writer.write_package(clean=clean)
    return 0

def header_line() -> str:
    return f"Python OpenAPI Parser Command-Line Interface v{__version__}"
def version_line() -> str:
    return f"{__title__} {__version__}"
def usage_line() -> str:
    return 'python -m openapi_parser SCHEMA [DESTINATION] [PACKAGE_NAME]'
def usage_options() -> List[str]:
    return \
    [
        "-v, --verbose | Enables extra verbosity",
        "--dry-run     | Performs dry run (does not create any files)",
        "--no-cleanup  | Does not perform cleanup before running",
        "-h, --help -? | Print this message and exit",
        "-V, --version | Print version and exit",
    ]

def cli(args: Optional[List[str]] = None) -> int:
    if (args is None):
        args = sys.argv[1:]
    
    if (len(args) < 1):
        print(header_line(), file=sys.stderr)
        print(f"Not enough arguments, usage: {usage_line()}", file=sys.stderr)
        return 1
    
    help = bool(list_pop_any(args, '-h', '--help', '-?'))
    if (help):
        print(header_line())
        print(f"Usage: {usage_line()}")
        print()
        print("Options:")
        for opt in usage_options():
            print(' '*4 + opt)
        return 0
    
    version = bool(list_pop_any(args, '-V', '--version'))
    if (version):
        print(version_line())
        return 0
    
    verbose = bool(list_pop_any(args, '-v', '--verbose'))
    dry_run = bool(list_pop_any(args, '--dry-run'))
    clean = not bool(list_pop_any(args, '--no-cleanup'))
    schema_file = args.pop(0)
    
    return run(schema_file, *args, verbose=verbose, dry_run=dry_run, clean=clean)


__all__ = \
[
    'cli',
    'run',
    'get_logger',
    'usage_options',
    'version_line',
    'header_line',
    'usage_line',
    'JUSTIFICATION_SIZE',
]
__pdoc_extras__ = \
[
    'JUSTIFICATION_SIZE',
]
