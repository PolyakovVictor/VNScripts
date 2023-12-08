import requests

login_url = 'http://virt.lac.lviv.ua/login/index.php'
data = {
    'username': 'c20-0712-006-02',
    'password': 'alivudfoa'
}

# Отправляем POST-запрос с данными для входа
response = requests.post(login_url, data=data)

# Проверяем успешность запроса и выводим содержимое
if response.ok:
    cookies = {
        'MoodleSession': response.cookies['MoodleSession']
    }
    print(cookies)
else:
    print("Ошибка при получении страницы:", response.status_code)