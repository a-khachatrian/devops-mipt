FROM alpine:3.19

RUN apk add --no-cache nginx

RUN adduser -D -H -u 101 -s /sbin/nologin nginx || true

RUN mkdir -p /var/lib/nginx /var/log/nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/lib/nginx /var/log/nginx /var/cache/nginx && \
    chmod -R 755 /var/lib/nginx /var/log/nginx /var/cache/nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN chown nginx:nginx /etc/nginx/nginx.conf && \
    chmod 644 /etc/nginx/nginx.conf

EXPOSE 8080

USER nginx

CMD ["nginx", "-g", "daemon off;"] 