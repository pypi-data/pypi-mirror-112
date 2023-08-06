# Preprocessing for CMIP6 models
import warnings

import numpy as np
import pandas as pd
import xarray as xr


def cmip6_renaming_dict():
    """a universal renaming dict. Keys correspond to source id (model name)
    and valuse are a dict of target name (key) and a list of variables that
    should be renamed into the target."""
    rename_dict = {
        # dim labels (order represents the priority when checking for the dim labels)
        "x": ["x", "i", "ni", "xh", "nlon", "lon", "longitude"],
        "y": ["y", "j", "nj", "yh", "nlat", "lat", "latitude"],
        "lev": ["lev", "deptht", "olevel", "zlev", "olev", "depth"],
        "bnds": ["bnds", "axis_nbounds", "d2"],
        "vertex": ["vertex", "nvertex", "vertices"],
        # coordinate labels
        "lon": ["lon", "longitude", "nav_lon"],
        "lat": ["lat", "latitude", "nav_lat"],
        "lev_bounds": [
            "lev_bounds",
            "deptht_bounds",
            "lev_bnds",
            "olevel_bounds",
            "zlev_bnds",
        ],
        "lon_bounds": [
            "bounds_lon",
            "bounds_nav_lon",
            "lon_bnds",
            "x_bnds",
            "vertices_longitude",
        ],
        "lat_bounds": [
            "bounds_lat",
            "bounds_nav_lat",
            "lat_bnds",
            "y_bnds",
            "vertices_latitude",
        ],
        "time_bounds": ["time_bounds", "time_bnds"],
    }
    return rename_dict


def rename_cmip6(ds, rename_dict=None):
    """Homogenizes cmip6 dadtasets to common naming"""
    ds = ds.copy()
    source_id = ds.attrs["source_id"]

    if rename_dict is None:
        rename_dict = cmip6_renaming_dict()

    # rename variables
    if len(rename_dict) == 0:
        warnings.warn(
            "input dictionary empty.",
            UserWarning,
        )
    else:
        for di in rename_dict.keys():

            # make sure the input is a list
            if not isinstance(rename_dict[di], list):
                raise ValueError(
                    f"Input dict must have a list as value. Got {rename_dict[di]} for key {di}"
                )

            if di not in ds.variables:

                # For now just stop in the list if the dimension is already there, or one 'hit'
                # was already encountered.
                trigger = False
                for wrong in rename_dict[di]:
                    if wrong in ds.variables or wrong in ds.dims:
                        if not trigger:
                            ds = ds.rename({wrong: di})
                            trigger = True

    return ds


def promote_empty_dims(ds):
    """Convert empty dimensions to actual coordinates"""
    ds = ds.copy()
    for di in ds.dims:
        if di not in ds.coords:
            ds = ds.assign_coords({di: ds[di]})
            # ds.coords[di] = ds[di]
    return ds


# some of the models do not have 2d lon lats, correct that.
def broadcast_lonlat(ds, verbose=True):
    """Some models (all `gr` grid_labels) have 1D lon lat arrays
    This functions broadcasts those so lon/lat are always 2d arrays."""
    if "lon" not in ds.variables:
        ds.coords["lon"] = ds["x"]
    if "lat" not in ds.variables:
        ds.coords["lat"] = ds["y"]

    if len(ds["lon"].dims) < 2:
        ds.coords["lon"] = ds["lon"] * xr.ones_like(ds["lat"])
    if len(ds["lat"].dims) < 2:
        ds.coords["lat"] = xr.ones_like(ds["lon"]) * ds["lat"]

    return ds


def _interp_nominal_lon(lon_1d):
    x = np.arange(len(lon_1d))
    idx = np.isnan(lon_1d)
    return np.interp(x, x[~idx], lon_1d[~idx], period=360)


