# MITgcm Parallel Computing Reference

## MPI Distributed Memory Parallelism

### Core Consistency Rule (Critical)

The total number of MPI processes launched by `mpirun` **must exactly equal** `nPx × nPy` as specified in `code/SIZE.h`. There is no runtime detection or fallback — a mismatch causes immediate failure.

```
mpirun -n N ./mitgcmuv   →   N must equal nPx × nPy
```

Example:
```fortran
! SIZE.h
PARAMETER (nPx = 4, nPy = 3, ...)   ! 12 processes total
```
```bash
mpirun -n 12 ./mitgcmuv              # correct
mpirun -n 8  ./mitgcmuv              # WRONG — will fail or corrupt results
```

### Standard MPI Tile Layout

For typical MPI-only runs (no OpenMP):
```fortran
PARAMETER (
 &  nSx = 1,    ! 1 tile per process in X — standard
 &  nSy = 1,    ! 1 tile per process in Y — standard
 &  nPx = 4,    ! 4 MPI processes in X
 &  nPy = 3,    ! 3 MPI processes in Y
 &  ...)
```

Each MPI rank owns one tile of dimensions `(sNx × sNy)`.

### Running with MPI

**Standard run:**
```bash
mpirun -n 12 ./mitgcmuv
```

**With hardware thread (hyperthreading) support:**
```bash
mpirun -n 12 --use-hwthread-cpus ./mitgcmuv
```
Use `--use-hwthread-cpus` when `nPx × nPy` exceeds physical core count but fits within logical thread count (e.g., 6 physical cores × 2 HT threads = 12 logical CPUs).

**Oversubscription (use sparingly):**
```bash
mpirun -n 24 --oversubscribe ./mitgcmuv
```
Only appropriate for testing, not production runs.

**CPU binding (for NUMA-aware performance):**
```bash
mpirun -n 12 --bind-to core ./mitgcmuv
```

### Recompile Required for MPI Changes
Any change to `nPx`, `nPy`, `nSx`, or `nSy` in `SIZE.h` requires a full recompile with `-mpi` flag. A binary compiled without `-mpi` cannot run with `mpirun` (or will run as a single process ignoring MPI).

---

## OpenMP Shared Memory Parallelism

### Configuration Files

OpenMP threading is configured in `input/eedata` (without recompiling):

```fortran
&EEPARMS
 nTx = 2,   ! Thread count in X
 nTy = 1,   ! Thread count in Y
&
```

### Consistency Rules

1. `nTx × nTy` must equal the value of `OMP_NUM_THREADS` in the environment:
   ```bash
   export OMP_NUM_THREADS=2
   ./mitgcmuv
   ```

2. The number of tiles per process (`nSx × nSy` in `SIZE.h`) must be divisible by the thread count:
   ```
   nSx * nSy mod (nTx * nTy) == 0
   ```
   Example: `nSx=2, nSy=2` → 4 tiles per process → can use `nTx*nTy = 1, 2, or 4` threads.

### Typical SIZE.h for OpenMP:
```fortran
PARAMETER (
 &  sNx = 60,
 &  sNy = 60,
 &  nSx = 2,    ! 2 tiles per process in X
 &  nSy = 2,    ! 2 tiles per process in Y  → 4 tiles total per rank
 &  nPx = 2,
 &  nPy = 2,
 &  ...)
```
```fortran
! eedata
&EEPARMS
 nTx = 2,
 nTy = 2,    ! 4 threads per process
&
```
```bash
export OMP_NUM_THREADS=4
mpirun -n 4 ./mitgcmuv
```

---

## Hybrid MPI + OpenMP

For large-scale runs using both:

| Parameter | Location | Value |
|-----------|----------|-------|
| `nPx`, `nPy` | `SIZE.h` | Total MPI processes in X/Y |
| `nSx`, `nSy` | `SIZE.h` | Tiles per MPI rank (≥ nTx×nTy) |
| `nTx`, `nTy` | `eedata` | OpenMP threads per rank |
| `OMP_NUM_THREADS` | Shell env | Must equal `nTx × nTy` |

Total concurrency = `(nPx × nPy) × (nTx × nTy)`

---

## Diagnosing Parallel Issues

| Symptom | Likely cause |
|---------|-------------|
| `MPI_Comm_size` mismatch error | `mpirun -n N` ≠ `nPx × nPy` in SIZE.h |
| Model hangs after "Starting..." | Deadlock — usually one rank failed to initialize; check all `STDOUT.*` files |
| Non-reproducible results | Data race in OpenMP region; check `OMP_NUM_THREADS` vs `nTx×nTy` |
| Halo exchange errors | `OLx`/`OLy` too small for the stencil width of the chosen advection scheme |
| Tile boundary artifacts in output | `nSx`/`nSy` > 1 with a package that doesn't support multi-tile; set `nSx=nSy=1` |

---

## Output Files per MPI Rank

Each MPI rank writes its own `STDOUT.XXXX` file (`STDOUT.0000` for rank 0). When diagnosing issues:
```bash
# Check all ranks for errors
grep -l "ABNORMAL" STDOUT.*

# Monitor CFL across all ranks
grep "%MON trAdv_CFL_u_max" STDOUT.* | sort -t= -k2 -n | tail -5
```
