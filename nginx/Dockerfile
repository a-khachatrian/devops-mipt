FROM alpine:3.20

RUN apk add --no-cache nginx && \
    addgroup -S nginxgroup && \
    adduser -S nginxuser -G nginxgroup && \
    mkdir -p /var/lib/nginx/tmp /var/log/nginx && \
    chown -R nginxuser:nginxgroup /var/lib/nginx /var/log/nginx /run/nginx
USER nginxuser

EXPOSE 80

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]