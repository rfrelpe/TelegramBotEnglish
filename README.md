# TelegramBotEnglish

Реализован функциональный телеграм бот согласно тз:
- Кастомная клавиатура с 6 функциональными кнопками:
  - Запуск режима "ru -> en"
  - Запуск режима "en -> ru"
  - Информация о боте, где указан создатель и ссылка на vk
  - Информация о статистике пользователя
  - __В режиме тренировки:__ кнопка пропуска слова
  - __В режиме тренировки:__ кнопка окончания тренировки
- В режиме *тренировки* бот выводит русские или английские случайные слова для их перевода пользователем на другой язык. За правильно переведённые слова пользователь получает очки.
- В файле .pickle хранятся записанные очки для всех когда-либо использовавших бот пользователей. Обновление файла происходит каждый раз, когда какой-либо из пользователей смотрит свою статистику.
- Слова для перевода берутся из библиотеки RandomWords. Проверка осуществляется с помощью перевода Google Translate библиотекой googletrans.
- Слова для перевода __подсвечиваются жирным__ для чёткости.

Из минусов бота:
- Библиотека RandomWords содержит большое количество очень сложных слов, так что данный бот будет полезен разве что осваивающим уровень С2
- В ходе проверки и генерации русских слов бот обращается к API Google Translate, что иногда может занимать до 5-7 секунд (при перегенерации совсем сложных слов). В среднем 1-2 секунды.
- Написан без использования ООП с глобальными переменными и функциональщиной. Отмечу, запихнуть весь код в один класс не представляет особой сложности, мне просто было лень, каюсь. PEP8 вроде выдержал.
