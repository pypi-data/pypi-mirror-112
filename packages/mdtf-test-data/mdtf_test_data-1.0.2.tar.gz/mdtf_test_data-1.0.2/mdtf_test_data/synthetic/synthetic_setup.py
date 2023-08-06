#!/usr/bin/env python

__all__ = ["create_output_dirs", "synthetic_main"]
""" Script to generate synthetic GFDL CM4 output """
import os
from .synthetic_data import generate_synthetic_dataset
from .synthetic_data import write_to_netcdf


def create_output_dirs(CASENAME=""):
    """Create output data directories"""
    print("Creating output data directories")
    if not os.path.exists(f"{CASENAME}/day"):
        os.makedirs(f"{CASENAME}/day")
    if "NCAR" in CASENAME:
        if not os.path.exists(f"{CASENAME}/mon"):
            os.makedirs(f"{CASENAME}/mon")
        if not os.path.exists(f"{CASENAME}/3hr"):
            os.makedirs(f"{CASENAME}/3hr")
        if not os.path.exists(f"{CASENAME}/1hr"):
            os.makedirs(f"{CASENAME}/1hr")


def synthetic_main(
    yaml_dict={},
    DLAT=20.0,
    DLON=20.0,
    STARTYEAR=1,
    NYEARS=10,
    CASENAME="",
    TIME_RES="",
    DATA_FORMAT="",
):
    """Main script to generate synthetic data using GFDL naming conventions"""
    create_output_dirs(CASENAME)
    # parse the yaml dictionary
    var_names = yaml_dict["variables.name"]
    # -- Create Data
    print("Generating data with time resolution of ", TIME_RES)
    for v in var_names:
        stats = (
            yaml_dict[v + ".stats"]
            if str(v + ".stats") in list(yaml_dict.keys())
            else None
        )
        generator = (
            yaml_dict[v + ".generator.name"]
            if str(v + ".generator.name") in list(yaml_dict.keys())
            else "normal"
        )
        generator_kwargs = (
            yaml_dict[v + ".generator.args"]
            if str(v + ".generator.args") in list(yaml_dict.keys())
            else {}
        )
        # vinfo = yaml_dict[v]
        # print(vinfo)
        dset_out = generate_synthetic_dataset(
            DLON,
            DLAT,
            STARTYEAR,
            NYEARS,
            v,
            timeres=TIME_RES,
            attrs=yaml_dict[v + ".atts"],
            fmt=DATA_FORMAT,
            generator=generator,
            stats=stats,
            generator_kwargs=generator_kwargs,
        )
        write_to_netcdf(dset_out, f"{CASENAME}/{TIME_RES}/{CASENAME}.{v}.{TIME_RES}.nc")
