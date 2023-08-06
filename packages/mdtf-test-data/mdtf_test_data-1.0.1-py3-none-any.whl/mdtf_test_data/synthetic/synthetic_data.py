#!/usr/bin/env python
""" Module for generating synthetic datasets """

___all__ = [
    "dataset_stats",
    "generate_daily_time_axis",
    "generate_hourly_time_axis",
    "generate_monthly_time_axis",
    "generate_synthetic_dataset",
    "generate_random_array",
    "gfdl_vertical_coord",
    "gfdl_plev19_vertical_coord",
    "ncar_hybrid_coord",
    "write_to_netcdf",
    "generate_monthly_time_axis",
]

import cftime
import xarray as xr
import numpy as np
from mdtf_test_data.util.rectilinear import construct_rect_grid
import mdtf_test_data.generators as generators


def dataset_stats(filename, var=None, limit=None):
    """Prints statistics and attributes for a NetCDF file

    Parameters
    ----------
    filename : str, path-like
        Path to NetCDF file to analyze
    var : str, optional
        Variable to analyze (None prints a list of variables), by default None
    """
    dset = xr.open_dataset(filename, use_cftime=True)
    dset = dset.isel(time=slice(0, limit)) if limit is not None else dset
    if var is None:
        print(list(dset.variables))
    else:
        means = dset[var].mean(axis=(0, -2, -1)).values
        stds = dset[var].std(axis=(0, -2, -1)).values

        means = [means] if means.shape == () else list(means)
        stds = [stds] if stds.shape == () else list(stds)

        means = [float(x) for x in means]
        stds = [float(x) for x in stds]

        print(dset[var].attrs)
        print(list(zip(means, stds)))

    dset.close()

    return list(zip(means, stds))


def generate_daily_time_axis(startyear, nyears, timefmt="ncar"):
    """Construct a daily noleap time dimension with associated bounds

    Parameters
    ----------
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    timefmt : str, optional
        Time axis format, either "gfdl" or "ncar", "ncar" by default

    Returns
    -------
    xarray.DataArray
        time and time_bnds xarray DataArray types
    """
    daysinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = list(np.arange(1, 13))
    days = [np.arange(1, daysinmonth[n] + 1) for n, x in enumerate(months)]
    days = [item for sublist in days for item in sublist]
    days = days * nyears
    months = [[months[n]] * daysinmonth[n] for n, x in enumerate(months)]
    months = [item for sublist in months for item in sublist]
    months = months * nyears
    years = list(np.arange(startyear, startyear + nyears))
    years = [[years[x]] * 365 for x in range(0, len(years))]
    years = [item for sublist in years for item in sublist]

    if timefmt == "gfdl":
        hours = [12] * len(days)
    else:
        hours = [0] * len(days)

    timetuple = list(zip(years, months, days, hours))
    boundstuple = list(zip(years, months, days)) + [(startyear + nyears, 1, 1)]

    return xr_times_from_tuples(timetuple, boundstuple, timefmt=timefmt)


def generate_hourly_time_axis(startyear, nyears, dhour, timefmt="ncar"):
    """Construct an hourly noleap time dimension with associated bounds

    Parameters
    ----------
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    dhour : int
        Delta skip for hours (e.g. 1 hour, 3 hours, 6 hours)
    timefmt : str, optional
        Time axis format, either "gfdl" or "ncar", "ncar" by default

    Returns
    -------
    xarray.DataArray
        time and time_bnds xarray DataArray types
    """

    nhours = int(24 / dhour)
    hours = list(np.arange(0, 24, dhour))
    hours = hours * 365 * nyears
    daysinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = list(np.arange(1, 13))
    days = [np.arange(1, daysinmonth[n] + 1) for n in range(0, len(months))]
    days = [item for sublist in days for item in sublist]
    days = [item for item in days for i in range(nhours)]
    days = days * nyears
    months = [[months[n]] * daysinmonth[n] for n, x in enumerate(months)]
    months = [item for sublist in months for item in sublist]
    months = [item for item in months for i in range(nhours)]
    months = months * nyears
    years = list(np.arange(startyear, startyear + nyears))
    years = [[years[x]] * 365 for x in range(0, len(years))]
    years = [item for sublist in years for item in sublist]
    years = [item for item in years for i in range(nhours)]
    timetuple = list(zip(years, months, days, hours))
    boundstuple = (
        [(startyear, 1, 1, 0)]
        + list(zip(years, months, days, hours))
        + [(startyear + nyears, 1, 1, dhour)]
    )
    boundstuple = boundstuple[0:-1]

    return xr_times_from_tuples(timetuple, boundstuple, timefmt=timefmt)


