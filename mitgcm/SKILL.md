---
name: mitgcm
description: "MITgcm full-workflow skill covering compilation (SIZE.h static memory,
  genmake2 build chain), package management (two-step activation), runtime namelist
  config, binary I/O (Big-Endian, Fortran-order), MPI/OpenMP parallel constraints,
  xmitgcm post-processing, LLC grid handling, and ECCO offline state estimation.
  TRIGGER when user mentions: MITgcm, mitgcm, mitgcmuv, genmake2, SIZE.h, mdsio,
  xmitgcm, open_mdsdataset, LLC90, LLC270, LLC4320, ECCO, packages.conf, data.pkg,
  eedata, deltaTClock, CFL stability, bathymetry .bin, Big-Endian ocean model,
  or any MITgcm package name such as KPP, GM, ptracers, thsice, exf, gchem,
  seaice, offline, mnc, gmredi, diagnostics."
---

# MITgcm Skill

## Mandatory Checklists (Apply to Every Conversation)

Whenever you assist with MITgcm tasks, always enforce the following:

**Python scripts:**
- File naming: `test_*.py` for tests · `plot_*.py` for figures · `process_*.py` for data processing
- Always use `xmitgcm` (`open_mdsdataset`) to read MITgcm output — never parse `.data`/`.meta` files manually
- Execute Python scripts by switching to the `mitgcm` conda environment first

**Code quality:**
- If any code section contains placeholder data, stub implementations, or simplified stand-ins for real functionality, **warn the user explicitly in every response** until resolved
- After the user confirms results are correct, remind them to delete all test scripts and placeholder data files

---

## Domain Index

Load the relevant reference file(s) when a topic is raised. Multiple files may be needed.

| Topic | Reference File | Key triggers |
|-------|---------------|--------------|
| Compilation & build | `references/compilation.md` | `genmake2`, `SIZE.h`, `make`, `build`, `sNx`, `nPx`, `Nr`, compile error |
| Package management | `references/package-management.md` | `packages.conf`, `data.pkg`, `useKPP`, `gchem`, `ptracers`, `thsice`, enable/disable pkg |
| Runtime config (namelists) | `references/runtime-config.md` | `data` file, `&PARM`, `deltaTClock`, `nonHydrostatic`, `implicitFreeSurface`, `exactConserv` |
| Data I/O & grid | `references/data-io.md` | `.bin`, `.data`, `.meta`, `bathymetry`, `forcing`, `Big-Endian`, Arakawa C-grid, `mnc`, `NetCDF` |
| Parallel computing | `references/parallel-computing.md` | `mpirun`, `eedata`, `nTx`, `nTy`, `OMP_NUM_THREADS`, OpenMP, MPI |
| Post-processing & visualization | `references/postprocess.md` | `xmitgcm`, `open_mdsdataset`, `plot_`, `process_`, LLC visualization, `pyresample`, `cartopy` |
| ECCO / LLC offline | `references/ecco-offline.md` | `LLC90`, `LLC270`, `LLC4320`, `ECCO`, `offline`, `offlineForcingPeriod`, 1170×90, compact format |

---

## Critical Rules (Always Apply)

### Static Memory — Recompile Triggers
MITgcm uses **static memory allocation only** (no Fortran 90 dynamic allocation). Whenever the user changes any of the following in `code/SIZE.h`, **immediately warn that a full recompile is required**:
- `sNx`, `sNy` — tile dimensions
- `Nr` — vertical levels
- `nPx`, `nPy` — MPI process counts
- `nSx`, `nSy` — tiles per process

### Package Two-Step Activation
Every MITgcm package must be activated in **two independent steps**:
1. `code/packages.conf` — compile-time inclusion
2. `input/data.pkg` → `&PACKAGES` block — runtime enable (`useXxx=.TRUE.`)

Omitting either step is a silent failure mode. Always check both.

### Non-Hydrostatic Triplet
If `nonHydrostatic=.TRUE.` is set, **all three** must be present:
```fortran
 nonHydrostatic      = .TRUE.,
 implicitFreeSurface = .TRUE.,
 exactConserv        = .TRUE.,
```

### xmitgcm Is Mandatory
Never suggest manually reading `.data`/`.meta` binary files with raw `numpy.fromfile` or similar. Always use:
```python
from xmitgcm import open_mdsdataset
ds = open_mdsdataset(data_dir, grid_dir=grid_dir, iters='all')
```

### Conda Environment
All Python scripts must be run inside the `mitgcm` conda environment:
```bash
conda activate mitgcm
python process_myanalysis.py
```

---

## Quick Reference: Compilation Command Chain

For details see `references/compilation.md`. The condensed chain is:

```bash
sudo su mitgcmer
# In build/:
rm * -rf
# In run/:
rm *.data *.meta STD*
# Back in build/:
export MPI_HOME=/usr
../../../tools/genmake2 -mpi -mods=../code \
  -of=../../../tools/build_options/linux_amd64_gfortran
make depend
make
cp mitgcmuv ../run
# Determine cores from SIZE.h: cores = nPx × nPy
mpirun -n {cores} ./mitgcmuv
# or with hyperthreading:
mpirun -n {cores} --use-hwthread-cpus ./mitgcmuv
```

> CFL stability check after run: `grep -E "%MON (trAdv_CFL|advcfl)" STDOUT.0000`

---

## Common Pitfalls

| Symptom | Likely Cause | Reference |
|---------|-------------|-----------|
| Array out-of-bounds crash | `SIZE.h` mismatch, forgot to recompile | `compilation.md` |
| Package has no effect | Only did one of the two activation steps | `package-management.md` |
| Model blows up at step 1 | `deltaTClock` too large (CFL > 0.8) | `compilation.md` §CFL |
| Output files are zeros | Wrong endianness in forcing/bathymetry | `data-io.md` |
| LLC plot has discontinuities | Used 2D lat/lon interpolation instead of 3D Cartesian | `ecco-offline.md` |
| `mpirun` fails with wrong process count | `nPx×nPy` in SIZE.h ≠ `-n` argument | `parallel-computing.md` |
