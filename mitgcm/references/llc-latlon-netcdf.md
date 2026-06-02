# LLC Compact / MDS to Lat-Lon NetCDF

Use this reference when converting ECCO/MITgcm LLC output such as `pickup_ptracers.*`
from native LLC90 compact/MDS files to regular latitude-longitude NetCDF.

## Core Lesson

LLC compact files are fragile. A file whose `.meta` says `dimList = [90, 1170, 50]`
is not safely decoded by:

```python
np.memmap(path, dtype='>f8').reshape(ntracer, nz, 13, 90, 90)
```

That plain reshape ignores LLC face orientation, cap topology, and compact packing.
It produces believable array shapes but visually wrong fields: crossed blocks,
checkerboard tile seams, or Arctic/equatorial faces pasted in the wrong orientation.

For MDS outputs, especially `pickup_ptracers.*`, let `xmitgcm` decode topology first:

```python
from xmitgcm import open_mdsdataset

ds = open_mdsdataset(
    str(run_dir),
    grid_dir=str(run_dir),
    prefix=['pickup_ptracers'],
    iters=[iteration],
    geometry='llc',
    endian='>',
    read_grid=True,
    delta_t=delta_t,
    extra_variables=extra_variables,
)
```

## Required Workflow

1. Read grid and fields with `xmitgcm(..., geometry='llc')`.
2. Define `extra_variables` for nonstandard pickup fields such as `pTr01`..`pTr54`.
3. Use decoded `ds['XC']`, `ds['YC']`, `ds['hFacC']`, and tracer arrays directly.
4. Wrap longitudes consistently, usually to `[-180, 180)`.
5. Flatten source points in the decoded face/j/i order:
   `source_lon = wrap(XC).ravel()`, `source_lat = YC.ravel()`, `field.reshape(..., -1)`.
6. Build a spherical nearest-neighbor map from target lat-lon cells to wet LLC cells.
7. Apply the nearest-source map per vertical level, using `hFacC[k] > 0` as a wet mask.
8. Write one NetCDF per time/year if memory or file size is large.
9. Validate with surface total plots before bulk conversion.

## Minimal Pattern for `pickup_ptracers`

```python
import numpy as np
from scipy.spatial import cKDTree
from xmitgcm import open_mdsdataset


def wrap_lon(lon, center=0.0):
    wrapped = np.mod(lon - center + 180.0, 360.0) - 180.0 + center
    return np.where(np.isclose(wrapped, center + 180.0), center - 180.0, wrapped)


def lonlat_to_xyz(lon, lat):
    lon_r = np.deg2rad(lon)
    lat_r = np.deg2rad(lat)
    cos_lat = np.cos(lat_r)
    return np.column_stack((cos_lat*np.cos(lon_r),
                            cos_lat*np.sin(lon_r),
                            np.sin(lat_r)))


def build_maps(xc, yc, wet_mask, lon, lat, radius_m=120000.0):
    src_lon = wrap_lon(xc).ravel()
    src_lat = yc.ravel()
    lon2d, lat2d = np.meshgrid(lon, lat)
    target_xyz = lonlat_to_xyz(lon2d.ravel(), lat2d.ravel())
    chord_radius = 2.0 * np.sin((radius_m / 6371000.0) / 2.0)

    maps = np.full((wet_mask.shape[0], target_xyz.shape[0]), -1, dtype=np.int64)
    flat = np.arange(src_lon.size, dtype=np.int64)
    for k in range(wet_mask.shape[0]):
        valid = wet_mask[k].ravel()
        if not np.any(valid):
            continue
        tree = cKDTree(lonlat_to_xyz(src_lon[valid], src_lat[valid]))
        dist, local = tree.query(target_xyz, distance_upper_bound=chord_radius, workers=-1)
        found = np.isfinite(dist)
        maps[k, found] = flat[valid][local[found]]
    return maps


num_tracers = 54
extra_variables = {
    f'pTr{i:02d}': {'dims': ['k', 'j', 'i'], 'attrs': {}}
    for i in range(1, num_tracers + 1)
}

ds = open_mdsdataset(
    str(run_dir),
    grid_dir=str(run_dir),
    prefix=['pickup_ptracers'],
    iters=[iteration],
    geometry='llc',
    endian='>',
    read_grid=True,
    delta_t=delta_t,
    extra_variables=extra_variables,
)

xc = ds['XC'].values
yc = ds['YC'].values
wet = ds['hFacC'].values > 0
source_maps = build_maps(xc, yc, wet, lon_1d, lat_1d)

# Chunk tracers to limit memory.
native = np.stack(
    [ds[f'pTr{i:02d}'].isel(time=0).values for i in range(1, 7)],
    axis=0,
)  # (nchunk, k, face, j, i)

flat_native = native.astype('f4', copy=False).reshape(native.shape[0], native.shape[1], -1)
out = np.full((native.shape[0], native.shape[1], len(lat_1d) * len(lon_1d)),
              np.nan, dtype='f4')
for k in range(native.shape[1]):
    src = source_maps[k]
    found = src >= 0
    out[:, k, found] = flat_native[:, k, src[found]]
out = out.reshape(native.shape[0], native.shape[1], len(lat_1d), len(lon_1d))
```

## Longitude Wrapping

Use the same wrapping for plotting and conversion:

```python
wrapped = np.mod(lon - center + 180.0, 360.0) - 180.0 + center
wrapped = np.where(np.isclose(wrapped, center + 180.0), center - 180.0, wrapped)
```

Do not mix `[0, 360)` source longitudes with `[-180, 180)` target longitudes without
normalization.

## NetCDF Shape and Memory

For annual/yearly pickup conversion, prefer one file per iteration/year:

- dimensions: `(time=1, k=50, lat, lon)`
- variables: one variable per tracer (`PE_s1_fl`, etc.) or `pTrXX`
- compression: NetCDF4 `zlib=True`, moderate `complevel=4`
- chunk tracers: e.g. 6 tracers per chunk

This avoids memory blowups from holding all years × 54 tracers × 50 levels × global
lat-lon cells in RAM.

## Validation Checklist

Before bulk conversion:

- Plot the latest native LLC surface field directly with xmitgcm and tile pcolormesh.
- Convert only one latest pickup/checkpoint to lat-lon NetCDF.
- Plot the lat-lon NetCDF surface sum over all tracers.
- Compare the two visually: coastlines, gyres, basin-scale maxima, and no crossed blocks.
- Inspect NetCDF dimensions and metadata: `time=1`, `k=50`, expected `lat/lon`, 54 tracer variables.

If the lat-lon plot shows crossed rectangular blocks, stop and check for manual compact reshape,
wrong face orientation, or longitude wrapping mismatch.

## Known Good Local Pattern

In this repository, use `utils/convert_pickup_ptracers_to_latlon_nc.py` as the reference
implementation for `pickup_ptracers.*` conversion. It uses:

- `xmitgcm.open_mdsdataset(..., geometry='llc')`
- `extra_variables` for `pTr01`..`pTr54`
- flattened decoded `XC/YC` point clouds
- per-level `hFacC` wet masks
- spherical `scipy.spatial.cKDTree` nearest-neighbor mapping
- tracer chunking
- one NetCDF per pickup iteration

Use `utils/plot_latest_surface_microplastic.py` as the reference native LLC visual check.
