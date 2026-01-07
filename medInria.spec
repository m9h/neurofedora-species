%define commit cd1a18b842d8e65bc7a93a0273bb4ae780833b00
%define shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           medInria
Version:        4.0.0
Release:        0.2.%{shortcommit}%{?dist}
Summary:        Medical image navigation and research tool
License:        BSD
URL:            https://github.com/medInria/medInria-public
Source0:        medInria-public-%{shortcommit}.tar.gz
# We provide dtk source manually so we can patch it
Source1:        dtk-1.7.1.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtwebengine-devel
# We still need system dtk-devel for some paths, but SuperBuild recompiles it
BuildRequires:  dtk-devel
BuildRequires:  xtl-devel
BuildRequires:  xtensor-devel

%description
medInria is a medical image navigation and research tool.

%prep
# 1. Unpack medInria
%setup -q -n medInria-public

# 2. Unpack dtk into a subdirectory called 'dtk-source'
# We use -a 1 to unpack Source1
%setup -q -T -D -a 1 -n medInria-public
mv dtk-1.7.1 dtk-source

# ---------------------------------------------------------
# INTERCEPT: Configure SuperBuild to use LOCAL dtk source
# ---------------------------------------------------------
# We find the External_dtk.cmake file and replace the GIT download commands 
# with a SOURCE_DIR pointing to our patched directory.
find . -name "External_dtk.cmake" -exec sed -i 's|GIT_REPOSITORY.*|SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/../../dtk-source"|' {} \;
find . -name "External_dtk.cmake" -exec sed -i '/GIT_TAG/d' {} \;

# ---------------------------------------------------------
# FIX: Patch the LOCAL dtk source
# ---------------------------------------------------------
# Fix A: C++20 'concept' keyword collision
find dtk-source -name "*.h" -o -name "*.cpp" -o -name "*.tpp" | xargs -r sed -i 's/\bconcept\b/pluginConcept/g'

# Fix B: Const-correctness bug in dtkDistributedArray (The Error You Saw)
# The code tries to call non-const 'get' from const 'range'. We use const_cast.
sed -i 's/this->get(index/const_cast<dtkDistributedArray *>(this)->get(index/' dtk-source/src/dtkDistributed/dtkDistributedArray.tpp

# ---------------------------------------------------------
# FIX: medInria source patches
# ---------------------------------------------------------
grep -rl "dtkCoreObjectManager" src | xargs -r sed -i 's/dtkCoreObjectManager/dtkObjectManager/g'
grep -rl "#include <dtkWidgetsWidget>" src | xargs -r sed -i 's|#include <dtkWidgetsWidget>|#include <dtkWidgets>|g'
grep -rl "dtkWidgetsWidget" src | xargs -r sed -i 's/dtkWidgetsWidget/QWidget/g'

# Safety header for xtensor
mkdir -p local_include/xtensor
echo '#include "xtensor/containers/xarray.hpp"' > local_include/xtensor/xarray.hpp

%build
# Force system compilers to avoid Conda
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export PATH=/usr/bin:$PATH

export CXXFLAGS="%{optflags} \
  -I$(pwd)/local_include \
  -I%{_includedir}/dtk \
  -I%{_includedir}/dtkCore \
  -I%{_includedir}/dtkLog \
  -I%{_includedir}/dtkMath \
  -I%{_includedir}/dtkMeta \
  -I%{_includedir}/dtkWidgets \
  -idirafter %{_includedir}"

# We disable Qt WebEngine if it causes issues, but try enabled first.
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=/usr/bin/gcc \
    -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DUSE_SYSTEM_VTK=OFF \
    -DUSE_SYSTEM_DCMTK=OFF \
    -DUSE_SYSTEM_DTK=OFF 

%cmake_build

%install
%cmake_install

%files
%{_bindir}/medInria
%{_libdir}/lib*.so*
%{_datadir}/medInria

%changelog
* Tue Jan 06 2026 Morgan Hough <morgan.hough@gmail.com> - 4.0.0-0.2
- Intercept SuperBuild to fix dtk source code errors locally
