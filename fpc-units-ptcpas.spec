%define fpc_ver 2.6.0
%define oname ptcpas

Summary:	A free, portable framebuffer library, written in Free Pascal
Name:		fpc-units-%{oname}
Version:	503
Release:	2
Group:		Development/Other
License:	Modified LGPL
Url:		http://ptcpas.sourceforge.net/
# svn info -r HEAD https://ptcpas.svn.sourceforge.net/svnroot/ptcpas/trunk | grep Revision
# svn co https://ptcpas.svn.sourceforge.net/svnroot/ptcpas/trunk ptcpas-402
Source0:	%{oname}-%{version}.tar.gz
Patch0:		ptcpas-%{version}-fpcdir.patch

BuildRequires:	fpc == %{fpc_ver}
BuildRequires:	fpc-src
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xf86dgaproto)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xxf86vm)
Requires:	fpc-base == %{fpc_ver}
Requires:	pkgconfig(x11)
Requires:	pkgconfig(xext)
Requires:	pkgconfig(xf86dgaproto)
Requires:	pkgconfig(xrandr)
Requires:	pkgconfig(xxf86vm)

%description
PTCPas is a free, portable framebuffer library, written in Free Pascal.
It allows low-level high-speed graphics access on multiple platforms and
is distributed under the terms of a modified (to allow static linking)
GNU LGPL license. Currently supports DirectX, X11, VBE1.2+ and
fakemodes. It has been tested on Windows (all versions since Windows 95;
on i386 and x86_64), Linux (i386, x86_64 and ppc), FreeBSD and DOS.

%package demos
Group:		Development/Other
Summary:	Demo applications for %{name}
Requires:	fpc-base %{name}

%description demos
%summary

%prep
%setup -n %{oname}-%{version}
#patch0 -p1

find . -depth -name .svn -exec rm -rf {} \;

for N in core/*; do sed -i 's@/usr/share/ptcpas/ptcpas.conf@%{_sysconfdir}/%{oname}.conf@' $N; done

%build
export FPCDIR=%{_datadir}/fpcsrc

./configure

make
make demos examples

%install
%ifarch %ix86
%define fpcarch i386
%else
%define fpcarch %{_arch}
%endif
%define unitdir %{_libdir}/fpc/%{fpc_ver}/units/%fpcarch-linux/
mkdir -p %{buildroot}%{unitdir}/%{oname}
install units/%fpcarch-linux/* %{buildroot}%{unitdir}/%{oname}
mkdir -p %{buildroot}%{_libdir}/%{name}-demos
cp -a demos examples %{buildroot}%{_libdir}/%{name}-demos
rm -rf %{buildroot}%{_libdir}/%{name}-demos/*/units
install -D ptcpas.cfg %{buildroot}%{_sysconfdir}/%{oname}.conf

%files
%doc docs
%{unitdir}/%{oname}
%config %{_sysconfdir}/%{oname}.conf

%files demos
%{_libdir}/%{name}-demos

