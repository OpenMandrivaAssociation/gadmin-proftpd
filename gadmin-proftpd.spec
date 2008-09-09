Summary:	GNOME GUI Tool for Proftpd Server Configuration
Name:		gadmin-proftpd
Version:	0.3.0
Release:	%mkrel 1
Group:		System/Configuration/Networking
License:	GPL
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynup.net/linux/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Requires:	proftpd >= 1.2.8
Requires:	usermode-consoleonly
BuildRequires:	gtk+2-devel
BuildRequires:	desktop-file-utils
Obsoletes:	gproftpd
Provides:	gproftpd
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GProftpd is a fast and easy to use GNOME2 administration tool for
the Proftpd standalone server.

%prep

%setup -q

%build
# (Abel) otherwise it would try to find files such as /var/lib/log/xferlog
%define _localstatedir /var

%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall
rm -fr $RPM_BUILD_ROOT/%_docdir

install -d %{buildroot}%{_sysconfdir}/pam.d/
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

# locales
%find_lang %name

# Mandriva Icons
install -D -m644 pixmaps/%{name}32.png %{buildroot}%{_iconsdir}/%{name}.png
install -D -m644 pixmaps/%{name}16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m644 pixmaps/%{name}48.png %{buildroot}%{_liconsdir}/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*


# Prepare usermode entry
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_sbindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog README
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_sbindir}/gprostats
%{_datadir}/pixmaps/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*
%defattr(0600,root,root,0700)
%config(noreplace) %{_sysconfdir}/%{name}


