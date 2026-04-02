# MITgcm Data I/O and Grid Reference

## Binary File Format Requirements

MITgcm reads and writes **flat (unblocked), Big-Endian, Fortran column-major** binary files. This applies to:
- Bathymetry / topography files
- Initial condition files (temperature, salinity, velocity)
- External forcing fields
- Passive tracer initial conditions

### Format specifications:

| Property | Value |
|----------|-------|
| Byte order | **Big-Endian** (most significant byte first) |
| Memory layout | **Fortran column-major** (X varies fastest, then Y, then Z) |
| Precision | 32-bit float (`real*4`) by default; 64-bit (`real*8`) if `readBinaryPrec=64` in `input/data` |
| Structure | Flat / unblocked — no Fortran record markers |
| File extension | `.bin` (input) or `.data` + `.meta` (output from pkg/mdsio) |

---

## Generating Input Files with Python/NumPy

> **Critical:** NumPy uses C-order (row-major) by default. MITgcm expects Fortran-order (column-major). A simple `tofile()` on a `(Ny, Nx)` array works correctly because MITgcm reads X-fast, and a C-order `(Ny, Nx)` array has X varying fastest in memory.

### Bathymetry file generation:
```python
# process_generate_bathymetry.py
import numpy as np

Nx, Ny = 360, 160

# Build depth array: shape (Ny, Nx), depth negative downward
bathy = np.zeros((Ny, Nx), dtype='>f4')  # '>f4' = Big-Endian float32

# Fill with your depth values (ocean = negative, land = 0)
# bathy[j, i] = depth at grid point (i, j)
bathy[...] = -3000.0   # example: uniform 3000 m ocean

# Write Big-Endian binary
bathy.astype('>f4').tofile('bathymetry.bin')
```

### 3D forcing field (e.g., initial temperature):
```python
# process_generate_init_T.py
import numpy as np

Nx, Ny, Nr = 360, 160, 50

# Shape must be (Nr, Ny, Nx) for correct vertical ordering
T_init = np.zeros((Nr, Ny, Nx), dtype='>f4')

# Fill with values...
# T_init[k, j, i] = temperature at level k, y-index j, x-index i

T_init.astype('>f4').tofile('init_T.bin')
```

### Precision control:
```python
# For 64-bit input (set readBinaryPrec=64 in data &PARM01):
array.astype('>f8').tofile('field.bin')   # Big-Endian float64

# For 32-bit input (default, readBinaryPrec=32):
array.astype('>f4').tofile('field.bin')   # Big-Endian float32
```

---

## Arakawa C-Grid Layout

MITgcm uses the **Arakawa C-grid** for spatial discretization. Velocity components and scalars are stored at different spatial positions:

```
    V(i,j+1)
      |
U(i,j)--T(i,j)--U(i+1,j)
      |
    V(i,j)
```

| Variable | Grid position | Description |
|----------|-------------|-------------|
| `T`, `S`, tracers, `eta` | Cell center (tracer point) | Scalar quantities |
| `U` (zonal velocity) | West cell face | Staggered in X |
| `V` (meridional velocity) | South cell face | Staggered in Y |
| `W` (vertical velocity) | Cell top/bottom interface | Located at layer interfaces, not centers |

**Implications for data handling:**

- **Boundary conditions:** A no-slip boundary on the eastern wall means `U=0` at the east face, not at the tracer point. The indexing differs from the tracer grid by half a cell.
- **Momentum forcing (wind stress):** `fu` (zonal wind) lives on the U-grid (west face), `fv` on the V-grid (south face). When interpolating from regular lat/lon wind data, shift by 0.5 grid cells.
- **Flux calculations:** Tracer fluxes are computed at cell faces (U/V points), then divergence is evaluated at the cell center (T point).
- **W velocity:** Located at layer interfaces (`Nr+1` levels, from surface to bottom), not at the `Nr` layer centers where temperature lives.

---

## MDS Output Format (pkg/mdsio — default)

Default output from pkg/mdsio produces paired files:

```
T.0000001080.data    ← raw binary data (Big-Endian)
T.0000001080.meta    ← ASCII metadata (dimensions, tile info)
```

The number `0000001080` is the iteration number (zero-padded to 10 digits).

With MPI, output is split per tile:
```
T.0000001080.001.001.data   ← tile (1,1)
T.0000001080.001.001.meta
T.0000001080.002.001.data   ← tile (2,1)
...
```

### Reading with xmitgcm:
```python
from xmitgcm import open_mdsdataset

ds = open_mdsdataset(
    data_dir='./run',    # directory with .data/.meta files
    grid_dir='./input',  # directory with grid files (XC.data, etc.)
    iters='all',         # or specific list: [1080, 2160]
    prefix=['T', 'S', 'UVEL', 'VVEL']
)
# ds is an xarray.Dataset with dimensions (time, k, j, i)
```

---

## NetCDF Output (pkg/mnc)

When `useMNC=.TRUE.`, MITgcm writes NetCDF files instead of (or in addition to) MDS binary.

**Important:** pkg/mnc still outputs **one `.nc` file per tile**, not a single global file:
```
state.0000001080.t001.nc   ← tile 1
state.0000001080.t002.nc   ← tile 2
...
```

### Assembling global NetCDF files:

**Option A — gluemncbig (shell script, official):**
```bash
cd run/
/path/to/MITgcm/utils/matlab/gluemncbig -o global_state.nc state.*.nc
```

**Option B — xmitgcm (Python, recommended):**
```python
from xmitgcm import open_mdsdataset
# xmitgcm handles tiled .nc assembly transparently
ds = open_mdsdataset('./run', grid_dir='./input', iters='all')
# Save as single global NetCDF
ds.to_netcdf('global_output.nc')
```

---

## Common I/O Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Output is all zeros or NaN | Wrong byte order (Little-Endian file read as Big-Endian) | Use `dtype='>f4'` in NumPy |
| Model crashes at step 0 | Bathymetry values have wrong sign or wrong units | Ocean depth must be negative; check magnitude |
| `readBinaryPrec` mismatch | 64-bit file but model expects 32-bit (or vice versa) | Set `readBinaryPrec=64` in `&PARM01` or regenerate file |
| Forcing has wrong phase | Time-varying forcing file sequence offset | Check `forcing_period` vs file iteration numbers |
| xmitgcm dimension error | `iters` list contains non-existent iteration | Use `iters='all'` to auto-detect |