def replace_x_y_nominal_lat_lon(ds):
    """Approximate the dimensional values of x and y with mean lat and lon at the equator"""
    ds = ds.copy()

    def maybe_fix_non_unique(data, pad=False):
        """remove duplicate values by linear interpolation
        if values are non-unique. `pad` if the last two points are the same
        pad with -90 or 90. This is only applicable to lat values"""
        if len(data) == len(np.unique(data)):
            return data
        else:
            # pad each end with the other end.
            if pad:
                if len(np.unique([data[0:2]])) < 2:
                    data[0] = -90
                if len(np.unique([data[-2:]])) < 2:
                    data[-1] = 90

            ii_range = np.arange(len(data))
            _, indicies = np.unique(data, return_index=True)
            double_idx = np.array([ii not in indicies for ii in ii_range])
            # print(f"non-unique values found at:{ii_range[double_idx]})")
            data[double_idx] = np.interp(
                ii_range[double_idx], ii_range[~double_idx], data[~double_idx]
            )
            return data

    if "x" in ds.dims and "y" in ds.dims:
        # define 'nominal' longitude/latitude values
        # latitude is defined as the max value of `lat` in the zonal direction
        # longitude is taken from the `middle` of the meridonal direction, to
        # get values close to the equator

        # pick the nominal lon/lat values from the eastern
        # and southern edge, and
        eq_idx = len(ds.y) // 2

        nominal_x = ds.isel(y=eq_idx).lon.load()
        nominal_y = ds.lat.max("x").load()

        # interpolate nans
        # Special treatment for gaps in longitude
        nominal_x = _interp_nominal_lon(nominal_x.data)
        nominal_y = nominal_y.interpolate_na("y").data

        # eliminate non unique values
        # these occour e.g. in "MPI-ESM1-2-HR"
        nominal_y = maybe_fix_non_unique(nominal_y)
        nominal_x = maybe_fix_non_unique(nominal_x)

        ds = ds.assign_coords(x=nominal_x, y=nominal_y)
        ds = ds.sortby("x")
        ds = ds.sortby("y")

        # do one more interpolation for the x values, in case the boundary values were
        # affected
        ds = ds.assign_coords(
            x=maybe_fix_non_unique(ds.x.load().data),
            y=maybe_fix_non_unique(ds.y.load().data, pad=True),
        )

    else:
        warnings.warn(
            "No x and y found in dimensions for source_id:%s. This likely means that you forgot to rename the dataset or this is the German unstructured model"
            % ds.attrs["source_id"]
        )
    return ds


def unit_conversion_dict():
    """Units conversion database"""
    unit_dict = {"m": {"centimeters": 1 / 100}}
    return unit_dict


def correct_units(ds, verbose=False, stric=False):
    "Converts coordinates into SI units using `unit_conversion_dict`"
    unit_dict = unit_conversion_dict()
    ds = ds.copy()
    # coordinate conversions
    for co, expected_unit in [("lev", "m")]:
        if co in ds.coords:
            if "units" in ds.coords[co].attrs.keys():
                unit = ds.coords[co].attrs["units"]
                if unit != expected_unit:
                    if unit in unit_dict[expected_unit].keys():
                        factor = unit_dict[expected_unit][unit]
                        ds.coords[co] = ds.coords[co] * factor
                        ds.coords[co].attrs["units"] = expected_unit
                    else:
                        warnings.warn("No conversion found in unit_dict")
            else:
                warnings.warn(f'{ds.attrs["source_id"]}: No units found for {co}')
    return ds


def correct_coordinates(ds, verbose=False):
    """converts wrongly assigned data_vars to coordinates"""
    ds = ds.copy()
    for co in [
        "x",
        "y",
        "lon",
        "lat",
        "lev",
        "bnds",
        "lev_bounds",
        "lon_bounds",
        "lat_bounds",
        "time_bounds",
        "lat_verticies",
        "lon_verticies",
    ]:
        if co in ds.variables:
            if verbose:
                print("setting %s as coord" % (co))
            ds = ds.set_coords(co)
    return ds


