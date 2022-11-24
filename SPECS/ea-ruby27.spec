# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby27

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%scl_package ruby

# this will never change through the life of this specfile
# new specfiles with newer versions of ruby will need to update this
%global major_minor_version 2.7

# Tests require that you build the RPM as a non-root user,
# and can take a long time to run.
# You skip them by setting the runselftest global to 0.
%{!?runselftest: %{expand: %%global runselftest 0}}

# Bundled libraries versions
%global rubygems_base_version 3.1.6
%global molinillo_base_version 0.6.6

%global bigdecimal_base_version 2.0.0
%global bundler_base_version 2.1.4
%global did_you_mean_base_version 1.4.0
%global io_console_base_version 0.5.6
%global irb_base_version 1.2.6
%global json_base_version 2.3.0
%global minitest_base_version 5.13.0
%global net_telnet_base_version 0.2.0
%global openssl_base_version 2.1.3
%global power_assert_base_version 1.1.7
%global psych_base_version 3.1.0
%global racc_base_version 1.4.16
%global rake_base_version 13.0.1
%global rdoc_base_version 6.2.1.1
%global rexml_base_version 3.2.3.1
%global test_unit_base_version 3.3.4
%global webrick_base_version 1.6.1
%global xmlrpc_base_version 0.3.0

# Might not be needed in the future, if we are lucky enough.
# https://bugzilla.redhat.com/show_bug.cgi?id=888262
%global tapset_root %{_datadir}/systemtap
%global tapset_dir %{tapset_root}/tapset
%global tapset_libdir %(echo %{_libdir} | sed 's/64//')*

