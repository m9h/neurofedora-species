Name:           mitk
Version:        2024.12
Release:        1%{?dist}
Summary:        Medical Imaging Interaction Toolkit

License:        BSD
URL:            https://www.mitk.org/
Source0:        https://github.com/MITK/MITK/archive/v%{version}.tar.gz

# core build deps
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

# system libraries (The Big Three)
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtwebengine-devel
BuildRequires:  vtk-devel
BuildRequires:  insight-toolkit-devel
BuildRequires:  gdcm-devel
BuildRequires:  dcmtk-devel
BuildRequires:  hdf5-devel

# MITK often needs these
BuildRequires:  eigen3-devel
BuildRequires:  tinyxml-devel

%description
The Medical Imaging Interaction Toolkit (MITK) is a free open-source 
software system for development of interactive medical image processing 
software. It combines the Insight Toolkit (ITK) and the Visualization 
Toolkit (VTK) with an application framework.

%package devel
Summary:        Development files for MITK
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files and headers for building plugins for MITK.

%prep
%autosetup -n MITK-%{version}

%build
# Create a build directory specifically for the Superbuild container
mkdir -p build
cd build

# NOTE: MITK configuration is very sensitive. 
# We enable the Superbuild but force it to use system libraries where possible.
# If MITK_USE_SUPERBUILD is OFF, you must have CTK installed on the system.
%cmake .. \
    -DMITK_USE_SUPERBUILD:BOOL=ON \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DMITK_USE_SYSTEM_QT:BOOL=ON \
    -DMITK_USE_SYSTEM_ITK:BOOL=ON \
    -DMITK_USE_SYSTEM_VTK:BOOL=ON \
    -DMITK_USE_SYSTEM_GDCM:BOOL=ON \
    -DMITK_USE_SYSTEM_DCMTK:BOOL=ON \
    -DMITK_USE_SYSTEM_HDF5:BOOL=ON \
    -DBUILD_TESTING:BOOL=OFF \
    -DMITK_BUILD_EXAMPLES:BOOL=OFF \
    -DMITK_USE_Qt6:BOOL=ON 

# The superbuild will trigger the internal build of dependencies (like CTK)
# and then build MITK itself.
%cmake_build

%install
cd build
# The install target in Superbuild mode can be tricky. 
# Sometimes you have to enter the MITK-build directory inside the build dir.
# If the Superbuild handles install correctly:
%cmake_install

# If Superbuild fails to install to buildroot, you might need to manually
# invoke install on the inner build directory:
# cmake --install MITK-build --prefix %{buildroot}/usr

%files
%license LICENSE
%doc README.md
%{_bindir}/MitkWorkbench
%{_libdir}/libMitk*.so*
%{_libdir}/plugins/*

%files devel
%{_includedir}/mitk*
%{_libdir}/cmake/MITK*

%changelog
* Mon Jan 06 2026 User <user@example.com> - 2024.12-1
- Initial RPM packaging attempt