def correct_lon(ds):
    """Wraps negative x and lon values around to have 0-360 lons.
    longitude names expected to be corrected with `rename_cmip6`"""
    ds = ds.copy()

    # remove out of bounds values found in some
    # models as missing values
    ds["lon"] = ds["lon"].where(abs(ds["lon"]) <= 1000)
    ds["lat"] = ds["lat"].where(abs(ds["lat"]) <= 1000)

    # adjust lon convention
    lon = ds["lon"].where(ds["lon"] > 0, 360 + ds["lon"])
    ds = ds.assign_coords(lon=lon)

    if "lon_bounds" in ds.variables:
        lon_b = ds["lon_bounds"].where(ds["lon_bounds"] > 0, 360 + ds["lon_bounds"])
        ds = ds.assign_coords(lon_bounds=lon_b)

    return ds


def parse_lon_lat_bounds(ds):
    """both `regular` 2d bounds and vertex bounds are parsed as `*_bounds`.
    This function renames them to `*_verticies` if the vertex dimension is found.
    Also removes time dimension from static bounds as found in e.g. `SAM0-UNICON` model.
    """
    if "source_id" in ds.attrs.keys():
        if ds.attrs["source_id"] == "FGOALS-f3-L":
            warnings.warn("`FGOALS-f3-L` does not provide lon or lat bounds.")

    ds = ds.copy()

    if "lat_bounds" in ds.variables:
        if "x" not in ds.lat_bounds.dims:
            ds.coords["lat_bounds"] = ds.coords["lat_bounds"] * xr.ones_like(ds.x)

    if "lon_bounds" in ds.variables:
        if "y" not in ds.lon_bounds.dims:
            ds.coords["lon_bounds"] = ds.coords["lon_bounds"] * xr.ones_like(ds.y)

    # I am assuming that all bound fields with time were broadcasted in error (except time bounds obviously),
    # and will drop the time dimension.
    error_dims = ["time"]
    for ed in error_dims:
        for co in ["lon_bounds", "lat_bounds", "lev_bounds"]:
            if co in ds.variables:
                if ed in ds[co].dims:
                    warnings.warn(
                        f"Found {ed} as dimension in `{co}`. Assuming this is an error and just picking the first step along that dimension."
                    )
                    stripped_coord = ds[co].isel({ed: 0}).squeeze()
                    # make sure that dimension is actually dropped
                    if ed in stripped_coord.coords:
                        stripped_coord = stripped_coord.drop(ed)

                    ds = ds.assign_coords({co: stripped_coord})

    # Finally rename the bounds that are given in vertex convention
    for va in ["lon", "lat"]:
        va_name = va + "_bounds"
        if va_name in ds.variables and "vertex" in ds[va_name].dims:
            ds = ds.rename({va_name: va + "_verticies"})

    return ds


def maybe_convert_bounds_to_vertex(ds):
    """Converts renamed lon and lat bounds into verticies, by copying
    the values into the corners. Assumes a rectangular cell."""
    ds = ds.copy()
    if "bnds" in ds.dims:
        if "lon_bounds" in ds.variables and "lat_bounds" in ds.variables:
            if (
                "lon_verticies" not in ds.variables
                and "lat_verticies" not in ds.variables
            ):
                lon_b = xr.ones_like(ds.lat) * ds.coords["lon_bounds"]
                lat_b = xr.ones_like(ds.lon) * ds.coords["lat_bounds"]

                lon_bb = xr.concat(
                    [lon_b.isel(bnds=ii).squeeze(drop=True) for ii in [0, 0, 1, 1]],
                    dim="vertex",
                )
                lon_bb = lon_bb.reset_coords(drop=True)

                lat_bb = xr.concat(
                    [lat_b.isel(bnds=ii).squeeze(drop=True) for ii in [0, 1, 1, 0]],
                    dim="vertex",
                )
                lat_bb = lat_bb.reset_coords(drop=True)

                ds = ds.assign_coords(lon_verticies=lon_bb, lat_verticies=lat_bb)

    return ds


