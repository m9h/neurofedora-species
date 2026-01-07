Name:    liblsl
Version: 1.16.2
Release: 1%{?dist}
Summary: Lab Streaming Layer (LSL) is a system for the unified collection of measurement time series in research experiments.

License: MIT
URL:     https://github.com/sccn/liblsl
Source0: https://github.com/sccn/liblsl/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: boost-devel

%description
The Lab Streaming Layer (LSL) is a system for the unified collection of
measurement time series in research experiments that handles both the
networking, time-synchronization, (near-) real-time access as well as
optionally the centralized collection, viewing and disk recording of the data.

%prep
%setup -q -n %{name}-%{version}

%build
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_BUILD_TYPE=Release
cmake --build build -- -j$(nproc)

%install
DESTDIR=%{buildroot} cmake --install build

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_libdir}/liblsl.so.*
%{_bindir}/lslver

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries needed to
develop applications that use the Lab Streaming Layer.

%files devel
%{_libdir}/liblsl.so
%{_includedir}/lsl
%{_includedir}/lsl_c.h
%{_includedir}/lsl_cpp.h
%{_libdir}/cmake/LSL

%changelog
* Thu Jul 25 2024 Jules <jules@example.com> - 1.16.2-1
- Renamed package to liblsl
- Use modern RPM macros
- Use %{_libdir} macro
- Corrected Source0 URL and %setup macro
- Add missing files to %files section

* Wed Jul 24 2024 Jules <jules@example.com> - 1.16.2-1
- Initial packaging
