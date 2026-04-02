# MITgcm Post-Processing Reference

## xmitgcm — Mandatory Data Access Library

All MITgcm output must be read using `xmitgcm`. Never manually parse `.data`/`.meta` files with raw `numpy.fromfile`.

### Installation (mitgcm conda environment)
```bash
conda activate mitgcm
pip install xmitgcm
# Optional but recommended for LLC grids:
pip install pyresample
```

---

## Reading Standard MDS Output

### Basic usage:
```python
# process_read_output.py
from xmitgcm import open_mdsdataset

ds = open_mdsdataset(
    data_dir='./run',        # directory containing .data/.meta output files
    grid_dir='./input',      # directory containing grid definition files
    iters='all',             # auto-detect all available time steps
    prefix=['T', 'S', 'UVEL', 'VVEL', 'WVEL']  # variable prefixes to load
)

print(ds)
# xarray.Dataset with dimensions: (time, k, j, i)
# Coordinates: XC, YC, XG, YG, Z, Zp1, drC, drF, rA, hFacC, ...
```

### Specifying iterations explicitly:
```python
ds = open_mdsdataset(
    './run',
    grid_dir='./input',
    iters=[1080, 2160, 4320],   # specific time steps
    prefix=['T', 'S']
)
```

### LLC geometry (cubed-sphere / lat-lon-cap):
```python
ds = open_mdsdataset(
    './run',
    grid_dir='./grid',
    iters='all',
    geometry='llc'             # must specify for LLC grids!
)
# Coordinates include face dimension (13 faces for LLC90)
```

---

## Standard Post-Processing Workflows

### Plot_*.py naming convention:
All plotting scripts must be named `plot_*.py`. Each script should produce one figure or a closely related set of figures.

### Process_*.py naming convention:
All data transformation scripts must be named `process_*.py`. These produce derived quantities or reformatted output files.

---

## Plotting Standard Lat/Lon Output

```python
# plot_sst_map.py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from xmitgcm import open_mdsdataset

# Load data
ds = open_mdsdataset('./run', grid_dir='./input', iters='all', prefix=['T'])

# Surface temperature at last time step
sst = ds['T'].isel(time=-1, k=0)
lon = ds['XC']
lat = ds['YC']

fig, ax = plt.subplots(
    figsize=(12, 6),
    subplot_kw={'projection': ccrs.Robinson()}
)
ax.set_global()
im = ax.pcolormesh(
    lon, lat, sst,
    transform=ccrs.PlateCarree(),
    cmap='RdYlBu_r',
    vmin=-2, vmax=32
)
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.coastlines(linewidth=0.5)
plt.colorbar(im, ax=ax, label='SST (°C)', shrink=0.8)
ax.set_title('Sea Surface Temperature')
plt.savefig('plot_sst_map.png', dpi=150, bbox_inches='tight')
plt.close()
```

---

## LLC Grid Visualization Pipeline

LLC (Lat-Lon-Cap) grids require a special workflow because the native grid has topology discontinuities that make direct 2D plotting wrong.

**Complete pipeline (5 steps):**

### Step 1 — Read LLC data with xmitgcm
xmitgcm automatically handles the 13-face LLC topology, assembling the compact binary format into a coherent DataArray with face/j/i dimensions.

```python
# process_llc_read.py
from xmitgcm import open_mdsdataset

ds = open_mdsdataset(
    './run',
    grid_dir='./grid',
    iters=[0],
    geometry='llc'    # triggers LLC topology assembly
)

# Extract surface temperature
T_surf = ds['T'].isel(time=0, k=0)  # shape: (face, j, i) or (tile, j, i)

# Get LLC coordinate matrices (same shape as data)
XC = ds['XC']   # longitude, shape (face, j, i)
YC = ds['YC']   # latitude,  shape (face, j, i)
```

### Step 2 — Flatten LLC coordinates
```python
import numpy as np

# Flatten to 1D arrays for pyresample
lons_llc = XC.values.ravel()
lats_llc = YC.values.ravel()
data_llc  = T_surf.values.ravel()

# Remove land/NaN points
mask = np.isfinite(data_llc)
lons_llc = lons_llc[mask]
lats_llc = lats_llc[mask]
data_llc  = data_llc[mask]
```

