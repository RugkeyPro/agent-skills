# MITgcm Compilation Reference

## Static Memory Allocation — Fundamental Constraint

MITgcm does **not** use dynamic (Fortran 90) memory allocation. Every array dimension is fixed at compile time through `code/SIZE.h`. This is non-negotiable and cannot be worked around at runtime.

**Any change to the following parameters in `SIZE.h` requires a full recompile:**

| Parameter | Meaning |
|-----------|---------|
| `sNx` | Number of X points per tile |
| `sNy` | Number of Y points per tile |
| `Nr` | Number of vertical levels |
| `nPx` | Number of MPI processes in X |
| `nPy` | Number of MPI processes in Y |
| `nSx` | Number of tiles per process in X |
| `nSy` | Number of tiles per process in Y |
| `OLx` / `OLy` | Tile overlap (halo) width |

**Full domain size is derived automatically:**
```fortran
Nx = sNx * nSx * nPx   ! Total X points
Ny = sNy * nSy * nPy   ! Total Y points
```

**Example SIZE.h block:**
```fortran
PARAMETER (
 &           sNx =  90,
 &           sNy =  30,
 &           OLx =   2,
 &           OLy =   2,
 &           nSx =   1,
 &           nSy =   1,
 &           nPx =   4,
 &           nPy =   3,
 &           Nx  = sNx*nSx*nPx,
 &           Ny  = sNy*nSy*nPy,
 &           Nr  =  50)
```
This example: 4×3 = **12 MPI processes**, 360×90 global grid, 50 levels.

---

## Standard Build Workflow (7 Steps)

### Step 1 — Switch to build user
```bash
sudo su mitgcmer
```

### Step 2 — Clean old build artifacts
When `SIZE.h` or `packages.conf` has been modified, do a full clean:
```bash
# In the build directory:
cd /path/to/experiment/build
rm * -rf

# In the run directory, remove old outputs:
cd ../run
rm *.data *.meta STD*
```
> Skipping this step after `SIZE.h` changes will produce a binary with mismatched array sizes — the model will either crash immediately or produce silently wrong results.

### Step 3 — Generate Makefile
```bash
cd ../build
export MPI_HOME=/usr
../../../tools/genmake2 \
    -mpi \
    -mods=../code \
    -of=../../../tools/build_options/linux_amd64_gfortran
```

Key flags:
- `-mpi` — enable MPI parallel build (required; rebuilding without it disables MPI)
- `-mods=../code` — path to experiment-specific overrides (`SIZE.h`, `DIAGNOSTICS_SIZE.h`, custom `.F` files)
- `-of=...` — compiler option file; `linux_amd64_gfortran` is the standard for modern Linux + GFortran

### Step 4 — Resolve dependencies
```bash
make depend
```
This generates include-file dependency chains. Must be re-run whenever `.h` files change.

### Step 5 — Compile
```bash
make
```
Uses all available cores by default. To limit: `make -j4`.

Common errors:
- `SIZE.h not found` → the `-mods` path is wrong; verify `../code/SIZE.h` exists
- `Implicit type` errors → missing CPP macro; check `packages.conf` or `CPP_OPTIONS.h`
- Linker errors with MPI symbols → `MPI_HOME` not set, or `-mpi` flag missing

### Step 6 — Deploy executable
```bash
cp mitgcmuv ../run
cd ../run
```

### Step 7 — Determine core count and run

**The total MPI process count is dictated by `SIZE.h`:**
```
Total cores = nPx × nPy
```
This value must match the `-n` argument to `mpirun`. Using a different number causes immediate failure (MPI topology mismatch).

**Standard run:**
```bash
mpirun -n {nPx*nPy} ./mitgcmuv
# Example (nPx=4, nPy=3 → 12 cores):
mpirun -n 12 ./mitgcmuv
```

**Hyperthreading / oversubscription mode:**

When the node has Hyper-Threading enabled, each physical core exposes two logical threads. If `nPx × nPy` exceeds the physical core count but is within the logical thread count, use `--use-hwthread-cpus`:
```bash
mpirun -n 12 --use-hwthread-cpus ./mitgcmuv
```
This flag tells Open MPI to include hardware threads (HT/SMT logical CPUs) in its available slot pool, allowing oversubscription without explicit `--oversubscribe`. Useful when, e.g., you have 6 physical cores with HT → 12 logical threads, and `nPx*nPy = 12`.

> **Note:** `--use-hwthread-cpus` is an Open MPI flag. For MPICH-based MPI, use `-bind-to hwthread` instead.

---

## CFL Stability Monitoring and Time-Step Optimization

After each run, **check the CFL numbers before proceeding**. MITgcm prints monitoring statistics to `STDOUT.0000` (for MPI rank 0).

### Extract CFL lines:
```bash
grep -E "%MON (trAdv_CFL|advcfl)" STDOUT.0000
```

### Typical output:
```
%MON trAdv_CFL_u_max =  3.4560E-01
%MON trAdv_CFL_v_max =  2.0110E-01
%MON trAdv_CFL_w_max =  8.3200E-02
%MON advcfl_uvel_max =  2.8910E-01
%MON advcfl_vvel_max =  1.9450E-01
%MON advcfl_wvel_max =  7.1200E-02
```

The most critical value is typically `trAdv_CFL_u_max` or `advcfl_uvel_max`.

### Decision table:

| Max CFL value | Stability status | Recommended action |
|---------------|-----------------|-------------------|
| < 0.5 | Stable | May cautiously increase `deltaTClock` by ≤ 20% |
| 0.5 – 0.8 | Marginal | Keep current `deltaTClock`; monitor closely |
| > 0.8 | Unstable risk | Reduce `deltaTClock` by factor 0.5–0.75, rerun |
| NaN / blow-up | Crashed | Reduce `deltaTClock` × 0.5; inspect forcing field magnitudes |

### Adjusting time step — no recompile needed:
Edit `input/data`:
```fortran
&PARM03
 deltaTClock  = 1800.0,   ! was 3600.0
 deltaTMom    = 1800.0,
 deltaTtracer = 1800.0,
&
```
> `deltaTClock`, `deltaTMom`, and `deltaTtracer` must remain physically consistent. See `runtime-config.md` for details.

### Iterative tuning workflow:
1. Run with conservative `deltaTClock` (e.g., 900 s)
2. Check `grep "%MON trAdv_CFL" STDOUT.0000`
3. If max CFL < 0.5 after the first 10 time steps, increase by 50% and rerun
4. Repeat until CFL settles in the 0.3–0.5 range for optimal efficiency
5. For long production runs, aim for CFL ≈ 0.4 as a safety margin

---

## Re-running After Parameter Changes

| What changed | Action required |
|-------------|----------------|
| `SIZE.h` parameters | Full clean + recompile (Steps 2–7) |
| `packages.conf` | Full clean + recompile (Steps 2–7) |
| Custom `.F` source files | `make depend` + `make` (Steps 4–7) |
| `input/data` namelist | No recompile; edit and rerun Step 7 |
| `input/data.pkg` runtime flags | No recompile; edit and rerun Step 7 |
| Forcing/bathymetry `.bin` files | No recompile; replace files and rerun Step 7 |
