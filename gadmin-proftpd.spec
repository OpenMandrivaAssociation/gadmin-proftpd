# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	GNOME GUI Tool for Proftpd Server Configuration
Name:		gadmin-proftpd
Version:	0.4.2
Release:	2
Group:		System/Configuration/Networking
License:	GPLv3+
URL:		https://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gadmin-proftpd/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Requires:	proftpd >= 1.2.8
Requires:	usermode-consoleonly
BuildRequires:	gtk+2-devel
BuildRequires:	desktop-file-utils
Obsoletes:	gproftpd
Provides:	gproftpd
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gadmin-proftpd is a fast and easy to use GTK+-based administration tool
for the Proftpd FTP server.

%prep
%setup -q

%build
# (Abel) otherwise it would try to find files such as /var/lib/log/xferlog
%define _localstatedir /var

%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -fr %{buildroot}/%{_docdir}

install -d %{buildroot}%{_sysconfdir}/pam.d/
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

# locales
%find_lang %{name}

# Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -D -m644 pixmaps/%{name}32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m644 pixmaps/%{name}16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m644 pixmaps/%{name}48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-PROFTPD,Gadmin-Proftpd,g' desktop/%{name}.desktop

mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --remove-key="Encoding" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*


# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

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

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog README
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_sbindir}/gprostats
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%defattr(0600,root,root,0700)
%config(noreplace) %{_sysconfdir}/%{name}




%changelog
* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 0.4.2-1mdv2011.0
+ Revision: 677005
- update to new version 0.4.2

* Thu Jan 20 2011 Funda Wang <fwang@mandriva.org> 0.4.1-1
+ Revision: 631775
- update to new version 0.4.1

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-2mdv2011.0
+ Revision: 610788
- rebuild

* Fri Mar 19 2010 Funda Wang <fwang@mandriva.org> 0.4.0-1mdv2010.1
+ Revision: 525189
- new version 0.4.0

* Fri Feb 12 2010 Funda Wang <fwang@mandriva.org> 0.3.9-1mdv2010.1
+ Revision: 504476
- New version 0.3.9

* Fri Sep 11 2009 Emmanuel Andry <eandry@mandriva.org> 0.3.8-1mdv2010.0
+ Revision: 438458
- New version 0.3.8

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.3.5-2mdv2010.0
+ Revision: 437642
- rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.3.5-1mdv2009.1
+ Revision: 324084
- put the consolehelper link in bindir, not sbindir - there's no point having
  it in sbindir as it's not in a user's path (this broke the menu entry)
- don't have encoding key in the menu entry
- don't have the name IN CAPITALS in menu entry
- fd.o icons
- clean macro use
- fix description a bit
- new license policy
- disable Werror as I can't fix the string errors without it crashing on start
- new release 0.3.5

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.3.0-1mdv2009.0
+ Revision: 283093
- import gadmin-proftpd


