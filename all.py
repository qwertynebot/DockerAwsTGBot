import telebot
import docker
import boto3
import subprocess
import random
import string

bot = telebot.TeleBot("6455802370:AAFgm1yac0d5ywr3h3PUBfynHJprJi9pd78")
docker_client = docker.from_env()
region_name = 'eu-north-1'
aws_access_key = 'AKIAZJXJWEFKSLN5FGPK'
aws_secret_key = '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'
##################### ФУНКЦІЯ ВХОДУ
user_roles = {
    "111": "admin",
    "222": "docker_user",
    "333": "aws_user",
}
authenticated_users = set(user_roles) 

def is_authenticated(user_id):
    return str(user_id) in authenticated_users

@bot.message_handler(commands=['login'])
def handle_login(message):
    user_id = message.from_user.id
    if is_authenticated(user_id):
        bot.send_message(user_id, "Ви увійшли.")
    else:
        bot.send_message(user_id, "Будь-ласка введіть ваш айді:")
        bot.register_next_step_handler(message, authenticate_user)

def authenticate_user(message):
    user_id = message.from_user.id
    user_input = message.text

    if user_input in user_roles:
        authenticated_users.add(str(user_id))
        bot.send_message(user_id, "Ви увійшли.")
    else:
        bot.send_message(user_id, "Неправильний айді.Помилка.")

