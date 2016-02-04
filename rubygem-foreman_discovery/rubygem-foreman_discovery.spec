# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html

%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_discovery

%global mainver 1.4.0
#%global prever .rc4
%global release 1
%{?prever:
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{mainver}%{?prever}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{mainver}%{?prever}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{mainver}%{?prever}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{mainver}%{?prever}.gemspec
}

%define rubyabi 1.9.1
%global foreman_dir /usr/share/foreman
%global foreman_bundlerd_dir %{foreman_dir}/bundler.d

Summary:    MaaS Discovery Plugin for Foreman
Name:       %{?scl_prefix}rubygem-%{gem_name}
Version:    %{mainver}
Release:    %{?prever:0.}%{release}%{?prever}%{?dist}
Group:      Applications/System
License:    GPLv3
URL:        http://github.com/theforeman/foreman_discovery
Source0:    http://rubygems.org/downloads/%{gem_name}-%{version}%{?prever}.gem

Requires:   foreman >= 1.6.0
Requires:   %{?scl_prefix}rubygem(open4)
Requires:   %{?scl_prefix}rubygem(ftools)
Requires:   advancecomp
Requires:   squashfs-tools
Requires:   sudo

%if 0%{?fedora} > 18
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) >= %{rubyabi}
%endif
Requires: %{?scl_prefix}rubygems

%if 0%{?fedora} > 18
BuildRequires: %{?scl_prefix}ruby(release)
%else
BuildRequires: %{?scl_prefix}ruby(abi) >= %{rubyabi}
%endif
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}rubygems

BuildArch: noarch

Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-discovery

%description
MaaS Discovery Plugin engine for Foreman.

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0} --no-rdoc --no-ri
%{?scl:"}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{foreman_bundlerd_dir}
cat <<GEMFILE > %{buildroot}%{foreman_bundlerd_dir}/%{gem_name}.rb
gem '%{gem_name}'
GEMFILE

mkdir -p %{buildroot}/etc/sudoers.d
cat <<SUDOERS > %{buildroot}/etc/sudoers.d/%{gem_name}
# Required to run the discovery:build_image rake task as 'foreman'
foreman ALL = NOPASSWD : %{gem_instdir}/extra/build_iso.sh *, /bin/true
Defaults:foreman !requiretty
SUDOERS

# Output directory of the imgae build task
mkdir -p %{buildroot}/%{foreman_dir}/discovery_image

%files
%dir %{gem_instdir}
%{gem_instdir}/app
%{gem_instdir}/lib
%{gem_instdir}/config
%{gem_instdir}/extra
%{gem_instdir}/locale
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_dir}/%{gem_name}.rb
%attr(0755,foreman,foreman) %{foreman_dir}/discovery_image
%config %attr(0440,root,root) /etc/sudoers.d/%{gem_name}
%doc %{gem_instdir}/LICENSE

%exclude %{gem_instdir}/test
%exclude %{gem_dir}/cache/%{gem_name}-%{version}%{?prever}.gem

%files doc
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Wed Oct 01 2014 Lukas Zapletal <lzap+git@redhat.com> 1.4.0-0.1.rc4
- Update rubygem-foreman_discovery to 1.4.0.rc4 (lzap+git@redhat.com)

* Wed Oct 01 2014 Lukas Zapletal <lzap+rpm@redhat.com> - 1.4.0-0.1.rc4
- Update foreman_discovery to 1.4.0.rc4

* Tue Sep 23 2014 Dominic Cleal <dcleal@redhat.com> 1.4.0-0.1.rc3
- Update foreman_discovery to 1.4.0.rc3 (dcleal@redhat.com)

* Mon Sep 22 2014 Dominic Cleal <dcleal@redhat.com> 1.4.0-0.1.rc2
- Update foreman_discovery to 1.4.0.rc2 (dcleal@redhat.com)

* Thu Aug 28 2014 Dominic Cleal <dcleal@redhat.com> 1.4.0-0.1.rc1
- Update foreman_discovery to 1.4.0.rc1 (dcleal@redhat.com)

* Fri Jun 06 2014 Lukas Zapletal <lzap+git@redhat.com> 1.3.0-1
- Updated foreman_discovery to 1.3.0 final version (lzap+git@redhat.com)

* Wed May 21 2014 Dominic Cleal <dcleal@redhat.com> 1.3.0-0.1.rc3
- Update foreman_discovery to 1.3.0.rc3 (dcleal@redhat.com)

* Fri Apr 18 2014 Lukas Zapletal <lzap+git@redhat.com> 1.3.0-0.1.rc2
- foreman_discovery-1.3.0.rc2 bump (lzap+git@redhat.com)
- Set minimum Foreman version of 1.5 (dcleal@redhat.com)

* Wed Apr 09 2014 Marek Hulan <mhulan@redhat.com> 1.3.0-0.1.rc1
- Update foreman discovery (mhulan@redhat.com)

* Wed Apr 02 2014 Dominic Cleal <dcleal@redhat.com> 1.2.0-1
- Update to 1.2.0 (dcleal@redhat.com)

* Fri Jan 24 2014 Lukas Zapletal <lzap+git@redhat.com> 1.2.0-0.1.rc2
- Bump foreman_discovery to 1.2.0.rc2 (lzap+git@redhat.com)
- Bump foreman_discovery to 1.2.0.rc1 (lzap+git@redhat.com)

* Sat Oct 19 2013 Dominic Cleal <dcleal@redhat.com> 1.1.1-1
- Update to 1.1.1 (dcleal@redhat.com)

* Fri Oct 18 2013 Dominic Cleal <dcleal@redhat.com> 1.1.0-1
- Update to 1.1.0 (dcleal@redhat.com)

* Thu Aug 22 2013 Dominic Cleal <dcleal@redhat.com> 1.0.2-7
- Create ~foreman/discovery_dir for image building (dcleal@redhat.com)
- Add patch for #2949, don't use bundler to find build_iso.sh
  (dcleal@redhat.com)
- Add dependencies and sudoers file for image building (dcleal@redhat.com)
- Remove SCL prefix from foreman-plugin-* provide (dcleal@redhat.com)

* Tue Aug 13 2013 Lukas Zapletal <lzap+git@redhat.com> 1.0.2-6
- adding SCL prefix to the provides statement (lzap+git@redhat.com)
- fixing dependency name (lzap+git@redhat.com)

* Tue Aug 13 2013 Lukas Zapletal <lzap+git@redhat.com> 1.0.2-5
- adding provides statement (lzap+git@redhat.com)

* Mon Aug 12 2013 Lukas Zapletal <lzap+git@redhat.com> 1.0.2-4
- adding missing source file (lzap+git@redhat.com)

* Mon Aug 12 2013 Lukas Zapletal <lzap+git@redhat.com> 1.0.2-3
- removing alpha tags (lzap+git@redhat.com)

* Thu Aug 01 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.0.2-1
- bump to 1.0.2 release

* Wed Jun 26 2013 Dominic Cleal <dcleal@redhat.com> 1.0.0-0.1.rc4
- initial package build
