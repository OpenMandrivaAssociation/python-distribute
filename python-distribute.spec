%define	module	distribute

Summary:	Python Distutils Enhancements
Name:		python-%{module}
Version:	0.6.45
Release:	2
License:	Zope Public License (ZPL)
Group:		Development/Python
Url:		http://pypi.python.org/pypi/%{module}
Source0:	http://pypi.python.org/packages/source/d/distribute/distribute-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
Requires:	python-devel
Requires:	python-pkg-resources
%rename	python-setuptools

%description
A collection of enhancements to the Python distutils that allow 
you to more easily build and distribute Python packages, especially 
ones that have dependencies on other packages.

%package -n python3-%{module}
Summary:	Python Distutils Enhancements
Group:		Development/Python

BuildRequires:	python3-devel

Requires:	python3-devel
Requires:	python3-pkg-resources

%description -n python3-%{module}
A collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially
ones that have dependencies on other packages.

%package -n	python-pkg-resources
Summary:	Runtime module to access python resources
Group:		Development/Python

%description -n	python-pkg-resources
Module used to find and manage Python package/version dependencies and access
bundled files and resources, including those inside of zipped .egg files.

%package -n python3-pkg-resources
Summary:	Runtime module to access python 3 resources
Group:		Development/Python

%description -n python3-pkg-resources
Module used to find and manage Python 3 package/version dependencies and access
bundled files and resources, including those inside of zipped .egg files.

%prep
%setup -q -c
mv distribute-%{version} python2
pushd python2
    find -name '*.txt' | xargs chmod -x
    find . -name '*.orig' -exec rm \{\} \;
popd

cp -r python2 python3

pushd python3
    find -name '*.py' -exec sed -i '1s|^#!python|#!python3|' {} \;
popd

%build
export CFLAGS="%{optflags}"
pushd python2
    %__python setup.py build
popd

pushd python3
    python3 setup.py build
popd

#%check
#pushd python2
#    python setup.py test
#popd
#
#pushd python3
#    python3 setup.py test
#popd

%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
pushd python3
    PYTHONDONTWRITEBYTECODE= python3 setup.py install --skip-build --root=%{buildroot}
#    rm -rf %{buildroot}%{python3_sitelib}/setuptools/tests

    find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f
    chmod +x %{buildroot}%{python3_sitelib}/setuptools/command/easy_install.py
popd

pushd python2
    PYTHONDONTWRITEBYTECODE= %__python setup.py install --skip-build --root=%{buildroot}
#    rm -rf %{buildroot}%{python_sitelib}/setuptools/tests

    find %{buildroot}%{python_sitelib} -name '*.exe' | xargs rm -f
    chmod +x %{buildroot}%{python_sitelib}/setuptools/command/easy_install.py
popd

%files
%doc python2/*.txt
%{_bindir}/easy_install
%{_bindir}/easy_install-2.*
%{py_sitedir}/*
%exclude %{py_sitedir}/pkg_resources.py*

%files -n python-pkg-resources
%{py_sitedir}/pkg_resources.py*

%files -n python3-%{module}
%doc python3/*.txt
%{_bindir}/easy_install-3.*
%{python3_sitelib}/*
%exclude %{python3_sitelib}/pkg_resources.py*

%files -n python3-pkg-resources
%{python3_sitelib}/pkg_resources.py*

