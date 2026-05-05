# Fedora 44 Repair Log

## 🛠️ Applied Fixes

### 📦 python-samseg
- **Fix:** Removed `BuildRequires: vtk-devel < 9.3`. Fedora 44 has VTK 9.5.2, and this restriction was causing build dependency failures.
- **Fix:** Added `-std=c++17` and `-fpermissive` to `CXXFLAGS` (already present but verified).

### 📦 python-charm-gems
- **Fix:** Removed `BuildRequires: vtk-devel < 9.3`.
- **Fix:** Verified `-std=c++17` and `-fpermissive` are present.

### 📦 freesurfer
- **Fix:** Added `-std=gnu17` to `CFLAGS` to handle C23 prototype changes in GCC 15.
- **Fix:** Verified `-fpermissive` and `-include cstdint` in `CXXFLAGS`.

### 📦 mrtrix3
- **Fix:** Added `-std=gnu++17` and `-fpermissive` to handle GCC 15 template strictness.

### 📦 quit
- **Fix:** Added `-std=gnu17` to `CFLAGS` for C23 compatibility.
- **Fix:** Added `-include cstdint` to `CXXFLAGS` for missing headers in GCC 15.
- **Fix:** Verified `-Wno-template-body` is present.

## 🚀 Next Steps
1. Push these updated spec files to `neurofedora-species` repo.
2. Trigger Copr builds for Fedora 44.
3. Investigate `python-fmm3dpy` failure (likely meson/python 3.14 related).
