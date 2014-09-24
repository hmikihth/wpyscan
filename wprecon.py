"""
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
ganapati (@G4N4P4T1) wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
----------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
import re
import requests
import random


class WPRecon():
    def __init__(self, proxy):
        self.req = requests.Session()
        self.req.verify = False
        self.version = None
        if proxy is not None:
            self.req.proxies = proxy

    def scan(self, url):
        if not url.endswith('/'):
            url = "%s/" % url

        results = {'printable_results': [],
                   'modules': []}

        results['printable_results'] = self.get_printable_results(url)
        results['modules'] = self.get_modules(url)
        return results

    def get_printable_results(self, url):
        results = {
            'Robots': self.get_robots(url),
            'Readme': self.get_readme(url),
            'Fpd': self.get_fpd(url),
            'Backup': self.get_backup(url),
            'Upload_listing': self.get_upload_listing(url),
            'Version': self.get_version(url),
            'Theme': self.get_theme(url)}
        return results

    def get_user_agent(self):
        user_agents = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.50",
                       "Opera/9.70 (Linux ppc64 ; U; en) Presto/2.2.1",
                       "Mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)",
                       "Mozilla/5.0(Windows; U; Windows NT 5.2; rv:1.9.2) Gecko/20100101 Firefox/3.6",
                       "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1) Gecko/20090612 Firefox/3.5",
                       "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.2) Gecko/20100115 Firefox/3.6",
                       "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) Safari/419.3"]
        return random.choice(user_agents)

    # Recon methods

    def get_modules(self, url):
        modules = []
        headers = {'User-Agent': self.get_user_agent()}
        page_req = self.req.get(url, headers=headers)
        soup = BeautifulSoup(page_req.text)

        # Search modules in css
        module_paths = soup.findAll("link", {"rel": "stylesheet"})
        for module_path in module_paths:
            if '/wp-content/plugins/' in module_path['href']:
                regex = re.compile("/wp-content/plugins/(.+)/",
                                   re.IGNORECASE)
                r = regex.findall(module_path['href'])
                for module_name in r:
                    modules.append(module_name.split('/')[0])

        # Search modules in javascript
        module_paths = soup.findAll("script",
                                    {"type": "text/javascript"})
        for module_path in module_paths:
            try:
                if '/wp-content/plugins/' in module_path['src']:
                    regex = re.compile("/wp-content/plugins/(.+)/",
                                       re.IGNORECASE)
                    r = regex.findall(module_path['src'])
                    for module_name in r:
                        modules.append(module_name.split('/')[0])
            except:
                # Silently pass, parsing html is pain in the ass
                pass

        return list(set(modules))

    def get_robots(self, url):
        robots = []
        headers = {'User-Agent': self.get_user_agent()}
        full_url = "%s%s" % (url, 'robots.txt')
        robots_req = self.req.get(full_url, headers=headers)
        if robots_req.status_code == 200:
            robots_text = robots_req.text.split("\r\n")
            for robot_text in robots_text:
                if (robot_text.lower().startswith('allow') or
                   robot_text.lower().startswith('disallow')):
                    robots.append(robot_text)
        if not robots:
            return None
        else:
            return robots

    def get_readme(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        full_url = "%s%s" % (url, 'readme.html')
        readme_req = self.req.get(full_url, headers=headers)
        if readme_req.status_code == 200:
            soup = BeautifulSoup(readme_req.text)
            version = soup.find("h1").getText().strip()
            self.version = version.replace('Version ', '')
            return full_url
        else:
            return None

    def get_fpd(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        full_url = "%s%s" % (url, "wp-includes/rss-functions.php")
        fpd_req = self.req.get(full_url, headers=headers)
        if fpd_req.status_code == 200:
            if "Fatal error:" in fpd_req.text:
                return fpd_req.text
        return None

    def get_backup(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        backups_find = []
        backups = ["wp-config.php~",
                   "wp-config.php.save",
                   ".wp-config.php.swp",
                   "wp-config.php.swp",
                   "wp-config.php.swo",
                   "wp-config.php_bak",
                   "wp-config.bak",
                   "wp-config.php.bak",
                   "wp-config.save",
                   "wp-config.old",
                   "wp-config.php.old",
                   "wp-config.php.orig",
                   "wp-config.orig",
                   "wp-config.php.original",
                   "wp-config.original",
                   "wp-config.txt"]
        for backup in backups:
            full_url = "%s%s" % (url, backup)
            backup_req = self.req.get(full_url, headers=headers)
            if backup_req.status_code == 200:
                backups_find.append(backup)

        if not backups_find:
            return None
        else:
            return backups_find

    def get_upload_listing(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        full_url = "%s%s" % (url, "/wp-content/uploads/")
        upload_req = self.req.get(full_url, headers=headers)
        if upload_req.status_code == 200:
            if "index of" in upload_req.text.lower():
                return full_url
        return None

    def get_version(self, url):
        if self.version is not None:
            return self.version
        headers = {'User-Agent': self.get_user_agent()}
        page_req = self.req.get(url, headers=headers)
        soup = BeautifulSoup(page_req.text)
        generator = soup.find("meta", {'name': 'generator'})
        self.version = generator['content'].replace('Wordpress ', '').strip()
        return self.version

    def get_theme(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        page_req = self.req.get(url, headers=headers)
        soup = BeautifulSoup(page_req.text)
        theme_paths = soup.findAll("link", {"rel": "stylesheet",
                                            "type": "text/css"})
        for theme_path in theme_paths:
            if '/wp-content/themes/' in theme_path['href']:
                regex = re.compile("/wp-content/themes/(.+)/css/",
                                   re.IGNORECASE)
                r = regex.findall(theme_path['href'])
                if len(r) > 0:
                    return r[0]
        return None
