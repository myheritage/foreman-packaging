%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name CFPropertyList

Summary: A simple utility to manage VMware Fusion VMs from the command line
Name: %{?scl_prefix}rubygem-%{gem_name}

Version: 2.2.8
Release: 1%{dist}
Group: Development/Ruby
License: MIT
URL: http://github.com/fog/fog
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix}rubygems
%if 0%{?fedora} > 18
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
%endif
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}rubygems
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%define gembuilddir %{buildroot}%{gem_dir}

%description
A simple utility to manage VMware Fusion VMs from the command line

# Disabled as docs were added post-0.0.1
#%package doc
#BuildArch:  noarch
#Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
#Summary:    Documentation for rubygem-%{gem_name}
#
#%description doc
#This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -T -c

%build

%install
mkdir -p %{gembuilddir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir %{gembuilddir} --force %{SOURCE0} --no-rdoc --no-ri 
%{?scl:"}

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}
#%{gem_instdir}/config
%exclude %{gem_instdir}/.*
%{gem_instdir}/README

#%files doc
#%exclude %{gem_instdir}/CFPropertyList.gemspec

%changelog
* Tue Mar 25 2014 Dominic Cleal <dcleal@redhat.com> 0.0.1-1
- new package built with tito

