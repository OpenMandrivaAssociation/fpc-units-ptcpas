#set fpc version
Epoch: 1
%define fpc_ver 2.4.4

%define self ptcpas

Name:		fpc-units-%self
# svn info -r HEAD https://ptcpas.svn.sourceforge.net/svnroot/ptcpas/trunk | grep Revision
Version:	0.99.12
Release:	%mkrel 1
Group:		Development/Other
License:	Modified LGPL
Summary:	A free, portable framebuffer library, written in Free Pascal
# svn co https://ptcpas.svn.sourceforge.net/svnroot/ptcpas/trunk ptcpas-402
Source:		%self-%version.tar.bz2
Patch0:		%self-503-fpcdir.patch
URL:		http://ptcpas.sourceforge.net/

BuildRequires: fpc == %fpc_ver
BuildRequires: %{_lib}x11-devel %{_lib}xext-devel %{_lib}xrandr2-devel %{_lib}xxf86dga-devel %{_lib}xxf86vm-devel fpc-src

Requires: fpc-base == %fpc_ver
Requires: %{_lib}x11-devel %{_lib}xext-devel %{_lib}xrandr2-devel %{_lib}xxf86dga-devel %{_lib}xxf86vm-devel

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

