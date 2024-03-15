import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

cookies_str = os.getenv('COOKIES')
cookies = {'MoodleSession': cookies_str}
# Базовый URL страницы с вопросами и вариантами ответов
print('Please enter test URL:')
base_url = input()


def save_question_and_answer(question, answer, filename='questions_and_answers.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
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


def send_question_to_chatGPT(question, options):
    prompt = " ".join([question, 'Варіанти відповідей:'] + options)
    save_question_and_answer(question=question, answer=options)
    print("Вопрос:", prompt)


def main():
    page_number = 0
    seen_questions = set()
    while page_number < 5:
        page_number += 1
        url = f'{base_url}&page={page_number}'

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
                send_question_to_chatGPT(question, answer_options)
        else:
            print("Ошибка при получении страницы:", response.status_code)
            break


if __name__ == "__main__":
    main()
