Name:           morpheus
Version:        2.3.6
Release:        1%{?dist}
Summary:        Modeling and simulation environment for multi-cellular systems biology
License:        BSD
URL:            https://morpheus.gitlab.io/
Source0:        https://gitlab.com/morpheus.lab/morpheus/-/archive/v%{version}/morpheus-v%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtcharts-devel
BuildRequires:  libsbml-devel
BuildRequires:  libssh-devel
BuildRequires:  libtiff-devel
BuildRequires:  muParser-devel
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  doxygen
BuildRequires:  graphviz

Requires:       gnuplot
Requires:       graphviz

%description
Morpheus is a modeling environment for the simulation and integration of 
cell-based models with ordinary differential equations and reaction-diffusion 
systems. It supports the Cellular Potts Model (CPM) and allows rapid 
development of multiscale models in biological terms using a declarative 
language.

%prep
%setup -q -n morpheus-v2.3.6

# Fix xtensor header paths for Fedora 43 (xtensor 0.27+)
# We use 'xargs -r' to ensure the build doesn't fail if a specific file isn't found.

# Containers
grep -rl "xtensor/xtensor.hpp" . | xargs -r sed -i 's|xtensor/xtensor.hpp|xtensor/containers/xtensor.hpp|g'
grep -rl "xtensor/xarray.hpp" . | xargs -r sed -i 's|xtensor/xarray.hpp|xtensor/containers/xarray.hpp|g'
grep -rl "xtensor/xfixed.hpp" . | xargs -r sed -i 's|xtensor/xfixed.hpp|xtensor/containers/xfixed.hpp|g'

# Views
grep -rl "xtensor/xview.hpp" . | xargs -r sed -i 's|xtensor/xview.hpp|xtensor/views/xview.hpp|g'
grep -rl "xtensor/xindex_view.hpp" . | xargs -r sed -i 's|xtensor/xindex_view.hpp|xtensor/views/xindex_view.hpp|g'
grep -rl "xtensor/xstrided_view.hpp" . | xargs -r sed -i 's|xtensor/xstrided_view.hpp|xtensor/views/xstrided_view.hpp|g'

# IO
grep -rl "xtensor/xio.hpp" . | xargs -r sed -i 's|xtensor/xio.hpp|xtensor/io/xio.hpp|g'

# Math/Adaptors
grep -rl "xtensor/xadapt.hpp" . | xargs -r sed -i 's|xtensor/xadapt.hpp|xtensor/containers/xadapt.hpp|g'

# Core (Fixing the xnoalias error)
# We replace both standard and potential 'math' variant paths to the correct 'core' path found on your system
grep -rl "xtensor/xnoalias.hpp" . | xargs -r sed -i 's|xtensor/xnoalias.hpp|xtensor/core/xnoalias.hpp|g'
grep -rl "xtensor/math/xnoalias.hpp" . | xargs -r sed -i 's|xtensor/math/xnoalias.hpp|xtensor/core/xnoalias.hpp|g'

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DMORPHEUS_RELEASE_BUNDLE=OFF \
    -DBoost_USE_STATIC_LIBS=OFF \
    -DBUILD_DOC=ON

%cmake_build

%install
%cmake_install

# Verify desktop file installation
desktop-file-validate %{buildroot}%{_datadir}/applications/morpheus.desktop

%files
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/morpheus
%{_bindir}/morpheus-gui
%{_libdir}/morpheus/
%{_datadir}/applications/morpheus.desktop
%{_datadir}/icons/hicolor/*/apps/morpheus.png
%{_datadir}/mime/packages/morpheus.xml
%{_datadir}/morpheus/

%changelog
* Wed Jan 07 2026 Fedora Packager <packager@example.com> - 2.3.6-1
- Initial package for Fedora
