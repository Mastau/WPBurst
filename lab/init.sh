#!/bin/bash
set -e

echo "Waiting for database..."
until mysqladmin ping -h"$WORDPRESS_DB_HOST" --silent; do
  sleep 2
done

if ! wp core is-installed --allow-root; then
  echo "Installing WordPress..."
  wp core install \
    --url="http://localhost:4080" \
    --title="Mon WP préinstallé" \
    --admin_user="admin" \
    --admin_password="adminpass" \
    --admin_email="admin@example.com" \
    --skip-email \
    --allow-root

  wp plugin install classic-editor --activate --allow-root
  wp plugin install wordfence --activate --allow-root

  wp theme install twentytwentythree --activate --allow-root

  echo "Wordpress installed"
else
  echo "WordPress already install"
fi

