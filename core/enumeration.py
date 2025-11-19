#!/usr/bin/env python3
"""
WPBurst - Enumeration module for Wordpress 
"""

import requests
from urllib.parse import urljoin
import re

class WPEnumerator:
    def __init__(self, base_url: str):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WPBurst/1.0",
            "Accept": "application/json, */*;q=0.9",
        })

    def _get(self, path: str):
        try:
            url = urljoin(self.base_url, path)
            return self.session.get(url, timeout=7)
        except Exception:
            return None

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

        print("[-] Version introuvable")
        return None

    # ------------------------ Plugins ------------------------
    def enumerate_plugins(self):
        print("[+] Énumération des plugins…")
        found = set()

        # Heuristique de plugins connus
        common_plugins = [
            "akismet", "jetpack", "woocommerce", "wordfence",
            "contact-form-7", "wpforms", "elementor", "yoast-seo"
        ]
        for p in common_plugins:
            r = self._get(f"wp-content/plugins/{p}/")
            if r and r.status_code == 200:
                found.add(p)

        # Parsing HTML
        r = self._get("")
        if r:
            matches = re.findall(r"wp-content/plugins/([^/]+)/", r.text)
            for m in matches:
                found.add(m)

        # readme.txt des plugins trouvés
        for p in found:
            r = self._get(f"wp-content/plugins/{p}/readme.txt")
            if r and r.status_code == 200:
                print(f"    ↳ readme find for {p}")

        if not found:
            print("[-] No plugins found")
        return list(found)

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

