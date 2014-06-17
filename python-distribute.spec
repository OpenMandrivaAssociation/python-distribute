%define	module	distribute
%define py2_version	0.6.49

Summary:	Python Distutils Enhancements
Name:		python-%{module}
Version:	0.7.3
Release:	1
License:	Zope Public License (ZPL)
Group:		Development/Python
Url:		http://pypi.python.org/pypi/%{module}
Source0:	http://pypi.python.org/packages/source/d/distribute/distribute-%{py2_version}.tar.gz
Source1:	http://pypi.python.org/packages/source/d/distribute/distribute-%{version}.zip
BuildArch:	noarch
BuildRequires:	pkgconfig(python3)
Requires:	pkgconfig(python3)
Provides:	python3egg(setuptools) = %{version}
%rename	python-setuptools
%rename python3-%{module}
%rename python3-pkg-resources

%description
A collection of enhancements to the Python distutils that allow 
you to more easily build and distribute Python packages, especially 
ones that have dependencies on other packages.

%package -n python2-%{module}
Summary:	Python 2 Distutils Enhancements
Version:	%{py2_version}
Release:	10
Group:		Development/Python

BuildRequires:	pkgconfig(python)

Requires:	pkgconfig(python)
Requires:	python2-pkg-resources

%description -n python2-%{module}
A collection of enhancements to the Python 2 distutils that allow
you to more easily build and distribute Python 2 packages, especially
ones that have dependencies on other packages.

%package -n python2-pkg-resources
Summary:	Runtime module to access python 2 resources
Version:	%{py2_version}
Release:	10
Group:		Development/Python

%description -n python2-pkg-resources
Module used to find and manage Python 2 package/version dependencies and access
bundled files and resources, including those inside of zipped .egg files.

%prep
%setup -q -b 1 -c
cd ../distribute-0.6.*
find -name '*.py' -exec sed -i '1s|^#!python|#!python2|' {} \;

%build
export CFLAGS="%{optflags}"
cd ../distribute-0.6.*
python2 setup.py build

cd ../distribute-0.7.3
python3 setup.py build

%install
cd ../distribute-0.6.*
PYTHONDONTWRITEBYTECODE= python2 setup.py install --skip-build --root=%{buildroot}

cd ../distribute-0.7.3
PYTHONDONTWRITEBYTECODE= python3 setup.py install --skip-build --root=%{buildroot}

%files
%{_bindir}/easy_install
%{py_sitedir}/*

%files -n python2-%{module}
%{_bindir}/easy_install-2.*
%{python2_sitelib}/*
%exclude %{python2_sitelib}/pkg_resources.py*

%files -n python2-pkg-resources
%{python2_sitelib}/pkg_resources.py*

