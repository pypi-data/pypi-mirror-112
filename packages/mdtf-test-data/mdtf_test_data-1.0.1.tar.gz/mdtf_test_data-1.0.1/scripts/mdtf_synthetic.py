#!/usr/bin/env python
""" mdtf_test_data driver program """
import sys
# add mdtf_test_data to system path
sys.path.insert(0, '../mdtf_test_data')
from mdtf_test_data.synthetic.synthetic_setup import synthetic_main
from mdtf_test_data.util.cli import cli_holder
import argparse
import pkg_resources as pkgr
import pytest
from envyaml import EnvYAML

def read_yaml(file_name):
    """ A function to read YAML files """
    config = EnvYAML(file_name)
    return config

def main():
    """The the central nervous system of the mdtf_test_data package"""
    print("Starting mdtf_test_data")
    # Define the the CLI arguments and call the parser.
    parser = argparse.ArgumentParser(description="parse mdtf_test_data command-line arguments")
    # @TODO add support for CMIP convention
    parser.add_argument("--convention","-c", type=str, help="Model convention", choices=['GFDL', 'CESM', 'NCAR'],
                    required=True, default="")
    parser.add_argument("--startyear", type=int, help="Start year of time period",
                    required=False, default=1)
    parser.add_argument("--nyears", type=int, help="Total length of time period in years",
                    required=False, default=10)
    parser.add_argument("--dlat", type=float, help="Latitude resolution in degrees (will not change default value for NCAR daily data)",
                    required=False, default=20.0)
    parser.add_argument("--dlon", type=float, help="Longitude resolution in degrees (will not change default value for NCAR daily data)",
                    required=False, default=20.0)
    parser.add_argument("--unittest","-ut", action='store_true', help="Run unit tests",
                    required=False)
    args = parser.parse_args()
    cli_info = cli_holder(args.convention, args.startyear,
                          args.nyears, args.dlat, args.dlon, args.unittest)

    assert cli_info.dlat <= 30.0 and cli_info.dlat >= 0.5, "Error: dlat value is invalid; valid range is [0.5 30.0]"
    assert cli_info.dlon <= 60.0 and cli_info.dlon >= 0.5, "Error: dlon value is invalid; valid range is [0.5 60.0]"

    if cli_info.unittest:
       retcode_1 = pytest.main(["-x", "mdtf_test_data/tests/test_synthetic_data.py"])
       if retcode_1 != 0 :
           print('test_synthetic_data failed. Check output log for details. Exiting program')
           sys.exit(retcode_1)
       retcode_2 = pytest.main(["-x", "mdtf_test_data/tests/test_generators.py"])
       if retcode_2 != 0 :
           print('test_generators failed. Check output log for details. Exiting program.')
           sys.exit(retcode_2)

    if cli_info.convention == 'GFDL':
        print("Importing GFDL variable information")
        input_data = pkgr.resource_filename("mdtf_test_data", "config/gfdl_day.yml")
        input_data = read_yaml(input_data)

        print("Calling Synthetic Data Generator for GFDL data")
        synthetic_main(input_data, DLAT=cli_info.dlat, DLON=cli_info.dlon,
                         STARTYEAR=cli_info.startyear, NYEARS=cli_info.nyears,
                         CASENAME="GFDL.Synthetic", TIME_RES="day", DATA_FORMAT="gfdl")
    elif cli_info.convention == 'CESM' or cli_info.convention == 'NCAR':
        print("Importing NCAR variable information")
        time_res = ["mon","day","3hr","1hr"]
        for t in time_res:
            input_data = pkgr.resource_filename("mdtf_test_data", f"config/ncar_{t}.yml")
            input_data = read_yaml(input_data)
            dlat = cli_info.dlat
            dlon = cli_info.dlon
            if t == "day":
                dlat=5.0
                dlon=5.0
            print("Calling Synthetic Data Generator for NCAR data")
            synthetic_main(input_data, DLAT=dlat, DLON=dlon,
                        STARTYEAR=cli_info.startyear, NYEARS=cli_info.nyears,
                        CASENAME="NCAR.Synthetic", TIME_RES=t, DATA_FORMAT="ncar")

if __name__ == '__main__':
    main()
    sys.exit()
