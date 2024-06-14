#!/bin/sh

# Your domain name (this will be provided by the CI/CD environment)
DOMAIN=$1

# Path to your nginx configuration file
NGINX_CONFIG="nginx/nginx.conf"

# Replace "localhost" with your domain name in nginx.conf
sed -i "s/server_name localhost;/server_name $DOMAIN;/g" $NGINX_CONFIG
