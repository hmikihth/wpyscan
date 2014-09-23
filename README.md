Wpyscan
=======

Wordpress pentest tool

Description :
-------------

Scan wordpress for infos (modules, theme, backups, etc.)

Search exploits on exploit-db.

Input arguments :
-----------------
usage: wpyscan.py [-h] -u URL [-g GRABBER] [-r] [-t] [-p PROXY]

Sploit Wordpress for fun

optional arguments:
  - h, --help : show this help message and exit
  - u URL, --url URL : victim url
  - g GRABBER, --grabber GRABBER : Sploit grabber (default : exploit-db)
  - r, --recon : Just recon (no sploits)
  - t, --tor : Use Tor
  - p PROXY, --proxy PROXY : Use proxy (ip:port)
