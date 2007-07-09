Epoch: 1

%define gcj_support     1
%define eclipse_base    %{_datadir}/eclipse

Name:           eclipse-changelog
Version:        2.3.4
Release:        %mkrel 1.1.1
Summary:        Eclipse ChangeLog plug-in

Group:          Development/Java
License:        EPL
URL:            http://sources.redhat.com/eclipse

Source0:        http://sourceware.org/eclipse/changelog/%{name}-src-%{version}.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:          eclipse-pde >= 1:3.2.0
BuildRequires:          eclipse-cdt >= 1:3.1.1
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%else
BuildArch:              noarch
BuildRequires:          java-devel >= 1.4.2
%endif

# These plugins are really noarch but they need cdt which 
# we only build on these architectures.
%if %{gcj_support}
ExclusiveArch: %{ix86} x86_64 ppc ia64
%else
ExclusiveArch: %{ix86} x86_64 ppc ia64
%endif

Requires:               eclipse-platform >= 1:3.2.0

%description
The Eclipse ChangeLog package contains Eclipse features and plugins that are
useful for ChangeLog maintenance within the Eclipse IDE.

%prep
%setup -q -c -n eclipse-changelog-%{version}

%build
# See comments in the script to understand this.
/bin/sh -x %{_datadir}/eclipse/buildscripts/copy-platform SDK %{eclipse_base} cdt
SDK=$(cd SDK > /dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

# build the main ChangeLog feature
%{_bindir}/eclipse \
     -Duser.home=$homedir                              \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=com.redhat.eclipse.changelog                 \
     -DsourceDirectory=$(pwd)                          \
     -DbaseLocation=$SDK                               \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{eclipse_base}
unzip -q -d $RPM_BUILD_ROOT%{eclipse_base}/.. build/rpmBuild/com.redhat.eclipse.changelog.zip

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
%defattr(0644,root,root,0755)
%{eclipse_base}/features/com.redhat.eclipse.changelog*
%{eclipse_base}/plugins/com.redhat.eclipse.changelog*
%doc %{eclipse_base}/features/com.redhat.eclipse.changelog_*/epl-v10.html
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
