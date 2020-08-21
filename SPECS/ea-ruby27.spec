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

%global major_version 2
%global minor_version 7
%global teeny_version 1
%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_release %{ruby_version}

# Tests require that you build the RPM as a non-root user,
# and can take a long time to run.
# You skip them by setting the runselftest global to 0.
%{!?runselftest: %{expand: %%global runselftest 1}}

%global ruby_archive %{pkg_name}-%{ruby_version}

# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/ruby/ruby-%{ruby_version}/rubygems

# Bundled libraries versions
%global rubygems_version 2.6.14.4
%global molinillo_version 0.5.7

# TODO: The IRB has strange versioning. Keep the Ruby's versioning ATM.
# http://redmine.ruby-lang.org/issues/5313
%global irb_version %{ruby_version}

# NOTE: These versions are determined the hard way, I wait till they fail
# in deployment because the filename is wrong (the version is in the filename)
# then I corrected these versions.

%global bigdecimal_version 2.0.0
%global bundler_version 2.1.4
%global did_you_mean_version 1.4.0
%global io_console_version 0.5.6
%global irb_version 1.2.3
%global json_version 2.3.0
%global minitest_version 5.13.0
%global net_telnet_version 0.2.0
%global openssl_version 2.1.2
%global power_assert_version 1.1.7
%global psych_version 3.1.0
%global racc_version 1.4.16
%global rake_version 13.0.1
%global rdoc_version 6.2.1
%global test_unit_version 3.3.4
%global xmlrpc_version 0.3.0

# Might not be needed in the future, if we are lucky enough.
# https://bugzilla.redhat.com/show_bug.cgi?id=888262
%global tapset_root %{_datadir}/systemtap
%global tapset_dir %{tapset_root}/tapset
%global tapset_libdir %(echo %{_libdir} | sed 's/64//')*

