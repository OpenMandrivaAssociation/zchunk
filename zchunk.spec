%define major 1
%define libname %mklibname zck %{major}
%define devname %mklibname zck -d

Summary:	Compressed file format that allows easy deltas
Name:		zchunk
Version:	1.1.15
Release:	1
Group:		Archiving/Compression
License:	BSD and MIT
URL:		https://github.com/zchunk/zchunk
Source0:	%{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	meson
Requires:	%{libname} = %{EVRD}

%description
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

%package -n %{libname}
Summary:	Zchunk library
Group:		System/Libraries

%description -n %{libname}
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the zchunk library, libzck.

%package -n %{devname}
Summary:	Headers for building against zchunk
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
This package contains the headers necessary for building against the zchunk
library, libzck.

%prep
%autosetup -p1

# Remove bundled sha libraries
rm -rf src/lib/hash/sha*

%build
%meson -Dwith-openssl=enabled -Dwith-zstd=enabled
%meson_build

%install
%meson_install

# Install script for generating XML dictionaries
install -Dpm 0755 contrib/gen_xml_dictionary %{buildroot}%{_libexecdir}/zck_gen_xml_dictionary

%check
%meson_test

%files
%doc README.md
%license LICENSE
%{_bindir}/zck*
%{_bindir}/unzck
%{_libexecdir}/zck_gen_xml_dictionary
%{_mandir}/man1/*zck*.1.*

%files -n %{libname}
%{_libdir}/libzck.so.%{major}
%{_libdir}/libzck.so.%{version}

%files -n %{devname}
%doc zchunk_format.txt
%{_libdir}/libzck.so
%{_libdir}/pkgconfig/zck.pc
%{_includedir}/zck.h
