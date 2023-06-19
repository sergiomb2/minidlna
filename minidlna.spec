# globals for minidlna-1.3.3-20230619-db8a2f2.tar.bz2
%global gitdate 20230619
%global gitversion db8a2f2
%global shortcommit0 %(c=%{gitversion}; echo ${c:0:7})

Name:           minidlna
Version:        1.3.3
Release:        2%{?shortcommit0:.%{gitdate}git%{shortcommit0}}%{?dist}
Summary:        Lightweight DLNA/UPnP-AV server targeted at embedded systems

License:        GPLv2
URL:            http://sourceforge.net/projects/minidlna/
Source0:        http://downloads.sourceforge.net/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch1:         v1_3_3..%{shortcommit0}_multiple_captions_support.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  avahi-devel
BuildRequires:  libuuid-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  sqlite-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libexif-devel
BuildRequires:  zlib-devel
BuildRequires:  gettext
BuildRequires:  systemd-rpm-macros
BuildRequires:  ffmpegthumbnailer-devel
BuildRequires:  opusfile-devel
Requires(pre):  shadow-utils
%{?systemd_requires}

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being fully
compliant with DLNA/UPnP-AV clients.

The minidlna daemon serves media files (music, pictures, and video) to
clients on your network.  Example clients include applications such as
Totem and XBMC, and devices such as portable media players, smartphones,
and televisions.


%prep
%autosetup -p1

# Edit the default config file
sed -i 's/#log_dir=\/var\/log/#log_dir=\/var\/log\/minidlna/' \
  %{name}.conf


%build
./autogen.sh
%configure \
  --disable-silent-rules \
  --with-db-path=%{_localstatedir}/cache/%{name} \
  --with-log-path=%{_localstatedir}/log/%{name} \
  --enable-tivo \
  --enable-thumbnail \

%make_build


%install
%make_install

# Install config file
mkdir -p %{buildroot}%{_sysconfdir}/
install -p -m 644 minidlna.conf %{buildroot}%{_sysconfdir}/

# Install systemd unit file
mkdir -p %{buildroot}%{_unitdir}/
install -p -m 644 minidlna.service %{buildroot}%{_unitdir}/

# Install tmpfiles configuration
mkdir -p %{buildroot}%{_tmpfilesdir}/
install -p -m 644 minidlna-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf
mkdir -p %{buildroot}/run/
install -d -m 755 %{buildroot}/run/%{name}/

# Create cache and log directories
mkdir -p %{buildroot}%{_localstatedir}/cache/
install -d -m 755 %{buildroot}%{_localstatedir}/cache/%{name}/
mkdir -p %{buildroot}%{_localstatedir}/log/
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}/

%find_lang %{name}


%pre
getent group minidlna >/dev/null || groupadd -r minidlna
getent passwd minidlna >/dev/null || \
useradd -r -g minidlna -d /dev/null -s /sbin/nologin \
  -c "minidlna service account" minidlna
exit 0


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files -f %{name}.lang
%attr(-,minidlna,minidlna) %config(noreplace) %{_sysconfdir}/minidlna.conf
%{_sbindir}/minidlnad
%{_unitdir}/minidlna.service
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/minidlnad.8*
%dir %attr(-,minidlna,minidlna) /run/%{name}/
%{_tmpfilesdir}/%{name}.conf
%dir %attr(-,minidlna,minidlna) %{_localstatedir}/cache/%{name}/
%dir %attr(-,minidlna,minidlna) %{_localstatedir}/log/%{name}/
%license COPYING LICENCE.miniupnpd
%doc AUTHORS NEWS README TODO


%changelog
* Sun Jun 18 2023 Sérgio Basto <sergio@serjux.com> - 1.3.3-1
- Update minidlna to 1.3.3

* Tue Feb 28 2023 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-3
- Rebuild for new ffmpeg

* Wed Feb 08 2023 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-2
- Rebuild for new flac

