# Technical architecture

## Global architecture

WPBurst follows a modular architecture based on three stages: Collection (Enumeration), Analysis (CVE Check), and Reporting.

## Component Description

| Component          | Role                                                                                   | Files                 |
|--------------------|----------------------------------------------------------------------------------------|-----------------------|
| `WPEnumerator` Class | Handles HTTP communication,  fingerprinting, and multi-threaded enumeration methods. | `core/enumeration.py` |
| CVE Engine         | Discovers, loads, and executes CVE modules.                                            | `core/cve_engine.py`  |
| CVE Modules        | Autonomous Python files for checking and exploiting specific vulnerabilities.          | `modules/*.py`        |
| CLI (Main)         | Entry point, argument parsing, orchestration.                                          | `cli/main.py `        |

## Execution flow

1) The CLI initializes a WPEnumerator instance with the target URL.
2) The CLI calls the enumeration methods (`enumerate_plugins`, `get_version`, etc.).
3) WPEnumerator uses `concurrent.futures.ThreadPoolExecutor` to perform parallel HTTP requests.
4) The enumeration results (e.g., list of plugins and versions) are aggregated into a dictionary.
5) The aggregated data is passed to the CVE Engine.
6) The CVE Engine loads the CVE Modules and executes their `check()` function.
7) Vulnerability findings are consolidated and presented to the user.

## Exchanged data

The central data structure exchanged between the Core and the CVE Engine is an enumeration dictionary (e.g., `enum_data`):

```Json
{
    "plugins": {
        "akismet": "5.5",
        "contact-form-7": "5.0.3"
    },
    "themes": [
        "twentytwentyfive"
    ],
    "users": [
        "admin"
    ],
    "rest": {
        "root_available": true,
        "namespaces": [
            "oembed/1.0",
            "contact-form-7/v1",
            "wp/v2",
            "wp-site-health/v1",
            "wp-block-editor/v1"
        ],
        "routes": [
            "/",
            "/batch/v1",
            "/oembed/1.0",
            "/oembed/1.0/embed",
            "/oembed/1.0/proxy",
            "/contact-form-7/v1",
            "/contact-form-7/v1/contact-forms",
            "/contact-form-7/v1/contact-forms/(?P<id>\\d+)",
            "/contact-form-7/v1/contact-forms/(?P<id>\\d+)/feedback",
            "/contact-form-7/v1/contact-forms/(?P<id>\\d+)/refill",
            "/wp/v2",
            "/wp/v2/posts",
            "[...]",
            "/wp/v2/themes",
        ],
"valid_routes": [
            "/",
            "/oembed/1.0",
            "/contact-form-7/v1",
            "/wp/v2",
            "/wp/v2/posts",
            "[...]",
            "/wp-block-editor/v1"
        ],
        "invalid_routes": [
            "/batch/v1",
            "/oembed/1.0/embed",
            "/oembed/1.0/proxy",
            "[...]",
            "/wp/v2/font-collections",
            "/wp/v2/font-collections/(?P<slug>[\\/\\w-]+)"
        ],
        "errors": []
    }
}
```