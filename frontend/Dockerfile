# syntax=docker/dockerfile:1

FROM nginx:1.27-alpine

# Copy Nginx config and static assets
COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 8080