* Thu Sep 01 2022 Andrea Musuruane <musuruan@gmail.com> - 1.3.2-1
- Updated to new upstream release

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.0-6
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Mar 20 2021 Andrea Musuruane <musuruan@gmail.com> - 1.3.0-4
- Fix core dump (BZ #5938)
- Fix leaked sockets by correctly initialising the ev struct

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.0-2
- Rebuilt for new ffmpeg snapshot

* Wed Dec  9 11:29:39 CET 2020 Andrea Musuruane <musuruan@gmail.com> - 1.3.0-1
- Updated to new upstream release

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.2.1-11
- Rebuild for ffmpeg-4.3 git

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 06 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.1-9
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.1-6
- Rebuild for ffmpeg-4.0 release

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.2.1-5
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.1-3
- Rebuilt for ffmpeg-3.5 git

* Mon Oct 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.2.1-2
- Rebuild for ffmpeg update

* Thu Sep 21 2017 Andrea Musuruane <musuruan@gmail.com> - 1.2.1-1
- Updated to upstream 1.2.1

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 11 2017 Andrea Musuruane <musuruan@gmail.com> - 1.2.0-2
- Fixed systemd service unit configuration (#4517)
- Updated systemd snippets
- Preserve timestamps
- Dropped obsolete Group tag

* Fri Jun 02 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-1
- Updated to upstream 1.2.0
- Add build requires avahi-devel

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.5-5
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.5-3
- Patch for libavformat-57 compatibility

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.1.5-2
- Rebuilt for ffmpeg-3.1.1

* Sun Oct 04 2015 Andrea Musuruane <musuruan@gmail.com> - 1.1.5-1
- Updated to upstream 1.1.5

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 1.1.4-3
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-2
- Rebuilt for FFmpeg 2.4.x

* Sat Aug 30 2014 Andrea Musuruane <musuruan@gmail.com> - 1.1.4-1
- Updated to upstream 1.1.4

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 1.1.3-2
- Rebuilt for ffmpeg-2.3

* Sat Jun 07 2014 Andrea Musuruane <musuruan@gmail.com> - 1.1.3-1
- Updated to upstream 1.1.3

* Sat Mar 29 2014 Andrea Musuruane <musuruan@gmail.com> - 1.1.2-2
- Rebuilt for new ffmpeg

* Sat Mar 08 2014 Andrea Musuruane <musuruan@gmail.com> - 1.1.2-1
- Updated to upstream 1.1.2

* Sun Jan 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-2
- Rebuilt

* Sun Sep 15 2013 Andrea Musuruane <musuruan@gmail.com> - 1.1.0-1
- Updated to upstream 1.1.0
- Better systemd integration

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.26-3
- Rebuilt for FFmpeg 2.0.x

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.26-2
- Rebuilt for x264/FFmpeg

* Wed May 08 2013 Andrea Musuruane <musuruan@gmail.com> - 1.0.26-1
- Updated to upstream 1.0.26

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.25-4
- Rebuilt for ffmpeg

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.25-3
- Rebuilt for FFmpeg 1.0

* Sat Nov 03 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.25-2
- Fixed FTBFS caused by ffmpeg 1.0
- Updated minidlna.service I forgot to commit (BZ #2294)

* Sat Jul 14 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.25-1
- Updated to upstream 1.0.25

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.24-3
- Rebuilt for FFmpeg

* Wed Apr 25 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.24-2
- Run the daemon with the minidlna user (BZ #2294)
- Updated Debian man pages

* Sun Feb 19 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.24-1
- Updated to upstream 1.0.24

* Sat Jan 28 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.23-1
- Updated to upstream 1.0.23

* Sun Jan 22 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.22-2
- Fixed systemd unit file

* Sun Jan 15 2012 Andrea Musuruane <musuruan@gmail.com> 1.0.22-1
- Updated to upstream 1.0.22
- Removed default Fedora RPM features (defattr, BuildRoot, clean section)
- Better consistent macro usage

* Sat Jul 23 2011 Andrea Musuruane <musuruan@gmail.com> 1.0.21-1
- Updated to upstream 1.0.21

* Sat Jun 18 2011 Andrea Musuruane <musuruan@gmail.com> 1.0.20-1
- First release
- Used Debian man pages

