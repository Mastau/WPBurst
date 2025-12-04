import sys


#Default popularity (NEED TO REWORK, External db ? how to deteminate this) More the Weights is, more its a popularity plugin
POPULARITY_WEIGHTS = {
    "jetpack": 1.2,
    "woocommerce": 1.15,
    "contact-form-7": 1.1,
    "yoast-seo": 1.1,
    "akismet": 1.05,
    # Default wheights 
    "default": 1.0
}

class VulnerabilityScorer:
    """
    Calculate impact score & confidence score for a given CVE with more contextual factor (Signature, endpoints ect..)
    """

    def __init__(self, enum_data: dict):
        """Init scorer"""
        self.enum_data = enum_data

    def _get_plugin_popularity_weight(self, plugin_slug: str) -> float:
        """Return popularity weight"""
        return POPULARITY_WEIGHTS.get(plugin_slug, POPULARITY_WEIGHTS['default'])

    def _calculate_malus_incertitude(self, cve_result: dict) -> float:
        """
        Calculate malus based on incertitude

        - 0.0 : Confirmed version (ex: w/ readme.txt).
        - 1.5 : Version deducted (?? make sense) 
        - 3.0 : Plugin found but unknown version.
        """
        installed_version = cve_result.get("version")
        
        if installed_version is None:
            return 3.0
        
        return 0.5 

    def _calculate_contextual_bonus(self, cve_result: dict) -> float:
        """
        Calculate bonus based on signature & context
        
        Need this info from modules CVE
        """
        bonus = 0.0
        
        signature_score = cve_result.get("signature_match_score", 0.0)
        bonus += signature_score

        required_endpoint = cve_result.get("required_endpoint")
        
        if required_endpoint:
            rest_data = self.enum_data.get("rest_api", {})
            if required_endpoint in rest_data.get("valid_routes", []):
                print(f"[+] Context Bonus: Endpoint {required_endpoint} detected as VALID.")
                bonus += 2.0 
            else:
                pass 
        
        return bonus


    def calculate_score(self, cve_result: dict) -> float:
        """
        Main method for calculate impact score
        Args:
            cve_result: Dict return form 'check()'.
                        Need: 'cve', 'plugin', 'version', 'cvss'.
                        
        Returns:
            Final score (float).
        """
        
        cvss_base = cve_result.get("cvss")
        plugin_slug = cve_result.get("plugin")

        if cvss_base is None or plugin_slug is None:
            print(f"[!] Erreur de Scoring: CVE {cve_result.get('cve', 'N/A')} manque CVSS ou Plugin Slug.")
            return 0.0

        popularity_weight = self._get_plugin_popularity_weight(plugin_slug)
        base_score = cvss_base * popularity_weight
        contextual_bonus = self._calculate_contextual_bonus(cve_result)
        
        uncertainty_malus = self._calculate_malus_incertitude(cve_result)
        
        final_score = base_score + contextual_bonus - uncertainty_malus
        
        return max(0.0, round(final_score, 2)) # Minimum is 0.0 
