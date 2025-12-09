# Technical Documentation - WPBurst
## Intro/Overview

### Project Vision

WPBurst is an open-source Command Line Interface (CLI) tool designed for the security auditing of WordPress installations. Its primary goal is to perform fast and reliable enumeration of components (WP version, plugins, themes, users, REST API) to identify known vulnerabilities (CVEs). The tool focuses on performance through multithreading and modularity for easy maintenance of vulnerability checks.

### Technical Objectives

- Performance: Utilization of concurrency (via `concurrent.futures.ThreadPoolExecutor`) to execute thousands of HTTP requests rapidly.
- Reliable Enumeration: Employment of fingerprinting techniques to differentiate a standard 404 error from a default homepage, which is crucial for directory fuzzing.
- Modularity: A CVE module system allowing for the addition or updating of vulnerability checks without modifying the core tool.

### General Architecture

WPBurst's architecture is split into two main components:
1) The Core: Contains the WPEnumerator class for HTTP interaction, target enumeration, and base logic (fingerprinting, error handling).
2) The Vulnerability Engine (CVE Engine): Manages the automatic loading of CVE modules and the execution of passive/active checks on the enumerated data.

### Target Audience

This tool is primarily aimed at security professionals (Pentesters, Red Teamers, Auditors) and Developers seeking to verify the security posture of their own WordPress installations.