%global _normalized_cpu %(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/')

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
Version: %{ruby_version}
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
# ABRT hoook test case.
Source12: test_abrt.rb
# TODO: SystemTap tests skipped cause they fail on OBS
# check by hand: PIG-2955
# Source13: test_systemtap.rb
# To test Ruby software collection
Source14: test_dependent_scls.rb

# %%load function should be supported in RPM 4.12+.
# http://lists.rpm.org/pipermail/rpm-maint/2014-February/003659.html
Source100: load.inc
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

# FROM SOURCE4
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

Requires: %{?scl_prefix}%{pkg_name}-libs%{?_isa} = %{version}-%{release}
Requires: %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Requires: %{?scl_prefix}rubygem(bigdecimal) >= %{bigdecimal_version}
Requires: %{?scl_prefix}rubygem(did_you_mean) >= %{did_you_mean_version}
Requires: %{?scl_prefix}rubygem(openssl) >= %{openssl_version}

%{?scl:Requires: %{scl}-runtime >= 2.4.3-2}

BuildRequires: tree

%if 0%{rhel} > 6
BuildRequires: autoconf
%else
BuildRequires: autotools-latest-autoconf
%endif
BuildRequires: gdbm-devel
BuildRequires: libffi-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: scl-utils
BuildRequires: scl-utils-build
%{?scl:BuildRequires: %{scl}-runtime >= 2.4.3-2}
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
Requires:   ea-openssl11 >= %{ea_openssl_ver}
Requires:   %{?scl_prefix}ruby(release)
Requires:   %{?scl_prefix}ruby(rubygems) >= %{rubygems_version}
Provides:   %{?scl_prefix}rubygem(openssl) = %{version}-%{release}
BuildRequires: ea-openssl11 >= %{ea_openssl_ver}
BuildRequires: ea-openssl11-devel >= %{ea_openssl_ver}

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

export LDFLAGS="-Wl,-rpath=/opt/cpanel/ea-openssl11/lib64"

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
        --enable-rpath=/opt/cpanel/ea-openssl11/lib \
        --enable-shared \
        --with-ruby-version="ruby-%{ruby_version}" \
        --enable-multiarch \
        --with-prelude=./abrt_prelude.rb \
        --with-opt-dir=/opt/cpanel/ea-openssl11

# Q= makes the build output more verbose and allows to check Fedora
# compiler options.
make %{?_smp_mflags} COPY="cp -p" Q=

%install
rm -rf %{buildroot}
%{?scl:scl enable %scl - << \EOF
make install DESTDIR=%{buildroot}
EOF}

mkdir -p %{buildroot}%{gem_dir}/specifications

# Rename ruby/config.h to ruby/config-<arch>.h to avoid file conflicts on
# multilib systems and install config.h wrapper
mv %{buildroot}%{_includedir}/%{pkg_name}/config.h %{buildroot}%{_includedir}/%{pkg_name}/config-%{_arch}.h
install -m644 %{SOURCE7} %{buildroot}%{_includedir}/%{pkg_name}/config.h

# Rename the ruby executable. It is replaced by RubyPick.
%{?with_rubypick:mv %{buildroot}%{_bindir}/%{pkg_name}{,-mri}}

# Version is empty if --with-ruby-version is specified.
# http://bugs.ruby-lang.org/issues/7807
sed -i 's/Version: \${ruby_version}/Version: %{ruby_version}/' %{buildroot}%{_libdir}/x86_64-linux/pkgconfig/%{pkg_name}.pc

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
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
sed 's/@SCL@/%{scl}/' %{SOURCE1} > %{buildroot}%{rubygems_dir}/rubygems/defaults/%{basename:%{SOURCE1}}

# Move gems root into common directory, out of Ruby directory structure.
mv %{buildroot}%{ruby_libdir}/gems %{buildroot}%{gem_dir}

# Create folders for gem binary extensions.
# TODO: These folders should go into rubygem-filesystem but how to achieve it,
# since noarch package cannot provide arch dependent subpackages?
# http://rpm.org/ticket/78
mkdir -p %{buildroot}%{_exec_prefix}/lib{,64}/gems/%{pkg_name}

# Move bundled rubygems to %%gem_dir and %%gem_extdir_mri
# make symlinks in ruby_stdlib for unbundled Gems, so that everything works as expected
# bigdecimal and io-console are not enough for scl

mkdir -p %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib
mv %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/rdoc* %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib

mv %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/rdoc-%{rdoc_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/rdoc-%{rdoc_version}/lib/rdoc.rb %{buildroot}%{ruby_libdir}/rdoc.rb
ln -s %{gem_dir}/gems/rdoc-%{rdoc_version}/lib/rdoc %{buildroot}%{ruby_libdir}/rdoc

mkdir -p %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_version}
mv %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/bigdecimal %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mv .ext/x86_64-linux/bigdecimal.so %{buildroot}%{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_version}
mv ext/bigdecimal/bigdecimal.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib/bigdecimal %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/bigdecimal
ln -s %{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_version}/bigdecimal.so %{buildroot}%{ruby_libarchdir}/bigdecimal.so

mkdir -p %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/io-console-%{io_console_version}/io
mv %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/io %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mv .ext/x86_64-linux/io/console.so %{buildroot}%{_libdir}/gems/%{pkg_name}/io-console-%{io_console_version}/io
mv ext/io/console/io-console.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/io-console-%{io_console_version}/lib/io %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/io
mkdir -p %{buildroot}%{ruby_libarchdir}/io
ln -s %{_libdir}/gems/%{pkg_name}/io-console-%{io_console_version}/io/console.so %{buildroot}%{ruby_libarchdir}/io/console.so

mkdir -p %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/json-%{json_version}
mv %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/json* %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mv ext/json/ %{buildroot}%{_libdir}/gems/%{pkg_name}/json-%{json_version}/

mv %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/json-%{json_version}.gemspec %{buildroot}%{gem_dir}/specifications
mkdir -p %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/openssl-%{openssl_version}
mv %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/openssl* %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib

mv .ext/x86_64-linux/openssl.so %{buildroot}%{_libdir}/gems/%{pkg_name}/openssl-%{openssl_version}/

mv %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/openssl-%{openssl_version}.gemspec %{buildroot}%{gem_dir}/specifications

# This used to be directory when OpenSSL was integral part of StdLib => Keep
# it as directory and link everything in it to prevent directory => symlink
# conversion RPM issues.

mkdir -p %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/openssl
find %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl -maxdepth 1 -type f -exec \
  sh -c 'ln -s %{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl/`basename {}` %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/openssl' \;
ln -s %{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl.rb %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/openssl.rb
ln -s %{_libdir}/gems/%{pkg_name}/openssl-%{openssl_version}/openssl.so %{buildroot}%{ruby_libarchdir}/openssl.so

mkdir -p %{buildroot}%{gem_dir}/gems/psych-%{psych_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{pkg_name}/psych-%{psych_version}
mv %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/psych* %{buildroot}%{gem_dir}/gems/psych-%{psych_version}/lib
mv .ext/x86_64-linux/psych.so %{buildroot}%{_libdir}/gems/%{pkg_name}/psych-%{psych_version}/

mv ext/psych/psych.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/psych-%{psych_version}/lib/psych %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/psych
ln -s %{gem_dir}/gems/psych-%{psych_version}/lib/psych.rb %{buildroot}%{ruby_libdir}/ruby-%{ruby_version}/psych.rb
ln -s %{_libdir}/gems/%{pkg_name}/psych-%{psych_version}/psych.so %{buildroot}%{ruby_libarchdir}/psych.so

# Adjust the gemspec files so that the gems will load properly
sed -i '/^end$/ i\
  s.extensions = ["json/ext/parser.so", "json/ext/generator.so"]' %{buildroot}%{gem_dir}/specifications/json-%{json_version}.gemspec

# Move man pages into proper location
mv %{buildroot}%{gem_dir}/gems/ruby-%{ruby_version}/gems/rake-%{rake_version}/doc/rake.1 %{buildroot}%{_mandir}/man1

# Install a tapset and fix up the path to the library.
mkdir -p %{buildroot}%{tapset_dir}
sed -e "s|@LIBRARY_PATH@|%{tapset_libdir}/libruby.so.%{major_minor_version}|" \
  %{SOURCE2} > %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp
# Escape '*/' in comment.
sed -i -r "s|( \*.*\*)\/(.*)|\1\\\/\2|" %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp

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
# tests.
#make test-all TESTS="%{SOURCE14}" || exit 1

rm -rf ./lib/rubygems/defaults

# TODO: Check Ruby hardening. needed?
#checksec -f libruby.so.%{ruby_version} | \
  #grep "Full RELRO.*Canary found.*NX enabled.*DSO.*No RPATH.*No RUNPATH.*Yes.*\d*.*\d*.*libruby.so.%{ruby_version}"

# Check RubyGems version correctness.
[ "`make runruby TESTRUN_SCRIPT='bin/gem -v' | tail -1`" == '%{rubygems_version}' ]
# Check Molinillo version correctness.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\"module Gem; module Resolver; end; end; require 'rubygems/resolver/molinillo/lib/molinillo/gem_metadata'; puts Gem::Resolver::Molinillo::VERSION\\\"\" | tail -1`" \
  == '%{molinillo_version}' ]

# test_debug(TestRubyOptions) fails due to LoadError reported in debug mode,
# when abrt.rb cannot be required (seems to be easier way then customizing
# the test suite).
touch abrt.rb

# Check if abrt hook is required (RubyGems are disabled by default when using
# runruby, so re-enable them).
make runruby TESTRUN_SCRIPT="--enable-gems %{SOURCE12}"

# TODO: This test does not run, someone with Ruby knowledge will need to update these
# tests.
# Check if systemtap is supported.
#make runruby TESTRUN_SCRIPT=%{SOURCE13}

DISABLE_TESTS=""

# https://bugs.ruby-lang.org/issues/11480
# Once seen: http://koji.fedoraproject.org/koji/taskinfo?taskID=12556650
DISABLE_TESTS="$DISABLE_TESTS -x test_fork.rb"

make check TESTS="-v $DISABLE_TESTS"
echo "DO NOT REMOVE this echo command, or the tests fail"
EOF}
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc BSDL
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc GPL
%doc LEGAL
%{_bindir}/erb
%{_bindir}/%{pkg_name}%{?with_rubypick:-mri}
%{_mandir}/man1/erb*
%{_mandir}/man1/ruby*

%dir %{_mandir}/man1
%dir %{_exec_prefix}/share/doc

# catch all file lists
%{_exec_prefix}/bin/*
%{_exec_prefix}/lib64/gems/ruby/json-%{json_version}/json/*

%{_exec_prefix}/lib64/ruby/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/enc/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/io/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/json/ext/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/bignum/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/complex/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/fixnum/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/float/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/integer/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/math/fixtures/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/math/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/mathn/rational/*
%{_exec_prefix}/lib64/ruby/ruby-%{ruby_version}/*
%{_exec_prefix}/share/gems/gems/io-console-%{io_console_version}/lib/io/*
%{_exec_prefix}/share/gems/gems/json-%{json_version}/lib/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/bundler-%{bundler_version}/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/bundler-%{bundler_version}/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/irb-%{irb_version}/exe/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/racc-%{racc_version}/bin/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/rdoc-%{rdoc_version}/exe/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/.*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/specifications/default/*
%{_exec_prefix}/share/gems/gems/ruby-%{ruby_version}/specifications/*
%{_exec_prefix}/share/gems/specifications/*
%{_exec_prefix}/share/man/man1/*
%{_exec_prefix}/share/man/man5/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/benchmark/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/bundler/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/did_you_mean/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/getoptlong/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/logger/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/observer/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/open3/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/ostruct/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/pstore/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/reline/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/singleton/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/timeout/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/tracer/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/csv/core_ext/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/csv/*
%{_exec_prefix}/share/ruby/ruby-%{ruby_version}/delegate/*

%dir %{_exec_prefix}/share/ruby/
%dir %{gem_dir}/gems/

%files devel
%doc BSDL
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc GPL
%doc LEGAL

%config(noreplace) %{_root_sysconfdir}/rpm/macros.ruby%{?scl:.%{scl}}

%{_includedir}/*
%{_libdir}/x86_64-linux/libruby.so
%{_libdir}/x86_64-linux/pkgconfig/%{pkg_name}.pc

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
%{ruby_libdir_ver}/*.rb
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

%{_libdir}/x86_64-linux/libruby.so.*
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
%{ruby_libarchdir_ver}/openssl.so
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
%dir %{_exec_prefix}/lib*/gems
%dir %{_exec_prefix}/lib*/gems/ruby

%exclude %{gem_dir}/gems/ruby-%{ruby_version}/cache/*

%files -n %{?scl_prefix}rubygems-devel
%config(noreplace) %{_root_sysconfdir}/rpm/macros.rubygems%{?scl:.%{scl}}

%files -n %{?scl_prefix}rubygem-rake
%{_bindir}/rake
%{gem_dir}/gems/ruby-%{ruby_version}/gems/rake-%{rake_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/rake-%{rake_version}.gemspec
%{_mandir}/man1/rake.1*

%files irb
%{_bindir}/irb
%{ruby_libdir_ver}/irb.rb
%{ruby_libdir_ver}/irb
%{_mandir}/man1/irb.1*

%files -n %{?scl_prefix}rubygem-rdoc
%{ruby_libdir}/rdoc*
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_dir}/gems/rdoc-%{rdoc_version}
%{gem_dir}/specifications/rdoc-%{rdoc_version}.gemspec
%{_mandir}/man1/ri*

%files doc -f .ruby-doc.en -f .ruby-doc.ja
%doc README.md
%doc ChangeLog
%doc ruby-exercise.stp
%{_datadir}/ri

%files -n %{?scl_prefix}rubygem-bigdecimal
%{ruby_libdir_ver}/bigdecimal
%{ruby_libarchdir_ver}/bigdecimal.so
%{_libdir}/gems/%{pkg_name}/bigdecimal-%{bigdecimal_version}
%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/bigdecimal-%{bigdecimal_version}.gemspec

%files -n %{?scl_prefix}rubygem-did_you_mean
%{gem_dir}/gems/ruby-%{ruby_version}/gems/did_you_mean-%{did_you_mean_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/did_you_mean-%{did_you_mean_version}/.*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/did_you_mean-%{did_you_mean_version}.gemspec

%files -n %{?scl_prefix}rubygem-io-console
%{ruby_libdir_ver}/io
%{ruby_libarchdir}/io/console.so
%{_libdir}/gems/%{pkg_name}/io-console-%{io_console_version}
%{gem_dir}/gems/ruby-%{ruby_version}/gems/io-console-%{io_console_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/io-console-%{io_console_version}.gemspec

%files -n %{?scl_prefix}rubygem-json
%dir %{ruby_libarchdir_ver}/json
%dir %{_libdir}/gems/%{pkg_name}/json-%{json_version}
%dir %{gem_dir}/gems/ruby-%{ruby_version}/gems/json-%{json_version}
%{gem_dir}/specifications/json-%{json_version}.gemspec

%files -n %{?scl_prefix}rubygem-minitest
%{gem_dir}/gems/ruby-%{ruby_version}/gems/minitest-%{minitest_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/minitest-%{minitest_version}/.*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/minitest-%{minitest_version}.gemspec

%files -n %{?scl_prefix}rubygem-openssl
%{ruby_libdir_ver}/openssl
%{ruby_libdir_ver}/openssl.rb
%{ruby_libarchdir}/openssl.so
%{_libdir}/gems/%{pkg_name}/openssl-%{openssl_version}
%{gem_dir}/gems/openssl-%{openssl_version}
%{gem_dir}/specifications/openssl-%{openssl_version}.gemspec

%files -n %{?scl_prefix}rubygem-power_assert
%{gem_dir}/gems/ruby-%{ruby_version}/gems/power_assert-%{power_assert_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/power_assert-%{power_assert_version}/.*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/power_assert-%{power_assert_version}.gemspec

%files -n %{?scl_prefix}rubygem-psych
%{ruby_libdir_ver}/psych
%{ruby_libdir_ver}/psych.rb
%{ruby_libarchdir_ver}/psych.so
%{_libdir}/gems/%{pkg_name}/psych-%{psych_version}
%{gem_dir}/gems/psych-%{psych_version}
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/default/psych-%{psych_version}.gemspec

%files -n %{?scl_prefix}rubygem-net-telnet
%{gem_dir}/gems/ruby-%{ruby_version}/gems/net-telnet-%{net_telnet_version}
%exclude %{gem_dir}/gems/ruby-%{ruby_version}/gems/net-telnet-%{net_telnet_version}/.*
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/net-telnet-%{net_telnet_version}.gemspec

%files -n %{?scl_prefix}rubygem-test-unit
%{gem_dir}/gems/ruby-%{ruby_version}/gems/test-unit-%{test_unit_version}
%{gem_dir}/gems/ruby-%{ruby_version}//specifications/test-unit-%{test_unit_version}.gemspec

%files -n %{?scl_prefix}rubygem-xmlrpc
%doc %{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/LICENSE.txt
%dir %{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/Gemfile
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/Rakefile
%doc %{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/README.md
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/bin
%{gem_dir}/gems/ruby-%{ruby_version}/gems/xmlrpc-%{xmlrpc_version}/lib
%{gem_dir}/gems/ruby-%{ruby_version}/specifications/xmlrpc-%{xmlrpc_version}.gemspec

%changelog
* Fri Aug 14 2020 Julian Brown <julian.brown@cpanel.net> - 2.7.1-1
- Initial commits