def generate_monthly_time_axis(startyear, nyears, timefmt="ncar"):
    """Construct a monthly noleap time dimension with associated bounds

    Parameters
    ----------
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    timefmt : str, optional
        Time axis format, either "gfdl" or "ncar", "ncar" by default

    Returns
    -------
    xarray.DataArray
        time and time_bnds xarray DataArray types
    """

    nyears = nyears + 1

    years = np.arange(startyear, startyear + nyears)
    years = [year for year in years for x in range(12)]
    months = list(np.arange(1, 13)) * nyears
    days = 1 if timefmt == "ncar" else 15
    days = [days] * len(months)
    timetuple = list(zip(years, months, days))
    timetuple = timetuple[1:-11] if timefmt == "ncar" else timetuple[0:-12]

    days = [1] * len(months)
    boundstuple = list(zip(years, months, days))
    boundstuple = boundstuple[0:-11]

    return xr_times_from_tuples(timetuple, boundstuple, timefmt=timefmt)


def generate_synthetic_dataset(
    dlon,
    dlat,
    startyear,
    nyears,
    varname,
    timeres="mon",
    attrs=None,
    fmt="ncar",
    generator="normal",
    generator_kwargs=None,
    stats=None,
):
    """Generates xarray dataset of syntheic data in NCAR format

    Parameters
    ----------
    dlon : float, optional
        Grid spacing in the x-dimension (longitude)
    dlat : float, optional
        Grid spacing in the y-dimension (latitude)
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    varname : str
        Variable name in output dataset
    attrs : dict, optional
        Variable attributes, by default None
    attrs : dict, optional
        Variable attributes, by default None
    attrs : dict, optional
        Variable attributes, by default None
    stats : tuple or list of tuples
        Array statistics in the format of [(mean,stddev)]

    Returns
    -------
    xarray.Dataset
        Dataset of synthetic data
    """

    attrs = {} if attrs is None else attrs

    dset = construct_rect_grid(dlon, dlat, add_attrs=True, attr_fmt=fmt)
    lat = dset.lat
    lon = dset.lon
    xyshape = (len(dset["lat"]), len(dset["lon"]))

    if timeres == "mon":
        ds_time = generate_monthly_time_axis(startyear, nyears, timefmt=fmt)
    elif timeres == "day":
        ds_time = generate_daily_time_axis(startyear, nyears, timefmt=fmt)
    elif timeres == "3hr":
        ds_time = generate_hourly_time_axis(startyear, nyears, 3, timefmt=fmt)
    elif timeres == "1hr":
        ds_time = generate_hourly_time_axis(startyear, nyears, 1, timefmt=fmt)
    else:
        print(timeres)
        raise ValueError("Unknown time resolution requested")

    dset = ds_time.merge(dset)
    time = dset["time"]

    generator_kwargs = {} if generator_kwargs is None else generator_kwargs

    if stats is not None:
        stats = [stats] if not isinstance(stats, list) else stats
        if len(stats) > 1:
            if fmt == "ncar":
                dset = dset.merge(ncar_hybrid_coord())
                lev = dset.lev
            elif fmt == "gfdl":
                if len(stats) == 19:
                    dset = dset.merge(gfdl_plev19_vertical_coord())
                    lev = dset.plev19
                else:
                    dset = dset.merge(gfdl_vertical_coord())
                    lev = dset.pfull
        generator_kwargs["stats"] = stats

    assert generator in list(
        generators.__dict__.keys()
    ), f"Unknown generator method: {generator}"
    generator = generators.__dict__[generator]

    data = generators.generate_random_array(
        xyshape, len(time), generator=generator, generator_kwargs=generator_kwargs
    )
    data = data.squeeze()

    if len(data.shape) == 4:
        assert data.shape[1] == len(lev), "Length of stats must match number of levels"
        dset[varname] = xr.DataArray(data, coords=(time, lev, lat, lon), attrs=attrs)
    else:
        dset[varname] = xr.DataArray(data, coords=(time, lat, lon), attrs=attrs)

    dset.attrs["convention"] = fmt

    return dset


