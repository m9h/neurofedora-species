Name:           compucell3d
Version:        4.5.0
Release:        1%{?dist}
Summary:        Multi-scale, multi-cellular Virtual Tissue Modeling Environment
License:        MIT
URL:            https://compucell3d.org/
# Source needs to be verified against specific git tags as CC3D release tarballs are inconsistent
Source0:        https://github.com/CompuCell3D/CompuCell3D/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.10
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  swig
BuildRequires:  vtk-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  qscintilla-qt5-devel
BuildRequires:  qwt-qt5-devel
BuildRequires:  tbb-devel
BuildRequires:  eigen3-devel

Requires:       python3-numpy
Requires:       python3-vtk
Requires:       python3-qt5
Requires:       python3-scipy
Requires:       python3-pandas

%description
CompuCell3D is a flexible scriptable modeling environment, which allows the 
rapid construction of sharable Virtual Tissue in-silico simulations of a 
wide variety of multi-scale, multi-cellular problems including angiogenesis, 
bacterial colonies, cancer, developmental biology, evolution, the immune 
system, and tissue engineering.

%prep
%autosetup -n CompuCell3D-%{version}

%build
# CC3D often requires specific cmake flags to find Python and VTK correctly on Fedora
%cmake -S CompuCell3D \
    -DCMAKE_BUILD_TYPE=Release \
    -DPYTHON_EXECUTABLE=%{__python3} \
    -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python3_version} \
    -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_version}.so \
    -DNO_OPENGL=OFF \
    -DCOMPUCELL3D_INSTALL_PATH=%{_libdir}/compucell3d \
    -DBUILD_SHARED_LIBS=ON

%cmake_build

%install
%cmake_install

# Fix shebangs
find %{buildroot} -name "*.py" -exec sed -i '1s|^#!.*|#!%{__python3}|' {} +

# Create standard bin wrapper because CC3D installs weird scripts
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/compucell3d <<EOF
#!/bin/bash
export PYTHONPATH=%{_libdir}/compucell3d/lib/python
exec %{_libdir}/compucell3d/compucell3d.sh "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/compucell3d

%files
%license LICENSE
%doc README.md
%{_bindir}/compucell3d
%{_libdir}/compucell3d/

%changelog
* Wed Jan 07 2026 Fedora Packager <packager@example.com> - 4.5.0-1
- Initial package for Fedora
