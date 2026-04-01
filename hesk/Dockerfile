FROM php:8.2-apache

# Instalar dependencias necesarias + curl (IMPORTANTE para healthcheck)
RUN apt-get update && apt-get install -y \
    curl \
    libpng-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libzip-dev \
    unzip \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install mysqli gd zip \
 && a2enmod rewrite

# Copiar archivos de HESK
COPY . /var/www/html/

# Permisos
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80