%define qualifier      201106060936
%define eclipse_base   %{_libdir}/eclipse

Epoch: 1

Name:           eclipse-changelog
Version:        2.7.0
Release:        3
Summary:        Eclipse ChangeLog plug-in

Group:          Development/Java
License:        EPL
URL:            http://sources.redhat.com/eclipse

Obsoletes:      eclipse-changelog-cdt < 1:%{version}-%{release}
Obsoletes:      eclipse-changelog-jdt < 1:%{version}-%{release}

Provides:       eclipse-changelog-cdt = 1:%{version}-%{release}
Provides:       eclipse-changelog-jdt = 1:%{version}-%{release}

# Note that 0.0.1 != 2.7.0 but this is an upstream issue
Source0:        http://download.eclipse.org/technology/linuxtools/0.8.0-sources/linuxtools-changelog-0.0.1-src.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# CDT 7 requires at least 3.6
BuildRequires:          eclipse-pde >= 1:3.6.0
# CParser requires at least CDT 7.0.0
BuildRequires:          eclipse-cdt >= 1:7.0.0
BuildRequires:          java-devel >= 1.4.2

# These plugins are really noarch but they need cdt which
# we only build on these architectures.
ExclusiveArch: %{ix86} x86_64 ppc ia64
%define debug_package %{nil}

Requires:               eclipse-platform >= 1:3.6.0

%description
The Eclipse ChangeLog package contains Eclipse features and plugins that are
useful for ChangeLog maintenance within the Eclipse IDE.  It includes
fragments for parsing C, C++, and Java source files to create more detailed
entries containing function or method names.

%prep
%setup -q -c -n linuxtools-changelog-0.0.1-src

%build
%{eclipse_base}/buildscripts/pdebuild -d cdt \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \
 -f org.eclipse.linuxtools.changelog


%install
rm -rf $RPM_BUILD_ROOT
installDir=$RPM_BUILD_ROOT/%{eclipse_base}/dropins/changelog
install -d -m 755 $installDir
unzip -q -d $installDir \
 build/rpmBuild/org.eclipse.linuxtools.changelog.zip

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc linuxtools-changelog-0.0.1-src/org.eclipse.linuxtools.changelog-feature/epl-v10.html
%{eclipse_base}/dropins/changelog

