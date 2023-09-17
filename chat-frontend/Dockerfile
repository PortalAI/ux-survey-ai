# build environment
FROM node:14.17-alpine as build
WORKDIR /app
COPY . .
RUN yarn
RUN yarn build

# production environment
FROM nginx:stable-alpine
#COPY /build /usr/share/nginx/html
COPY --from=build /app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