def gfdl_vertical_coord():
    """Generates GFDL AM4 pressure coordinate

    Returns
    -------
    xarray.DataArray
        GFDL AM4 pressure levels and half levels
    """

    pfull = np.array(
        [
            2.164043,
            5.845308,
            10.74508,
            17.106537,
            25.113805,
            35.221197,
            48.137904,
            64.560184,
            85.114482,
            110.419627,
            141.09261,
            177.729388,
            220.892397,
            271.066624,
            328.516337,
            392.785273,
            461.947262,
            532.465907,
            600.430867,
            663.107383,
            719.307118,
            768.814284,
            811.846869,
            848.836021,
            880.346139,
            906.995722,
            929.394583,
            948.128523,
            963.73257,
            976.687397,
            987.392458,
            996.109949,
        ]
    )

    phalf = np.array(
        [
            1.0,
            4.0,
            8.186021,
            13.788865,
            20.917952,
            29.836408,
            41.217896,
            55.792215,
            74.201906,
            97.047864,
            124.966648,
            158.549553,
            198.396959,
            245.027221,
            298.888576,
            360.040179,
            427.458025,
            498.243573,
            568.220535,
            633.836047,
            693.266329,
            745.991986,
            792.097373,
            831.921945,
            865.977814,
            894.872525,
            919.22792,
            939.635932,
            956.672132,
            970.827661,
            982.570665,
            992.23,
            1000.0,
        ]
    )

    pfull_attrs = {
        "long_name": "ref full pressure level",
        "units": "mb",
        "cartesian_axis": "Z",
        "positive": "down",
        "edges": "phalf",
    }

    phalf_attrs = {
        "long_name": "ref half pressure level",
        "units": "mb",
        "cartesian_axis": "Z",
        "positive": "down",
    }

    dset_out = xr.Dataset()
    dset_out["pfull"] = xr.DataArray(
        pfull, dims={"pfull": pfull}, coords={"pfull": pfull}, attrs=pfull_attrs
    )
    dset_out["phalf"] = xr.DataArray(
        phalf, dims={"phalf": phalf}, coords={"phalf": phalf}, attrs=phalf_attrs
    )

    return dset_out


def gfdl_plev19_vertical_coord():
    """Generates GFDL CMIP-like 19-level pressure coordinate

    Returns
    -------
    xarray.DataArray
        GFDL CMIP-like 19-level pressure coordinate
    """

    plev19 = np.array(
        [
            100000.0,
            92500.0,
            85000.0,
            70000.0,
            60000.0,
            50000.0,
            40000.0,
            30000.0,
            25000.0,
            20000.0,
            15000.0,
            10000.0,
            7000.0,
            5000.0,
            3000.0,
            2000.0,
            1000.0,
            500.0,
            100.0,
        ]
    )

    plev19_attrs = {
        "long_name": "pressure",
        "units": "Pa",
        "axis": "Z",
        "positive": "down",
    }

    dset_out = xr.Dataset()
    dset_out["plev19"] = xr.DataArray(
        plev19, dims={"plev19": plev19}, coords={"plev19": plev19}, attrs=plev19_attrs
    )

    return dset_out


