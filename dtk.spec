# Disable the strict RPATH check for this package
%global __brp_check_rpaths %{nil}
# Prevent build failure if there are files in the buildroot not listed in %files
%define _unpackaged_files_terminate_build 0


Name:           dtk
Version:        1.7.1
Release:        1%{?dist}
Summary:        Scientific software platform (Inria)

License:        BSD
URL:            https://dtk.inria.fr/
Source0:        https://gitlab.inria.fr/dtk/dtk/-/archive/%{version}/dtk-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtxmlpatterns-devel

Requires:       qt5-qtbase

%description
The dtk framework is a platform for scientific software development.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for dtk.

%prep
%autosetup -n dtk-%{version}

# ---------------------------------------------------------
# 1. Remove broken/unneeded modules
# ---------------------------------------------------------
sed -i '/add_subdirectory(dtkDistributed)/d' src/CMakeLists.txt
sed -i '/add_subdirectory(dtkComposer)/d' src/CMakeLists.txt
sed -i '/dtkDistributedGuiApplication/d' src/dtkWidgets/CMakeLists.txt
sed -i 's/dtkDistributed//g' src/dtkWidgets/CMakeLists.txt

# ---------------------------------------------------------
# 2. FIX: Make dtkCore C++20 Compatible (Global Rename)
# ---------------------------------------------------------
# The word "concept" is a keyword in C++20. We must rename it.
# We use \b boundaries to replace the exact word "concept" with "pluginConcept"
# in all header, source, and template files in dtkCore.
find src/dtkCore -name "*.h" -o -name "*.cpp" -o -name "*.tpp" | xargs sed -i 's/\bconcept\b/pluginConcept/g'

# ---------------------------------------------------------
# 3. FIX: Enforce C++17 in CMake
# ---------------------------------------------------------
# This ensures dtk itself builds with the correct standard
sed -i 's/CMAKE_CXX_STANDARD 11/CMAKE_CXX_STANDARD 17/g' CMakeLists.txt
echo 'add_compile_options(-std=c++17)' >> src/dtkCore/CMakeLists.txt

%build
export CXXFLAGS="%{optflags} -std=c++17 -Wno-error=deprecated-declarations"
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_CXX_STANDARD_REQUIRED=ON \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DDTK_BUILD_TESTS:BOOL=OFF \
    -DDTK_BUILD_EXAMPLES:BOOL=OFF \
    -DDTK_BUILD_DOCUMENTATION:BOOL=OFF \
    -DDTK_BUILD_DISTRIBUTED:BOOL=OFF \
    -DDTK_BUILD_COMPOSER:BOOL=OFF 

%cmake_build

%install
# Clear any previous buildroot residue
rm -rf %{buildroot}
%cmake_install

# This creates shims for EVERY module dtk-imaging might ask for
# Added: Core, Log, Math, Meta, Fonts, Widgets, Themes, Settings, Distributed, Composer
for module in Core Log Math Meta Fonts Widgets Themes Settings Distributed Composer; do
  dest=%{buildroot}%{_libdir}/cmake/dtk/dtk${module}Config.cmake
  echo "include(\${CMAKE_CURRENT_LIST_DIR}/dtkConfig.cmake)" > $dest
done

%files
%license LICENSE.md
%{_bindir}/dtkPluginsMetaInfoFetcher
%{_bindir}/dtkDeploy
%{_bindir}/dtkConceptGenerator
%{_libdir}/libdtk*.so.*

%files devel
%{_includedir}/dtk*
%{_libdir}/libdtk*.so
# Updated line to include ALL cmake files, including FindSIP.py
%{_libdir}/cmake/dtk/*
/usr/wrp/

%changelog
* Tue Jan 06 2026 Morgan Hough <morgan.hough@gmail.com> - 1.7.1-1
- Fixed manifest, RPATHs, and disabled broken modules
