FROM nginx:1.12

#  default conf for proxy service
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx_proxy.conf /etc/nginx/nginx.conf

# Proxy configurations
COPY ./includes/ /etc/nginx/includes/