@bot.message_handler(func=lambda message: not is_authenticated(message.from_user.id))
def handle_unauthenticated(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть команду /login щоб залогінитись")

######################################## МОНІТОРИНГ ДОКЕРА
def monitor_docker_containers():
    containers = docker_client.containers.list()
    status_messages = []

    for container in containers:
        status = container.status
        container_name = container.name
        message = f"Контейнер {container_name} має статус: {status}"
        status_messages.append(message)

    return status_messages

######################################## МОНІТОРИНГ ЕС2
def monitor_ec2_instances(region_name, aws_access_key, aws_secret_key):
    ec2 = boto3.resource('ec2', region_name=region_name, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    instance_status_messages = []

    for instance in ec2.instances.all():
        instance_id = instance.id
        instance_state = instance.state['Name']
        message = f"EC2 інстанс {instance_id} має стан: {instance_state}"
        instance_status_messages.append(message)

    return instance_status_messages

#################################### КНОПКИ МЕНЮ
@bot.message_handler(commands=['start']) 
def handle_start(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    docker_button = telebot.types.KeyboardButton('Docker')
    ansible_button = telebot.types.KeyboardButton('Ансібл')
    ec2_button = telebot.types.KeyboardButton('EC2')
    notifications_button = telebot.types.KeyboardButton('Повідомлення') 
    markup.row(docker_button, ansible_button, ec2_button)
    
    markup.row(notifications_button) 
    bot.send_message(user_id, "Виберіть операцію:", reply_markup=markup)#ВИБІР ОПЕРАЦІЇ

######################################ПОВІДОМЛЕННЯ
@bot.message_handler(func=lambda message: message.text == 'Повідомлення')
def handle_notifications(message):
    user_id = message.from_user.id
    docker_status_messages = monitor_docker_containers()
    ec2_status_messages = monitor_ec2_instances(region_name, aws_access_key, aws_secret_key)
    
    if docker_status_messages:
        bot.send_message(user_id, "Статус контейнерів:\n" + "\n".join(docker_status_messages))
    else:
        bot.send_message(user_id, "Немає запущених контейнерів.")

    if ec2_status_messages:
        bot.send_message(user_id, "Статус EC2 інстансів:\n" + "\n".join(ec2_status_messages))
    else:
        bot.send_message(user_id, "Немає запущених EC2 інстансів.")


##################### DOCKER
@bot.message_handler(func=lambda message: message.text == 'Docker')
def docker_operations(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_container_button = telebot.types.KeyboardButton('Створити Docker контейнер')
    start_container_button = telebot.types.KeyboardButton('Запустити Docker контейнер')
    stop_container_button = telebot.types.KeyboardButton('Зупинити Docker контейнер')
    remove_container_button = telebot.types.KeyboardButton('Видалити Docker контейнер')
    markup.row(create_container_button)
    markup.row(start_container_button, stop_container_button)
    markup.row(remove_container_button)
    bot.send_message(user_id, "Виберіть операцію для Docker:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Створити Docker контейнер')#СТВОРЕННЯ КОНТЕЙНЕРА
def create_docker_container(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    random_name_button = telebot.types.KeyboardButton('З випадковим іменем')#З РАНДОМНИМ ІМ'ЯМ
    specify_name_button = telebot.types.KeyboardButton('Задати ім\'я')#З ЗАДАНИМ
    markup.row(random_name_button, specify_name_button)
    bot.send_message(user_id, "Оберіть, як створити контейнер:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_create_docker_container)

def handle_create_docker_container(message):
    user_id = message.from_user.id
    selected_option = message.text

    if selected_option == 'З випадковим іменем':
        container_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))  # Генерувати випадкове ім'я
    elif selected_option == 'Задати ім\'я':
        bot.send_message(user_id, "Введіть ім'я для контейнера:")
        bot.register_next_step_handler(message, handle_custom_container_name)
        return
    else:
        bot.send_message(user_id, "Неправильний вибір опції.")
        return

    try:
        container = docker_client.containers.run("ubuntu:latest", detach=True, name=container_name)
        if container_name:
            bot.send_message(user_id, f"Контейнер створено з іменем: {container_name}")
        else:
            bot.send_message(user_id, f"Контейнер створено з ID: {container.id}")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при створенні контейнера: {str(e)}")

def handle_custom_container_name(message):
    user_id = message.from_user.id
    container_name = message.text

    try:
        container = docker_client.containers.run("ubuntu:latest", detach=True, name=container_name)
        bot.send_message(user_id, f"Контейнер створено з іменем: {container_name}")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при створенні контейнера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Запустити Docker контейнер')#ЗАПУСК КОНТЕЙНЕРА
def start_container_button(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть ID контейнера, який ви хочете запустити:")
    bot.register_next_step_handler(message, handle_start_container)

def handle_start_container(message):
    user_id = message.from_user.id
    container_id = message.text

    try:
        container = docker_client.containers.get(container_id)
        container.start()
        bot.send_message(user_id, f"Контейнер {container_id} запущено")
    except docker.errors.NotFound:
        bot.send_message(user_id, f"Контейнер {container_id} не знайдено")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при запуску контейнера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Зупинити Docker контейнер')#ЗУПИНКА ДОКЕР КОНТЕЙНЕРА
def stop_container_button(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть ID контейнера, який ви хочете зупинити:")
    bot.register_next_step_handler(message, handle_stop_container)

def handle_stop_container(message):
    user_id = message.from_user.id
    container_id = message.text

    try:
        container = docker_client.containers.get(container_id)
        container.stop()
        bot.send_message(user_id, f"Контейнер {container_id} зупинено")
    except docker.errors.NotFound:
        bot.send_message(user_id, f"Контейнер {container_id} не знайдено")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при зупинці контейнера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Видалити Docker контейнер')#ВИДАЛЕННЯ ДОКЕР КОНТЕЙНЕРА
def remove_container_button(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть ID контейнера, який ви хочете видалити:")
    bot.register_next_step_handler(message, handle_remove_container)

def handle_remove_container(message):
    user_id = message.from_user.id
    container_id = message.text

    try:
        container = docker_client.containers.get(container_id)
        container.remove()
        bot.send_message(user_id, f"Контейнер {container_id} видалено")
    except docker.errors.NotFound:
        bot.send_message(user_id, f"Контейнер {container_id} не знайдено")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при видаленні контейнера: {str(e)}")


################## ANSIBLE
@bot.message_handler(func=lambda message: message.text == 'Ансібл')
def ansible_operations(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    configure_server_button = telebot.types.KeyboardButton('Налаштувати сервер')
    install_docker_button = telebot.types.KeyboardButton('Встановити Docker')
    markup.row(configure_server_button)
    markup.row(install_docker_button)
    bot.send_message(user_id, "Виберіть операцію для Ansible:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Налаштувати сервер')#СКРИПТ ДЛЯ БОТА №1
def configure_server(message):
    user_id = message.from_user.id
    try:
        subprocess.run(['ansible-playbook', 'configure_server.yml'])
        bot.send_message(user_id, "Сервер успішно налаштовано за допомогою Ansible.")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при налаштуванні сервера: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Встановити Docker')#СКРИПТ ДЛЯ БОТА №2
def install_docker(message):
    user_id = message.from_user.id
    try:
        subprocess.run(['ansible-playbook', 'install_docker.yml'])
        bot.send_message(user_id, "Docker успішно встановлено за допомогою Ansible.")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при встановленні Docker: {str(e)}")

#########################      EC2
ec2 = boto3.resource('ec2', region_name=region_name, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

@bot.message_handler(func=lambda message: message.text == 'EC2')
def ec2_operations(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_ec2_button = telebot.types.KeyboardButton('Створити EC2')
    start_ec2_button = telebot.types.KeyboardButton('Запустити EC2')
    stop_ec2_button = telebot.types.KeyboardButton('Зупинити EC2')
    terminate_ec2_button = telebot.types.KeyboardButton('Завершити EC2')
    markup.row(create_ec2_button, start_ec2_button)
    markup.row(stop_ec2_button, terminate_ec2_button)
    bot.send_message(user_id, "Виберіть операцію для EC2:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Створити EC2')#СТВОРЕННЯ ЕС2
def create_ec2_instance(message):
    user_id = message.from_user.id
    try:
        user_data_script = '''#!/bin/bash
                                sudo apt-get update -y
                                sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
                                curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
                                sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
                                sudo apt-get update -y
                                sudo apt-get install -y docker-ce
                                sudo usermod -aG docker $USER
                            '''
        instance = ec2.create_instances(
            ImageId='ami-0989fb15ce71ba39e',
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',
            KeyName='Kluc',
            SecurityGroups=['launch-wizard-2'],
            UserData=user_data_script,
        )
        bot.send_message(user_id, f"EC2 інстанс створено з ID: {instance[0].id}")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при створенні EC2: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Запустити EC2')#ЗАПУСК ЕС2
def request_start_ec2_instance(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть ідентифікатор EC2 інстанса, який ви хочете запустити:")#ВВДЕННЯ АЙДІ ІНСТАНСА
    bot.register_next_step_handler(message, start_ec2_instance)

def start_ec2_instance(message):
    user_id = message.from_user.id
    instance_id = message.text
    try:
        ec2_instance = ec2.Instance(instance_id)
        ec2_instance.start()
        bot.send_message(user_id, f"EC2 інстанс {instance_id} успішно запущено")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при запуску EC2 інстанса: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Зупинити EC2')#ЗУПИНКА ІНСТАНСА
def request_stop_ec2_instance(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть ідентифікатор EC2 інстанса, який ви хочете зупинити:")
    bot.register_next_step_handler(message, stop_ec2_instance)

def stop_ec2_instance(message):
    user_id = message.from_user.id
    instance_id = message.text
    try:
        ec2_instance = ec2.Instance(instance_id)
        ec2_instance.stop()
        bot.send_message(user_id, f"EC2 інстанс {instance_id} успішно зупинено")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при зупинці EC2 інстанса: {str(e)}")

@bot.message_handler(func=lambda message: message.text == 'Завершити EC2')#TERMINATE ІНСТАНС
def request_terminate_ec2_instance(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введіть ідентифікатор EC2 інстанса, який ви хочете завершити:")
    bot.register_next_step_handler(message, terminate_ec2_instance)

def terminate_ec2_instance(message):
    user_id = message.from_user.id
    instance_id = message.text
    try:
        ec2_instance = ec2.Instance(instance_id)
        ec2_instance.terminate()
        bot.send_message(user_id, f"EC2 інстанс {instance_id} успішно завершено")
    except Exception as e:
        bot.send_message(user_id, f"Помилка при завершенні EC2 інстанса: {str(e)}")


if __name__ == "__main__":
    bot.polling()
