%global debug_package %{nil}
%global commit_date 20250101
%global git_commit master

Name:           mricrogl
Version:        1.2.%{commit_date}
Release:        2%{?dist}
Summary:        GL-accelerated medical image viewer with Python scripting

License:        BSD-2-Clause
URL:            https://github.com/rordenlab/MRIcroGL
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  lazarus >= 2.0
BuildRequires:  fpc
BuildRequires:  fpc-src
BuildRequires:  qt5pas-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  lazarus-lcl-qt5
BuildRequires:  python3-devel
BuildRequires:  dos2unix

Requires:       qt5pas
Requires:       python3-libs
Requires:       dcm2niix

%description
MRIcroGL is a cross-platform NIfTI format image viewer that uses your graphics 
card's hardware acceleration (OpenGL) to provide interactive volume rendering. 
It includes embedded Python scripting for automated analysis.

%prep
%autosetup -n MRIcroGL-%{git_commit}

# 1. Clean up Permissions & Line Endings
find . -type f \( -name "*.ini" -o -name "*.lut" -o -name "*.txt" -o -name "*.py" -o -name "*.glsl" \) -exec dos2unix {} \;
find . -type f -exec chmod 644 {} \;

%build
# 2. Build the Main Application
# Note: MRIcroGL depends on the "LazOpenGLContext" package which is included 
# in the standard Lazarus install, but lazbuild needs to know to compile it 
# if it hasn't been built for Qt5 yet.
chmod 644 MRIcroGL.lpi
lazbuild -B --ws=qt5 MRIcroGL.lpi

%install
rm -rf %{buildroot}

# 1. Prepare Directories
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps

# 2. Install Binary
install -m 755 MRIcroGL %{buildroot}%{_libexecdir}/%{name}/%{name}

# 3. Install Resources
# Copy all resources
cp -r Resources/* %{buildroot}%{_libexecdir}/%{name}/

# CLEANUP: Remove bundled artifacts that confuse Linux packaging
rm -rf %{buildroot}%{_libexecdir}/%{name}/python37
rm -rf %{buildroot}%{_libexecdir}/%{name}/*.bat
rm -rf %{buildroot}%{_libexecdir}/%{name}/*.command

# Copy docs
cp *.txt %{buildroot}%{_libexecdir}/%{name}/

# 4. Create Wrapper Script
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
exec %{_libexecdir}/%{name}/%{name} "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

# 5. Symlink dcm2niix (Relative path)
ln -s ../../bin/dcm2niix %{buildroot}%{_libexecdir}/%{name}/dcm2niix

# 6. Desktop Entry
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=MRIcroGL
Comment=Advanced Medical Image Viewer
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Science;MedicalSoftware;
EOF

# 7. Install Icon
# We confirmed 'mricrogl.png' is in the source root
install -m 644 mricrogl.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

%files
%license license.txt
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

%changelog
* Sun Jan 04 2026 Morgan Hough <morgan.hough@gmail.com> - 1.2.20250101-1
- Initial RPM release for MRIcroGL
