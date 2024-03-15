import requests
from bs4 import BeautifulSoup
import json

# Функция для отправки вопросов и вариантов ответов


def save_question_and_answer(question, answer, filename='questions_and_answers.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(question + '\n')
        file.write('\n'.join(answer) + '\n\n')


def send_question_to_chatGPT(question, options):
    # Здесь можно реализовать отправку вопроса и вариантов ответов куда-либо,
    # например, через API или как угодно, в зависимости от вашего интерфейса с мной
    # В этом примере просто печатаем вопрос и варианты ответов
    save_question_and_answer(question=question, answer=options)


def write_to_file(data):
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(data)


login_url = 'http://virt.lac.lviv.ua/login/index.php'  # Замените на URL страницы входа


data = {
    'username': 'c20-0712-006-02',
    'password': 'alivudfoa'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'  # Устанавливаем Content-Type
}


response = requests.post(login_url, data=data, headers=headers, allow_redirects=True)

print('here 3', response.content)
if response.history:
    # Получаем окончательный ответ после перенаправления
    final_response = response.history[0]

    # Извлекаем файлы cookie из окончательного ответа
    cookies = final_response.cookies
else:
    # Перенаправления не было, извлекаем файлы cookie из первоначального ответа
    cookies = response.cookies


soup = BeautifulSoup(response.content, 'html.parser')
print('here 1', cookies)


# URL страницы с вопросами и вариантами ответов
url = 'http://virt.lac.lviv.ua/mod/quiz/attempt.php?attempt=1056132&page=25'  # Замените на реальный URL


# with open(url, 'r', encoding='utf-8') as file:
#     html_content = file.read()
if response.ok:
    # Отправляем GET-запрос к странице
    cookie_str = '; '.join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    print('here 2', cookie_str)
    cookies = {cookie_str.split('=')[0]: cookie_str.split('=')[1]}
    response = requests.get(url, cookies=cookies, allow_redirects=True)

    # Проверяем успешность запроса
    if response.status_code == 200:
        print('200')
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        write_to_file(soup.prettify())
        # soup = BeautifulSoup(html_content, 'html.parser')

        # Находим блок с вопросом
        question_block = soup.find('div', class_='formulation clearfix')
        print('question_block', question_block)

        # Получаем текст вопроса
        question = question_block.find('div', class_='qtext').text.strip()

        # Находим блок с вариантами ответов
        answers_block = question_block.find('div', class_='answer')

        # Получаем список вариантов ответов
        answer_options = [answer.text.strip() for answer in answers_block.find_all('label')]

        send_question_to_chatGPT(question, answer_options)

# else:
#     print("Ошибка при получении страницы:", response.status_code)