### Step 3 — Define target regular grid
```python
# Target: 0.5° × 0.5° global regular grid
lon_1d = np.arange(-180, 180, 0.5)
lat_1d = np.arange(-90,  90,  0.5)
lon_grid, lat_grid = np.meshgrid(lon_1d, lat_1d)
```

### Step 4 — Reproject using pyresample (3D Cartesian interpolation)
**Do NOT use 2D lat/lon interpolation** — the spherical geometry causes discontinuities near the Arctic cap.

```python
import pyresample

# Define source swath (LLC native grid)
source_def = pyresample.geometry.SwathDefinition(
    lons=lons_llc,
    lats=lats_llc
)

# Define target grid
target_def = pyresample.geometry.GridDefinition(
    lons=lon_grid,
    lats=lat_grid
)

# Nearest-neighbour reprojection (internally uses 3D Cartesian KD-tree)
data_regular = pyresample.kd_tree.resample_nearest(
    source_def,
    data_llc,
    target_def,
    radius_of_influence=55000,   # metres; ~0.5° at equator
    fill_value=np.nan
)
# Result shape: (Nlat, Nlon) — globally regular, land = NaN
```

### Step 5 — Plot with Cartopy
```python
# plot_llc_global.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig, ax = plt.subplots(
    figsize=(14, 7),
    subplot_kw={'projection': ccrs.Robinson()}
)
ax.set_global()

im = ax.pcolormesh(
    lon_grid, lat_grid, data_regular,
    transform=ccrs.PlateCarree(),
    cmap='RdYlBu_r',
    vmin=-2, vmax=32
)

# Land is naturally NaN — no masking needed
ax.add_feature(cfeature.COASTLINE, linewidth=0.4)
plt.colorbar(im, ax=ax, label='SST (°C)', shrink=0.75, orientation='horizontal')
ax.set_title('LLC90 Sea Surface Temperature — Global Regridded')

plt.savefig('plot_llc_global.png', dpi=150, bbox_inches='tight')
plt.close()
```

---

## Visualizing Raw LLC Compact `.bin` Files

When the source data is a pre-existing LLC binary file (not a model output), use `xmitgcm.utils.read_raw_data` or build a minimal dataset:

```python
# plot_llc_bin.py
import numpy as np
from xmitgcm import open_mdsdataset
import pyresample

# Read the compact 1170×90 LLC binary (Big-Endian float32)
raw = np.fromfile('llc90_forcing.bin', dtype='>f4').reshape(1170, 90)
# raw is the compact 13-face format (1170 = 13 × 90)

# Load LLC90 grid coordinates from a reference run
ds_grid = open_mdsdataset('./grid', grid_dir='./grid',
                           iters=[], geometry='llc')
XC = ds_grid['XC'].values.ravel()
YC = ds_grid['YC'].values.ravel()

# The LLC compact format stacks faces differently — use xmitgcm to read
# correctly rather than manually reshaping the 1170×90 array.
# → Prefer using xmitgcm with geometry='llc' for all LLC data reads.
```

---

## Computing Derived Quantities

```python
# process_heat_content.py
import numpy as np
from xmitgcm import open_mdsdataset

ds = open_mdsdataset('./run', grid_dir='./input', iters='all', prefix=['T'])

# Ocean heat content (J/m²) for each water column
rho0   = 1025.0   # kg/m³ reference density
cp     = 3994.0   # J/(kg·K) specific heat

# Vertical integration weighted by layer thickness and area
dz   = ds['drF']           # layer thickness (m), shape (Nr,)
hfac = ds['hFacC']         # fractional cell depth
T    = ds['T']             # shape (time, k, j, i)

OHC = (rho0 * cp * (T * hfac * dz).sum(dim='k'))
# OHC shape: (time, j, i), units: J/m²

OHC.to_netcdf('process_ohc.nc')
```