%global _normalized_cpu %(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/')

%global gem_name ruby

%define ea_openssl_ver 1.1.1d-1

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
#
# NOTE: If there is a ruby version update, you need to make sure that all of the 'rubygems' included in
# the package were updated in order to reset the release_prefix back to 1.
#
# If any of the rubygems were not updated then the release_prefix *MUST* be bumped, as yum will not be
# able to properly handle the dependencies otherwise.
%define release_prefix 1

%if 0%{?fedora} >= 19
%global with_rubypick 1
%endif

Summary: An interpreter of object-oriented scripting language
Name: %{?scl_prefix}ruby
Version: 2.7.7
Release: %{release_prefix}%{?dist}.cpanel
Group: Development/Languages
# Public Domain for example for: include/ruby/st.h, strftime.c, missing/*, ...
# MIT and CCO: ccan/*
# zlib: ext/digest/md5/md5.*, ext/nkf/nkf-utf8/nkf.c
# UCD: some of enc/trans/**/*.src
License: (Ruby or BSD) and Public Domain and MIT and CC0 and zlib and UCD
URL: http://ruby-lang.org/
Source0: %{pkg_name}/%{major_minor_version}/%{ruby_archive}.tar.gz
Source1: operating_system.rb
# TODO: Try to push SystemTap support upstream.
Source2: libruby.stp
Source3: ruby-exercise.stp
Source4: macros.ruby
Source5: macros.rubygems
Source6: abrt_prelude.rb
# This wrapper fixes https://bugzilla.redhat.com/show_bug.cgi?id=977941
# Hopefully, it will get removed soon:
# https://fedorahosted.org/fpc/ticket/312
# https://bugzilla.redhat.com/show_bug.cgi?id=977941
Source7: config.h
Source13: test_systemtap.rb
# To test Ruby software collection
Source14: test_dependent_scls.rb

# %%load function should be supported in RPM 4.12+.
# http://lists.rpm.org/pipermail/rpm-maint/2014-February/003659.html
Source100: load.inc

%global ruby_version %{version}
%global ruby_release %{ruby_version}
%global ruby_archive %{pkg_name}-%{ruby_version}

%global version_prefix 27

# TODO: The IRB has strange versioning. Keep the Ruby's versioning ATM.
# http://redmine.ruby-lang.org/issues/5313
#
# Refactored versioning to include ruby version so that it updates
# nicely.

%global bigdecimal_version %{version_prefix}.%{ruby_version}.%{bigdecimal_base_version}
%global bundler_version %{version_prefix}.%{ruby_version}.%{bundler_base_version}
%global did_you_mean_version %{version_prefix}.%{ruby_version}.%{did_you_mean_base_version}
%global io_console_version %{version_prefix}.%{ruby_version}.%{io_console_base_version}
%global irb_version %{version_prefix}.%{ruby_version}.%{irb_base_version}
%global json_version %{version_prefix}.%{ruby_version}.%{json_base_version}
%global minitest_version %{version_prefix}.%{ruby_version}.%{minitest_base_version}
%global net_telnet_version %{version_prefix}.%{ruby_version}.%{net_telnet_base_version}
%global openssl_version %{version_prefix}.%{ruby_version}.%{openssl_base_version}
%global power_assert_version %{version_prefix}.%{ruby_version}.%{power_assert_base_version}
%global psych_version %{version_prefix}.%{ruby_version}.%{psych_base_version}
%global racc_version %{version_prefix}.%{ruby_version}.%{racc_base_version}
%global rake_version %{version_prefix}.%{ruby_version}.%{rake_base_version}
%global rdoc_version %{version_prefix}.%{ruby_version}.%{rdoc_base_version}
%global rexml_version %{version_prefix}.%{ruby_version}.%{rexml_base_version}
%global test_unit_version %{version_prefix}.%{ruby_version}.%{test_unit_base_version}
%global webrick_version %{version_prefix}.%{ruby_version}.%{webrick_base_version}
%global xmlrpc_version %{version_prefix}.%{ruby_version}.%{xmlrpc_base_version}
%global molinillo_version %{version_prefix}.%{ruby_version}.%{molinillo_base_version}

%global rubygems_version %{version_prefix}.%{ruby_version}.%{rubygems_base_version}

# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/ruby/ruby-%{ruby_version}/rubygems

%include %{SOURCE100}

# NOTE: the macro load syntax is not working with our macro files on C8. 
# So I am going to manually do them here.   Also if they change
# in the SOURCE file they need to change here as well.
# The SOURCE files are distributed with Ruby, so I do not know
# if I can change the syntax.
#
# NOTE: I also put %%global in front of each macro definition so it
# is not a simple copy and paste
#
# this line was in scl-ruby27: %%{load %%{SOURCE4}}
# this line was in scl-ruby27: %%{load %%{SOURCE5}}

## FROM SOURCE4
%global ruby_libdir %{_datadir}/%{pkg_name}
%global ruby_libdir_ver %{_datadir}/%{pkg_name}/ruby-%{ruby_version}
%global ruby_libarchdir %{_libdir}/%{pkg_name}
%global ruby_libarchdir_ver %{ruby_libarchdir}/ruby-%{ruby_version}

# This is the local lib/arch and should not be used for packaging.
%global ruby_sitedir site_ruby
%global ruby_sitelibdir %{_prefix}/local/share/%{pkg_name}/%{ruby_sitedir}
%global ruby_sitearchdir %{_prefix}/local/%{_lib}/%{pkg_name}/%{ruby_sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the Fedora repositories.
%global ruby_vendordir vendor_ruby
%global ruby_vendorlibdir %{ruby_libdir}/%{ruby_vendordir}
%global ruby_vendorarchdir %{ruby_libarchdir}/%{ruby_vendordir}

# For ruby packages we want to filter out any provides caused by private
# libs in %%{ruby_vendorarchdir}/%%{ruby_sitearchdir}.
#
# Note that this must be invoked in the spec file, preferably as
# "%%{?ruby_default_filter}", before any %%description block.
%global ruby_default_filter %{expand: \
%global __provides_exclude_from %{?__provides_exclude_from:%{__provides_exclude_from}|}^(%{ruby_vendorarchdir}|%{ruby_sitearchdir})/.*\\\\.so$ \
}
# END SOURCE4

# FROM SOURCE5
# The RubyGems root folder.
%global gem_dir %{_datadir}/gems
%global gem_dir2 %{_datadir}/gems/gems/ruby-%{ruby_version}
%global gem_archdir %{_libdir}/gems

# Common gem locations and files.
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_extdir_mri %{gem_archdir}/ruby/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}

# Install gem into appropriate directory.
# -n<gem_file>      Overrides gem file name for installation.
# -d<install_dir>   Set installation directory.
%global gem_install(d:n:) \
mkdir -p %{-d*}%{!?-d:.%{gem_dir}} \
\
CONFIGURE_ARGS="--with-cflags='%{optflags}' $CONFIGURE_ARGS" \\\
gem install \\\
        -V \\\
        --local \\\
        --build-root %{-d*}%{!?-d:.} \\\
        --force \\\
        --document=ri,rdoc \\\
        %{-n*}%{!?-n:%{gem_name}-%{version}.gem} \
%{nil}

# For rubygems packages we want to filter out any provides caused by private
# libs in %%{gem_archdir}.
#
# Note that this must be invoked in the spec file, preferably as
# "%%{?rubygems_default_filter}", before any %description block.
%global rubygems_default_filter %{expand: \
%global __provides_exclude_from %{?__provides_exclude_from:%{__provides_exclude_from}|}^%{gem_extdir_mri}/.*\\\\.so$ \
}
# END SOURCE5

Patch01: 0001-Use-ruby_version_dir_name-for-versioned-directories.patch
Patch02: 0002-Add-ruby_version_dir_name-support-for-RDoc.patch
Patch03: 0003-Add-ruby_version_dir_name-support-for-RubyGems.patch
Patch04: 0004-Let-headers-directories-follow-the-configured-versio.patch
Patch05: 0005-Prevent-duplicated-paths-when-empty-version-string-i.patch
Patch06: 0006-Allow-to-configure-libruby.so-placement.patch
Patch07: 0007-Always-use-i386.patch
Patch08: 0008-Allow-to-install-RubyGems-into-custom-location-outsi.patch
Patch09: 0009-Verbose-mkmf.patch
Patch10: 0010-Allow-to-specify-addition-preludes-by-configuration.patch
Patch11: 0011-Generate-preludes-using-miniruby.patch
Patch12: 0012-Rely-on-ldd-to-detect-glibc.patch
Patch13: 0013-Skip-multicast-tests-when-multicast-is-not-available.patch

Requires: %{?scl_prefix}%{pkg_name}-libs%{?_isa} = %{version}-%{release}
Requires: %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Requires: %{?scl_prefix}rubygem(bigdecimal) >= %{bigdecimal_version}
Requires: %{?scl_prefix}rubygem(did_you_mean) >= %{did_you_mean_version}
Requires: %{?scl_prefix}rubygem(openssl) >= %{openssl_version}

%{?scl:Requires: %{scl}-runtime >= 2.7.0}

BuildRequires: ea-ruby27-libuv
Requires: ea-ruby27-libuv

%if 0%{rhel} > 6
BuildRequires: autoconf
%else
BuildRequires: autotools-latest-autoconf
%endif

%if 0%{rhel} == 7
BuildRequires: libyaml
%endif

%if 0%{rhel} >= 8
# Believe it or not Ruby uses Python
Requires: python36 python2
%endif

BuildRequires: gdbm-devel
BuildRequires: libffi-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: scl-utils
BuildRequires: scl-utils-build
%{?scl:BuildRequires: %{scl}-runtime >= 2.7.0}
# Needed to pass test_set_program_name(TestRubyOptions)
BuildRequires: procps
BuildRequires: binutils
BuildRequires: systemtap-sdt-devel
# RubyGems test suite optional dependencies.
BuildRequires: git
BuildRequires: cmake

# This package provides %%{_bindir}/ruby-mri therefore it is marked by this
# virtual provide. It can be installed as dependency of rubypick.
Provides: ruby(runtime_executable) = %{ruby_release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%package devel
Summary:    A Ruby development environment
Group:      Development/Languages
Requires:   %{?scl_prefix}%{pkg_name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package libs
Summary:    Libraries necessary to run Ruby
Group:      Development/Libraries
License:    Ruby or BSD
Provides:   %{?scl_prefix}ruby(release) = %{ruby_release}

# Virtual provides for CCAN copylibs.
# https://fedorahosted.org/fpc/ticket/364
Provides: bundled(ccan-build_assert)
Provides: bundled(ccan-check_type)
Provides: bundled(ccan-container_of)
Provides: bundled(ccan-list)

%description libs
This package includes the libruby, necessary to run Ruby.

# TODO: Rename or not rename to ruby-rubygems?
%package -n %{?scl_prefix}rubygems
Summary:    The Ruby standard for packaging ruby libraries
Version:    %{rubygems_version}
Group:      Development/Libraries
License:    Ruby or MIT
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}rubygem(rdoc) >= %{rdoc_version}

Requires: %{?scl_prefix}rubygem(rdoc) >= %{rdoc_version}
Requires: %{?scl_prefix}rubygem(io-console) >= %{io_console_version}
Requires: %{?scl_prefix}rubygem(openssl) >= %{openssl_version}
Requires: %{?scl_prefix}rubygem(psych) >= %{psych_version}
Provides: %{?scl_prefix}gem = %{version}-%{release}
Provides: %{?scl_prefix}ruby(rubygems) = %{version}-%{release}
# https://github.com/rubygems/rubygems/pull/1189#issuecomment-121600910
Provides: bundled(rubygem(molinillo)) = %{molinillo_version}
Provides: bundled(rubygem-molinillo) = %{molinillo_version}
BuildArch: noarch

%description -n %{?scl_prefix}rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%package -n %{?scl_prefix}rubygems-devel
Summary:    Macros and development tools for packaging RubyGems
Version:    %{rubygems_version}
Group:      Development/Libraries
License:    Ruby or MIT
Requires:   %{?scl_prefix}ruby(rubygems) = %{version}-%{release}
# Needed for RDoc documentation format generation.
Requires:   %{?scl_prefix}rubygem(json) >= %{json_version}
Requires:   %{?scl_prefix}rubygem(rdoc) >= %{rdoc_version}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygems-devel
Macros and development tools for packaging RubyGems.

%package -n %{?scl_prefix}rubygem-rake
Summary:    Ruby based make-like utility
Version:    %{rake_version}
Group:      Development/Libraries
License:    MIT
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rake = %{version}-%{release}
Provides:   %{?scl_prefix}rubygem(rake) = %{version}-%{release}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygem-rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.

%package irb
Summary:    The Interactive Ruby
Version:    %{irb_version}
Group:      Development/Libraries
Requires:   %{?scl_prefix}%{pkg_name}-libs = %{ruby_version}
Provides:   %{?scl_prefix}irb = %{version}-%{release_prefix}
Provides:   %{?scl_prefix}ruby(irb) = %{version}-%{release_prefix}
BuildArch:  noarch

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.

%package -n %{?scl_prefix}rubygem-rdoc
Summary:    A tool to generate HTML and command-line documentation for Ruby projects
Version:    %{rdoc_version}
Group:      Development/Libraries
# SIL: lib/rdoc/generator/template/darkfish/css/fonts.css
License:    GPLv2 and Ruby and MIT and SIL

Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Requires:   %{?scl_prefix}ruby(irb) = %{irb_version}
Requires:   %{?scl_prefix}rubygem(io-console) >= %{io_console_version}
# Hardcode the dependency to keep it compatible with dependencies of the
# official rubygem-rdoc gem.
Requires:   %{?scl_prefix}rubygem(json) >= %{json_version}
Provides:   %{?scl_prefix}rdoc = %{version}-%{release}
Provides:   %{?scl_prefix}ri = %{version}-%{release}
Provides:   %{?scl_prefix}rubygem(rdoc) = %{version}-%{release}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygem-rdoc
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.

%package doc
Summary:    Documentation for %{pkg_name}
Group:      Documentation
Requires:   %{_bindir}/ri
BuildArch:  noarch

%description doc
This package contains documentation for %{pkg_name}.

%package -n %{?scl_prefix}rubygem-bigdecimal
Summary:    BigDecimal provides arbitrary-precision floating point decimal arithmetic
Version:    %{bigdecimal_version}
Group:      Development/Libraries
License:    GPL+ or Artistic
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(bigdecimal) = %{version}-%{release}

%description -n %{?scl_prefix}rubygem-bigdecimal
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect - whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.

%package -n %{?scl_prefix}rubygem-did_you_mean
Summary:    "Did you mean?" experience in Ruby
Version:    %{did_you_mean_version}
Group:      Development/Libraries
License:    MIT
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(did_you_mean) = %{version}-%{release}

%description -n %{?scl_prefix}rubygem-did_you_mean
"did you mean?" experience in Ruby: the error message will tell you the right
one when you misspelled something.

%package -n %{?scl_prefix}rubygem-io-console
Summary:    IO/Console is a simple console utilizing library
Version:    %{io_console_version}
Group:      Development/Libraries
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(io-console) = %{version}-%{release}

%description -n %{?scl_prefix}rubygem-io-console
IO/Console provides very simple and portable access to console. It doesn't
provide higher layer features, such like curses and readline.

%package -n %{?scl_prefix}rubygem-json
Summary:    This is a JSON implementation as a Ruby extension in C
Version:    %{json_version}
Group:      Development/Libraries
# UCD: ext/json/generator/generator.c
License:    (Ruby or GPLv2) and UCD
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(json) = %{version}-%{release}

%description -n %{?scl_prefix}rubygem-json
This is a implementation of the JSON specification according to RFC 4627.
You can think of it as a low fat alternative to XML, if you want to store
data to disk or transmit it over a network rather than use a verbose
markup language.

%package -n %{?scl_prefix}rubygem-minitest
Summary:    Minitest provides a complete suite of testing facilities
Version:    %{minitest_version}
Group:      Development/Libraries
License:    MIT
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(minitest) = %{version}-%{release}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygem-minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.

%package -n %{?scl_prefix}rubygem-openssl
Summary:    OpenSSL provides SSL, TLS and general purpose cryptography
Version:    %{openssl_version}
Group:      Development/Libraries
License:    Ruby or BSD
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(openssl) = %{version}-%{release}

%if 0%{rhel} < 8
BuildRequires: ea-openssl11 >= %{ea_openssl_ver}
BuildRequires: ea-openssl11-devel >= %{ea_openssl_ver}
Requires: ea-openssl11
%else
# In C8 we use system openssl. See DESIGN.md in ea-openssl11 git repo for details
BuildRequires: openssl
BuildRequires: openssl-devel
Requires: openssl
%endif

%description -n %{?scl_prefix}rubygem-openssl
OpenSSL provides SSL, TLS and general purpose cryptography. It wraps the
OpenSSL library.

%package -n %{?scl_prefix}rubygem-power_assert
Summary:    Power Assert for Ruby
Version:    %{power_assert_version}
Group:      Development/Libraries
License:    Ruby or BSD
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(power_assert) = %{version}-%{release}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygem-power_assert
Power Assert shows each value of variables and method calls in the expression.
It is useful for testing, providing which value wasn't correct when the
condition is not satisfied.

%package -n %{?scl_prefix}rubygem-psych
Summary:    A libyaml wrapper for Ruby
Version:    %{psych_version}
Group:      Development/Libraries
License:    MIT
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(psych) = %{version}-%{release}

%description -n %{?scl_prefix}rubygem-psych
Psych is a YAML parser and emitter. Psych leverages
libyaml[http://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting
capabilities. In addition to wrapping libyaml, Psych also knows how to
serialize and de-serialize most Ruby objects to and from the YAML format.

%package -n %{?scl_prefix}rubygem-net-telnet
Summary:    Provides telnet client functionality
Version:    %{net_telnet_version}
Group:      Development/Libraries
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(net-telnet) = %{version}-%{release}

%description -n %{?scl_prefix}rubygem-net-telnet
Provides telnet client functionality.

This class also has, through delegation, all the methods of a socket object
(by default, a TCPSocket, but can be set by the Proxy option to new()). This
provides methods such as close() to end the session and sysread() to read data
directly from the host, instead of via the waitfor() mechanism. Note that if
you do use sysread() directly when in telnet mode, you should probably pass
the output through preprocess() to extract telnet command sequences.

# The Summary/Description fields are rather poor.
# https://github.com/test-unit/test-unit/issues/73

%package -n %{?scl_prefix}rubygem-test-unit
Summary:    Improved version of Test::Unit bundled in Ruby 1.8.x
Version:    %{test_unit_version}
Group:      Development/Libraries
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:    (Ruby or BSD) and (Ruby or BSD or Python) and (Ruby or BSD or LGPLv2+)
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Requires:   %{?scl_prefix}rubygem(power_assert)
Provides:   %{?scl_prefix}rubygem(test-unit) = %{version}-%{release}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygem-test-unit
Ruby 1.9.x bundles minitest not Test::Unit. Test::Unit
bundled in Ruby 1.8.x had not been improved but unbundled
Test::Unit (test-unit) is improved actively.

%package -n %{?scl_prefix}rubygem-xmlrpc
Summary:    XMLRPC is a lightweight protocol that enables remote procedure calls over HTTP
Version:    %{xmlrpc_version}
Group:      Development/Libraries
License:    Ruby or BSD
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(xmlrpc) = %{version}-%{release}
BuildArch:  noarch

%description -n %{?scl_prefix}rubygem-xmlrpc
XMLRPC is a lightweight protocol that enables remote procedure calls over
HTTP.

%prep
%setup -q -n %{ruby_archive}

%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

echo "Correct shebangs and other references to /usr/local/bin/ruby"
find . -type f -print0 | xargs -0 grep -lI '\/usr\/local\/bin\/ruby' | xargs sed -i 's:/usr/local/bin/ruby:/opt/cpanel/ea-ruby27/root/usr/bin/ruby:g' || /bin/true

# Remove bundled libraries to be sure they are not used.
rm -rf ext/psych/yaml
rm -rf ext/fiddle/libffi*

# Provide an example of usage of the tapset:
cp -a %{SOURCE3} .

# Make abrt_prelude.rb available for compilation process. The prelude must be
# available together with Ruby's source due to
# https://github.com/ruby/ruby/blob/trunk/tool/compile_prelude.rb#L26
cp -a %{SOURCE6} .

%build
%if 0%{rhel} > 6
autoconf
%else
scl enable autotools-latest 'autoconf'
%endif

%if 0%{rhel} < 8
export LDFLAGS="-Wl,-rpath=/opt/cpanel/ea-openssl11/lib64 -Wl,-rpath=/opt/cpanel/ea-ruby27/root/usr/lib64"
%else
export LDFLAGS="-Wl,-rpath=/opt/cpanel/ea-ruby27/root/usr/lib64"
%endif

%configure \
        --with-rubylibprefix='%{ruby_libdir}' \
        --with-archlibdir='%{_libdir}' \
        --with-rubyarchprefix='%{ruby_libarchdir}' \
        --with-sitedir='%{ruby_sitelibdir}' \
        --with-sitearchdir='%{ruby_sitearchdir}' \
        --with-vendordir='%{ruby_vendorlibdir}' \
        --with-vendorarchdir='%{ruby_vendorarchdir}' \
        --with-rubyhdrdir='%{_includedir}' \
        --with-rubyarchhdrdir='%{_includedir}' \
        --with-sitearchhdrdir='$(sitehdrdir)/$(arch)' \
        --with-vendorarchhdrdir='$(vendorhdrdir)/$(arch)' \
        --with-ruby-pc='%{pkg_name}.pc' \
        --with-compress-debug-sections=no \
%if 0%{rhel} < 8
        --enable-rpath=/opt/cpanel/ea-openssl11/lib \
%else
        --enable-rpath=/opt/cpanel/ea-ruby27/root/usr/lib64 \
%endif
        --enable-shared \
        --with-ruby-version="ruby-%{ruby_version}" \
        --enable-multiarch \
%if 0%{rhel} < 8
        --with-prelude=./abrt_prelude.rb \
        --with-opt-dir=/opt/cpanel/ea-openssl11
%else
        --with-prelude=./abrt_prelude.rb
%endif

# Q= makes the build output more verbose and allows to check Fedora
# compiler options.
make %{?_smp_mflags} COPY="cp -p" Q=

%install

# for the catch all file lists
%global ruby_usr /opt/cpanel/ea-ruby27/root/usr
%global share_ruby %{ruby_usr}/share/ruby
%global share_gems %{ruby_usr}/share/gems
%global ruby_full ruby-%{ruby_version}

rm -rf %{buildroot}
%{?scl:scl enable %scl - << \EOF
make install DESTDIR=%{buildroot}
EOF}

mkdir -p %{buildroot}%{gem_dir}/specifications

# Rename ruby/config.h to ruby/config-<arch>.h to avoid file conflicts on
# multilib systems and install config.h wrapper
cp -ar %{buildroot}%{_includedir}/%{pkg_name}/config.h %{buildroot}%{_includedir}/%{pkg_name}/config-%{_arch}.h
install -m644 %{SOURCE7} %{buildroot}%{_includedir}/%{pkg_name}/config.h

# Rename the ruby executable. It is replaced by RubyPick.
%{?with_rubypick:mv %{buildroot}%{_bindir}/%{pkg_name}{,-mri}}

# Version is empty if --with-ruby-version is specified.
# http://bugs.ruby-lang.org/issues/7807
sed -i 's/Version: \${ruby_version}/Version: %{ruby_version}/' %{buildroot}%{_libdir}/pkgconfig/%{pkg_name}.pc

# Kill bundled certificates, as they should be part of ca-certificates.
for cert in \
  rubygems.global.ssl.fastly.net/DigiCertHighAssuranceEVRootCA.pem \
  rubygems.org/AddTrustExternalCARoot.pem \
  index.rubygems.org/GlobalSignRootCA.pem
do
    if test -f "%{buildroot}%{rubygems_dir}/ssl_certs/$cert"; then
        rm %{buildroot}%{rubygems_dir}/ssl_certs/$cert
    fi

    if test -f "$(dirname %{buildroot}%{rubygems_dir}/ssl_certs/$cert)"; then
        rm -r $(dirname %{buildroot}%{rubygems_dir}/ssl_certs/$cert)
    fi
done

# Ensure there are no certificates still in the directory
test ! "$(ls -A  %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/ 2>/dev/null)"

# Move macros file into proper place and replace the %%{pkg_name} macro, since it
# would be wrongly evaluated during build of other packages.
mkdir -p %{buildroot}%{_root_sysconfdir}/rpm
install -m 644 %{SOURCE4} %{buildroot}%{_root_sysconfdir}/rpm/macros.ruby%{?scl:.%{scl}}
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_root_sysconfdir}/rpm/macros.ruby%{?scl:.%{scl}}
install -m 644 %{SOURCE5} %{buildroot}%{_root_sysconfdir}/rpm/macros.rubygems%{?scl:.%{scl}}
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_root_sysconfdir}/rpm/macros.rubygems%{?scl:.%{scl}}

# Install custom operating_system.rb.
mkdir -p %{buildroot}%{rubygems_dir}/defaults
sed 's/@SCL@/%{scl}/' %{SOURCE1} > %{buildroot}%{rubygems_dir}/defaults/%{basename:%{SOURCE1}}

# Move gems root into common directory, out of Ruby directory structure.
#mv %{buildroot}%{ruby_libdir}/gems %{buildroot}%{gem_dir}
cp -ar %{buildroot}%{ruby_libdir}/gems %{buildroot}%{gem_dir}

# Create folders for gem binary extensions.
# TODO: These folders should go into rubygem-filesystem but how to achieve it,
# since noarch package cannot provide arch dependent subpackages?
# http://rpm.org/ticket/78
mkdir -p %{buildroot}%{_exec_prefix}/lib{,64}/gems/%{pkg_name}

# Move bundled rubygems to %%gem_dir and %%gem_extdir_mri
# make symlinks in ruby_stdlib for unbundled Gems, so that everything works as expected
# bigdecimal and io-console are not enough for scl

mkdir -p %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_base_version}/lib
mkdir -p %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_base_version}/exe
cp -ar %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/rdoc* %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_base_version}/lib
cp -ar libexec/rdoc %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_base_version}/exe

