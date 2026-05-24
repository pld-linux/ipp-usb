# TODO: system goipp 1.1.0 (github.com/OpenPrinting/goipp)
#
# Conditional build:
%bcond_without	tests	# go tests

Summary:	IPP-over-USB - driverless IPP printing on USB-connected printers
Summary(pl.UTF-8):	IPP po USB - drukowanie przez IPP na drukarkach podłączonych przez USB bez sterownika
Name:		ipp-usb
Version:	0.9.33
Release:	1
License:	BSD
Group:		Applications/Printing
#Source0Download: https://github.com/OpenPrinting/ipp-usb/tags
Source0:	https://github.com/OpenPrinting/ipp-usb/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	88e9b53cb7edfc94df92a7a39ec4871a
URL:		https://github.com/OpenPrinting/ipp-usb
BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	avahi-devel
BuildRequires:	dbus-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	golang >= 1.11
BuildRequires:	ronn
BuildRequires:	rpmbuild(macros) >= 2.011
Requires:	systemd-units >= 1:250.1
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ipp-usb is a daemon that enables driverless IPP printing on
USB-connected printers. It emulates an IPP network printer, providing
full access to the physical printer: Printing, scanning, fax out, and
the admin web interface.

%description -l pl.UTF-8
ipp-usb to demon umożliwiający drukowanie po IPP na drukarkach
podłączonych przez USB bez sterownika. Emuluje drukarkę sieciową IPP,
zapewniając pełny dostep do fizycznej drukarki: drukowanie,
skanowanie, wysyłanie faksów oraz interfejs administracyjny WWW.

%prep
%setup -q

%build
%{__go} build -tags nethttpomithttp2 -mod=vendor

%if %{with tests}
%{__go} test -mod=vendor
%endif

%{__make} man

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/lib/udev/rules.d,%{systemdunitdir},%{_sysconfdir}/ipp-usb,%{_mandir}/man8,%{_datadir}/ipp-usb/quirks}

# see make install, but without stripping and with dirs adjusted
install ipp-usb $RPM_BUILD_ROOT%{_sbindir}
cp -p systemd-udev/*.rules $RPM_BUILD_ROOT/lib/udev/rules.d
cp -p systemd-udev/*.service $RPM_BUILD_ROOT%{systemdunitdir}
cp -p ipp-usb.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipp-usb
cp -p ipp-usb.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p ipp-usb-quirks/* $RPM_BUILD_ROOT%{_datadir}/ipp-usb/quirks

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post ipp-usb.service

%preun
%systemd_preun ipp-usb.service

%postun
%systemd_postun_with_restart ipp-usb.service

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_sbindir}/ipp-usb
%{_datadir}/ipp-usb
/lib/udev/rules.d/71-ipp-usb.rules
%{systemdunitdir}/ipp-usb.service
%dir %{_sysconfdir}/ipp-usb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipp-usb/ipp-usb.conf
%{_mandir}/man8/ipp-usb.8*
