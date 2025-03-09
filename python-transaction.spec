#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		transaction

Summary:	Generic transaction implementation for Python, mainly used by the ZODB
Summary(pl.UTF-8):	Ogólna implementacja transakcji dla Pythona, używana głównie przez ZODB
Name:		python-%{module}
Version:	3.1.0
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/t/transaction/%{module}-%{version}.tar.gz
# Source0-md5:	7e66f49195e9a54cf0af3121febb38a3
Patch0:		%{name}-mock.patch
URL:		https://github.com/zopefoundation/transaction
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%endif
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3 >= 1.8
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a generic transaction implementation for Python.
It is mainly used by the ZODB.

%description -l pl.UTF-8
Ten pakiet zawiera ogólną implementację transakcji dla Ptyhona. Jest
używany głównie przez ZODB.

%package -n python3-%{module}
Summary:	Generic transaction implementation for Python, mainly used by the ZODB
Summary(pl.UTF-8):	Ogólna implementacja transakcji dla Pythona, używana głównie przez ZODB
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
This package contains a generic transaction implementation for Python.
It is mainly used by the ZODB.

%description -n python3-%{module} -l pl.UTF-8
Ten pakiet zawiera ogólną implementację transakcji dla Ptyhona. Jest
używany głównie przez ZODB.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

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
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