cp -ar %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/rdoc-%{rdoc_base_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/rdoc-%{rdoc_base_version}/lib/rdoc.rb %{buildroot}%{ruby_libdir}/rdoc.rb
ln -s %{gem_dir}/gems/rdoc-%{rdoc_base_version}/lib/rdoc %{buildroot}%{ruby_libdir}/rdoc

mkdir -p %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_base_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_base_version}
cp -ar %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/bigdecimal %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_base_version}/lib
cp -ar .ext/x86_64-linux/bigdecimal.so %{buildroot}%{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_base_version}
cp -ar ext/bigdecimal/bigdecimal.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_base_version}/lib/bigdecimal %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/bigdecimal
ln -s %{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_base_version}/bigdecimal.so %{buildroot}%{ruby_libarchdir}/bigdecimal.so

mkdir -p %{buildroot}%{gem_dir}/gems/io-console-%{io_console_base_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/io-console-%{io_console_base_version}/io
cp -ar %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/io %{buildroot}%{gem_dir}/gems/io-console-%{io_console_base_version}/lib
cp -ar .ext/x86_64-linux/io/console.so %{buildroot}%{_libdir}/gems/%{pkg_name}/io-console-%{io_console_base_version}/io
cp -ar ext/io/console/io-console.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/io-console-%{io_console_base_version}/lib/io %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/io
mkdir -p %{buildroot}%{ruby_libarchdir}/io
ln -s %{_libdir}/gems/%{pkg_name}/io-console-%{io_console_base_version}/io/console.so %{buildroot}%{ruby_libarchdir}/io/console.so

mkdir -p %{buildroot}%{gem_dir}/gems/json-%{json_base_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/json-%{json_base_version}
cp -ar %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/json* %{buildroot}%{gem_dir}/gems/json-%{json_base_version}/lib
cp -ar ext/json/ %{buildroot}%{_libdir}/gems/%{pkg_name}/json-%{json_base_version}/

cp -ar %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/json-%{json_base_version}.gemspec %{buildroot}%{gem_dir}/specifications
mkdir -p %{buildroot}%{gem_dir}/gems/openssl-%{openssl_base_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/openssl-%{openssl_base_version}
cp -ar %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/openssl* %{buildroot}%{gem_dir}/gems/openssl-%{openssl_base_version}/lib

cp -ar .ext/x86_64-linux/openssl.so %{buildroot}%{_libdir}/gems/%{pkg_name}/openssl-%{openssl_base_version}/
cp -ar %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/openssl-%{openssl_base_version}.gemspec %{buildroot}%{gem_dir}/specifications

# This used to be directory when OpenSSL was integral part of StdLib => Keep
# it as directory and link everything in it to prevent directory => symlink
# conversion RPM issues.

mkdir -p %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/openssl
mkdir -p %{buildroot}%{gem_dir}/gems/psych-%{psych_base_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/psych-%{psych_base_version}
cp -ar %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/psych* %{buildroot}%{gem_dir}/gems/psych-%{psych_base_version}/lib
cp -ar .ext/x86_64-linux/psych.so %{buildroot}%{_libdir}/gems/%{pkg_name}/psych-%{psych_base_version}/

# Adjust the gemspec files so that the gems will load properly
sed -i '/^end$/ i\
  s.extensions = ["json/ext/parser.so", "json/ext/generator.so"]' %{buildroot}%{gem_dir}/specifications/json-%{json_base_version}.gemspec

# Move man pages into proper location
cp -ar %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/gems/rake-%{rake_base_version}/doc/rake.1 %{buildroot}%{_mandir}/man1

# Install a tapset and fix up the path to the library.
mkdir -p %{buildroot}%{tapset_dir}
sed -e "s|@LIBRARY_PATH@|%{tapset_libdir}/libruby.so.%{major_minor_version}|" \
  %{SOURCE2} > %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp
# Escape '*/' in comment.
sed -i -r "s|( \*.*\*)\/(.*)|\1\\\/\2|" %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp

mkdir -p %{buildroot}/%{share_gems}/gems/rake-%{rake_base_version}/exe
cp -a %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/rake-%{rake_base_version}.gemspec %{buildroot}%{gem_dir}/specifications
cp -a %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/rake-%{rake_base_version}.gemspec %{buildroot}%{gem_dir}/specifications
cp -ar gems/rake-%{rake_base_version}/* %{buildroot}/%{share_gems}/gems/rake-%{rake_base_version}

# Prepare -doc subpackage file lists.
find doc -maxdepth 1 -type f ! -name '.*' ! -name '*.ja*' > .ruby-doc.en
echo 'doc/images' >> .ruby-doc.en
echo 'doc/syntax' >> .ruby-doc.en

find doc -maxdepth 1 -type f -name '*.ja*' > .ruby-doc.ja
echo 'doc/irb' >> .ruby-doc.ja
echo 'doc/pty' >> .ruby-doc.ja

sed -i 's/^/%doc /' .ruby-doc.*
sed -i 's/^/%lang(ja) /' .ruby-doc.ja

# other files seen in ruby2.4
mkdir -p %{buildroot}%{ruby_libarchdir_ver}
cp -R spec/ruby/library/mathn %{buildroot}%{ruby_libarchdir_ver}
cp .ext/x86_64-linux/-test-/rational.so %{buildroot}%{ruby_libarchdir_ver}/mathn

# file realignment fixes

%global rubybase opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/ruby-%{ruby_version}
%global gemsbase opt/cpanel/ea-ruby27/root/usr/share/gems
%global gemsdir  %{gemsbase}/gems

%global gemsminitest  %{gemsdir}/minitest-%{minitest_base_version}
%global gemsnettelnet %{gemsdir}/net-telnet-%{net_telnet_base_version}
%global gemspowerassert %{gemsdir}/power_assert-%{power_assert_base_version}
%global gemstestunit %{gemsdir}/test-unit-%{test_unit_base_version}
%global gemsxmlrpc %{gemsdir}/xmlrpc-%{xmlrpc_base_version}

mkdir -p %{buildroot}/%{gemsbase}

mkdir -p %{buildroot}/%{gemsminitest}
mkdir -p %{buildroot}/%{rubybase}/minitest-%{minitest_base_version}

cp -ar gems/minitest-%{minitest_base_version}/* %{buildroot}/%{gemsminitest}
cp -a  gems/minitest-%{minitest_base_version}/minitest.gemspec %{buildroot}/%{gemsbase}/specifications
cp -a  gems/minitest-%{minitest_base_version}/minitest.gemspec %{buildroot}/%{gemsbase}/specifications/minitest-%{minitest_base_version}.gemspec

mkdir -p %{buildroot}/%{gemsnettelnet}
mkdir -p %{buildroot}/%{rubybase}/net-telnet-%{net_telnet_base_version}

cp -ar gems/net-telnet-%{net_telnet_base_version}/* %{buildroot}/%{gemsnettelnet}
cp -a  gems/net-telnet-%{net_telnet_base_version}/net-telnet.gemspec %{buildroot}/%{gemsbase}/specifications
cp -a  gems/net-telnet-%{net_telnet_base_version}/net-telnet.gemspec %{buildroot}/%{gemsbase}/specifications/net-telnet-%{net_telnet_base_version}.gemspec

mkdir -p %{buildroot}/%{gemspowerassert}
mkdir -p %{buildroot}/%{rubybase}/power_assert-%{power_assert_base_version}

cp -ar gems/power_assert-%{power_assert_base_version}/* %{buildroot}/%{gemspowerassert}
cp -a  gems/power_assert-%{power_assert_base_version}/power_assert.gemspec %{buildroot}/%{gemsbase}/specifications
cp -a  gems/power_assert-%{power_assert_base_version}/power_assert.gemspec %{buildroot}/%{gemsbase}/specifications/power_assert-%{power_assert_base_version}.gemspec

mkdir -p %{buildroot}/%{gemstestunit}
mkdir -p %{buildroot}/%{rubybase}/test-unit-%{test_unit_base_version}

cp -ar gems/test-unit-%{test_unit_base_version}/* %{buildroot}/%{gemstestunit}
cp -a  gems/test-unit-%{test_unit_base_version}/test-unit.gemspec %{buildroot}/%{gemsbase}/specifications
cp -a  gems/test-unit-%{test_unit_base_version}/test-unit.gemspec %{buildroot}/%{gemsbase}/specifications/test-unit-%{test_unit_base_version}.gemspec

mkdir -p %{buildroot}/%{gemsxmlrpc}
mkdir -p %{buildroot}/%{rubybase}/xmlrpc-%{xmlrpc_base_version}

cp -ar gems/xmlrpc-%{xmlrpc_base_version}/* %{buildroot}/%{gemsxmlrpc}
cp -a  gems/xmlrpc-%{xmlrpc_base_version}/xmlrpc.gemspec %{buildroot}/%{gemsbase}/specifications
cp -a  gems/xmlrpc-%{xmlrpc_base_version}/xmlrpc.gemspec %{buildroot}/%{gemsbase}/specifications/xmlrpc-%{xmlrpc_base_version}.gemspec

%check
%if %runselftest

# Probably silly to regen each time, but
# its less of a maintenance burden.
pushd ./test/net/fixtures/
make regen_certs
popd

# Ruby software collection tests
%{?scl:scl enable %scl - << \EOF
mkdir -p ./lib/rubygems/defaults
cp %{SOURCE1} ./lib/rubygems/defaults

# TODO: This test does not run, someone with Ruby knowledge will need to update these
# tests. Remove the double percent symbol after uncommenting
make test-all TESTS="%{SOURCE14}" || exit 1

rm -rf ./lib/rubygems/defaults

# TODO: Check Ruby hardening. needed?
#checksec -f libruby.so.%{ruby_version} | \
  #grep "Full RELRO.*Canary found.*NX enabled.*DSO.*No RPATH.*No RUNPATH.*Yes.*\d*.*\d*.*libruby.so.%{ruby_version}"

# Check RubyGems version correctness.
[ "`make runruby TESTRUN_SCRIPT='bin/gem -v' | tail -1`" == '%{rubygems_base_version}' ]
# Check Molinillo version correctness.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\"module Gem; module Resolver; end; end; require 'rubygems/resolver/molinillo/lib/molinillo/gem_metadata'; puts Gem::Resolver::Molinillo::VERSION\\\"\" | tail -1`" \
  == '%{molinillo_base_version}' ]

make runruby TESTRUN_SCRIPT=%{SOURCE13}

DISABLE_TESTS=""

# https://bugs.ruby-lang.org/issues/11480
# Once seen: http://koji.fedoraproject.org/koji/taskinfo?taskID=12556650
DISABLE_TESTS="$DISABLE_TESTS -x test_fork.rb -x test_https.rb -x test_rinda.rb -x clock_getres_spec.rb -x test_fiber.rb"

make check TESTS="-v $DISABLE_TESTS"

# Trying systemtab
make runruby TESTRUN_SCRIPT="--enable-gems %{SOURCE13}"

EOF}
%endif

%post libs

/sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc BSDL
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc GPL
%doc LEGAL
%{_bindir}/erb
%{_bindir}/%{pkg_name}%{?with_rubypick:-mri}
%dir %{_mandir}/man1

%dir %{_exec_prefix}/share/doc

# catch all file lists
/opt/cpanel/ea-ruby27/root/usr/bin/bundle
/opt/cpanel/ea-ruby27/root/usr/bin/bundler
/opt/cpanel/ea-ruby27/root/usr/bin/racc
/opt/cpanel/ea-ruby27/root/usr/bin/racc2y
/opt/cpanel/ea-ruby27/root/usr/bin/y2racc
/opt/cpanel/ea-ruby27/root/usr/lib64/libruby.so.2.7
/opt/cpanel/ea-ruby27/root/usr/lib64/libruby.so.%{ruby_version}
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/enc/cesu_8.so
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/enc/trans/cesu_8.so
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/bignum/exponent_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/complex/Complex_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/fixnum/exponent_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/float/exponent_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/integer/from_prime_division_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/integer/prime_division_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/math/fixtures/classes.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/mathn_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/math/rsqrt_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/math/shared/rsqrt.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/math/shared/sqrt.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/math/sqrt_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/rational/inspect_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/mathn/rational/Rational_spec.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/monitor.so
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/rbconfig/sizeof.so
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/bundler-%{bundler_base_version}/libexec/bundle
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/bundler-%{bundler_base_version}/libexec/bundler
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/racc-%{racc_base_version}/bin/racc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/racc-%{racc_base_version}/bin/racc2y
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/racc-%{racc_base_version}/bin/y2racc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/benchmark-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/bundler-%{bundler_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/cgi-0.1.0.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/csv-3.1.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/date-3.0.3.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/dbm-1.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/delegate-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/etc-1.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/fcntl-1.0.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/fiddle-1.0.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/fileutils-1.4.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/forwardable-1.3.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/gdbm-2.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/getoptlong-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/ipaddr-1.2.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/logger-1.4.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/matrix-%{net_telnet_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/mutex_m-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/net-pop-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/net-smtp-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/observer-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/open3-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/ostruct-%{net_telnet_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/prime-0.1.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/pstore-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/racc-%{racc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/readline-0.0.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/readline-ext-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/reline-0.1.5.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/rexml-%{rexml_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/rss-0.2.8.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/sdbm-1.0.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/singleton-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/stringio-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/strscan-1.0.3.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/timeout-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/tracer-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/uri-0.10.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/webrick-%{webrick_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/yaml-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/zlib-1.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/bundler-%{bundler_base_version}/libexec/bundle
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/bundler-%{bundler_base_version}/libexec/bundler
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/racc-%{racc_base_version}/bin/racc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/racc-%{racc_base_version}/bin/racc2y
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/racc-%{racc_base_version}/bin/y2racc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/benchmark-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/bundler-%{bundler_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/cgi-0.1.0.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/csv-3.1.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/date-3.0.3.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/dbm-1.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/delegate-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/etc-1.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/fcntl-1.0.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/fiddle-1.0.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/fileutils-1.4.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/forwardable-1.3.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/gdbm-2.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/getoptlong-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/ipaddr-1.2.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/logger-1.4.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/matrix-%{net_telnet_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/mutex_m-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/net-pop-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/net-smtp-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/observer-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/open3-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/ostruct-%{net_telnet_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/prime-0.1.1.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/pstore-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/psych-%{psych_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/racc-%{racc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/rdoc-%{rdoc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/readline-0.0.2.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/readline-ext-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/reline-0.1.5.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/rexml-%{rexml_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/rss-0.2.8.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/sdbm-1.0.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/singleton-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/stringio-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/strscan-1.0.3.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/timeout-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/tracer-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/uri-0.10.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/webrick-%{webrick_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/yaml-0.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/zlib-1.1.0.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/abbrev.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/base64.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/benchmark.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/benchmark/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/build_metadata.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/capistrano.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/add.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/binstubs.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/cache.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/check.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/clean.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/common.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/config.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/console.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/doctor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/exec.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/gem.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/info.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/init.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/inject.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/install.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/issue.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/list.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/lock.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/open.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/outdated.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/package.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/platform.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/plugin.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/pristine.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/remove.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/show.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/update.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/cli/viz.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/compact_index_client/cache.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/compact_index_client.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/compact_index_client/updater.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/constants.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/current_ruby.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/definition.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/dependency.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/deployment.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/dep_proxy.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/deprecate.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/dsl.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/endpoint_specification.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/environment_preserver.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/env.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/errors.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/feature_flag.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/fetcher/base.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/fetcher/compact_index.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/fetcher/dependency.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/fetcher/downloader.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/fetcher/index.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/fetcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/friendly_errors.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/gemdeps.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/gem_helper.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/gem_helpers.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/gem_remote_fetcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/gem_tasks.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/gem_version_promoter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/graph.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/index.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/injector.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/inline.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/installer/gem_installer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/installer/parallel_installer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/installer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/installer/standalone.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/lazy_specification.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/lockfile_generator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/lockfile_parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/match_platform.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/mirror.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/api.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/api/source.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/dsl.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/events.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/index.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/installer/git.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/installer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/installer/rubygems.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/plugin/source_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/process_lock.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/psyched_yaml.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/remote_specification.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/resolver.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/resolver/spec_group.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/retry.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/ruby_dsl.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/rubygems_ext.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/rubygems_gem_installer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/rubygems_integration.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/ruby_version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/runtime.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/settings.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/settings/validator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/setup.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/shared_helpers.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/similarity_detector.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/gemspec.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/git/git_proxy.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/git.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/metadata.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/path/installer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/path.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/rubygems.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/source/rubygems/remote.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/spec_set.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/stub_specification.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/Executable
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/Executable.bundler
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/Executable.standalone
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/gems.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/bin/console.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/bin/setup.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/CODE_OF_CONDUCT.md.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/exe/newgem.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/ext/newgem/extconf.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/ext/newgem/newgem.c.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/ext/newgem/newgem.h.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/Gemfile.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/gitignore.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/lib/newgem.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/lib/newgem/version.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/LICENSE.txt.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/newgem.gemspec.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/Rakefile.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/README.md.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/rspec.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/spec/newgem_spec.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/spec/spec_helper.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/test/newgem_test.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/test/test_helper.rb.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/templates/newgem/travis.yml.tt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/ui.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/ui/rg_proxy.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/ui/shell.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/ui/silent.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/uri_credentials_filter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/connection_pool/lib/connection_pool/monotonic_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/connection_pool/lib/connection_pool.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/connection_pool/lib/connection_pool/timed_stack.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/connection_pool/lib/connection_pool/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendored_fileutils.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendored_molinillo.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendored_persistent.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendored_thor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendored_uri.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/fileutils/lib/fileutils.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/fileutils/lib/fileutils/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/compatibility.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/delegates/resolution_state.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/delegates/specification_provider.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/action.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/add_edge_no_circular.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/add_vertex.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/delete_edge.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/detach_vertex_named.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/log.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/set_payload.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/tag.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/dependency_graph/vertex.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/errors.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/gem_metadata.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/modules/specification_provider.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/modules/ui.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/resolution.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/resolver.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/molinillo/lib/molinillo/state.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/net-http-persistent/lib/net/http/persistent/connection.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/net-http-persistent/lib/net/http/persistent/pool.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/net-http-persistent/lib/net/http/persistent.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/net-http-persistent/lib/net/http/persistent/timed_stack_multi.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions/create_file.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions/create_link.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions/directory.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions/empty_directory.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions/file_manipulation.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions/inject_into_file.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/actions.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/base.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/command.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/core_ext/hash_with_indifferent_access.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/core_ext/io_binary_read.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/core_ext/ordered_hash.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/error.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/group.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/invocation.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/line_editor/basic.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/line_editor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/line_editor/readline.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/nested_context.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/parser/argument.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/parser/arguments.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/parser/option.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/parser/options.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/rake_compat.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/runner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/shell.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/util.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/thor/lib/thor/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/common.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/file.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/ftp.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/generic.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/http.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/https.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/ldap.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/ldaps.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/mailto.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/rfc2396_parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/rfc3986_parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vendor/uri/lib/uri/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/version_ranges.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/vlad.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/worker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bundler/yaml_serializer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/cgi.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/coverage.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/core_ext/array.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/core_ext/string.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/delete_suffix.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/fields_converter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/match_p.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/row.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/table.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/csv/writer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/date.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/debug.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/delegate.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/delegate/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/digest.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/drb.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/English.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/erb.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/expect.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/fiddle.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/fileutils.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/find.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/forwardable.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/getoptlong.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/getoptlong/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/ipaddr.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/kconv.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger/errors.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger/formatter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger/log_device.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger/period.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger/severity.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/logger/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/matrix.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/mkmf.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/monitor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/mutex_m.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/observer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/observer/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/open3.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/open3/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/open-uri.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/optionparser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/optparse.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/ostruct.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/ostruct/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/pathname.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/pp.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/prettyprint.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/prime.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/pstore.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/pstore/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/racc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/readline.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/ansi.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/config.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/general_io.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/history.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/key_actor/base.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/key_actor/emacs.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/key_actor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/key_actor/vi_command.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/key_actor/vi_insert.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/key_stroke.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/kill_ring.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/line_editor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/unicode/east_asian_width.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/unicode.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/reline/windows.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/resolv.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/resolv-replace.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/ripper.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rss.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rubygems.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/securerandom.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/set.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/shellwords.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/singleton.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/singleton/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/socket.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/tempfile.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/timeout.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/timeout/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/time.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/tmpdir.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/tracer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/tracer/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/tsort.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/un.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/uri.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/weakref.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/webrick.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/yaml.rb

%dir %{_exec_prefix}/share/ruby/
%dir %{gem_dir}/gems/

%files devel
%doc BSDL
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc GPL
%doc LEGAL
/opt/cpanel/ea-ruby27/root/usr/include/rb_mjit_min_header-%{ruby_version}.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/assert.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward/classext.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward/cxxanyargs.hpp
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward/rubyio.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward/rubysig.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward/st.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/backward/util.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/config.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/config-x86_64.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/debug.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/defines.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/digest.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/encoding.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/intern.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/io.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/missing.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/onigmo.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/oniguruma.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/regex.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/re.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/ruby.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/st.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/subst.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/thread.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/thread_native.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/util.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/version.h
/opt/cpanel/ea-ruby27/root/usr/include/ruby/vm.h

%config(noreplace) %{_root_sysconfdir}/rpm/macros.ruby%{?scl:.%{scl}}

%{_libdir}/libruby.so
%{_libdir}/pkgconfig/%{pkg_name}.pc

%files libs
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc GPL
%doc LEGAL
%doc README.md
%doc NEWS
# Exclude /usr/local directory since it is supposed to be managed by
# local system administrator.
%exclude %{ruby_sitelibdir}
%exclude %{ruby_sitearchdir}
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorarchdir}

# List all these files explicitly to prevent surprises
# Platform independent libraries.
%dir %{ruby_libdir_ver}
%exclude %{ruby_libdir_ver}/irb.rb
%exclude %{ruby_libdir_ver}/psych.rb
%{ruby_libdir_ver}/cgi
%{ruby_libdir_ver}/digest
%{ruby_libdir_ver}/drb
%{ruby_libdir_ver}/fiddle
%{ruby_libdir_ver}/forwardable
%exclude %{ruby_libdir_ver}/irb
%{ruby_libdir_ver}/matrix
%{ruby_libdir_ver}/net
%{ruby_libdir_ver}/openssl
%{ruby_libdir_ver}/optparse
%{ruby_libdir_ver}/racc
%{ruby_libdir_ver}/rexml
%{ruby_libdir_ver}/rinda
%{ruby_libdir_ver}/ripper
%{ruby_libdir_ver}/rss
%{ruby_libdir_ver}/bundler/vendor/thor/lib/thor/shell
%{ruby_libdir_ver}/syslog
%{ruby_libdir_ver}/unicode_normalize
%{ruby_libdir_ver}/uri
%{ruby_libdir_ver}/webrick
%{ruby_libdir_ver}/yaml

# Platform specific libraries.

%dir %{ruby_libarchdir_ver}
%dir %{ruby_libarchdir_ver}/cgi
%{ruby_libarchdir_ver}/cgi/escape.so
%{ruby_libarchdir_ver}/continuation.so
%{ruby_libarchdir_ver}/coverage.so
%{ruby_libarchdir_ver}/date_core.so
%{ruby_libarchdir_ver}/dbm.so
%dir %{ruby_libarchdir_ver}/digest
%{ruby_libarchdir_ver}/digest.so
%{ruby_libarchdir_ver}/digest/bubblebabble.so
%{ruby_libarchdir_ver}/digest/md5.so
%{ruby_libarchdir_ver}/digest/rmd160.so
%{ruby_libarchdir_ver}/digest/sha1.so
%{ruby_libarchdir_ver}/digest/sha2.so
%dir %{ruby_libarchdir_ver}/enc
%{ruby_libarchdir_ver}/enc/big5.so
%{ruby_libarchdir_ver}/enc/cp949.so
%{ruby_libarchdir_ver}/enc/emacs_mule.so
%{ruby_libarchdir_ver}/enc/encdb.so
%{ruby_libarchdir_ver}/enc/euc_jp.so
%{ruby_libarchdir_ver}/enc/euc_kr.so
%{ruby_libarchdir_ver}/enc/euc_tw.so
%{ruby_libarchdir_ver}/enc/gb18030.so
%{ruby_libarchdir_ver}/enc/gb2312.so
%{ruby_libarchdir_ver}/enc/gbk.so
%{ruby_libarchdir_ver}/enc/iso_8859_1.so
%{ruby_libarchdir_ver}/enc/iso_8859_10.so
%{ruby_libarchdir_ver}/enc/iso_8859_11.so
%{ruby_libarchdir_ver}/enc/iso_8859_13.so
%{ruby_libarchdir_ver}/enc/iso_8859_14.so
%{ruby_libarchdir_ver}/enc/iso_8859_15.so
%{ruby_libarchdir_ver}/enc/iso_8859_16.so
%{ruby_libarchdir_ver}/enc/iso_8859_2.so
%{ruby_libarchdir_ver}/enc/iso_8859_3.so
%{ruby_libarchdir_ver}/enc/iso_8859_4.so
%{ruby_libarchdir_ver}/enc/iso_8859_5.so
%{ruby_libarchdir_ver}/enc/iso_8859_6.so
%{ruby_libarchdir_ver}/enc/iso_8859_7.so
%{ruby_libarchdir_ver}/enc/iso_8859_8.so
%{ruby_libarchdir_ver}/enc/iso_8859_9.so
%{ruby_libarchdir_ver}/enc/koi8_r.so
%{ruby_libarchdir_ver}/enc/koi8_u.so
%{ruby_libarchdir_ver}/enc/shift_jis.so
%dir %{ruby_libarchdir_ver}/enc/trans
%{ruby_libarchdir_ver}/enc/trans/big5.so
%{ruby_libarchdir_ver}/enc/trans/chinese.so
%{ruby_libarchdir_ver}/enc/trans/ebcdic.so
%{ruby_libarchdir_ver}/enc/trans/emoji.so
%{ruby_libarchdir_ver}/enc/trans/emoji_iso2022_kddi.so
%{ruby_libarchdir_ver}/enc/trans/emoji_sjis_docomo.so
%{ruby_libarchdir_ver}/enc/trans/emoji_sjis_kddi.so
%{ruby_libarchdir_ver}/enc/trans/emoji_sjis_softbank.so
%{ruby_libarchdir_ver}/enc/trans/escape.so
%{ruby_libarchdir_ver}/enc/trans/gb18030.so
%{ruby_libarchdir_ver}/enc/trans/gbk.so
%{ruby_libarchdir_ver}/enc/trans/iso2022.so
%{ruby_libarchdir_ver}/enc/trans/japanese.so
%{ruby_libarchdir_ver}/enc/trans/japanese_euc.so
%{ruby_libarchdir_ver}/enc/trans/japanese_sjis.so
%{ruby_libarchdir_ver}/enc/trans/korean.so
%{ruby_libarchdir_ver}/enc/trans/single_byte.so
%{ruby_libarchdir_ver}/enc/trans/transdb.so
%{ruby_libarchdir_ver}/enc/trans/utf8_mac.so
%{ruby_libarchdir_ver}/enc/trans/utf_16_32.so
%{ruby_libarchdir_ver}/enc/utf_16be.so
%{ruby_libarchdir_ver}/enc/utf_16le.so
%{ruby_libarchdir_ver}/enc/utf_32be.so
%{ruby_libarchdir_ver}/enc/utf_32le.so
%{ruby_libarchdir_ver}/enc/windows_1250.so
%{ruby_libarchdir_ver}/enc/windows_1251.so
%{ruby_libarchdir_ver}/enc/windows_1252.so
%{ruby_libarchdir_ver}/enc/windows_1253.so
%{ruby_libarchdir_ver}/enc/windows_1254.so
%{ruby_libarchdir_ver}/enc/windows_1257.so
%{ruby_libarchdir_ver}/enc/windows_31j.so
%{ruby_libarchdir_ver}/etc.so
%{ruby_libarchdir_ver}/fcntl.so
%{ruby_libarchdir_ver}/fiber.so
%{ruby_libarchdir_ver}/fiddle.so
%{ruby_libarchdir_ver}/gdbm.so
%dir %{ruby_libarchdir_ver}/io
%{ruby_libarchdir_ver}/io/nonblock.so
%{ruby_libarchdir_ver}/io/wait.so
%dir %{ruby_libarchdir_ver}/mathn
# apparently complex.so is already in ruby so is not a separate .so
%{ruby_libarchdir_ver}/mathn/rational.so
%{ruby_libarchdir_ver}/nkf.so
%{ruby_libarchdir_ver}/objspace.so
%{ruby_libarchdir_ver}/pathname.so
%{ruby_libarchdir_ver}/pty.so
%dir %{ruby_libarchdir_ver}/racc
%{ruby_libarchdir_ver}/racc/cparse.so
%dir %{ruby_libarchdir_ver}/rbconfig
%{ruby_libarchdir_ver}/rbconfig.rb
%{ruby_libarchdir_ver}/readline.so
%{ruby_libarchdir_ver}/ripper.so
%{ruby_libarchdir_ver}/sdbm.so
%{ruby_libarchdir_ver}/socket.so
%{ruby_libarchdir_ver}/stringio.so
%{ruby_libarchdir_ver}/strscan.so
%{ruby_libarchdir_ver}/syslog.so
%{ruby_libarchdir_ver}/zlib.so

%{tapset_root}

%files -n %{?scl_prefix}rubygems
%{_bindir}/gem
%{rubygems_dir}

# Explicitly include only RubyGems directory strucure to avoid accidentally
# packaged content.
%dir %{gem_dir}
%dir %{gem_dir}/gems/ruby-%{ruby_version}
%dir %{gem_dir}/gems/ruby-%{ruby_version}/gems

%exclude %{gem_dir}/gems/ruby-%{ruby_version}/cache/*

%files -n %{?scl_prefix}rubygems-devel
%config(noreplace) %{_root_sysconfdir}/rpm/macros.rubygems%{?scl:.%{scl}}

%files -n %{?scl_prefix}rubygem-rake
%{_bindir}/rake
%dir %{gem_dir2}/gems/rake-%{rake_base_version}
%{gem_dir2}/specifications/rake-%{rake_base_version}.gemspec
%{share_ruby}/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/a.c
%{share_ruby}/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/b.c
%{share_ruby}/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/main.c
%{share_ruby}/gems/%{ruby_full}/gems/rake-%{rake_base_version}/exe/rake
%{share_ruby}/gems/%{ruby_full}/gems/rake-%{rake_base_version}/rake.gemspec
/%{share_gems}/gems/rake-%{rake_base_version}/doc/example/a.c
/%{share_gems}/gems/rake-%{rake_base_version}/doc/example/b.c
/%{share_gems}/gems/rake-%{rake_base_version}/doc/example/main.c
/%{share_gems}/gems/rake-%{rake_base_version}/exe/rake
/%{share_gems}/gems/rake-%{rake_base_version}/rake.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/bin/bundle
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/bin/rake
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/bin/rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/bin/rubocop
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/CONTRIBUTING.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/command_line_usage.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/example/Rakefile1
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/example/Rakefile2
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/glossary.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/jamis.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/proto_rake.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/rake.1
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/rakefile.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/doc/rational.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/exts.mk
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/History.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/application.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/backtrace.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/clean.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/cloneable.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/cpu_counter.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/default_loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/dsl_definition.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/early_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/ext/core.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/ext/string.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/file_creation_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/file_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/file_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/file_utils_ext.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/file_utils.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/invocation_chain.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/invocation_exception_mixin.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/late_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/linked_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/loaders/makefile.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/multi_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/name_space.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/packagetask.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/phony.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/private_reader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/promise.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/pseudo_status.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/rake_module.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/rake_test_loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/rule_recursion_overflow_error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/scope.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/task_argument_error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/task_arguments.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/tasklib.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/task_manager.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/testtask.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/thread_history_display.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/thread_pool.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/trace_output.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/lib/rake/win32.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/MIT-LICENSE
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/rake-%{rake_base_version}/README.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/bundle
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/rake
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/rubocop
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/CONTRIBUTING.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/command_line_usage.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/a.c
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/b.c
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/main.c
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/Rakefile1
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/Rakefile2
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/glossary.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/jamis.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/proto_rake.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/rake.1
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/rakefile.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/rational.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/exe/rake
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/macos.yml
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/ubuntu-rvm.yml
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/ubuntu.yml
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/windows.yml
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/History.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/application.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/backtrace.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/clean.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/cloneable.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/cpu_counter.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/default_loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/dsl_definition.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/early_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/ext/core.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/ext/string.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_creation_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_utils_ext.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_utils.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/invocation_chain.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/invocation_exception_mixin.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/late_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/linked_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/loaders/makefile.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/multi_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/name_space.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/packagetask.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/phony.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/private_reader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/promise.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/pseudo_status.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/rake_module.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/rake_test_loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/rule_recursion_overflow_error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/scope.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task_argument_error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task_arguments.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/tasklib.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task_manager.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/testtask.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/thread_history_display.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/thread_pool.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/trace_output.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/win32.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/MIT-LICENSE
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/rake.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rake-%{rake_base_version}/README.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/rake-%{rake_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/cache/rake-%{rake_base_version}.gem
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/bundle
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/rake
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/rubocop
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/CONTRIBUTING.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/command_line_usage.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/Rakefile1
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/example/Rakefile2
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/glossary.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/jamis.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/proto_rake.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/rake.1
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/rakefile.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/doc/rational.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/macos.yml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/ubuntu-rvm.yml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/ubuntu.yml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/.github/workflows/windows.yml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/History.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/application.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/backtrace.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/clean.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/cloneable.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/cpu_counter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/default_loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/dsl_definition.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/early_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/ext/core.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/ext/string.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_creation_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_utils_ext.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/file_utils.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/invocation_chain.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/invocation_exception_mixin.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/late_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/linked_list.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/loaders/makefile.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/multi_task.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/name_space.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/packagetask.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/phony.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/private_reader.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/promise.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/pseudo_status.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/rake_module.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/rake_test_loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/rule_recursion_overflow_error.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/scope.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task_argument_error.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task_arguments.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/tasklib.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task_manager.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/task.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/testtask.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/thread_history_display.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/thread_pool.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/trace_output.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/lib/rake/win32.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/MIT-LICENSE
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rake-%{rake_base_version}/README.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/rake-%{rake_base_version}.gemspec

%files irb
%{_bindir}/irb
%{ruby_libdir_ver}/irb.rb
%{ruby_libdir_ver}/irb
%{share_ruby}/gems/%{ruby_full}/gems/irb-*/exe/irb
%{ruby_usr}/share/gems/gems/%{ruby_full}/gems/irb-*/exe/irb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/irb-%{irb_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/irb-%{irb_base_version}.gemspec

%files -n %{?scl_prefix}rubygem-rdoc
#%{gem_dir}/gems/rdoc-%{rdoc_base_version}/exe
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_dir}/gems/rdoc-%{rdoc_base_version}
%{gem_dir}/specifications/rdoc-%{rdoc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rdoc-%{rdoc_base_version}/exe/rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/rdoc-%{rdoc_base_version}/exe/ri
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/rdoc-%{rdoc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/rdoc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/alias.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/anon_class.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/any_method.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/attr.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/class_module.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/code_object.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/code_objects.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/comment.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/constant.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/context.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/context/section.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/cross_reference.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/encoding.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/erbio.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/erb_partial.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/extend.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/darkfish.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/json_index.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/markup.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/pot/message_extractor.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/pot/po_entry.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/pot/po.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/pot.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/ri.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/class.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/css/fonts.css
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/css/rdoc.css
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/fonts/Lato-LightItalic.ttf
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/fonts/Lato-Light.ttf
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/fonts/Lato-RegularItalic.ttf
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/fonts/Lato-Regular.ttf
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/fonts/SourceCodePro-Bold.ttf
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/fonts/SourceCodePro-Regular.ttf
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_footer.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_head.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/add.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/arrow_up.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/brick_link.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/brick.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/bug.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/bullet_black.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/bullet_toggle_minus.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/bullet_toggle_plus.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/date.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/delete.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/find.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/loadingAnimation.gif
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/macFFBgHack.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/package.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/page_green.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/page_white_text.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/page_white_width.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/plugin.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/ruby.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/tag_blue.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/tag_green.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/transparent.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/wrench_orange.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/wrench.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/images/zoom.png
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/index.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/js/darkfish.js
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/js/search.js
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/page.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/servlet_not_found.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/servlet_root.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_classes.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_extends.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_includes.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_in_files.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_installed.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_methods.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_navigation.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_pages.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_parent.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_search.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_sections.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_table_of_contents.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/_sidebar_VCS_info.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/darkfish/table_of_contents.rhtml
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/json_index/js/navigation.js
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/generator/template/json_index/js/searcher.js
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ghost_method.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/i18n/locale.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/i18n.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/i18n/text.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/include.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/known_classes.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markdown/entities.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markdown/literals.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markdown.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/attr_changer.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/attribute_manager.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/attributes.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/attr_span.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/blank_line.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/block_quote.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/document.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/formatter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/hard_break.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/heading.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/include.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/indented_paragraph.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/list_item.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/list.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/paragraph.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/pre_process.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/raw.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/regexp_handling.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/rule.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_ansi.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_bs.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_html_crossref.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_html.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_html_snippet.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_joined_paragraph.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_label.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_markdown.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_rdoc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_table_of_contents.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_test.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/to_tt_only.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/markup/verbatim.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/meta_method.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/method_attr.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/mixin.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/normal_class.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/normal_module.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/options.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/changelog.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/c.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/markdown.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/rd.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/ripper_state_lex.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/ruby.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/ruby_tools.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/simple.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/parser/text.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/rd/block_parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/rd/inline_parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/rd/inline.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/rdoc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/rd.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/require.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ri/driver.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ri/formatter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ri/paths.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ri.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ri/store.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/ri/task.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/rubygems_hook.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/servlet.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/single_class.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/stats/normal.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/stats/quiet.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/stats.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/stats/verbose.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/store.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/task.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/text.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/token_stream.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/tom_doc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/top_level.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/rdoc/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rdoc-%{rdoc_base_version}/exe/rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/rdoc-%{rdoc_base_version}/exe/ri

%files doc -f .ruby-doc.en -f .ruby-doc.ja
%doc README.md
%doc ChangeLog
%doc ruby-exercise.stp
%{_datadir}/ri
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-add.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-binstubs.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-cache.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-check.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-clean.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-config.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-doctor.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-exec.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-gem.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-info.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-init.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-inject.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-install.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-list.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-lock.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-open.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-outdated.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-package.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-platform.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-pristine.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-remove.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-show.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-update.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/bundle-viz.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/erb.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/irb.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/rake.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/ri.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man1/ruby.1.gz
/opt/cpanel/ea-ruby27/root/usr/share/man/man5/gemfile.5.gz

%files -n %{?scl_prefix}rubygem-bigdecimal
%{ruby_libdir_ver}/bigdecimal
%{ruby_libarchdir_ver}/bigdecimal.so
%{ruby_usr}/lib64/ruby/bigdecimal.so
%{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_base_version}
%{gem_dir}/gems/bigdecimal-%{bigdecimal_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/bigdecimal-%{bigdecimal_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/bigdecimal-%{bigdecimal_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/bigdecimal.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/bigdecimal.rb

%files -n %{?scl_prefix}rubygem-did_you_mean
%{gem_dir}/gems/ruby-%{ruby_version}/gems/did_you_mean-%{did_you_mean_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/did_you_mean-%{did_you_mean_base_version}.gemspec
%{ruby_usr}/share/ruby/%{ruby_full}/did_you_mean/core_ext/name_error.rb
%{ruby_usr}/share/ruby/%{ruby_full}/did_you_mean/experimental.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/did_you_mean-%{did_you_mean_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/experimental/initializer_name_correction.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/experimental/ivar_name_correction.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/formatters/plain_formatter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/formatters/verbose_formatter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/jaro_winkler.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/levenshtein.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checkers/key_error_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checkers/method_name_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checkers/name_error_checkers/class_name_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checkers/name_error_checkers.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checkers/name_error_checkers/variable_name_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/spell_checkers/null_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/tree_spell_checker.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/verbose.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/did_you_mean/version.rb

%files -n %{?scl_prefix}rubygem-io-console
%{ruby_libdir_ver}/io
%{ruby_libarchdir}/io/console.so
%{_libdir}/gems/%{pkg_name}/io-console-%{io_console_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}/gems/io-console-%{io_console_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/io-console-%{io_console_base_version}.gemspec
%{ruby_usr}/lib64/ruby/%{ruby_full}/io/console.so
%{ruby_usr}/share/gems/gems/io-console-*/lib/io/console/size.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/io-console-%{io_console_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/io-console.gemspec

%files -n %{?scl_prefix}rubygem-json
%dir %{ruby_libarchdir_ver}/json
%dir %{_libdir}/gems/%{pkg_name}/json-%{json_base_version}
%dir %{gem_dir}/gems/ruby-%{ruby_version}/gems/json-%{json_base_version}
%{gem_dir}/specifications/json-%{json_base_version}.gemspec
%{ruby_usr}/lib64/gems/ruby/json-*/json/fbuffer/fbuffer.h
%{ruby_usr}/share/gems/gems/json-*/lib/json.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/depend
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/extconf.h
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/extconf.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/exts.mk
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/depend
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/extconf.h
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/extconf.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/generator.c
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/generator.h
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/generator.o
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/Makefile
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/generator/mkmf.log
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/json.gemspec
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/bigdecimal.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/complex.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/core.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/date.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/date_time.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/exception.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/ostruct.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/range.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/rational.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/regexp.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/set.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/struct.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/symbol.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/add/time.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/common.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/ext.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/generic_object.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/lib/json/version.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/Makefile
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/mkmf.log
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/depend
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/extconf.h
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/extconf.rb
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/Makefile
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/mkmf.log
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/parser.c
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/parser.h
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/parser.o
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/parser.rl
/opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/json-%{json_base_version}/json/parser/prereq.mk
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/bigdecimal.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/complex.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/core.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/date.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/date_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/exception.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/ostruct.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/range.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/rational.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/regexp.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/set.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/struct.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/symbol.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/add/time.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/common.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/ext.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/generic_object.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/json-%{json_base_version}/lib/json/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/json-%{json_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/json-%{json_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/json/ext/generator.so
/opt/cpanel/ea-ruby27/root/usr/lib64/ruby/%{ruby_full}/json/ext/parser.so
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/bigdecimal.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/complex.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/core.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/date.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/date_time.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/exception.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/ostruct.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/range.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/rational.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/regexp.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/set.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/struct.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/symbol.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/add/time.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/common.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/ext.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/generic_object.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/%{ruby_full}/json/version.rb

%files -n %{?scl_prefix}rubygem-minitest
%{gem_dir}/gems/ruby-%{ruby_version}/gems/minitest-%{minitest_base_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/minitest-%{minitest_base_version}/*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/minitest-%{minitest_base_version}.gemspec
%{share_ruby}/gems/%{ruby_full}/gems/minitest-*/.autotest
%{share_ruby}/gems/%{ruby_full}/gems/minitest-*/lib/hoe/minitest.rb
%{share_ruby}/gems/%{ruby_full}/gems/minitest-*/lib/minitest.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/cache/minitest-%{minitest_base_version}.gem
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/design_rationale.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/History.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/assertions.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/autorun.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/benchmark.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/expectations.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/hell.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/mock.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/parallel.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/pride_plugin.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/pride.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/spec.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/test.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/lib/minitest/unit.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/Manifest.txt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/README.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/metametameta.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/test_minitest_assertions.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/test_minitest_benchmark.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/test_minitest_mock.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/test_minitest_reporter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/test_minitest_spec.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/minitest-%{minitest_base_version}/test/minitest/test_minitest_test.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/minitest-%{minitest_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/minitest-%{minitest_base_version}
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/minitest-%{minitest_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/minitest.gemspec

%files -n %{?scl_prefix}rubygem-openssl
%{ruby_libdir_ver}/openssl
%{ruby_libdir_ver}/openssl.rb
%{ruby_libarchdir_ver}/openssl.so
%{_libdir}/gems/%{pkg_name}/openssl-%{openssl_base_version}
%{gem_dir}/gems/openssl-%{openssl_base_version}
%{gem_dir}/specifications/openssl-%{openssl_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/specifications/default/openssl-%{openssl_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/default/openssl-%{openssl_base_version}.gemspec

%files -n %{?scl_prefix}rubygem-power_assert
%{gem_dir}/gems/ruby-%{ruby_version}/gems/power_assert-%{power_assert_base_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/power_assert-%{power_assert_base_version}/.*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/power_assert-%{power_assert_base_version}.gemspec
%{share_ruby}/gems/%{ruby_full}/gems/power_assert-*/.gitignore
%{share_ruby}/gems/%{ruby_full}/gems/power_assert-*/.travis.yml
%{share_ruby}/gems/%{ruby_full}/gems/power_assert-*/bin/console
%{share_ruby}/gems/%{ruby_full}/gems/power_assert-*/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/cache/power_assert-%{power_assert_base_version}.gem
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/BSDL
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/COPYING
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/LEGAL
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/colorize.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/configuration.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/context.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/enable_tracepoint_events.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/inspector.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/lib/power_assert/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/power_assert.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/power_assert-%{power_assert_base_version}/README.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/power_assert-%{power_assert_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/power_assert-%{power_assert_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/power_assert.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/BSDL
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/COPYING
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/LEGAL
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/README.rdoc
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/exts.mk
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/colorize.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/configuration.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/context.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/enable_tracepoint_events.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/inspector.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/lib/power_assert/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/power_assert-%{power_assert_base_version}/power_assert.gemspec

%files -n %{?scl_prefix}rubygem-psych
%{ruby_libdir_ver}/psych
%{ruby_libdir_ver}/psych.rb
%{ruby_libarchdir_ver}/psych.so
%{_libdir}/gems/%{pkg_name}/psych-%{psych_base_version}
%{gem_dir}/gems/psych-%{psych_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/psych-%{psych_base_version}.gemspec

%files -n %{?scl_prefix}rubygem-net-telnet
%{gem_dir}/gems/ruby-%{ruby_version}/gems/net-telnet-%{net_telnet_base_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/net-telnet-%{net_telnet_base_version}/.*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/net-telnet-%{net_telnet_base_version}.gemspec
%{share_ruby}/gems/%{ruby_full}/gems/net-telnet-*/.gitignore
%{share_ruby}/gems/%{ruby_full}/gems/net-telnet-*/.travis.yml
%{share_ruby}/gems/%{ruby_full}/gems/net-telnet-*/lib/net-telnet.rb
%{share_ruby}/gems/%{ruby_full}/gems/net-telnet-*/lib/net/telnet.rb
%{share_ruby}/gems/%{ruby_full}/gems/net-telnet-*/lib/net/telnet/version.rb
%{share_ruby}/gems/%{ruby_full}/gems/net-telnet-*/net-telnet.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/cache/net-telnet-%{net_telnet_base_version}.gem
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/net-telnet-%{net_telnet_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/net-telnet-%{net_telnet_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/net-telnet-%{net_telnet_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/net-telnet-%{net_telnet_base_version}/LICENSE.txt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/net-telnet-%{net_telnet_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/net-telnet-%{net_telnet_base_version}/README.md
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/net-telnet-%{net_telnet_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/LICENSE.txt
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/README.md
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/exts.mk
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/lib/net-telnet.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/lib/net/telnet.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/lib/net/telnet/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/net-telnet.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/net-telnet-%{net_telnet_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/net-telnet.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/net-telnet-%{net_telnet_base_version}/Gemfile

%files -n %{?scl_prefix}rubygem-test-unit
%{gem_dir}/gems/ruby-%{ruby_version}/gems/test-unit-%{test_unit_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}//specifications/test-unit-%{test_unit_base_version}.gemspec
%{share_ruby}/gems/%{ruby_full}/gems/test-unit-*/lib/test/unit/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/cache/test-unit-%{test_unit_base_version}.gem
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/COPYING
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/doc/text/getting-started.md
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/doc/text/how-to.md
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/doc/text/news.md
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/GPL
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/LGPL
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/assertion-failed-error.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/assertions.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/attribute-matcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/attribute.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/auto-runner-loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/autorunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/code-snippet-fetcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/descendant.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/dir.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/load.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/objectspace.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/xml.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/color.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/color-scheme.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/data.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/data-sets.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/diff.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/error.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/exception-handler.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/failure.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/fault-location-detector.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/fixture.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/notification.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/omission.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/pending.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/priority.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test-unit.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/runner/console.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/runner/emacs.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/runner/xml.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/testcase.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/testresult.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/test-suite-creator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/testsuite.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/console/outputlevel.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/console/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/emacs/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/testrunnermediator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/testrunnerutilities.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/xml/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/backtracefilter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/method-owner-finder.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/observable.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/output.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/procwrapper.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/PSFL
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/README.md
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/sample/adder.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/sample/subtracter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/sample/test_adder.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/sample/test_subtracter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/sample/test_user.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/collector/test-descendant.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/collector/test_dir.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/collector/test-load.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/collector/test_objectspace.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/header.csv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/header-label.csv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/header-label.tsv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/header.tsv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/no-header.csv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/no-header.tsv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/fixtures/plus.csv
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/run-test.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-assertions.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-attribute-matcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-attribute.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-code-snippet.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-color.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-color-scheme.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-data.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-diff.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-emacs-runner.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-error.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-failure.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-fault-location-detector.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-fixture.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-notification.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-omission.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-pending.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-priority.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-test-case.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-test-result.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-test-suite-creator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/test-test-suite.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/testunit-test-util.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/ui/test_testrunmediator.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/util/test_backtracefilter.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/util/test-method-owner-finder.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/util/test_observable.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/util/test-output.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/test-unit-%{test_unit_base_version}/test/util/test_procwrapper.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/test-unit-%{test_unit_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/COPYING
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/GPL
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/LGPL
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/PSFL
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/README.md
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/doc/text/getting-started.md
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/doc/text/how-to.md
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/doc/text/news.md
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/exts.mk
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test-unit.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/assertion-failed-error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/assertions.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/attribute-matcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/attribute.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/auto-runner-loader.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/autorunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/code-snippet-fetcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/descendant.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/dir.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/load.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/objectspace.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/collector/xml.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/color-scheme.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/color.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/data-sets.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/data.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/diff.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/exception-handler.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/failure.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/fault-location-detector.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/fixture.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/notification.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/omission.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/pending.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/priority.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/runner/console.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/runner/emacs.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/runner/xml.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/test-suite-creator.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/testcase.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/testresult.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/testsuite.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/console/outputlevel.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/console/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/emacs/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/testrunnermediator.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/testrunnerutilities.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/ui/xml/testrunner.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/backtracefilter.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/method-owner-finder.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/observable.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/output.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/util/procwrapper.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/lib/test/unit/version.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/sample/adder.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/sample/subtracter.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/sample/test_adder.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/sample/test_subtracter.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/sample/test_user.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test-unit.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/collector/test-descendant.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/collector/test-load.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/collector/test_dir.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/collector/test_objectspace.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/header-label.csv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/header-label.tsv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/header.csv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/header.tsv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/no-header.csv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/no-header.tsv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/fixtures/plus.csv
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/run-test.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-assertions.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-attribute-matcher.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-attribute.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-code-snippet.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-color-scheme.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-color.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-data.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-diff.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-emacs-runner.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-error.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-failure.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-fault-location-detector.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-fixture.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-notification.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-omission.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-pending.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-priority.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-test-case.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-test-result.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-test-suite-creator.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/test-test-suite.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/testunit-test-util.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/ui/test_testrunmediator.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/util/test-method-owner-finder.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/util/test-output.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/util/test_backtracefilter.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/util/test_observable.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/test-unit-%{test_unit_base_version}/test/util/test_procwrapper.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/test-unit-%{test_unit_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/test-unit.gemspec

%files -n %{?scl_prefix}rubygem-xmlrpc
%doc %{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}/LICENSE.txt
%dir %{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}/Gemfile
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}/Rakefile
%doc %{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}/README.md
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}/bin
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_base_version}/lib
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/xmlrpc-%{xmlrpc_base_version}.gemspec
%{share_ruby}/gems/%{ruby_full}/gems/xmlrpc-*/.gitignore
%{share_ruby}/gems/%{ruby_full}/gems/xmlrpc-*/.travis.yml
%{share_gems}/gems/%{ruby_full}/gems/xmlrpc-*/.gitignore
%{share_gems}/gems/%{ruby_full}/gems/xmlrpc-*/.travis.yml
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/xmlrpc.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/cache/xmlrpc-%{xmlrpc_base_version}.gem
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/base64.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/client.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/config.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/create.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/datetime.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/marshal.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/server.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/utils.rb
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/LICENSE.txt
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/README.md
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/gems/xmlrpc-%{xmlrpc_base_version}/xmlrpc.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/%{ruby_full}/specifications/xmlrpc-%{xmlrpc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/Gemfile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/LICENSE.txt
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/README.md
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/Rakefile
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/bin/console
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/bin/setup
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/exts.mk
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/base64.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/client.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/config.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/create.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/datetime.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/marshal.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/parser.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/server.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/lib/xmlrpc/utils.rb
/opt/cpanel/ea-ruby27/root/usr/share/gems/gems/xmlrpc-%{xmlrpc_base_version}/xmlrpc.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/xmlrpc-%{xmlrpc_base_version}.gemspec
/opt/cpanel/ea-ruby27/root/usr/share/gems/specifications/xmlrpc.gemspec

%changelog
* Thu Nov 24 2022 Travis Holloway <t.holloway@cpanel.net> - 2.7.7-1
- EA-11073: Update ea-ruby27 from v2.7.6 to v2.7.7

* Tue Apr 12 2022 Cory McIntire <cory@cpanel.net> - 2.7.6-1
- EA-10620: Update ea-ruby27 from v2.7.5 to v2.7.6

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 2.7.5-2
- ZC-9589: Update DISABLE_BUILD to match OBS

* Wed Nov 24 2021 Travis Holloway <t.holloway@cpanel.net> - 2.7.5-1
- EA-10301: Update ea-ruby27 from v2.7.4 to v2.7.5

* Thu Jul 29 2021 Travis Holloway <t.holloway@cpanel.net> - 2.7.4-1
- EA-10007: Update ea-ruby27 from v2.7.3 to v2.7.4

* Mon Jun 14 2021 Julian Brown <julian.brown@cpanel.net> - 2.7.3-1
- EA-9864: Update ea-ruby27 from v2.7.2 to v2.7.3

* Tue Jun 08 2021 Travis Holloway <t.holloway@cpanel.net> - 2.7.2-8
- EA-9801: Reduce time needed to install this package

* Tue May 11 2021 Travis Holloway <t.holloway@cpanel.net> - 2.7.2-7
- EA-9759: Ensure ruby-devel is properly required

* Thu Feb 25 2021 Cory McIntire <cory@cpanel.net> - 2.7.2-6
- EA-9609: Update ea-ruby27 from v2.7.1 to v2.7.2
  Adjusted release to -6 due to OBS build issues of the gems

* Fri Dec 04 2020 Julian Brown <julian.brown@cpanel.net> - 2.7.1-5
- ZC-8079: remove requires ea-openssl for CentOS 8 (only)

* Wed Nov 25 2020 Julian Brown <julian.brown@cpanel.net> - 2.7.1-4
- ZC-8005: Replace ea-openssl11 with system openssl on C8

* Mon Nov 09 2020 Julian Brown <julian.brown@cpanel.net> - 2.7.1-3
- ZC-7540: Force a /usr/bin/python if it does not already exist.

* Fri Nov 06 2020 Julian Brown <julian.brown@cpanel.net> - 2.7.1-2
- ZC-7887: Fix postun

* Fri Aug 14 2020 Julian Brown <julian.brown@cpanel.net> - 2.7.1-1
- Initial commits

