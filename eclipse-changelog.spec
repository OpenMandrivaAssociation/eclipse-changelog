Epoch: 1

%define fedora          1
%define redhat          0
%if %{fedora}
%define gcj_support     1
%else
%define gcj_support     0
%endif

%define eclipse_name	eclipse
%define eclipse_base	%{_datadir}/%{eclipse_name}

Name:           eclipse-changelog
Version:        2.3.3
Release:        %mkrel 1.1
Summary:        Eclipse ChangeLog plug-in

Group:          Development/Java
License:        CPL
URL:            http://sources.redhat.com/eclipse/

Source0:	%{name}-src-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:		eclipse-pde >= 1:3.2.0
BuildRequires:		eclipse-cdt
%if %{gcj_support}
BuildRequires:		gcc-java >= 0:4.0.2
BuildRequires:		java-gcj-compat-devel
Requires(post):		java-gcj-compat
Requires(postun):	java-gcj-compat
%else
BuildRequires:		java-devel >= 0:1.4.2
%endif

# this plugins is really noarch but it needs cdt which 
# we only build on these architectures.
%if %{gcj_support}
ExclusiveArch: %{ix86} x86_64 ppc ia64
%else
ExclusiveArch: %{ix86} x86_64 ppc ia64
%endif

Requires:       	eclipse-platform >= 1:3.2.0

%description
The Eclipse ChangeLog package contains Eclipse features and plugins that are
useful for ChangeLog maintenance within the Eclipse IDE.

%prep
%setup -q -c -n eclipse-changelog-%{version}


%build
# See comments in the script to understand this.
/bin/sh -x %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base} cdt
SDK=$(cd SDK > /dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

# build the main phpeclips feature
%{java} -cp %{eclipse_base}/startup.jar                \
     -Duser.home=$homedir                              \
     org.eclipse.core.launcher.Main                    \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=com.redhat.eclipse.changelog 		       \
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
%defattr(-,root,root)
%{eclipse_base}/features/com.redhat.eclipse.changelog*
%{eclipse_base}/plugins/com.redhat.eclipse.changelog*
%if %{gcj_support}
%{_libdir}/gcj/%{name}/*
%endif


