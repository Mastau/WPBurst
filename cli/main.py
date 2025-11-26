from core.enumeration import WPEnumerator
import argparse
from core.module_loader import load_cve_modules
import sys

def main():
    parser = argparse.ArgumentParser(prog="WPBurst", usage='%(prog)s -h for help')
    parser.add_argument("url", help="Wordpress URL : http://example.org")
    parser.add_argument("--list-modules", action="store_true")
    parser.add_argument("-w", "--wordlist", default=None)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    cve_modules = load_cve_modules()
    #####DEBUG#####
    print("[DEBUG] Loaded CVE modules:", list(cve_modules.keys()))
    
    if args.list_modules:
        print("[+] Available CVE modules:")
        for mid, module in cve_modules.items():
            desc = getattr(module, "DESCRIPTION", "")
            print(f"  {mid:20s} {desc}")
        return


    wp = WPEnumerator(args.url)

    print("[*] Start enumerate")
    wp.detect_wordpress()
    wp.get_version()
    plugins = wp.enumerate_plugins("test.txt")
    rest = wp.enumerate_rest_api()
    themes = wp.enumerate_themes()
    users = wp.enumerate_users()

    #TEMPORARY MVP FOR CHECKING CVE MODULES (NOT A FEATURE YET)
    enum_data = {
        "plugins": plugins,
        "themes": themes,
        "users": users,
        "rest": rest,
    }
    print("\n[*] Running passive CVE checks...")
    for mid, module in cve_modules.items():
        if hasattr(module, "check"):
            result = module.check(enum_data)
            if result and result.get("vulnerable"):
                print(f"\n[!!!] Vulnerability detected:")
                print(f"    CVE : {result['cve']}")
                print(f"    Plugin : {result['plugin']}")
                print(f"    Installed Version : {result['version']}")
                print(f"    Details : {result['details']}")
            elif result and result.get("vulnerable") is None:
                print(f"\n[?] Unknown state for {mid} (version could not be determined)")

if __name__ == "__main__":
    main()

