# Internal API (Code Reference)

`WPEnumerator` Class (`core/enumeration.py`)

| Method | Description                                                                                                          |
|--------|----------------------------------------------------------------------------------------------------------------------|
| `__init__(base_url)`                 | Initializes the target URL, the requests session, and the thread pool size (`self.max_workers=10`). |
| `_get(path)`                         | Secure HTTP GET request wrapper (with timeout). |
| `_fingerprint(text)`                 | Calculates the page fingerprint (length + MD5). |
| `_is_homepage_like(response)`        | Checks if an HTTP response is a false 404/redirect to the homepage. |
| `detect_wordpress()`.                | Attempts to confirm the presence of WordPress. |
| `enumerate_plugins(wordlist)`        | Key Method. Executes the multi-threaded plugin enumeration. |
| `_check_plugin_dir(plugin)`          | Worker for the thread pool: checks the existence of a single plugin directory. |
| `_extract_version_from_readme(text)` | Uses RegEx to extract the version from a readme.txt |
