# Клара

[![](https://img.shields.io/github/license/montenegroit/pocisti_bot)]()
[![](https://badges.aleen42.com/src/telegram.svg)](https://t.me/montenergo_it) 

Документация будет написана, как только кому-нибудь одному она понадобится, пишите в личку https://t.me/i63PHC

[![](https://img.shields.io/github/contributors/montenegroit/pocisti_bot)]()
[![](https://img.shields.io/github/issues-raw/montenegroit/pocisti_bot)]() 
* [Кто такая Клара?]()
* [Как начать пилить фичи?]()
  * [Новая команда?]()
  * [Новая команда для донатеров?]()
  * [Как испльзовать бд?]()
  * [Новый сервис?]()
* [Как развернуть локально?](#quickstart)
  * [Установка докера]()
* [Как задеплоить?]()
* [Как тестировать?]()
* [Что если у меня есть идея, но я не программист?]()
* [Contributing]()


### Quickstart


```
cp .env.example .env
# add BOT_TOKEN
docker-composer -f docker-compose.dev.yml up -d
```

Чтобы оперативно рестартовать контейнер backend при изменениях можно поставить на локальный хост `nodemon` (`npm install --global nodemon`) и использовать его для мониторинга изменений в python-файлах:
```
nodemon --watch ./bot --ext py --exec 'docker-compose restart backend'
```

[![](https://badges.aleen42.com/src/buymeacoffee.svg)]()
