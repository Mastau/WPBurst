FROM wordpress:php8.3-fpm

RUN apt-get update \
    && apt-get install -y curl less mariadb-client netcat-openbsd \
    && docker-php-ext-install opcache \
    && curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    && chmod +x /usr/local/bin/wp

COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

ENTRYPOINT ["/usr/local/bin/init.sh"]
CMD ["php-fpm"]