def ncar_hybrid_coord():
    """Generates NCAR CAM2 hybrid vertical coordinate

    Returns
    -------
    xarray.DataArray
        NCAR vertical hybrid coordinate, a, and b coefficients
    """

    lev = np.array(
        [
            2.501651,
            4.187496,
            6.66766,
            10.099201,
            14.551163,
            19.943806,
            26.002806,
            32.250471,
            38.050216,
            42.70557,
            46.240154,
            49.511782,
            53.014888,
            56.765857,
            60.782212,
            65.082732,
            69.687527,
            74.618127,
            79.897583,
            85.550576,
            91.603545,
            98.084766,
            105.024556,
            112.455371,
            120.411924,
            128.931421,
            138.053706,
            147.821421,
            158.280234,
            169.479033,
            181.470176,
            194.309746,
            208.057754,
            222.778457,
            238.540693,
            255.418164,
            273.489746,
            292.839941,
            313.559268,
            335.744541,
            359.499453,
            384.935117,
            412.17043,
            441.332715,
            472.55834,
            505.993262,
            541.793789,
            580.127324,
            621.173066,
            665.12291,
            712.182383,
            762.571445,
            816.525625,
            858.699883,
            886.368125,
            912.162773,
            935.873203,
            957.301758,
            976.266953,
            992.556094,
        ]
    )

    hyam = np.array(
        [
            2.501651e-03,
            4.187496e-03,
            6.667660e-03,
            1.009920e-02,
            1.455116e-02,
            1.994381e-02,
            2.600281e-02,
            3.225047e-02,
            3.805022e-02,
            4.270557e-02,
            4.624015e-02,
            4.951178e-02,
            5.301489e-02,
            5.676586e-02,
            6.078221e-02,
            6.508273e-02,
            6.968753e-02,
            7.461813e-02,
            7.989758e-02,
            8.555058e-02,
            9.160354e-02,
            9.808477e-02,
            1.050246e-01,
            1.124554e-01,
            1.204119e-01,
            1.289314e-01,
            1.380537e-01,
            1.478214e-01,
            1.582802e-01,
            1.694790e-01,
            1.746796e-01,
            1.726401e-01,
            1.696388e-01,
            1.664251e-01,
            1.629841e-01,
            1.592996e-01,
            1.553543e-01,
            1.511300e-01,
            1.466068e-01,
            1.417635e-01,
            1.365776e-01,
            1.310247e-01,
            1.250790e-01,
            1.187125e-01,
            1.118957e-01,
            1.045965e-01,
            9.678086e-02,
            8.841227e-02,
            7.945159e-02,
            6.985690e-02,
            5.958334e-02,
            4.858288e-02,
            3.680412e-02,
            2.759706e-02,
            2.155681e-02,
            1.592557e-02,
            1.074934e-02,
            6.071232e-03,
            1.930966e-03,
            -1.648308e-09,
        ]
    )

    hybm = np.array(
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.006791,
            0.02167,
            0.038419,
            0.056353,
            0.075557,
            0.096119,
            0.118135,
            0.14171,
            0.166953,
            0.193981,
            0.222922,
            0.25391,
            0.287091,
            0.32262,
            0.360663,
            0.401397,
            0.445013,
            0.491715,
            0.541721,
            0.595266,
            0.652599,
            0.713989,
            0.779722,
            0.831103,
            0.864811,
            0.896237,
            0.925124,
            0.951231,
            0.974336,
            0.992556,
        ]
    )

    lev_attrs = {
        "long_name": "hybrid level at midpoints (1000*(A+B))",
        "units": "level",
        "positive": "down",
        "standard_name": "atmosphere_hybrid_sigma_pressure_coordinate",
        "formula_terms": "a: hyam b: hybm p0: P0 ps: PS",
    }

    dset_out = xr.Dataset()

    dset_out["hyam"] = xr.DataArray(
        hyam,
        dims={"lev": lev},
        coords={"lev": (lev)},
        attrs={"long_name": "hybrid A coefficient at layer midpoints"},
    )

    dset_out["hybm"] = xr.DataArray(
        hybm,
        dims={"lev": lev},
        coords={"lev": (lev)},
        attrs={"long_name": "hybrid B coefficient at layer midpoints"},
    )

    dset_out["lev"] = xr.DataArray(
        lev, dims={"lev": lev}, coords={"lev": (lev)}, attrs=lev_attrs
    )

    return dset_out


