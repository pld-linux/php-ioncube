%define		php_name	php%{?php_suffix}
%define		modname		ioncube
Summary:	ionCube loader module for PHP
Summary(pl.UTF-8):	Moduł wczytujący ionCube dla PHP
Name:		%{php_name}-%{modname}
Version:	6.1.0
Release:	1
License:	redistributable
Group:		Libraries
# www.ioncube.com/loaders.php
Source0:	http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86.tar.gz
# Source0-md5:	ab516ebc96a40ce45ea1ae1f49989fb6
Source1:	http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz
# Source1-md5:	f173c4d285440a7dc5f3fb1b20cacefc
URL:		http://www.ioncube.com/
BuildRequires:	%{php_name}-devel >= 4:5.2.0
BuildRequires:	rpmbuild(macros) >= 1.579
BuildRequires:	sed >= 4.0
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
ExclusiveArch:	%{ix86} %{x8664}
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

%build
mv ioncube_loader_lin_%{php_major_version}.%{php_minor_version}%{?zend_zts}.so %{modname}.so
ver=$(strings %{modname}.so | grep -F %{version} | grep "^%{version}" | sed -e s'# .*##g')
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
