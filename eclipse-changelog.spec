Epoch: 1

%define gcj_support     1
%define eclipse_base    %{_datadir}/eclipse

Name:           eclipse-changelog
Version:        2.6.1
Release:        %mkrel 0.3.1
Summary:        Eclipse ChangeLog plug-in

Group:          Development/Java
License:        Eclipse Public License 
URL:            http://sources.redhat.com/eclipse

Obsoletes:      eclipse-changelog-cdt < %{epoch}:%{version}-%{release}
Obsoletes:      eclipse-changelog-jdt < %{epoch}:%{version}-%{release}

Provides:       eclipse-changelog-cdt = %{epoch}:%{version}-%{release}
Provides:       eclipse-changelog-jdt = %{epoch}:%{version}-%{release}

# This tarball was generated like so:
#
# mkdir eclipse-changelog-src-2.6.1
# cd eclipse-changelog-src-2.6.1
# for f in \
# org.eclipse.linuxtools.changelog.core \
# org.eclipse.linuxtools.changelog.doc \
# org.eclipse.linuxtools.changelog.cparser \
# org.eclipse.linuxtools.changelog.javaparser \
# org.eclipse.linuxtools.changelog-feature \
# do \
#  svn export \
#  svn://anonymous@dev.eclipse.org/svnroot/technology/org.eclipse.linuxtools/changelog/tags/R2_6_1/$f;
# done
# zip -r eclipse-changelog-src-2.6.1.zip *

Source0:        http://sourceware.org/eclipse/changelog/%{name}-src-%{version}.zip

# Patch required to 2.6.1 sources to fix a number of problems
Patch1: %{name}-2.6.1.patch

BuildRequires:          eclipse-pde >= 1:3.3.0
BuildRequires:          eclipse-cdt >= 1:4.0.0
BuildRequires:          eclipse-cvs-client >= 1:3.3.0
BuildRequires:          java-rpmbuild
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
Requires:               eclipse-cvs-client >= 1:3.3.0

%description
The Eclipse ChangeLog package contains Eclipse features and plugins that are
useful for ChangeLog maintenance within the Eclipse IDE.  It includes
fragments for parsing C, C++, and Java source files to create more detailed
entries containing function or method names.

%prep
%setup -q -c -n eclipse-changelog-%{version}
%patch1 -p0

%build
# See comments in the script to understand this.
/bin/sh -x %{_datadir}/eclipse/buildscripts/copy-platform SDK %{eclipse_base} cdt
SDK=$(cd SDK > /dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

# build the main ChangeLog feature
%{java} -cp $SDK/startup.jar                              \
     -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration  \
     org.eclipse.core.launcher.Main                    \
     -application org.eclipse.ant.core.antRunner       \
     -Duser.home=$homedir                              \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=org.eclipse.linuxtools.changelog                 \
     -DsourceDirectory=$(pwd)                          \
     -DbaseLocation=$SDK                               \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{eclipse_base}
unzip -q -d $RPM_BUILD_ROOT%{eclipse_base}/.. \
 build/rpmBuild/org.eclipse.linuxtools.changelog.zip

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

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
%{eclipse_base}/features/org.eclipse.linuxtools.changelog_*
%{eclipse_base}/plugins/org.eclipse.linuxtools.changelog.core_*
%{eclipse_base}/plugins/org.eclipse.linuxtools.changelog.cparser_*
%{eclipse_base}/plugins/org.eclipse.linuxtools.changelog.parsers.java_*
%{eclipse_base}/plugins/org.eclipse.linuxtools.changelog.doc_*
%doc %{eclipse_base}/features/org.eclipse.linuxtools.changelog_*/epl-v10.html
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/org.eclipse.linuxtools.changelog.core_*
%{_libdir}/gcj/%{name}/org.eclipse.linuxtools.changelog.cparser_*
%{_libdir}/gcj/%{name}/org.eclipse.linuxtools.changelog.parsers.java_*
%endif
