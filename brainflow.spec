Name:           brainflow
Version:        5.19.0
Release:        1%{?dist}
Summary:        Biosensor library for EEG, EMG, ECG and other data

License:        MIT
URL:            https://brainflow.org/
Source0:        https://github.com/brainflow-dev/brainflow/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  libusb1-devel
BuildRequires:  bluez-libs-devel
BuildRequires:  dbus-devel
BuildRequires:  opencv-devel
BuildRequires:  chrpath

%description
BrainFlow is a library intended to obtain, parse and analyze EEG, EMG, ECG 
and other kinds of data from biosensors. It provides a uniform API for 
many popular devices including OpenBCI, Muse, Emotiv, and others.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries needed to
develop applications that use BrainFlow.

%prep
%autosetup -p1

%build
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_OYMOTION_SDK=OFF \
    -DBUILD_GFORCE_SDK=OFF \
    -DKISSFFT_STATIC=OFF \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

# 1. FIX LIB LOCATION: Move libraries from /usr/lib to /usr/lib64 if needed
if [ "%{_lib}" == "lib64" ] && [ -d %{buildroot}/usr/lib ]; then
    mkdir -p %{buildroot}%{_libdir}
    cp -a %{buildroot}/usr/lib/* %{buildroot}%{_libdir}/
    rm -rf %{buildroot}/usr/lib
fi

# 2. FIX HEADER LOCATION: Move from /usr/inc to /usr/include/brainflow
if [ -d %{buildroot}/usr/inc ]; then
    mkdir -p %{buildroot}%{_includedir}/brainflow
    mv %{buildroot}/usr/inc/* %{buildroot}%{_includedir}/brainflow/
    rm -rf %{buildroot}/usr/inc
fi

# 3. REMOVE BAD BINARIES (Proprietary/Incompatible Pre-compiled blobs)
# These files cause dependency errors (ARM symbols, old GCC versions)
rm -f %{buildroot}%{_libdir}/libunicorn_raspberry.so
rm -f %{buildroot}%{_libdir}/libunicorn.so
rm -f %{buildroot}%{_libdir}/libsensor_x64.so
rm -f %{buildroot}%{_libdir}/libeego-SDK.so
# Also remove static libs
rm -f %{buildroot}%{_libdir}/*.a

# 4. FIX PERMISSIONS (Ensure shared libs are executable for stripping)
chmod 755 %{buildroot}%{_libdir}/*.so

# 5. REMOVE RPATH
find %{buildroot}%{_libdir} -name "*.so" -exec chrpath --delete {} \; || :

%files
%license LICENSE
%doc README.md
%{_libdir}/lib*.so

%files devel
%{_includedir}/brainflow/
%{_libdir}/cmake/brainflow/

%changelog
* Wed Jan 07 2026 Morgan Hough <morgan.hough@gmail.com> - 5.19.0-1
- Initial RPM package for BrainFlow 5.19.0
- Removed incompatible proprietary binary blobs
