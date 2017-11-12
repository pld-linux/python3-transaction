# TODO:
# - Fix docs ((exception: No module named 'repoze'))
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTES:
%define		module		transaction
%define		egg_name	%{module}
%define		pypi_name	%{module}
Summary:	Generic transaction implementation for Python. It is mainly used by the ZODB
Summary(pl.UTF-8):	Ogólna implementacja transakcji dla Pythona. Głównie używana przez ZODB.
Name:		python-%{pypi_name}
Version:	2.1.2
Release:	1
License:	ZPL 2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	375a7f9d434ad0e9bf2039a3a0588e2b
URL:		https://github.com/zopefoundation/transaction
#URL:		https://pypi.python.org/pypi/%{pypi_name}
BuildRequires:	python-mock
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-mock
BuildRequires:	python3-modules
BuildRequires:	python3-pbr
BuildRequires:	python3-setuptools
%endif
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n python3-%{pypi_name}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}

%description -n python3-%{pypi_name} -l pl.UTF-8

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
