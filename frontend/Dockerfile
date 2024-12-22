FROM node:18 AS build

WORKDIR /app

COPY . .
RUN npm install --force
RUN npm install -g @quasar/cli

RUN test -f quasar.config.js || (echo "Error: quasar.config.js not found!" && exit 1)

RUN quasar build

FROM nginx:alpine
COPY --from=build /app/dist/spa /usr/share/nginx/html
RUN echo "server { listen 9000; root /usr/share/nginx/html; index index.html; location / { try_files \$uri \$uri/ /index.html; } }" > /etc/nginx/conf.d/default.conf

# Экспорт порта
EXPOSE 9000

# Команда для запуска Nginx
CMD ["nginx", "-g", "daemon off;"]


# # install simple http server for serving static content
# RUN npm install -g @vue/cli
#
# # make the 'app' folder the current working directory
# WORKDIR /app
#
# # copy both 'package.json' and 'package-lock.json' (if available)
# COPY package*.json ./
#
# # install project dependencies
# RUN npm install
#
# # copy project files and folders to the current working directory (i.e. 'app' folder)
# COPY . .
#
# # build app for production with minification
# RUN npm run build
#
# EXPOSE 8080
# CMD [ "http-server", "dist" ]