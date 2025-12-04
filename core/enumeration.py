#!/usr/bin/env python3
"""
WPBurst - Enumeration module for Wordpress 
"""

import requests
from urllib.parse import urljoin
import re
import hashlib
import os
import sys
import time
import concurrent.futures

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class WPEnumerator:
    def __init__(self, base_url: str):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WPBurst/1.0",
            "Accept": "application/json, */*;q=0.9",
        })
        self._home_fingerprint = None
        self.max_workers = 50

    def _get(self, path: str):
        try:
            url = urljoin(self.base_url, path)
            return self.session.get(url, timeout=7)
        except Exception:
            return None

    def _load_wordlist(self, wordlist_path):
        """
        Load external plugin list
        return slugs list
        """
        if not os.path.isabs(wordlist_path):
            wordlist_path = os.path.join(BASE_DIR, wordlist_path)
        try:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            return lines
        except Exception as e:
            print(f"[!] Can't read '{wordlist_path}': {e}")
            return []

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

    def _check_plugin_dir(self, plugin):
        r = self._get(f"wp-content/plugins/{plugin}/")
        if r and r.status_code == 200 and not self._is_homepage_like(r):
            return plugin
        return None

    def _extract_version_from_readme(self, text):
        """ Extract plugin version from readme.txt (Stable tag)"""
        match = re.search(r"Stable tag:\s*([0-9.]+)", text, re.IGNORECASE)
        if match:
            return match.group(1)

        # Some thime use Version: (weird case)
        match = re.search(r"Version:\s*([0-9.]+)", text, re.IGNORECASE)
        if match:
            return match.group(1)

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

        print("[-] Version not found")
        return None

    # ------------------------ Plugins ------------------------
    def enumerate_plugins(self, wordlist=None):
        print("[+] Listing plugins (Multithreaded)")
        found = set()
        plugin_info = {}

        if wordlist:
            plugin_list = self._load_wordlist(wordlist)
            if not plugin_list:
                print("[!] Wordlist empty or invalid, using default list.")
        else:
            plugin_list = []
        
        if not plugin_list:
            plugin_list = [
                "akismet", "jetpack", "woocommerce", "wordfence",
                "contact-form-7", "wpforms", "elementor", "yoast-seo",
                "revslider", "all-in-one-seo-pack"
            ]
            print(f"[+] Using default list with {len(plugin_list)} plugins.")
        else:
             print(f"[+] Loaded {len(plugin_list)} plugins from wordlist.")

        start = time.time()
        total = len(plugin_list)
        
        print(f"[+] Checking existence of {total} plugins with {self.max_workers} threads...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_plugin = {executor.submit(self._check_plugin_dir, plugin): plugin for plugin in plugin_list}
            
            checked_count = 0
            for future in concurrent.futures.as_completed(future_to_plugin):
                plugin = future_to_plugin[future]
                checked_count += 1
                
                try:
                    result = future.result()
                    if result:
                        sys.stdout.write("\r" + " " * 120 + "\r") 
                        print(f"    [+] Found plugin folder: {result}")
                        found.add(result)
                except Exception as exc:
                    sys.stderr.write(f"\n[!] Plugin {plugin} generated an exception: {exc}")
                
                if checked_count % 50 == 0 or checked_count == total:
                    elapsed = time.time() - start
                    speed = checked_count / elapsed if elapsed > 0 else 0
                    eta = (total - checked_count) / speed if speed > 0 else 0
                    
                    sys.stdout.write(
                        f"\r[+] Checking plugins {checked_count}/{total} "
                        f"({speed:.1f}/s, ETA {eta:.0f}s)"
                    )
                    sys.stdout.flush()

        sys.stdout.write("\r" + " " * 120 + "\r") 
        sys.stdout.flush()
        
        if found:
            print(f"[+] Initial check finished. Found {len(found)} potential plugins.")
        else:
            print("[-] Initial check did not find any plugin folders.")
            
        r = self._get("")
        if r:
            matches = re.findall(r"wp-content/plugins/([^/]+)/", r.text)
            for m in matches:
                if m not in found:
                    print(f"    [+] Found plugin via HTML source: {m}")
                    found.add(m)

        confirmed = set()
        print("\n[+] Detailed verification of found plugins...")
        for p in found:
            version = None
            
            r_readme = self._get(f"wp-content/plugins/{p}/readme.txt")
            if r_readme and r_readme.status_code == 200 and not self._is_homepage_like(r_readme):
                version = self._extract_version_from_readme(r_readme.text)
                print(f"    -> Readme found for {p} (Version: {version or 'N/A'})")
                confirmed.add(p)
            
            r_main = self._get(f"wp-content/plugins/{p}/{p}.php")
            if r_main and r_main.status_code == 200 and not self._is_homepage_like(r_main):
                print(f"    -> Main file found for {p}")
                confirmed.add(p)
                
            r_assets = self._get(f"wp-content/plugins/{p}/assets/")
            if r_assets and r_assets.status_code == 200 and not self._is_homepage_like(r_assets):
                print(f"    -> Assets directory exists for {p}")
                confirmed.add(p)

            if p in confirmed:
                plugin_info[p] = version

        if not confirmed:
            print("[-] No plugins confirmed after detailed checks.")
            return {}

        print(f"[+] Total confirmed plugins: {len(confirmed)}")
        return plugin_info

    # ------------------------ Endpoints ------------------------
    def enumerate_rest_api(self):
        print("[+] Enumerating WordPress REST API endpoints…")

        rest = {
            "root_available": False,
            "namespaces": [],
            "routes": {},
            "valid_routes": [],
            "invalid_routes": [],
            "errors": []
        }

        # Get wp-json
        r = self._get("wp-json")
        if not r:
            print("[-] Cannot access /wp-json/")
            return rest

        try:
            j = r.json()
        except:
            print("[-] /wp-json/ did not return JSON (rewrite/stale config?)")
            return rest

        rest["root_available"] = True

        namespaces = j.get("namespaces", [])
        rest["namespaces"] = namespaces

        routes = j.get("routes", {})
        rest["routes"] = list(routes.keys())

        print(f"    [+] {len(routes)} routes detected in /wp-json/")
        print(f"    [+] Namespaces: {', '.join(namespaces)}")

        # Analyse each route
        for route in routes:
            full = "wp-json" + route
            rr = self._get(full)
            # If homepage (permalink : plain)
            if rr and not self._is_homepage_like(rr):
                try:
                    jr = rr.json()
                    if isinstance(jr, dict) and jr.get("code") == "rest_no_route":
                        rest["invalid_routes"].append(route)
                    else:
                        rest["valid_routes"].append(route)
                except:
                    rest["errors"].append(route)
            else:
                rest["invalid_routes"].append(route)

        print(f"    [+] Valid routes found: {len(rest['valid_routes'])}")
        print(f"    [+] Invalid routes: {len(rest['invalid_routes'])}")

        return rest


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

    # ------------------------ Users ------------------------
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

