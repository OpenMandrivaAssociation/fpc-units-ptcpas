#set fpc version

%define fpc_ver 2.6.0

%define self ptcpas


Name:		fpc-units-%self
# svn info -r HEAD https://ptcpas.svn.sourceforge.net/svnroot/ptcpas/trunk | grep Revision
Version:	503
Release:	2
Group:		Development/Other
License:	Modified LGPL
Summary:	A free, portable framebuffer library, written in Free Pascal
# svn co https://ptcpas.svn.sourceforge.net/svnroot/ptcpas/trunk ptcpas-402
Source:		%self-%version.tar.gz
Patch0:		ptcpas-%version-fpcdir.patch
URL:		http://ptcpas.sourceforge.net/

BuildRequires: fpc == %fpc_ver
BuildRequires: %{_lib}x11-devel
BuildRequires: %{_lib}xext-devel
BuildRequires: pkgconfig(xrandr)
BuildRequires: %{_lib}xxf86dga-devel
BuildRequires: %{_lib}xxf86vm-devel
BuildRequires: fpc-src

Requires: fpc-base == %fpc_ver
Requires: %{_lib}x11-devel
Requires: %{_lib}xext-devel 
Requires: pkgconfig(xrandr)
Requires: %{_lib}xxf86dga-devel
Requires: %{_lib}xxf86vm-devel

%description
PTCPas is a free, portable framebuffer library, written in Free Pascal.
It allows low-level high-speed graphics access on multiple platforms and
is distributed under the terms of a modified (to allow static linking)
GNU LGPL license. Currently supports DirectX, X11, VBE1.2+ and
fakemodes. It has been tested on Windows (all versions since Windows 95;
on i386 and x86_64), Linux (i386, x86_64 and ppc), FreeBSD and DOS.

%package demos
Group:		Development/Other
Summary:	Demo applications for %name
Requires:	fpc-base %name
%description demos
%summary

%prep
%setup -n %self-%version
#patch0 -p1

find . -depth -name .svn -exec rm -rf {} \;

for N in core/*; do sed -i 's@/usr/share/ptcpas/ptcpas.conf@%_sysconfdir/%self.conf@' $N; done

%build
export FPCDIR=%_datadir/fpcsrc

./configure

make
make demos examples

%install
%ifarch %ix86
%define fpcarch i386
%else
%define fpcarch %_arch
%endif
%define unitdir %_libdir/fpc/%fpc_ver/units/%fpcarch-linux/
mkdir -p %buildroot%unitdir/%self
install units/%fpcarch-linux/* %buildroot%unitdir/%self
mkdir -p %buildroot%_libdir/%name-demos
cp -a demos examples %buildroot%_libdir/%name-demos
rm -rf %buildroot%_libdir/%name-demos/*/units
install -D ptcpas.cfg %buildroot%_sysconfdir/%self.conf

%files
%doc docs
%unitdir/%self
%config %_sysconfdir/%self.conf

%files demos
%_libdir/%name-demos



%changelog
* Sat Aug 20 2011 Александр Казанцев <kazancas@mandriva.org> 503-1mdv2012.0
+ Revision: 695900
- imported package fpc-units-ptcpas

