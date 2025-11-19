#!/bin/sh
set -e

cd /var/www/html

wp() {
    php -d memory_limit=-1 /usr/local/bin/wp "$@"
}

echo "Waiting for MariaDB..."
until nc -z mariadb 3306; do
    sleep 1
done
echo "MariaDB is up!"

if [ ! -f wp-config.php ]; then
    echo "Downloading WordPress..."
    wp core download --allow-root

    wp config create \
        --dbname="$DB_NAME" \
        --dbuser="$DB_USER" \
        --dbpass="$DB_PASS" \
        --dbhost="$DB_HOST" \
        --allow-root

    wp core install \
        --url="http://localhost" \
        --title="MonSite" \
        --admin_user="$WP_USER" \
        --admin_password="$WP_PASS" \
        --admin_email="admin@example.com" \
        --allow-root
fi

wp plugin install contact-form-7 --version=5.0.3 --activate --allow-root

exec "$@"

