TelegramBot
Проєкт Telegram бота для керування Docker контейнерами, AWS EC2 і Ansible операціями.

Опис
Цей проєкт включає в себе Telegram бота, який надає користувачам можливість керування Docker контейнерами, AWS EC2 і виконувати Ansible операції.

Функціональність
Docker Операції
Створення Docker контейнера (з випадковим або вказаним іменем).
Запуск, зупинка та видалення Docker контейнера.
Перегляд статусу запущених Docker контейнерів.
Ansible Операції
Налаштування сервера за допомогою Ansible playbook.
Встановлення Docker на сервері за допомогою Ansible playbook.
EC2 Операції
Створення, запуск, зупинка та завершення EC2 інстансів.
Використання Ansible для конфігурації EC2 інстансів.
Вимоги
Python 3.x
Бібліотеки: telebot, docker, boto3
Налаштування
Для коректної роботи бота необхідно вказати токен для Telegram бота, ключі доступу до AWS, та інші параметри.

python
Copy code
bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
Використання
Запустіть файл main.py. Бот буде готовий до прийому команд в чаті Telegram.

Внесок
Якщо у вас є ідеї для вдосконалення цього бота, будь ласка, робіть внесок через pull requests. Ваш внесок важливий для розвитку цього проєкту.Заголовок проєкту
Проєкт Telegram бота для керування Docker контейнерами, AWS EC2 і Ansible операціями.

Опис
Цей проєкт включає в себе Telegram бота, який надає користувачам можливість керування Docker контейнерами, AWS EC2 і виконувати Ansible операції.

Функціональність
Docker Операції
Створення Docker контейнера (з випадковим або вказаним іменем).
Запуск, зупинка та видалення Docker контейнера.
Перегляд статусу запущених Docker контейнерів.
Ansible Операції
Налаштування сервера за допомогою Ansible playbook.
Встановлення Docker на сервері за допомогою Ansible playbook.
EC2 Операції
Створення, запуск, зупинка та завершення EC2 інстансів.
Використання Ansible для конфігурації EC2 інстансів.
Вимоги
Python 3.x
Бібліотеки: telebot, docker, boto3
Налаштування
Для коректної роботи бота необхідно вказати токен для Telegram бота, ключі доступу до AWS, та інші параметри.

python
Copy code
bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
Використання
Запустіть файл main.py. Бот буде готовий до прийому команд в чаті Telegram.

Внесок
Якщо у вас є ідеї для вдосконалення цього бота, будь ласка, робіть внесок через pull requests. Ваш внесок важливий для розвитку цього проєкту.
