#
%define		_name		ioncube
Summary:	ionCube loader module for PHP
Name:		php-%{_name}
Version:	3.1
Release:	1
License:	redistributable
Group:		Libraries
Source0:	http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_x86.tar.bz2
# Source0-md5:	a6460e8cfabdd3c7c04c2d7181b4bf2d
Source1:	http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.bz2
# Source1-md5:	e6a3fe99bc850fe9c94a4074ec286139
Source2:	http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_ppc.tar.bz2
# Source2-md5:	233acef94ff789a799f0637648d1e10f
URL:		http://ioncube.com/
BuildRequires:	coreutils
Requires:	php-common >= 4:5.0.4
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ionCube loader module for PHP.

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

%build

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

%preun
if [ "$1" = 0 ]; then
	# remove last pieces of cache
	rm -rf /var/cache/%{_name}/*
fi

%files
%defattr(644,root,root,755)
%doc *.txt *.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{php_extensiondir}/ioncube.so
