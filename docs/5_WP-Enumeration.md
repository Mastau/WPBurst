# WP Enumeration

## How it works

The `WPEnumerator` class is the reconnaissance engine.

1) `_get(path)`: Wrapper function for requests.get, managing the full URL and a standard timeout (7s).
2) `_fingerprint(text)` / `_get_home_fingerprint()`: Calculates a unique digital fingerprint for the homepage (length + MD5 hash of the content).
3) `_is_homepage_like(response)`: Used to determine if a request to an unknown path (e.g., /wp-content/plugins/unknown_plugin/) returns the homepage content (often due to misconfigured permalinks/404 handling) instead of a true 404. This is crucial for avoiding false positives during fuzzing.

## Enumeration strategy

| Target     | Strategy                                                                                               | Method               |
|------------|--------------------------------------------------------------------------------------------------------|----------------------|
| WP Version | Try `/wp-json` (`generator` field), search for the `meta name="generator"` tag in HTML or read  readme.html. | `get_version()`        |
| Plugins    | Multithreading to check for the existence of directories from a wordlist (`/wp-content/plugins/SLUG/`).  | `enumerate_plugins()`  |
| Endpoints  | Try `/wp-json` (`namespace` field) and try each routes                                                     | `enumerate_rest_api()` |
| Themes     | Scan the homepage source code for paths (`wp-content/plugins/SLUG/`)                                     | `enumerate_themes()`   |
| Users      | Attempt to access `/?author=ID` (for ID from 1 to limit). WordPress redirects to `/author/USERNAME/`.      | `enumerate_users()`    |


## Plugin and Version Extraction

- Plugin Extraction (Phase 1): The `_check_plugin_dir()` method uses multithreading to check if `/wp-content/plugins/{plugin}/` returns a `200` status code and does not match the homepage fingerprint.
- Version Extraction (Phase 2): For each found plugin, a sequential request is made to `/wp-content/plugins/{plugin}/readme.txt`. The `_extract_version_from_readme()` function uses regular expressions to find `Stable tag:` or `Version:`.