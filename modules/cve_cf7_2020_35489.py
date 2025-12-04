# modules/cve_cf7_2018_20979.py
# first version of a module

CVE_ID = "CVE-2020-35489"
DESCRIPTION = "Contact Form 7 < 5.3.2 - Unrestricted File Upload"
PLUGIN_SLUG = "contact-form-7"
VULN_MAX_VERSION = "5.3.1"
CVSS = 9.8


# ------------- Version helpers -------------------------------------------

def _parse_version(v: str):
    if not v:
        return None
    result = []
    for part in v.split("."):
        try:
            result.append(int(part))
        except ValueError:
            break
    while len(result) < 3:
        result.append(0)
    return tuple(result[:3])


def _is_vulnerable_version(v):
    pv = _parse_version(v)
    vmax = _parse_version(VULN_MAX_VERSION)
    if not pv or not vmax:
        return False
    return pv <= vmax


# ------------- PASSIVE CHECK ----------------------------------------------

def check(enum_data):
    """Passive detection"""

    plugins = enum_data.get("plugins", {})
    if PLUGIN_SLUG not in plugins:
        return None

    installed = plugins.get(PLUGIN_SLUG)

    if installed is None:
        return {
            "cve": CVE_ID,
            "plugin": PLUGIN_SLUG,
            "version": None,
            "vulnerable": None,
            "details": "Version unknown; manual investigation required."
        }

    if _is_vulnerable_version(installed):
        signature_score = 4.0 
        required_endpoint = None
        return {
            "cve": CVE_ID,
            "plugin": PLUGIN_SLUG,
            "cvss": CVSS,
            "version": installed,
            "vulnerable": True,
            "details": f"{installed} <= {VULN_MAX_VERSION}",
            "required_endpoint": required_endpoint, 
            "signature_match_score": signature_score
            }

    return None


# ------------- OPTIONAL ACTIVE RUN ----------------------------------------

def run(target_url, enum_data):
    """
    OPTIONAL exploitation. (Insert PoC here)
    """

    result = check(enum_data)

    if not result or not result.get("vulnerable"):
        print(f"[+] {CVE_ID}: Not vulnerable -> nothing to exploit.")
        return

    #For example > say something
    print(f"[!] {CVE_ID} detected BUT:")
    print("    - This vulnerability requires a contributor account.")
    print("    - It cannot be exploited anonymously.")
    print("    - No remote PoC applicable.")
    print("    -> Use the passive detection only.")


