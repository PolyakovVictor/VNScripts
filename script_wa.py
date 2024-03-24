import requests
import os
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

cookies_str = os.getenv('COOKIES')
cookies = {'MoodleSession': cookies_str}
# Базовый URL страницы с вопросами и вариантами ответов
print('Please enter test URL:')
base_url = input()


def save_question_and_answer(question, answer, page_number, filename='questions_and_answers.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(str(page_number) + '\n')
        file.write(question + '\n')
        file.write('\n'.join(answer) + '\n\n')


def get_question_and_answer(soup):
    # Находим блок с вопросом
    question_block = soup.find('div', class_='formulation clearfix')

    # Получаем текст вопроса
    question = question_block.find('div', class_='qtext').text.strip()

    # Находим блок с вариантами ответов
    answers_block = question_block.find('div', class_='answer')

    # Получаем список вариантов ответов
    answer_options = [answer.text.strip() for answer in answers_block.find_all('label')]

    return question, answer_options


def send_question_to_chatGPT(question, options, page_number):
    prompt = " ".join([question, 'Варіанти відповідей:'] + options)
    save_question_and_answer(question=question, answer=options, page_number=page_number)
    print("Вопрос:", prompt)


def main():
    start_page = int(input('Enter start page:'))
    finish_page = int(input('Enter finish page:'))
    seen_questions = set()
    while start_page <= finish_page:
        time.sleep(1)
        url = f'{base_url}&page={start_page-1}'
        print(url)
        response = requests.get(url, cookies=cookies, allow_redirects=True)

        # Проверяем успешность запроса
        if response.status_code == 200:
            print('200')
            # Создаем объект BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            question, answer_options = get_question_and_answer(soup)
            if question in seen_questions:
                print("Обнаружено повторение вопроса:", question)
                break
            else:
                seen_questions.add(question)
                send_question_to_chatGPT(question, answer_options, start_page)
        else:
            print("Ошибка при получении страницы:", response.status_code)
            break

        start_page += 1

if __name__ == "__main__":
    main()
