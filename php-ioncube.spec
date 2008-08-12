%define		_name		ioncube
Summary:	ionCube loader module for PHP
Summary(pl.UTF-8):	Moduł wczytujący ionCube dla PHP
Name:		php-%{_name}
# this is version of x86 modules; ppc one are usually older
Version:	3.1.33
Release:	1
License:	redistributable
Group:		Libraries
# 3.1r32
Source0:	http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_x86.tar.bz2
# Source0-md5:	c04890a36ae97fb21834dde57041f90c
# 3.1r33
Source1:	http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.bz2
# Source1-md5:	8f9fef24582fba07fa06d051e336041e
# 3.1r32
Source2:	http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_ppc.tar.bz2
# Source2-md5:	e0aaac74350f344c5063d0b01a618999
URL:		http://ioncube.com/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ionCube loader module for PHP.

%description -l pl.UTF-8
Moduł wczytujący ionCube dla PHP.

%prep
%ifarch %{ix86}
%setup -q -T -b 0 -n %{_name}
%endif
%ifarch %{x8664}
%setup -q -T -b 1 -n %{_name}
%endif
%ifarch ppc
%setup -q -T -b 2 -n %{_name}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{php_sysconfdir}/conf.d}

install $(ls -1 *_ts.so  | sort | tail -n 1) $RPM_BUILD_ROOT%{php_extensiondir}/%{_name}.so
echo "zend_extension_ts=%{php_extensiondir}/%{_name}.so" > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_name}.ini

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
%doc *.txt *.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{php_extensiondir}/ioncube.so
