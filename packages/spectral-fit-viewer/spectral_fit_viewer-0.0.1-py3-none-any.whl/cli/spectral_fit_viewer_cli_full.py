"""
usage: spectral_fit_viewer full [-f FIT_CONFIG] [-b BASELINE] [-d DATA_PATH] [-l LOG] [-h] [-v]
                                        
Options:
    -f --fit-config <FIT_CONFIG>         Path to the fitter configuration yaml file
    -b --baseline <BASELINE>         Path to the baseline configuration yaml file
    -d --data-path <DATA_PATH>        Path to a directory of RDF files
    -l --log-path <LOG>        Path to spectral logging directory
    -h --help              Show this screen.
    -v --version           Show version.
"""

from docopt import docopt
from pathlib import Path
import os
#from colorama import Fore, init
from subprocess import call
import sys
from bokeh.server.server import Server
from spectral_fit_viewer import bokeh_og
from phlannel.serve_rdf import FileDataSource
from litho_tracktool_fitter.utils.config_loader import parse_fit_config, parse_baseline_config

ENV_CONFIG_NAME = "SPECTRAL_VIEWER_CONFIG"
CONFIG_SUFFIXES = [".yaml", ".yml"]

def main():

    args = docopt(__doc__)
    print(args)
    baseline_config = args.get('--baseline')
    fitter_config = args.get('--fit-config')
    data_path = args.get('--data-path')
    log_path = args.get('--log-path')
    #bokeh_data_dict = {}
    #bokeh_data_dict['data_path'] = args['--data-path']
    # Check data path exists 
    data_path = Path(data_path).expanduser().resolve()
    print(data_path)
    if not data_path.exists():
        print(f"Data path {data_path.as_posix()} does not exist.")
        sys.exit(1)

    # # Configure h5 filespri
    # temp = FileDataSource(data_path)
    # files = temp.h5_files
    # bokeh_data_dict['files_h5'] = files
    # bokeh_data_dict['data_path'] = str(data_path)

    #Check config and log paths for DS
    if all((fitter_config, baseline_config, log_path)):

        fit_config_path = Path(fitter_config).expanduser().resolve() 
        baseline_config_path = Path(baseline_config).expanduser().resolve() 
        print(fit_config_path, baseline_config_path)
        log_path = Path(log_path).expanduser().resolve() 
        if fit_config_path.exists() and baseline_config_path.exists() and log_path.exists():

        #check suffix
            if baseline_config_path.suffix not in CONFIG_SUFFIXES:
                print(f"baseline.yaml not found in {baseline_config_path.parent.as_posix()}")
                sys.exit(1)

            if not fit_config_path.exists() or fit_config_path.suffix not in CONFIG_SUFFIXES:
                print(f"fit_script.yaml not found in {fit_config_path.parent.as_posix()}")
                sys.exit(1)

            #fit_object = DS(fit_config_path, baseline_config, log_path)
            #fitargs, baseargs = parse_fit_config(fit_config_path), parse_baseline_config(baseline_config_path)
           
        else:
            print(f"Please check path specified by -f, -b and -l are correct and exist.")
            sys.exit(1)
        
        # bokeh_data_dict['fitargs'] = fitargs
        # bokeh_data_dict['baseargs'] = baseargs
        # bokeh_data_dict['log_path'] = args['--log-path']
        
    else:
        print(f"Please check path specified by -f, -b and -l are correct and exist.")
        sys.exit(1)

    #bokeh_og.main()

    p = os.path.realpath('./src/spectral_fit_viewer/bokeh_og.py')
    prefix, _ = os.path.split(p)
    bokeh_server_file = os.path.join(prefix, "bokeh_og.py")
    call(["bokeh", "serve", "--show", bokeh_server_file])

    # server = Server({"/edit": bokeh_og.init})
    # server.start()
    # print(Fore.GREEN + "Opening peakipy: Edit fits on http://localhost:5006/edit")
    # server.io_loop.add_callback(server.show, "/edit")
    # server.io_loop.start()


