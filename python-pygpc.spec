%global pypi_name pygpc
%global forgeurl https://github.com/pygpc-polynomial-chaos/pygpc
%global tag v0.4.4

Name:           python-%{pypi_name}
Version:        0.4.4
Release:        1%{?dist}
Summary:        Gaussian Process Computation in Python

License:        GPL-3.0-or-later
URL:            https://pygpc.readthedocs.io/
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
# Runtime deps needed for build/test
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
BuildRequires:  python3-h5py
BuildRequires:  python3-scikit-learn
BuildRequires:  python3-matplotlib
BuildRequires:  python3-tqdm
BuildRequires:  python3-joblib

%description
pygpc is a Python library for Gaussian Process Computation (GPC). 
It provides a framework for performing sensitivity analysis and 
uncertainty quantification using polynomial chaos expansions 
constructed via Gaussian process regression.

%package -n python3-%{pypi_name}
Summary:        %{summary}
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-h5py
Requires:       python3-scikit-learn
Requires:       python3-matplotlib
Requires:       python3-tqdm
Requires:       python3-joblib
Requires:       python3-dill
# multiprocessing_on_dill is often bundled or small, check if needed
Requires:       python3-multiprocess

%description -n python3-%{pypi_name}
This package provides the Python 3 library for pygpc.

%prep
%autosetup -n %{pypi_name}-%{version}

# Relax strict version pinning in requirements (common in scientific packages)
sed -i 's/==/>=/g' requirements.txt

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
# Basic import test
%py3_check_import %{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Wed Jan 07 2026 Fedora Packager <packager@example.com> - 0.4.1-1
- Initial package