def maybe_convert_vertex_to_bounds(ds):
    """Converts lon and lat verticies to bounds by averaging corner points
    on the appropriate cell face center."""

    ds = ds.copy()
    if "vertex" in ds.dims:
        if "lon_verticies" in ds.variables and "lat_verticies" in ds.variables:
            if "lon_bounds" not in ds.variables and "lat_bounds" not in ds.variables:
                lon_b = xr.concat(
                    [
                        ds["lon_verticies"].isel(vertex=[0, 1]).mean("vertex"),
                        ds["lon_verticies"].isel(vertex=[2, 3]).mean("vertex"),
                    ],
                    dim="bnds",
                )
                lat_b = xr.concat(
                    [
                        ds["lat_verticies"].isel(vertex=[0, 3]).mean("vertex"),
                        ds["lat_verticies"].isel(vertex=[1, 2]).mean("vertex"),
                    ],
                    dim="bnds",
                )

                ds = ds.assign_coords(lon_bounds=lon_b, lat_bounds=lat_b)
    ds = promote_empty_dims(ds)
    return ds


def sort_vertex_order(ds):
    """sorts the vertex dimension in a coherent order:
    0: lower left
    1: upper left
    2: upper right
    3: lower right
    """
    ds = ds.copy()
    if (
        "vertex" in ds.dims
        and "lon_verticies" in ds.variables
        and "lat_verticies" in ds.variables
    ):

        # pick a vertex in the middle of the domain, to avoid the pole areas
        x_idx = len(ds.x) // 2
        y_idx = len(ds.y) // 2

        lon_b = ds.lon_verticies.isel(x=x_idx, y=y_idx).load().data
        lat_b = ds.lat_verticies.isel(x=x_idx, y=y_idx).load().data
        vert = ds.vertex.load().data

        points = np.vstack((lon_b, lat_b, vert)).T

        # split into left and right
        lon_sorted = points[np.argsort(points[:, 0]), :]
        right = lon_sorted[:2, :]
        left = lon_sorted[2:, :]
        # sort again on each side to get top and bottom
        bl, tl = left[np.argsort(left[:, 1]), :]
        br, tr = right[np.argsort(right[:, 1]), :]

        points_sorted = np.vstack((bl, tl, tr, br))

        idx_sorted = (points_sorted.shape[0] - 1) - np.argsort(points_sorted[:, 2])
        ds = ds.assign_coords(vertex=idx_sorted)
        ds = ds.sortby("vertex")

    return ds


# TODO: Implement this in a sleeker way with daops
def fix_metadata(ds):
    """
    Fix known issues (from errata) with the metadata.
    """

    # https://errata.es-doc.org/static/view.html?uid=2f6b5963-f87e-b2df-a5b0-2f12b6b68d32
    if ds.attrs["source_id"] == "GFDL-CM4" and ds.attrs["experiment_id"] in [
        "1pctCO2",
        "abrupt-4xCO2",
        "historical",
    ]:
        ds.attrs["branch_time_in_parent"] = 91250
    # https://errata.es-doc.org/static/view.html?uid=61fb170e-91bb-4c64-8f1d-6f5e342ee421
    if ds.attrs["source_id"] == "GFDL-CM4" and ds.attrs["experiment_id"] in [
        "ssp245",
        "ssp585",
    ]:
        ds.attrs["branch_time_in_child"] = 60225
    return ds


def combined_preprocessing(ds):
    if "AWI" not in ds.attrs["source_id"]:
        ds = ds.copy()
        # fix naming
        ds = rename_cmip6(ds)
        # promote empty dims to actual coordinates
        ds = promote_empty_dims(ds)
        # demote coordinates from data_variables
        ds = correct_coordinates(ds)
        # broadcast lon/lat
        ds = broadcast_lonlat(ds)
        # shift all lons to consistent 0-360
        ds = correct_lon(ds)
        # fix the units
        ds = correct_units(ds)
        # rename the `bounds` according to their style (bound or vertex)
        ds = parse_lon_lat_bounds(ds)
        # sort verticies in a consistent manner
        ds = sort_vertex_order(ds)
        # convert vertex into bounds and vice versa, so both are available
        ds = maybe_convert_bounds_to_vertex(ds)
        ds = maybe_convert_vertex_to_bounds(ds)
        ds = fix_metadata(ds)
    return ds
