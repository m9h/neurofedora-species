Name:           ANTs
Version:        2.5.4
Release:        1%{?dist}
Summary:        Advanced Normalization Tools for medical imaging

License:        Apache-2.0
URL:            https://github.com/ANTsX/ANTs
Source0:        https://github.com/ANTsX/ANTs/archive/v%{version}/%{name}-%{version}.tar.gz

Conflicts:      ants
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  git 

%description
Advanced Normalization Tools (ANTs) extracts information from complex datasets
that include imaging.

%prep
%autosetup -n %{name}-%{version}

%build
# --- GCC 15 / Fedora 43 Fixes ---
# 1. CXXFLAGS (C++):
#   -std=c++17: Required by ITK/HDF5 on GCC 15 to avoid #error directives.
#   -include cstdint: Fixes missing type errors (uint8_t, etc.) in older code.
#   -fpermissive: Downgrades strict conformance errors to warnings.
export CXXFLAGS="%{optflags} -std=c++17 -include cstdint -fpermissive"

# 2. CFLAGS (C):
#   -std=gnu17: Reverts C standard to avoid C23 strictness.
#   -Wno-error...: Disables errors for legacy C syntax (implicit declarations).
export CFLAGS="%{optflags} -std=gnu17 -Wno-error=implicit-function-declaration -Wno-error=int-conversion -Wno-error=incompatible-pointer-types"

mkdir -p build
cd build

# CONFIGURE SUPERBUILD
# We explicitly pass the C/CXX flags again to ensure CMake passes them 
# down to the external projects (ITK) that it downloads.
cmake .. \
    -DANTs_SUPERBUILD=ON \
    -DUSE_SYSTEM_ITK=OFF \
    -DBUILD_TESTING=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_CXX_STANDARD_REQUIRED=ON \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS" \
    -DCMAKE_C_FLAGS="$CFLAGS"

# RUN THE BUILD
# 3. Prevent RAM exhaustion (OOM) on NUC
# Using -j2 to ensure linker memory usage fits in available RAM.
make -j1

%install
# SuperBuilds do not support standard "make install DESTDIR=..." well.
# We must manually copy the resulting binaries.

# 1. Create the destination directory in the RPM buildroot
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}

# 2. Find and copy the compiled binaries
# The SuperBuild puts the final ANTs executables in: build/ANTS-build/bin/
cp -a build/ANTS-build/bin/* %{buildroot}%{_bindir}/

# 3. Copy libraries if present
# (Using || true to prevent failure if static libs are cleaned up or not present)
if [ -d "build/ANTS-build/lib" ]; then
    cp -a build/ANTS-build/lib/* %{buildroot}%{_libdir}/ || true
fi

# 4. Copy Scripts
# ANTs scripts reside in the source 'Scripts' folder
cp -a Scripts/* %{buildroot}%{_bindir}/

%files
%license COPYING.txt
%doc README.md
%{_bindir}/*
%{_libdir}/*

%changelog
* Sun Jan 04 2026 mhough - 2.5.4-1
- Switched to SuperBuild due to incompatible system ITK v4
- Added C++17 and C17 flags for GCC 15 compatibility
- Added memory constraints for build stability
