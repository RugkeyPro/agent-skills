# ECCO / LLC Grid and Offline State Estimation Reference

## LLC Grid Architecture

### What is LLC?

LLC (Lat-Lon-Cap) is MITgcm's native global ocean grid used by ECCO (Estimating the Circulation and Climate of the Ocean) state estimates. It solves the distortion problem near the poles by using a composite grid:

- Equatorial and mid-latitude regions: standard lat/lon tiles
- Arctic region: a rotated cap tile (face 6 in the 6-face cs32/LLC decomposition)
- Antarctica: excluded from the computational domain

LLC variants:

| Name | Global resolution | Faces × tile size |
|------|------------------|--------------------|
| LLC90 | ~1° | 13 tiles × 90×90 |
| LLC270 | ~1/3° | 13 tiles × 270×270 |
| LLC4320 | ~1/12° | 13 tiles × 4320×4320 |

### LLC90 Compact Binary Format

When written to `.bin` files, the 13 LLC faces are packed into a **1170 × 90** 2D array (for LLC90):
```
1170 = 13 × 90
```

The packing is **not** a simple stack of 13 faces in order. The northern hemisphere faces are rotated and interleaved with the southern tiles to produce the compact layout. This is why:

- **Never** try to manually reshape a `1170×90` array to interpret individual faces
- **Always** use `xmitgcm` with `geometry='llc'` to correctly unpack the topology

```python
from xmitgcm import open_mdsdataset

# xmitgcm handles the full topology: unpack → rotate → assemble
ds = open_mdsdataset(
    data_dir='./run',
    grid_dir='./grid',
    iters='all',
    geometry='llc'   # ← mandatory for all LLC grids
)
```

### LLC Grid Coordinate Awareness

LLC90 excludes landlocked interior regions (central Asia, Antarctic highlands) that have no ocean coverage. Grid points in these regions are simply not defined — they will appear as `NaN` after reprojection.

When inspecting LLC longitude:
- Some LLC configurations use a [0°, 360°) longitude convention, others use [-180°, 180°)
- Always check `ds['XC'].min()` and `ds['XC'].max()` before interpolating
- Align longitude conventions between source and target before interpolation:
  ```python
  # Normalize to [-180, 180) if needed
  XC = ds['XC'].values
  XC = np.where(XC > 180, XC - 360, XC)
  ```

---

## Interpolating Between Regular and LLC Grids

### Rule: Use 3D Cartesian KD-tree — Not 2D Lat/Lon

Interpolation directly in lat/lon 2D space fails near the Arctic cap due to coordinate singularities and the rotated face geometry. Always convert to 3D Cartesian coordinates and use spatial KD-tree search.

`pyresample.kd_tree.resample_nearest` handles this correctly by internally converting to 3D Cartesian space.

### Regular lat/lon → LLC90 (e.g., forcing field injection)

```python
# process_interp_forcing_to_llc.py
import numpy as np
import pyresample
from xmitgcm import open_mdsdataset

# ---- Source: regular lat/lon grid ----
# Load source data (example: 0.5° × 0.5° atmospheric forcing)
lon_src_1d = np.arange(-180, 180, 0.5)   # (720,)
lat_src_1d = np.arange(-90,   90, 0.5)   # (360,)
lon_src, lat_src = np.meshgrid(lon_src_1d, lat_src_1d)
data_src = np.load('wind_stress.npy')     # shape (360, 720)

# ---- Target: LLC90 grid ----
ds_grid = open_mdsdataset('./grid', grid_dir='./grid',
                           iters=[], geometry='llc')
XC = ds_grid['XC'].values   # shape (face, j, i) or (j_compact, i)
YC = ds_grid['YC'].values

# Flatten target coordinates
lon_llc = XC.ravel()
lat_llc = YC.ravel()

# ---- pyresample: nearest-neighbour on sphere (3D Cartesian internally) ----
source_def = pyresample.geometry.GridDefinition(
    lons=lon_src, lats=lat_src
)
target_def = pyresample.geometry.SwathDefinition(
    lons=lon_llc, lats=lat_llc
)

data_on_llc = pyresample.kd_tree.resample_nearest(
    source_def,
    data_src,
    target_def,
    radius_of_influence=75000,   # metres
    fill_value=np.nan
)
# Reshape back to LLC face structure
data_on_llc = data_on_llc.reshape(XC.shape)

# Write to LLC binary (Big-Endian, compact format)
data_on_llc.astype('>f4').ravel().tofile('wind_stress_llc90.bin')
```

