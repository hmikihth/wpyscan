%define name 		wpyscan
%define Summary		Wordpress pentest tool
%define sourcetype      tar.gz
%define version         0.1.0

Name:         %name
Summary:       %Summary
Summary(hu):   %Summary_hu
Version:       %version
Release:       %mkrel 1
License:       BEER-WARE
Distribution: blackPanther OS
Vendor:       blackPanther Europe
Packager:     Miklos Horvath
Group:        Development/Tools
Source0:      %name-%version.%sourcetype
Buildroot:     %_tmppath/%name-%version-%release-root

Requires:     python3 >= 3.4
Requires:     python3-requests >= 2.3.0
Requires:     glibc >= 2.19.2

%description
Search exploits on exploit-db, wordpressexploit.com and wpvulndb.com according to recon informations (version, modules and theme).

%files
%defattr(-,root,root)
%_bindir/
%python3_sitelib

%prep
%setup -q 

%build
%{__python3} setup.py build
%{__python3} setup.py build_scripts

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
%{__python3} setup.py install --skip-build --no-compile --root %{buildroot}


%clean
rm -rf %buildroot


%changelog
* Mon Apr 11 2016 Miklos Horvath <hmiki@blackpantheros.eu> 
- initial version
