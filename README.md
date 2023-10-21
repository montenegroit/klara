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



Бот Клара 
https://github.com/montenegroit/klara
деплой по gha (secrets KLARA_…)
ssh pasha@94.24.248.254 -p 2102


! функционал бота пользуют только донатеры
OK
weather
help
prompt

TODO

восстановить бан
donate через https://github.com/montenegroit/donate-crypto/
Призыв к донатам надо подумать как организовать
https://python.langchain.com/docs/use_cases/chatbots/
https://github.com/gkorepanov/whisper-stream
events

Удалять системные сообщения  (входе, выход) 
Свой тест-валидация на входе 
Commands
Вот список моих команд:
  klara help, ... - Получить данное сообщение  (короткая команда kh)
  klara ban                                                             (короткая команда kb)
  klara events ..., ---> events week                       (короткая команда ke)

  
Список команд для донатеров:
  klara prompt, ... описание на англ - генератор изображения по тексту со stable diffusion        (короткая команда kp)

  klara answer me, ...  --> "promt" +  ... -->> gpt ---> answer (короткая команда ka)


SuperAdmin
  klara go quiz  -DB-qa-->  ban - 1 day (короткая команда kq)

  klara donate  (see https://github.com/montenegroit/donate-crypto/) (короткая команда kd)



ChatGPT
Между тем, уже месяц существует репозиторий,  GPT4Free (https://github.com/xtekky/gpt4free), где студент  нашел как прокидывать запросы к GPT-4 и GPT-3.5 и получать ответы бесплатно.  Запросы пропускаются через сайты, которые платят за доступ к GPT API, но не защитили свои собственные API. Среди таких лопухов: You.com, Quora, Bing, forefront.ai.

Пример кода, чтобы бесплатно обратиться к GPT-4:

from gpt4free import forefront
# create an account
token = forefront.Account.create(logging=False)
print(token)
# get a response
for response in forefront.StreamingCompletion.create(
 token=token,
 prompt='hello world',
 model='gpt-4'
):
    print(response.choices[0].text, end='')
print("")


Не знаю, как скоро эту лазейку прикроют. Но OpenAI уже пригрозили студенту подать на него в суд, если он не удалит репозиторий.

@ai_newz
У меня есть ключи на ГПТ-4



