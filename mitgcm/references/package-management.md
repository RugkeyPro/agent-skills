# MITgcm Package Management Reference

## The Two-Step Activation Principle

MITgcm functionality is modular. Every package must be activated in **two independent and separate steps**. Completing only one step causes silent failure — the package is either not compiled in, or compiled in but never initialized at runtime.

### Step A — Compile-time inclusion (`code/packages.conf`)

Add the package name (one per line) to the experiment's `code/packages.conf`:
```
gfd
mom_advdiff
kpp
gmredi
ptracers
gchem
```

Lines starting with `#` are comments. Package names are case-sensitive (all lowercase).

Alternatively, pass `-enable=pkgname` to `genmake2`:
```bash
../../../tools/genmake2 -mpi -mods=../code \
    -enable=kpp -enable=gmredi \
    -of=../../../tools/build_options/linux_amd64_gfortran
```

> **After changing `packages.conf`, a full recompile is required.** See `compilation.md`.

### Step B — Runtime activation (`input/data.pkg`)

In `input/data.pkg`, set the corresponding flag to `.TRUE.` in the `&PACKAGES` namelist:
```fortran
&PACKAGES
 useKPP      = .TRUE.,
 useGMRedi   = .TRUE.,
 usePTRACERS = .TRUE.,
 useGCHEM    = .TRUE.,
&
```

Runtime flags follow the naming pattern `use` + PascalCase package name. Check the package's own documentation for the exact flag name.

---

## Package Dependency Matrix

Some packages have mandatory prerequisites. Always check before enabling:

| Package | Requires | Notes |
|---------|---------|-------|
| `gchem` | `ptracers` | gchem operates on passive tracers defined by ptracers |
| `thsice` | `exf` (recommended) | Sea-ice thermodynamics needs external forcing fields |
| `seaice` | `exf` (recommended) | Dynamics sea-ice package also needs atmospheric forcing |
| `offline` | Pre-generated velocity/diffusivity snapshots | Advection-only mode; offline files must match grid exactly |
| `diagnostics` | None mandatory | But output fields must be registered in `data.diagnostics` |
| `mnc` | NetCDF library at compile time | Must be available in the build environment |
| `ctrl` | `optim` (for adjoint) | Control vector package for optimization/adjoint runs |

---

## Common Package Configurations

### Ocean biogeochemistry (passive tracers + chemistry)
```
# packages.conf
ptracers
gchem
```
```fortran
! data.pkg
&PACKAGES
 usePTRACERS = .TRUE.,
 useGCHEM    = .TRUE.,
&
```
Tracer initial conditions and sources/sinks are configured in `data.ptracers` and the specific `gchem` subpackage data file.

### KPP vertical mixing
```
# packages.conf
kpp
```
```fortran
! data.pkg
&PACKAGES
 useKPP = .TRUE.,
&
```
KPP parameters go in `data.kpp`.

### GM/Redi mesoscale eddy parameterization
```
# packages.conf
gmredi
```
```fortran
! data.pkg
&PACKAGES
 useGMRedi = .TRUE.,
&
```
Parameters in `data.gmredi`. Note: GM in residual-mean formulation (`GM_InMomAsStress`) changes momentum equations.

### Sea-ice with thermodynamics and external forcing
```
# packages.conf
seaice
thsice
exf
```
```fortran
! data.pkg
&PACKAGES
 useSEAICE = .TRUE.,
 useThSIce = .TRUE.,
 useEXF    = .TRUE.,
&
```

### NetCDF output (pkg/mnc)
```
# packages.conf
mnc
```
```fortran
! data.pkg
&PACKAGES
 useMNC = .TRUE.,
&
```
> MNC still outputs **one `.nc` file per tile**. Use `gluemncbig` or `xmitgcm` to assemble global files in post-processing.

---

## Diagnosing Package Issues

| Symptom | Likely cause |
|---------|-------------|
| Package routines not compiled | Missing from `packages.conf`; check with `grep -r pkgname model/` after compile |
| Package compiled but does nothing | `useXxx=.TRUE.` missing in `data.pkg` |
| Runtime error referencing package arrays | Package enabled in `data.pkg` but not in `packages.conf` → binary lacks arrays |
| gchem tracer values stay at initial condition | `usePTRACERS` not enabled alongside `useGCHEM` |
| thsice has no effect on SST | `useEXF` not enabled; no surface heat flux is reaching thsice |
