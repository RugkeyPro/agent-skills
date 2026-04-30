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

---

## Creating a New MITgcm Package

This section covers the full workflow for writing a brand-new package and hooking it into the `gchem` framework. The lessons here come from creating `pesticides` as a `gchem` sub-package.

### Milestone-first mindset

Split the work into two separate milestones and complete them in order:

1. **Milestone 1 — Compile integration**: `mitgcmuv` links successfully with the new package compiled in. The runtime switch (`usePESTICIDES = .FALSE.`) stays off; no physics runs yet.
2. **Milestone 2 — Runtime physics**: Turn on the switch, add tracer initial conditions, implement tendency calculations.

Do not try to implement physical processes until Milestone 1 is solid. A partial implementation that compiles cleanly is far more useful than complete physics that prevents the binary from linking.

### Recommended skeleton workflow

1. **Bootstrap the package directory** with the following files (copy-paste structure from a similar package such as `pkg/microp` or `pkg/pollutant` — isomorphic copying is safer than inventing new interfaces):
   ```
   pkg/pesticides/
   ├── README                  # one-paragraph summary
   ├── TODO                    # known gaps, planned tracers
   ├── PESTICIDES_SIZE.h       # tracer count constant (e.g. Nr_PEST = 3)
   ├── PESTICIDES_OPTIONS.h    # cpp options block
   ├── PESTICIDES.h            # COMMON block for runtime arrays
   └── pesticides_*.F          # stub routines (see below)
   ```

2. **Fix tracer design early** — decide tracer names, count (`Nr_PEST`), and whether they live inside ptracers slots. Changing this later forces cascading edits across `GCHEM.h`, `data.gchem`, and all tendency routines.

3. **Write stub routines first**, each with only the subroutine signature, a one-line comment, and a bare `RETURN`. The minimum set needed for `gchem` integration:
   - `pesticides_readparms.F`
   - `pesticides_init_fixed.F`
   - `pesticides_fields_load.F`
   - `pesticides_tr_register.F`
   - `pesticides_calc_tendency.F`
   - `pesticides_diagnostics_init.F`
   - `pesticides_check.F`

4. **Walk the gchem call chain** — do not assume `gchem` already has your hook. Verify each entry point by grepping the gchem sources:
   ```bash
   grep -n "PESTICIDES\|pesticides" pkg/gchem/*.F pkg/gchem/*.h
   ```
   The seven files to check (and add calls to if missing):
   | gchem file | what to add |
   |---|---|
   | `gchem_readparms.F` | `CALL PESTICIDES_READPARMS(...)` inside `USE_PESTICIDES` block |
   | `gchem_fields_load.F` | `CALL PESTICIDES_FIELDS_LOAD(...)` |
   | `gchem_init_fixed.F` | `CALL PESTICIDES_INIT_FIXED(...)` |
   | `gchem_tr_register.F` | `CALL PESTICIDES_TR_REGISTER(...)` |
   | `gchem_calc_tendency.F` | `CALL PESTICIDES_CALC_TENDENCY(...)` |
   | `gchem_diagnostics_init.F` | `CALL PESTICIDES_DIAGNOSTICS_INIT(...)` |
   | `gchem_check.F` | `CALL PESTICIDES_CHECK(...)` |

   The most commonly missing entry point is `gchem_check.F` — it is easy to overlook because it is not in the physics path.

5. **Add the compile-time switch to `GCHEM.h`** (alongside existing flags such as `USE_BLING`, `USE_DARWIN`):
   ```fortran
   #ifdef ALLOW_PESTICIDES
   # define USE_PESTICIDES
   #endif
   ```
   And add `usePESTICIDES` to the `COMMON /GCHEM_PARMS/` block.

6. **Add `ALLOW_PESTICIDES` to `PESTICIDES_OPTIONS.h`** and include it from `GCHEM_OPTIONS.h` if the gchem framework uses a centralised options file.

7. **Add the runtime namelist** in `gchem_readparms.F`:
   ```fortran
   NAMELIST /GCHEM_PARMS/ usePESTICIDES
   ```
   See fixed-form Fortran rules below before editing this file.

### Narrow-compile strategy

Do not run full `make` until the narrow compile passes. Target only the object files closest to your new switch:

```bash
# Inside build/ after make depend:
make gchem_readparms.o
make gchem_check.o
make gchem_add_tendency.o
make gchem_calc_tendency.o
```

Fix each error before widening scope. Only after all four compile cleanly run `make` for the full binary.

### Fixed-form Fortran rules (critical)

MITgcm Fortran source uses **fixed-form** layout. The preprocessor (`cpp`) and `set64bitConst.sh` expand macros before the compiler sees the file. Violations are invisible in the original source but blow up in the `build/` intermediate `.f` files.

**Column rules:**
- Columns 1–5: statement label (blank if none)
- Column 6: continuation character (use `&` or `+`; must be exactly in column 6, not 7)
- Columns 7–72: code
- Column 73+: ignored (invisible to compiler — a variable name that wraps past column 72 is silently truncated)

**`COMMON` blocks** — keep all variables on one line if possible. If you must continue, place `&` in column 6 of the continuation line (not column 7):
```fortran
      COMMON /GCHEM_PARMS/
     &  usePESTICIDES,
     &  useBLING
```
A stray space before `&` that pushes it to column 7 silently corrupts the entire `COMMON` block.

**`NAMELIST` declarations** — these are even more brittle than `COMMON` under continuation. The safest approach is one variable per `NAMELIST` declaration:
```fortran
      NAMELIST /GCHEM_PARMS/ usePESTICIDES
      NAMELIST /GCHEM_PARMS/ useBLING
```
Multi-variable `NAMELIST` with continuation lines has caused silent misparse in practice. Prefer the single-variable form.

**Always verify the expanded `.f` file** in `build/` before assuming the source is correct:
```bash
# After make depend / partial make:
grep -n "usePESTICIDES" build/gchem_readparms.f
```
Many column errors only become visible after cpp expansion.

### Data files for the new package

Add a `data.pesticides` namelist file and reference it from `data.gchem`:
```fortran
! data.gchem
&GCHEM_PARM1
 usePESTICIDES = .FALSE.,   ! keep FALSE during Milestone 1
&
```

Keep `usePESTICIDES = .FALSE.` until Milestone 2. This lets you verify the binary links without actually running any pesticide calculations.

### Pitfall summary

| Pitfall | What happened | Fix |
|---------|--------------|-----|
| Column-6 continuation in `COMMON` | A space pushed `&` to column 7; the entire `COMMON` block was silently corrupted | Move `&` back to exactly column 6 |
| `NAMELIST` continuation failure | Multi-variable `NAMELIST` with `&` continuation misparsed after cpp | Rewrite as one variable per `NAMELIST` statement |
| `gchem_check.F` hook missing | Binary compiled but runtime CHECK phase crashed | Add `CALL PESTICIDES_CHECK` to `gchem_check.F` |
| Editing `build/*.f` instead of source | Full `make` regenerates `.f` from `.F`; edits to `build/` are lost | Always edit `pkg/pesticides/*.F` source files |
| Trying to fix source without reading `build/` | Column errors invisible in `.F` because cpp hasn't run yet | Check `build/*.f` to see the post-cpp layout |
