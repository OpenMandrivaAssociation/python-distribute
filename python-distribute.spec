%define	module	distribute

Summary:	Python Distutils Enhancements
Name:		python-%{module}
Version:	0.6.18
Release:	1
License:	Zope Public License (ZPL)
Group:		Development/Python
Url:		http://pypi.python.org/pypi/%{module}
Source0:        http://pypi.python.org/packages/source/d/%{module}/%{module}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-devel
Requires:	python-devel
Requires:	python-pkg-resources
%rename		python-setuptools

%description
A collection of enhancements to the Python distutils that allow 
you to more easily build and distribute Python packages, especially 
ones that have dependencies on other packages.

%package -n	python-pkg-resources
Summary:	Runtime module to access python resources
Group:		Development/Python
Conflicts:	python-setuptools < 0.6c9-2mdv

%description -n	python-pkg-resources
Module used to find and manage Python package/version dependencies and access
bundled files and resources, including those inside of zipped .egg files.

%prep
%setup -q -n %{module}-%{version}

%build
export CFLAGS="%{optflags}"
%__python setup.py build

%check
%__python setup.py test

%install
%__python setup.py install --root=%{buildroot}

%files
%doc *.txt
%{_bindir}/*
%{py_sitedir}/*
%exclude %{py_sitedir}/pkg_resources.py*

%files -n python-pkg-resources
%{py_sitedir}/pkg_resources.py*