### LLC90 → Regular lat/lon (e.g., for visualization)

See `postprocess.md` §LLC visualization pipeline for the full 5-step workflow.

---

## Offline Tracer Advection (pkg/offline)

Offline mode re-runs passive tracer advection using pre-saved velocity/diffusivity snapshots, without recomputing the ocean dynamics. This enables efficient sensitivity experiments.

### Configuration (`input/data.offline`):
```fortran
&OFFLINE
# Period between consecutive forcing snapshots (seconds)
 offlineForcingPeriod = 2592000.0,    ! 30 days
# Total length of the repeating forcing cycle (seconds)
 offlineForcingCycle  = 31536000.0,   ! 365 days (1-year cycle)
# Path prefix for offline velocity snapshots
 uVelFile  = 'offline/uVel',
 vVelFile  = 'offline/vVel',
 wVelFile  = 'offline/wVel',
 diffKrFile= 'offline/diffKr',
&
```

### File sequence consistency check — Critical

The offline forcing files must be named with iteration numbers that correspond exactly to the time stamps implied by `offlineForcingPeriod`. Verify:

```
Expected file iteration N = round(N × offlineForcingPeriod / deltaTClock)
```

Example:
- `deltaTClock = 3600 s` (1-hour time step)
- `offlineForcingPeriod = 2592000 s` (30 days)
- Monthly snapshot files should have iterations: `720`, `1440`, `2160`, ..., `8760`
  - iter 720 = 720 × 3600 s = 30 days ✓

If file numbering does not match, the model interpolates between wrong snapshots — producing physically incorrect tracer fields with no error message.

**Validation script:**
```python
# process_check_offline_sequence.py
import os, numpy as np

deltaTClock         = 3600.0         # seconds
offlineForcingPeriod = 2592000.0     # 30 days
offlineForcingCycle  = 31536000.0    # 1 year
n_snapshots = int(round(offlineForcingCycle / offlineForcingPeriod))

print(f"Expected {n_snapshots} offline snapshots per cycle")
for n in range(1, n_snapshots + 1):
    time_s = n * offlineForcingPeriod
    expected_iter = int(round(time_s / deltaTClock))
    fname = f"offline/uVel.{expected_iter:010d}.data"
    exists = os.path.isfile(fname)
    print(f"  Snapshot {n:2d}: iter {expected_iter:8d} → {fname} {'✓' if exists else '✗ MISSING'}")
```

---

## ECCO Flux and Budget Analysis — Native Grid Rule

**Do not** regrid LLC fluxes to a regular lat/lon grid before performing closed-budget diagnostics (heat budget, salt budget, volume transport). Regridding introduces interpolation errors that break conservation.

All flux and budget work must be done in the **native LLC grid space**:

```python
# process_heat_budget_llc.py — correct approach
from xmitgcm import open_mdsdataset

ds = open_mdsdataset('./run', grid_dir='./grid', iters='all', geometry='llc')

# Work entirely in LLC native coordinates
# ds.rA  = cell area on LLC grid (correct for area-weighted sums)
# ds.hFacC = fractional cell depth (accounts for partial cells)
# ds.drF   = layer thickness

# Volume-weighted temperature mean (stays on native grid):
vol  = (ds['rA'] * ds['hFacC'] * ds['drF']).sum(dim=['face','j','i','k'])
OHC  = (ds['T'] * ds['rA'] * ds['hFacC'] * ds['drF']).sum(
           dim=['face','j','i','k']) / vol
```

Only regrid to regular lat/lon as the **final step** for human-readable visualization, never for intermediate budget computations.

---

## LLC90 Compact Format Technical Details

The 1170×90 compact layout for LLC90 is structured as follows:

```
Rows 0–449    (5 × 90 rows): Faces 0–4 — southern and equatorial lat/lon tiles
Row  450      (1 × 90 rows): Face 5 — northern cap (90×90, stored as-is)
Rows 540–989  (5 × 90 rows): Faces 6–10 — rotated northern tiles (transposed)
Rows 990–1169 (2 × 90 rows): Faces 11–12 — Arctic cap east/west
```

The `xmitgcm` library encodes these rotation and transposition rules in its `llcreader` module. There is no need to implement this manually — always use `xmitgcm` with `geometry='llc'`.
