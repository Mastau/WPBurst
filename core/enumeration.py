#!/usr/bin/env python3
"""
WPBurst - Enumeration module for Wordpress 
"""

import requests
from urllib.parse import urljoin
import re
import hashlib

class WPEnumerator:
    def __init__(self, base_url: str):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WPBurst/1.0",
            "Accept": "application/json, */*;q=0.9",
        })
        self._home_fingerprint = None

    def _get(self, path: str):
        try:
            url = urljoin(self.base_url, path)
            return self.session.get(url, timeout=7)
        except Exception:
            return None
    
    def _fingerprint(self, text: str):
        """Return page fingerprint (size + hash)"""
        if not text:
            return None
        return (len(text), hashlib.md5(text.encode(errors="ignore")).hexdigest())

    def _get_home_fingerprint(self):
        """Get home page fingerprint"""
        if self._home_fingerprint is None:
            r = self._get("")
            if r and r.text:
                self._home_fingerprint = self._fingerprint(r.text)
        return self._home_fingerprint

    def _is_homepage_like(self, response):
        """Return true if response == home page fingerprint"""
        if not response or not response.text:
            return False
        home_fp = self._get_home_fingerprint()
        if not home_fp:
            return False
        return self._fingerprint(response.text) == home_fp


    # ------------------------ Detect WordPress ------------------------
    def detect_wordpress(self):
        tests = ["wp-login.php", "readme.html"]
        for t in tests:
            r = self._get(t)
            if r and "wordpress" in r.text.lower():
                print(f"[+] WordPress detect with {t}")
                return True
        print("[-] Wordpress not found")
        return False

    # ------------------------ Version WordPress ------------------------
    def get_version(self):
        # wp-json
        r = self._get("wp-json")
        if r and r.status_code == 200:
            try:
                j = r.json()
                if "generator" in j:
                    print(f"[+] Version find with wp-json: {j['generator']}")
                    return j['generator']
            except:
                pass

        # meta
        r = self._get("")
        if r:
            m = re.search(r'content="WordPress ([0-9.]+)"', r.text)
            if m:
                print(f"[+] Version with meta: {m.group(1)}")
                return m.group(1)

        # readme.html
        r = self._get("readme.html")
        if r:
            m = re.search(r"Version ([0-9.]+)", r.text)
            if m:
                print(f"[+] Version with readme.html: {m.group(1)}")
                return m.group(1)

        print("[-] Version not found")
        return None

    # ------------------------ Plugins ------------------------
    def enumerate_plugins(self):
        print("[+] Listing plugins")
        found = set()

        # List common plugins (Use an extrnal list asap/ import custom list)
        common_plugins = [
            "akismet", "jetpack", "woocommerce", "wordfence",
            "contact-form-7", "wpforms", "elementor", "yoast-seo"
        ]
        for p in common_plugins:
            r = self._get(f"wp-content/plugins/{p}/")
            # bypass rewrite rules
            if r and r.status_code == 200 and not self._is_homepage_like(r):
                found.add(p)

        # Parsing HTML
        r = self._get("")
        if r:
            matches = re.findall(r"wp-content/plugins/([^/]+)/", r.text)
            for m in matches:
                found.add(m)

        # Check plugins found
        confirmed = set()
        for p in found:
            # Read readme.txt
            r_readme = self._get(f"wp-content/plugins/{p}/readme.txt")
            if r_readme and r_readme.status_code == 200 and not self._is_homepage_like(r_readme):
                print(f"    -> readme found for {p}")
                confirmed.add(p)
                continue  # c’est bon, plugin confirmé

            # Check unique file ({plugin}.php) :w
            r_main = self._get(f"wp-content/plugins/{p}/{p}.php")
            if r_main and r_main.status_code == 200 and not self._is_homepage_like(r_main):
                print(f"    -> main file found for {p}")
                confirmed.add(p)
                continue

            r_assets = self._get(f"wp-content/plugins/{p}/assets/")
            if r_assets and r_assets.status_code == 200 and not self._is_homepage_like(r_assets):
                print(f"    -> assets dir exists for {p}")
                confirmed.add(p)
                continue

        if not confirmed:
            print("[-] No plugins found")
            return []

        return sorted(confirmed)


    # ------------------------ Themes ------------------------
    def enumerate_themes(self):
        print("[+] Themes enumeration …")
        themes = set()

        r = self._get("")
        if r:
            matches = re.findall(r"wp-content/themes/([^/]+)/", r.text)
            for m in matches:
                themes.add(m)

        for t in themes:
            sc = self._get(f"wp-content/themes/{t}/style.css")
            if sc and sc.status_code == 200:
                print(f"[+] Themes found: {t}")

        if not themes:
            print("[-] No theme found")
        return list(themes)

    # ------------------------ Utilisateurs ------------------------
    def enumerate_users(self, limit=10):
        print("[+] User enumeration")
        users = []
        for i in range(1, limit+1):
            r = self._get(f"?author={i}")
            if r and "/author/" in r.url:
                username = r.url.rstrip('/').split('/')[-1]
                print(f"[+] User found: {username}")
                users.append(username)
        if not users:
            print("[-] No user found")
        return users

