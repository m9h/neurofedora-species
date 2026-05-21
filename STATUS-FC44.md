# Fedora 44 Build Status & Plan

## ✅ Recently Verified & Fixed (GCC 15 / ITK 5.4)
The following packages have been updated and verified to build on Fedora 44 (Rawhide) with GCC 15 and ITK 5.4.5:

### 📦 freesurfer (8.2.0-7)
- **Status:** ✅ Fixed.
- **Fixes:** Applied `-std=gnu17` for bundled C libs, `-fpermissive` for C++, and unbundled `libxml2`, `expat`, `tetgen`. Guarded SSE intrinsics for aarch64.

### 📦 mrtrix3 (3.0.8-1)
- **Status:** ✅ Fixed.
- **Fixes:** Added `-std=gnu++17` and `-fpermissive` to handle GCC 15 template strictness.

### 📦 simnibs (4.6.0-1)
- **Status:** ✅ Updated.
- **Fixes:** Ported to CGAL 6 (replaced `boost::optional` with `std::optional`, fixed const-correctness). Fixed GCC 15 C/C++ standard compliance.

### 📦 python-samseg (0.5a0-1)
- **Status:** ✅ Updated.
- **Fixes:** Migrated to ITK 5.4 API (SmartPointer `nullptr` fixes, `itkMacro.h` includes).

### 📦 python-charm-gems (1.3.3-2)
- **Status:** ✅ Fixed.
- **Fixes:** Complete migration to ITK 5.4 threading and SmartPointer APIs.

### 📦 quit (3.4-1)
- **Status:** ✅ Fixed.
- **Fixes:** Workaround for `fmt` v11 implicit ostream removal. Added `-Wno-template-body` for GCC 15.

### 📦 babelbrain (0.8.1-1)
- **Status:** ✅ Fixed.
- **Fixes:** Official update to v0.8.1 release tag. Verified build on Fedora 44.

### 📦 open-ephys-gui (1.0.2-1)
- **Status:** ✅ Fixed.
- **Fixes:** Major update to 1.0. Migrated to **Qt6 and CMake**. Fixed manual installation paths for binary, plugins, and resources.

### 📦 labrecorder (1.17.1-1)
- **Status:** ✅ Fixed.
- **Fixes:** Updated to latest and migrated to **Qt6**. Fixed `liblsl` unbundling.

### 📦 brainflow (5.21.0-1)
- **Status:** ✅ Updated.
- **Fixes:** Verified build for version 5.21.0.

### 📦 morpheus (2.3.9-1)
- **Status:** ✅ Updated.
- **Fixes:** Fixed `%autosetup` directory mapping for version 2.3.9.

### 📦 afni (26.1.01-1)
- **Status:** ✅ Updated.
- **Fixes:** Verified build for version 26.1.01.

## 🚧 Current Blockers
### ❌ medInria
- **Status:** Failing.
- **Issue:** SuperBuild trying to download dependencies.
- **Plan:** Further investigation into proper unbundling of ITK 6 / VTK 9 for medInria 5.


## 🛠️ General Workarounds
For packages failing due to C23/GCC 15, we continue to use:
1. `export CFLAGS="$CFLAGS -std=gnu17"`
2. `export CXXFLAGS="$CXXFLAGS -fpermissive -include cstdint"`
3. `-Wno-template-body` for complex C++ templates.
