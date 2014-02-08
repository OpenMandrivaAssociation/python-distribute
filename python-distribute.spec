%define	module	distribute

Summary:	Python Distutils Enhancements
Name:		python-%{module}
Version:	0.6.35
Release:	6
License:	Zope Public License (ZPL)
Group:		Development/Python
Url:		http://pypi.python.org/pypi/%{module}
Source0:	http://pypi.python.org/packages/source/d/distribute/distribute-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-devel
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

%changelog
* Mon Jul 23 2012 Lev Givon <lev@mandriva.org> 0.6.28-1
+ Revision: 810610
- Update to 0.6.28.

* Fri Jun 22 2012 Lev Givon <lev@mandriva.org> 0.6.27-1
+ Revision: 806717
- Update to 0.6.27.

* Sun Oct 16 2011 Lev Givon <lev@mandriva.org> 0.6.24-1
+ Revision: 704884
- Update to 0.6.24.

* Sun Aug 21 2011 Lev Givon <lev@mandriva.org> 0.6.21-1
+ Revision: 695924
- Update to 0.6.21.

* Thu Jun 02 2011 Lev Givon <lev@mandriva.org> 0.6.19-1
+ Revision: 682450
- Update to 0.6.19.

* Wed Jun 01 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.6.18-1
+ Revision: 682321
- cleanups
- new version
- rename package from python-setuptools to python-distribute

* Sun May 01 2011 Lev Givon <lev@mandriva.org> 0.6.16-1
+ Revision: 661111
- Update to 0.6.16.

* Mon Nov 01 2010 Funda Wang <fwang@mandriva.org> 0.6.14-4mdv2011.0
+ Revision: 591551
- wrong req on python-sqlalchemy

* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 0.6.14-3mdv2011.0
+ Revision: 591061
- add requires on python-sqlalchemy for tuntime

* Sat Oct 30 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 0.6.14-2mdv2011.0
+ Revision: 590349
- rebuild with new python 2.7

* Fri Oct 29 2010 Funda Wang <fwang@mandriva.org> 0.6.14-1mdv2011.0
+ Revision: 589963
- New fork distribute

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 0.6c11-1mdv2010.1
+ Revision: 462167
- Update to non-broken version 0.6c11

* Mon Oct 19 2009 Lev Givon <lev@mandriva.org> 0.6c10-1mdv2010.1
+ Revision: 458285
- Update to 0.6c10.

* Wed Dec 24 2008 Michael Scherer <misc@mandriva.org> 0.6c9-3mdv2009.1
+ Revision: 318435
- rebuild for new python

* Fri Nov 28 2008 Wanderlei Cavassin <cavassin@mandriva.com.br> 0.6c9-2mdv2009.1
+ Revision: 307480
- Splitted python-pkg-resources, then packages like elisa will not
  need to drag python-devel and others.

* Mon Oct 27 2008 Lev Givon <lev@mandriva.org> 0.6c9-1mdv2009.1
+ Revision: 297704
- Update to 0.6c9.
  Remove patch (included in 0.6c9).

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - remuve stupid redefines
    - fix mixture of tabs and spaces
    - better description
    - export CFLAGS
    - enable checks

* Tue Jul 08 2008 Colin Guthrie <cguthrie@mandriva.org> 0.6c8-3mdv2009.0
+ Revision: 232866
- Apply patch to fix bug when working with subversion 1.5 checkouts

* Sat Jul 05 2008 Funda Wang <fwang@mandriva.org> 0.6c8-2mdv2009.0
+ Revision: 231966
- setuptools requires python2.5/config/Makefile to work

* Thu Feb 21 2008 Lev Givon <lev@mandriva.org> 0.6c8-1mdv2008.1
+ Revision: 173464
- Update to 0.6c8.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 07 2007 Lev Givon <lev@mandriva.org> 0.6c7-2mdv2008.1
+ Revision: 106628
- Fix file installation issue.

* Thu Oct 11 2007 Lev Givon <lev@mandriva.org> 0.6c7-1mdv2008.1
+ Revision: 97177
- Update to 0.6c7.

* Mon Jun 18 2007 Lev Givon <lev@mandriva.org> 0.6c6-1mdv2008.0
+ Revision: 41112
- Update to 0.6c6.

* Tue Apr 24 2007 Lev Givon <lev@mandriva.org> 0.6c5-1mdv2008.0
+ Revision: 17935
- Update to 0.6c5.


* Fri Jan 05 2007 Michael Scherer <misc@mandriva.org> 0.6c3-1mdv2007.0
+ Revision: 104332
- upgrade to 0.6c3
- use %%rel for mkrel

* Wed Nov 29 2006 Michael Scherer <misc@mandriva.org> 0.6a11-2mdv2007.1
+ Revision: 88724
- rebuild for new python
- Import python-setuptools


