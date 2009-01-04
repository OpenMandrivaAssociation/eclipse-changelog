Epoch: 1

%define gcj_support     0
%define eclipse_base    %{_libdir}/eclipse

Name:           eclipse-changelog
Version:        2.6.4
Release:        %mkrel 0.1.0
Summary:        Eclipse ChangeLog plug-in

Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        Eclipse Public License
URL:            http://sources.redhat.com/eclipse

Obsoletes:      eclipse-changelog-cdt < %{epoch}:%{version}-%{release}
Obsoletes:      eclipse-changelog-jdt < %{epoch}:%{version}-%{release}

Provides:       eclipse-changelog-cdt = %{epoch}:%{version}-%{release}
Provides:       eclipse-changelog-jdt = %{epoch}:%{version}-%{release}

# This tarball was generated like so:
#
# mkdir eclipse-changelog-src-2.6.2
# cd eclipse-changelog-src-2.6.2
# for f in \
# org.eclipse.linuxtools.changelog.core \
# org.eclipse.linuxtools.changelog.doc \
# org.eclipse.linuxtools.changelog.cparser \
# org.eclipse.linuxtools.changelog.javaparser \
# org.eclipse.linuxtools.changelog-feature \
# do \
#  svn export \
#  svn://anonymous@dev.eclipse.org/svnroot/technology/org.eclipse.linuxtools/changelog/tags/R2_6_2/$f;
# done
# zip -r eclipse-changelog-src-2.6.2.zip *

Source0:        http://sourceware.org/eclipse/changelog/%{name}-src-%{version}.zip

BuildRequires:          eclipse-pde >= 1:3.3.0
BuildRequires:          eclipse-cdt >= 1:4.0.0
BuildRequires:          eclipse-cvs-client >= 1:3.3.0
BuildRequires:          java-rpmbuild
BuildRequires:          zip
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%else
BuildRequires:          java-devel >= 0:1.4.2
%endif

# These plugins are really noarch but they need cdt which
# we only build on these architectures.
%if %{gcj_support}
ExclusiveArch: %{ix86} x86_64 ppc ia64
%else
ExclusiveArch: %{ix86} x86_64 ppc ia64
%endif

Requires:               eclipse-platform >= 1:3.3.0

%description
The Eclipse ChangeLog package contains Eclipse features and plugins that are
useful for ChangeLog maintenance within the Eclipse IDE.  It includes
fragments for parsing C, C++, and Java source files to create more detailed
entries containing function or method names.

%prep
%setup -q -c -n eclipse-changelog-%{version}

%build
%{eclipse_base}/buildscripts/pdebuild -d cdt \
-a "-DjavacSource=1.5 -DjavacTarget=1.5" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar

%install
rm -rf $RPM_BUILD_ROOT
installDir=$RPM_BUILD_ROOT/%{eclipse_base}/dropins/changelog
install -d -m 755 $installDir
unzip -q -d $installDir \
 build/rpmBuild/org.eclipse.linuxtools.changelog.zip

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%doc org.eclipse.linuxtools.changelog-feature/epl-v10.html
%{eclipse_base}/dropins/changelog
%{gcj_files}

