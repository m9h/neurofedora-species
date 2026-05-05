# Fedora 44 Build Status & Plan

## 🚩 Current Blockers (GCC 15 / C23)
Fedora 44 has transitioned to GCC 15, which defaults to **C23** (`-std=gnu23`). This causes several issues:
- **Function Prototypes:** `void foo()` now means `void foo(void)`, causing pointer type mismatches in older C code.
- **Stricter C++ Templates:** Flagging previously hidden bugs in ITK and other complex libraries.
- **Missing Headers:** Implicit includes of `<cstdint>` are gone.

## 📊 Package Specifics

### ❌ freesurfer (8.2.0)
- **Status:** Failing on FC44.
- **Probable Cause:** ITK dependency issues and C23 strictness.
- **Plan:** Apply `-fpermissive` and check for missing `<cstdint>` in patches.

### ❌ mrtrix3 (3.0.8)
- **Status:** Failing on FC44.
- **Probable Cause:** Eigen3 compatibility or GCC 15 template strictness.
- **Plan:** Apply `-std=gnu++17` or `-fpermissive`.

### ❌ simnibs (4.5.0)
- **Status:** Failing on FC44.
- **Plan:** Update to **4.6.0** upstream and apply C23 fixes if needed.

### ❌ python-samseg (0.4a0)
- **Status:** Failing on FC44.
- **Plan:** Update to latest (check FreeSurfer 8.2.0 compatibility).

## 🛠️ General Workarounds
For packages failing due to C23/GCC 15, we will attempt:
1. `export CFLAGS="$CFLAGS -std=gnu17"`
2. `export CXXFLAGS="$CXXFLAGS -fpermissive"`
3. Explicitly adding `#include <cstdint>` where needed.
