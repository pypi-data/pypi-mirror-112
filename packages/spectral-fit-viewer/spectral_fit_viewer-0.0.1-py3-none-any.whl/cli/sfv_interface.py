"""
spectral_fit_viewer

Usage: 
    spectral_fit_viewer [<modules>] [-f FIT_CONFIG] [-b BASELINE] [-d DATA_PATH] [-l LOG] [-h] [-v]

Modules:
    full          Serve full R&D Bokeh dahsboard

Options:
    -f --fit-config <FIT_CONFIG>    Path to the fitter configuration yaml file
    -b --baseline <BASELINE>        Path to the baseline configuration yaml file
    -d --data-path <DATA_PATH>      Path to a directory of RDF files
    -l --log-path <LOG>             Path to spectral logging directory
    -h --help                       Show this screen.
    -v --version                    Show version.
"""

import sys
from docopt import docopt, DocoptExit
from timeit import default_timer as timer

#from lologger.lologger_client import get_logger_with_decorator

APPLICATION_NAME = 'spectral_fit_viewer'
__version__ = '1.1.1'
#logger = get_logger_with_decorator(name=APPLICATION_NAME)

def main():
    print(docopt(__doc__))
    try:
        start_time = timer()
        print(start_time)
        try:
            args = docopt(__doc__)
        except DocoptExit:
            print(__doc__)
        else:
            if args['<modules>']:
                if args['<modules>'] == 'full':
                    import cli.spectral_fit_viewer_cli_full as full
                    full.main()
                else:
                    sys.exit("%r is not a sfv module. See 'spectral_fit_viewer_run -h'." % args['<module>'])
            else:

                print(__doc__)
    except KeyboardInterrupt:
        print("key")
        sys.stderr.write("\n[X] Interrupted by user after %i seconds!\n" % (timer() - start_time))
        sys.exit(-1)
