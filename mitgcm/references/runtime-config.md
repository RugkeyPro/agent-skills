# MITgcm Runtime Configuration Reference

## Namelist File Overview

Runtime parameters are distributed across multiple Fortran namelist files:

| File | Content |
|------|---------|
| `input/data` | Core model parameters (grid, time-stepping, physics, I/O) |
| `input/eedata` | Execution environment parameters (threading, MPI) |
| `input/data.pkg` | Package enable/disable flags |
| `input/data.kpp` | KPP mixing parameters |
| `input/data.gmredi` | GM/Redi eddy parameters |
| `input/data.ptracers` | Passive tracer configuration |
| `input/data.diagnostics` | Diagnostics output configuration |
| `input/data.exf` | External forcing field paths and periods |
| `input/data.offline` | Offline advection field paths and periods |
| `input/data.mnc` | NetCDF output configuration |

---

## Fortran Namelist Syntax Rules

MITgcm uses standard Fortran namelist syntax with one important extension:

```fortran
&PARM01
# This is a comment (MITgcm-specific: # not ! for inline comments)
 tRef   = 20*20.0,          ! 20 levels all set to 20°C
 sRef   = 20*35.0,
 viscAh = 1000.0,
 diffKhT= 500.0,
&

&PARM02
 ...
&
```

**Key syntax rules:**
- Block starts with `&PARMXX`, ends with `&` or `/`
- Comments use `#` at the start of a line (MITgcm pre-processes these before Fortran sees them)
- Inline Fortran comments (`!`) also work after values
- Repeated values: `N*value` sets N consecutive array elements to the same value
- Always end parameter assignments with a comma, including the last one in a block
- Logical values: `.TRUE.` / `.FALSE.` (with dots; not `T` or `F`)

---

## Core Parameter Blocks (`input/data`)

### &PARM01 — Equations of state, viscosity, diffusivity
```fortran
&PARM01
# Reference temperature/salinity profiles (one value per level, or N*value)
 tRef       = 50*2.0,
 sRef       = 50*34.5,
# Horizontal viscosity (m^2/s)
 viscAh     = 1000.0,
# Horizontal diffusivity for tracers
 diffKhT    = 500.0,
 diffKhS    = 500.0,
# Implicit vertical diffusivity
 implicitDiffusion = .TRUE.,
 diffKzT    = 1.E-5,
&
```

### &PARM03 — Time-stepping
```fortran
&PARM03
# Master clock — controls output timing and package clocks
 deltaTClock  = 3600.0,
# Momentum time step (can differ from tracer for stability)
 deltaTMom    = 3600.0,
# Tracer time step
 deltaTtracer = 3600.0,
# Total number of time steps
 nTimeSteps   = 8760,
# Or equivalently set end time:
# endTime = 3.1536E7,
&
```

### &PARM04 — Grid specification
```fortran
&PARM04
# Cartesian grid with uniform spacing
 usingCartesianGrid = .TRUE.,
 delX = 360*1.0,      ! 360 1-degree cells in X
 delY = 160*1.0,      ! 160 1-degree cells in Y
# Spherical polar grid:
# usingSphericalPolarGrid = .TRUE.,
# xgOrigin = 0.0,
# ygOrigin = -80.0,
&
```

### &PARM05 — Input files
```fortran
&PARM05
 bathyFile      = 'bathymetry.bin',
 hydrogThetaFile= 'init_T.bin',
 hydrogSaltFile = 'init_S.bin',
&
```

---

## Time-Step Consistency Rules

When using the offline package or complex forcing, all time scales must be physically consistent:

```
deltaTClock  == deltaTMom  == deltaTtracer   (in most configurations)
```

For split-explicit time-stepping:
- `deltaTfreesurf` < `deltaTmom` (sub-cycling for free surface)
- Ratio `deltaTmom / deltaTfreesurf` should be an integer

**For offline advection specifically:**
```fortran
&OFFLINE
 offlineForcingPeriod = 2592000.0,   ! 30-day snapshots
 offlineForcingCycle  = 31536000.0,  ! 1-year repeat cycle
&
```
These must correspond exactly to the timestamps in the offline forcing files. See `ecco-offline.md` for validation.

---

## Non-Hydrostatic Configuration

When enabling non-hydrostatic approximation, **all three parameters must be set together**:

```fortran
&PARM01
 nonHydrostatic      = .TRUE.,
 implicitFreeSurface = .TRUE.,
 exactConserv        = .TRUE.,
&
```

**Why all three are required:**
- `nonHydrostatic` activates vertical momentum and pressure solver
- `implicitFreeSurface` is required for stability with non-hydrostatic pressure
- `exactConserv` ensures exact volume conservation — omitting it causes mass drift with non-hydrostatic dynamics

Setting `nonHydrostatic=.TRUE.` without the other two will likely produce incorrect or unstable results without necessarily producing an error message.

---

## Free Surface Options

```fortran
&PARM01
# Implicit free surface (standard, recommended)
 implicitFreeSurface = .TRUE.,
# Rigid lid (legacy, avoids fast barotropic waves)
# rigidLid = .TRUE.,
# Linear free surface (cheaper, less accurate)
# linearFS = .TRUE.,
&
```

For volume conservation with implicit free surface:
```fortran
 exactConserv = .TRUE.,
```

---

## Diagnostics Configuration (`input/data.diagnostics`)

```fortran
&DIAGNOSTICS_LIST
# Output frequency in seconds (negative = per-timestep output)
 frequency(1)  = 2592000.0,
 fields(1,1)   = 'THETA   ',
 fields(2,1)   = 'SALT    ',
 fields(3,1)   = 'UVEL    ',
 fields(4,1)   = 'VVEL    ',
 fileName(1)   = 'diag_state',
&
```

Available diagnostic names can be found by running the model with `dumpInitAndLast=.TRUE.` or checking `pkg/diagnostics/DIAGNOSTICS_SIZE.h`.

---

## Boundary Conditions

Open boundary conditions (package `obcs`):
```fortran
&OBCS_PARM01
 useOBCS      = .TRUE.,
 OBCsEast     = .TRUE.,
 OBCsWest     = .TRUE.,
 OBCsNorth    = .FALSE.,
 OBCsSouth    = .FALSE.,
&
```

Sponge layers at boundaries help smooth out artificial reflections.
