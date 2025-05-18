FROM alpine:3.20 AS build

RUN apk add --no-cache nodejs npm

WORKDIR /app
COPY . .

RUN npm ci --omit=dev && \
    npm run build

FROM alpine:3.20

COPY --from=build /app/build /usr/share/nginx/html

RUN apk add --no-cache nginx && \
    addgroup -S frontgroup && \
    adduser -S frontuser -G frontgroup && \
    mkdir -p /var/lib/nginx/tmp /var/log/nginx && \
    chown -R frontuser:frontgroup /var/lib/nginx /var/log/nginx /run/nginx
USER frontuser

EXPOSE 3000

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
