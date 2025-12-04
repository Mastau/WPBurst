from core.enumeration import WPEnumerator
import argparse
from core.module_loader import load_cve_modules 
from core.score_impact import VulnerabilityScorer
import sys

def main():
    parser = argparse.ArgumentParser(prog="WPBurst", usage='%(prog)s -h for help')
    parser.add_argument("url", help="Wordpress URL : http://example.org")
    parser.add_argument("--list-modules", action="store_true", help="List all available CVE modules.")
    parser.add_argument("-w", "--wordlist", default=None, help="Path to custom wordlist for plugin enumeration.")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    cve_modules = load_cve_modules()

    #####DEBUG#####
    print(f"[*] Loaded {len(cve_modules)} CVE modules.")
    
    if args.list_modules:
        print("\n[+] Available CVE modules:")
        print(f"{'ID':<20s} {'Description'}")
        print("-" * 40)
        for mid, module in cve_modules.items():
            desc = getattr(module, "DESCRIPTION", "No description available")
            print(f"  {mid:<20s} {desc}")
        return
    # KeyboardInterrupt safe exit
    try:
        wp = WPEnumerator(args.url)

        print(f"\n[*] Start enumeration on {args.url}")
        
        wp.detect_wordpress()
        wp_version = wp.get_version()
        
        plugins = wp.enumerate_plugins(args.wordlist)
        rest = wp.enumerate_rest_api()
        themes = wp.enumerate_themes()
        users = wp.enumerate_users()
        
    except KeyboardInterrupt:
        print("\n[!] Enumeration cancelled by user (Ctrl+C). Exiting.")
        return

    enum_data = {
        "wp_version": wp_version,
        "plugins": plugins,
        "themes": themes,
        "users": users,
        "rest_api": rest, 
    }
    
    scorer = VulnerabilityScorer(enum_data)
    vulnerabilities_found = []

    print("\n[*] Running passive CVE checks and calculating Impact Score...")
    
    for mid, module in cve_modules.items():
        if hasattr(module, "check"):
            try:
                result = module.check(enum_data)
                
                if result:
                    impact_score = scorer.calculate_score(result)
                    
                    result['impact_score'] = impact_score
                    vulnerabilities_found.append(result)

            except Exception as e:
                sys.stderr.write(f"\n[!] Error running module {mid}: {e}\n")


    if not vulnerabilities_found:
        print("\n[+] No known vulnerabilities detected based on passive checks.")
        return

    vulnerabilities_found.sort(key=lambda x: x.get('impact_score', 0), reverse=True)

    print(f"\n{'='*50}")
    print(f"[+] Scan Summary: {len(vulnerabilities_found)} potential vulnerabilities found.")
    print(f"{'='*50}")

    for result in vulnerabilities_found:
        score = result.get('impact_score', 0.0)
        
        if score >= 12.0:
            status = "HIGH CONFIDENCE / EXPLOIT CANDIDATE"
        elif score >= 8.0:
            status = "MEDIUM CONFIDENCE / INVESTIGATE"
        else:
            status = "LOW CONFIDENCE / THEORETICAL"
        
        print(f"\n[!!!] VULNERABILITY FOUND: {result['cve']}")
        print(f"  > Score Impact : {score:.2f} (Status: {status})")
        print(f"    Plugin / Version : {result.get('plugin')} / {result.get('version')}")
        print(f"    Base CVSS : {result.get('cvss', 'N/A')}")
        print(f"    Details : {result.get('details', 'N/A')}")
       
        #FOR THE FUTURE > IF RUN() EXIST
        # if score >= 12.0 and hasattr(module, "run"):
        #     # print("[!] Launching active exploit...")
        #     # module.run(args.url, enum_data) 
        #     pass

if __name__ == "__main__":
    main()
