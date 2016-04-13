%define debug_package  %nil
%define name 		wpyscan
%define Summary		Wordpress pentest tool
%define sourcetype      tar.gz
%define version         0.1.0

Name:         %name
Summary:       %Summary
Summary(hu):   %Summary_hu
Version:       %version
Release:       %mkrel 2
License:       BEER-WARE
Distribution: blackPanther OS
Vendor:       blackPanther Europe
Packager:     Miklos Horvath
Group:        Development/Tools
Source0:      %name-%version.%sourcetype
Buildroot:     %_tmppath/%name-%version-%release-root
Requires:     python(abi) >= 3.4
Requires:     python3-requests >= 2.9.1

%description
Search exploits on exploit-db, wordpressexploit.com 
and wpvulndb.com according to recon informations 
(version, modules and theme).

%files
%defattr(-,root,root)
%_bindir/%name
%python3_sitelib/%name/*
%python3_sitelib/%name-*

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
* Wed Apr 13 2016 Charles Barcza <info@blackpanther.hu> 0.1.0-2bP
- build for blackPanther OS v16.x
- fix specfile
------------------------------------------------------------------

* Mon Apr 11 2016 Miklos Horvath <hmiki@blackpantheros.eu> 
- initial version
