%ifarch %{ix86}
%define		ver	5.0.18
%endif
%ifarch %{x8664}
%define		ver	5.0.18
%endif
%ifarch ppc
%define		ver	3.1.33
%endif
%define		modname		ioncube
Summary:	ionCube loader module for PHP
Summary(pl.UTF-8):	Moduł wczytujący ionCube dla PHP
Name:		php%{?php_suffix}-%{modname}
Version:	%{ver}
# Never decrease release in this package.
# As not all arch versions are identical, you could be making some arch package older.
Release:	13
License:	redistributable
Group:		Libraries
# www.ioncube.com/loaders.php
Source0:	http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86.tar.bz2
# Source0-md5:	d6c19034730b5f4eb35b4f94e01cb93f
Source1:	http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.bz2
# Source1-md5:	20329d3b324039892215e84c2ea6b0bc
Source2:	http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_ppc.tar.bz2
# Source2-md5:	c9f44f2245e41cba0617c452488c3dc4
URL:		http://www.ioncube.com/
BuildRequires:	php%{?php_suffix}-devel >= 4:5.2.0
BuildRequires:	rpmbuild(macros) >= 1.579
BuildRequires:	sed >= 4.0
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ionCube loader module for PHP.

%description -l pl.UTF-8
Moduł wczytujący ionCube dla PHP.

%prep
%ifarch %{ix86}
%setup -q -T -b 0 -n %{modname}
%endif
%ifarch %{x8664}
%setup -q -T -b 1 -n %{modname}
%endif
%ifarch ppc
%setup -q -T -b 2 -n %{modname}
%endif

mv ioncube_loader_lin_%{php_major_version}.%{php_minor_version}%{?zend_zts}.so %{modname}.so
ver=$(strings %{modname}.so | grep -F %{version})
if [ "$ver" != "%{version}" ]; then
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{php_sysconfdir}/conf.d}

install -p %{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
%if %{php_major_version} == 5 && %{php_minor_version} < 3
zend_extension%{?zend_zts}=%{php_extensiondir}/%{modname}.so
%else
zend_extension=%{php_extensiondir}/%{modname}.so
%endif
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/ioncube.so
