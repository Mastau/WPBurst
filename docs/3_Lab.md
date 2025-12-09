# Lab

The lab is a self-contained Docker environment designed for safely testing WPBurst.

## Docker Lab presentation

The lab typically uses Docker Compose to set up a complete and vulnerable WordPress instance (e.g., specific versions or plugins known for flaws).

## How to modify the Lab

1) `lab/docker-compose.yml` File: This file defines the Docker services. Modify actual services or add other services (database, proxy, etc.).

2) Plugin/Theme Injection: To test specific CVEs, you can use Docker volumes to mount specific versions of plugins/themes directly into `wp-content/` or adding `wp plugin install contact-form-7 --version=5.0.3 --activate --allow-root` in `lab/wordpress/init.sh`.