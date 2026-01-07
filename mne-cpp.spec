%define _unpackaged_files_terminate_build 0
%define __brp_check_rpaths %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mne-cpp
Version:        1.1.0
Release:        1%{?dist}
Summary:        Cross-platform C++ framework for MEG/EEG data analysis

License:        BSD-3-Clause
URL:            https://mne-cpp.github.io/
Source0:        %{name}-%{version}.tar.gz

# Build dependencies based on Qt Creator requirements
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtcharts-devel
BuildRequires:  qt6-qt3d-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  eigen3-devel
BuildRequires:  fftw-devel
BuildRequires:  libcurl-devel

# Runtime dependencies (Fedora's find-requires usually handles these, 
# but Qt plugins often need explicit help)
Requires:       qt6-qtbase
Requires:       qt6-qtcharts
Requires:       qt6-qt3d

%description
MNE-CPP is a modular C++ framework for MEG/EEG data acquisition and analysis. 
It includes applications like MNE Scan for real-time acquisition and 
MNE Analyze for offline processing.

%prep
%setup -q -n mne-cpp-main

%build
cd src
mkdir -p build_rpm
cd build_rpm

# Passing the flags directly into CMake ensures they aren't overwritten by RPM macros
cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DMNECPP_CONFIG=dynamic \
    -DCMAKE_BUILD_TYPE=Release \
    -DMNECPP_BUILD_EXAMPLES=OFF \
    -DMNECPP_BUILD_TESTS=OFF \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_CXX_FLAGS="%{optflags} -Wno-error=format-security -Wno-error=unused-but-set-variable -Wno-error=reorder -Wno-array-compare" \
    -DCMAKE_C_FLAGS="%{optflags} -Wno-error=format-security"

# Build using available processing power
make %{?_smp_mflags}

%install
# 1. Clean previous attempts
rm -rf %{buildroot}

# 2. Run the standard install (handles the binaries like mne_scan)
cd src/build_rpm
make install DESTDIR=%{buildroot}

# 3. MANUAL FIX: Copy the missing libraries
# Create the system library directory (e.g., /usr/lib64)
mkdir -p %{buildroot}%{_libdir}

# Copy the compiled libraries from the source output to the buildroot
# We use -a to preserve links and permissions
# Path explanation: ../../ takes us out of 'src/build_rpm' to the root 'mne-cpp-main'
cp -a ../../out/Release/lib/lib*.so* %{buildroot}%{_libdir}/

%files
%license LICENSE
%doc README.md
%{_bindir}/*
# Now we specifically look in the standard 64-bit lib folder
%{_libdir}/*.so*
%{_includedir}/*
# Removed the %{_prefix}/lib/mne-cpp/ line as it likely doesn't exist yet

%changelog
* Tue Jan 06 2026 Morgan Hough <morgan.hough@gmail.com> - 1.1.0-1
- Initial RPM build for Fedora