def write_to_netcdf(dset_out, outfile, time_dtype="float"):
    """Writes xarray dataset to NetCDF with proper encodings

    Parameters
    ----------
    dset_out : xarray.Dataset
        xarray dataset to write to NetCDF
    outfile : str, path-like
        Path to output file
    """

    base_time_unit = (
        dset_out.attrs["base_time_unit"]
        if "base_time_unit" in list(dset_out.attrs.keys())
        else "days since 0001-01-01"
    )

    encoding = {}
    for var in list(dset_out.variables):
        if var in ["time", "time_bnds", "average_T1", "average_T2"]:
            dset_out[var].encoding["units"] = base_time_unit
            if time_dtype == "float":
                dset_out[var].encoding["dtype"] = "float64"
                dset_out[var].encoding["_FillValue"] = 1.0e20
            elif time_dtype == "int":
                dset_out[var].encoding["dtype"] = "i4"
        elif var == "date":
            dset_out[var].encoding["dtype"] = "i4"
        elif "float" in str(dset_out[var].dtype):
            dset_out[var].encoding["_FillValue"] = 1.0e20
        elif "int" in str(dset_out[var].dtype):
            dset_out[var].encoding["_FillValue"] = -999
        else:
            dset_out[var].encoding["_FillValue"] = None
    dset_out.to_netcdf(outfile, encoding=encoding)


def xr_times_from_tuples(timetuple, boundstuple, timefmt="ncar"):
    """[summary]

    Parameters
    ----------
    timetuple : list of tuples of ints
        List of tuples containing time coordinate values [(Y,M,D,H,...) ...]
    boundstuple : list of tuples of ints
        List of tuples containing time bounds values [((Y,M,D,...)(Y,M,D,...)) ...]
    timefmt : str, optional
        Modeling center time format, either "gfdl" or "ncar", by default "ncar"

    Returns
    -------
    xarray.Dataset
        Returns an xarray dataset
    """

    dset_out = xr.Dataset()
    nbnds = np.array([0, 1])

    times = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    bounds = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in boundstuple]
    bounds = list(zip(bounds[0:-1], bounds[1::]))

    if timefmt == "gfdl":
        bounds_index_name = "bnds"
        bnds_attrs = {"long_name": "time axis boundaries"}
        time_attrs = {
            "long_name": "time",
            "cartesian_axis": "T",
            "calendar_type": "noleap",
            "bounds": "time_bnds",
        }
    else:
        bounds_index_name = "nbnds"
        bnds_attrs = {"long_name": "time interval endpoints"}
        time_attrs = {"long_name": "time", "bounds": "time_bnds"}

    dims = (("time", times), (bounds_index_name, nbnds))

    dset_out["time_bnds"] = xr.DataArray(
        bounds,
        coords=dims,
        attrs=bnds_attrs,
    )

    dset_out["time"] = xr.DataArray(
        times,
        dims={"time": times},
        coords={"time": (times)},
        attrs=time_attrs,
    )

    if timefmt == "gfdl":
        dset_out["average_T1"] = (("time"), [x[0] for x in bounds])
        dset_out.average_T1.attrs = {"long_name": "Start time for average period"}

        dset_out["average_T2"] = (("time"), [x[1] for x in bounds])
        dset_out.average_T2.attrs = {"long_name": "End time for average period"}

        dset_out["average_DT"] = (("time"), [(x[1] - x[0]) for x in bounds])
        dset_out.average_DT.attrs = {"long_name": "Length of average period"}

    if timefmt == "ncar":
        dset_out["date"] = (
            ("time"),
            [int(x.strftime("%Y%m%d")) for x in dset_out.time.values],
        )
        dset_out.date.attrs = {"long_name": "current date (YYYYMMDD)"}

    if bounds_index_name in list(dset_out.variables):
        dset_out = dset_out.drop_vars(bounds_index_name)
    startyear = str(dset_out.time.values[0].strftime("%Y")).replace(" ", "0")
    dset_out.attrs["base_time_unit"] = f"days since {startyear}-01-01"

    return dset_out
