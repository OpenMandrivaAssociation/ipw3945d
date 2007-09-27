%define name ipw3945d
%define version 1.7.22
%define mdkrelease 4
%define release %mkrel %{mdkrelease}

# dont generate a debug package 
# otherwise we'll end up with an empty rpm
%define _enable_debug_packages 0
%define install %%install

Summary:	Intel PRO/Wireless 3945 (IPW3945ABG) 
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.bz2
Patch0:		ipw3945d-1.7.22-net.patch
License:	proprietary
Url:		http://sourceforge.net/projects/ipw3945
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-buildroot
Prefix:		%{_prefix}
Requires:	drakxtools >= 10-34.2mdk
Requires(preun):	rpm-helper
Requires(post):	rpm-helper


%description
Regulatory daemon for the Intel PRO/Wireless 3945 (IPW3945ABG) Wifi adapter.

%prep
%setup -q 
%patch0 -p1 -b .net

%build

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sbindir}
%ifarch %{ix86}
install -m755 x86/%{name}  $RPM_BUILD_ROOT/%{_sbindir}
%endif
%ifarch x86_64
install -m755 x86_64/%{name}  $RPM_BUILD_ROOT/%{_sbindir}
%endif

install -m755 %{name}-{start,stop} $RPM_BUILD_ROOT/%{_sbindir}
perl -pi -e 's,\B/sbin/%{name},/usr/sbin/%{name},' $RPM_BUILD_ROOT/%{_sbindir}/%{name}-{start,stop}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{name} <<EOF
install ipw3945 [ -w /var/run ] && /sbin/modprobe --ignore-install ipw3945 && /usr/sbin/ipw3945d-start
remove  ipw3945 /usr/sbin/ipw3945d-stop ; /sbin/modprobe -r --ignore-remove ipw3945
EOF

%clean
rm -rf $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE.ipw3945d
%doc README.ipw3945d
%{_sbindir}/ipw3945d
%{_sbindir}/%{name}-start
%{_sbindir}/%{name}-stop
%{_sysconfdir}/modprobe.d/%{name}


