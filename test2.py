import requests
from bs4 import BeautifulSoup

# Функция для отправки вопросов и вариантов ответов


def send_question_to_chatGPT(question, options):
    # Здесь можно реализовать отправку вопроса и вариантов ответов куда-либо,
    # например, через API или как угодно, в зависимости от вашего интерфейса с мной
    # В этом примере просто печатаем вопрос и варианты ответов
    print("Вопрос:", question)
    print("Варианты ответов:", options)


def write_to_file(data):
    with open('index.html', 'w') as file:
        file.write(data)


login_url = 'http://virt.lac.lviv.ua/login/index.php'  # Замените на URL страницы входа


data = {
    'username': 'c20-0712-006-02',
    'password': 'alivudfoa'
}


response = requests.post(login_url, data=data)
cookies = response.cookies
soup = BeautifulSoup(response.content, 'html.parser')
write_to_file(soup.prettify())
print(cookies)


# URL страницы с вопросами и вариантами ответов
url = 'http://virt.lac.lviv.ua/mod/quiz/attempt.php?attempt=1056132&page=25'  # Замените на реальный URL


# with open(url, 'r', encoding='utf-8') as file:
#     html_content = file.read()
if response.ok:
    # Отправляем GET-запрос к странице
    response = requests.get(url, cookies=cookies)
    print(response.cookies)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
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
