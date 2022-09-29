import requests
import json

# https://oauth.vk.com/authorize?client_id=51435525&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131

try:
    with open('vk_token.json') as file:
        try:
            access_token = json.load(file)['key']
        except json.decoder.JSONDecodeError:
            print('Vk токен не найден!')
except FileNotFoundError:
    with open('vk_token.json', 'w') as file:
        print('Создан файл vk_token.json')


def get_users_id(id):
    url = 'https://api.vk.com/method/{}'.format('users.get')
    response = requests.get(url, params={'user_ids': id,
                                         'fields': 'schools,occupation',
                                         'access_token': access_token, 'v': 5.131}).json()
    #print(response)
    return response['response']

def main():
    url = 'https://api.vk.com/method/{}'.format('friends.get')
    user = get_users_id(input())[0]
    response = requests.get(url, params={'user_id': user['id'],
                                         'count': 1000, 'access_token': access_token, 'v': 5.131}).json()
    print('У пользователя {} {} найдено {} друзей'.format(user['first_name'], user['last_name'], response['response']['count']))
    print('-'*30)

    friends_list = ','.join(list(map(str, response['response']['items'])))
    friends_list = get_users_id(friends_list)

    count = 1
    flag = False
    s = '''Алдохина Таисия (6)

Ахметшина Анна

Бахтеева Ольга

Былкина Александра

Герасимов Лев

Иванов Кирилл

Ковязина Софья (6)

Литкенс Дарья

Лучинец София

Максаков Иван

Мительмайер Максим

Михайлов Тимур

Моржаков Иван

Нахманович Дмитрий

Нестерская Варвара

Орлова Мария

Паршин Федор

Пашлова Алина

Петрова Дарья

Пивоваров Андрей

Попов Иван

Попова Наталья

Сенютина Надежда

Солодов Дмитрий

Стукалов Иван 

Фролова Полина

Шрейбер Ольга

Яворский Михаил

Яковлева Таисия

Антипов Антон 

Антонова Анна 

Афанасьева Варвара 

Беспалова Варвара 

Болтовский Глеб (6)

Воробьев Николай 

Глебов Илья 

Дмитриев Алексей 

Ионова Анастасия 

Кисилев Артем (6)

Коногоров Александр (6)

Лукашук Леонид 

Маракова Дарья 

Мелехова Полина 

Минеева Софья (7)

Моденов Максим 

Никоян Артем (7)

Пуляев Тихон 

Руденко Глеб 

Савинская Анна 

Сенюков Виктор 

Тюшагина Светлана 

Фильчаков Петр (6)

Храмова Дарья 

Храпова Екатерина 

Чеснокова Софья 

Чупрова Надежда 

Шаров Максим 

Шевченко Фея (7)

Беляков Александр

Белякова Ольга

Бунтман Лев

Бурлаков Максим

Васильева Мария

Горенко Денис

Демкин Георгий

Денисьев Артём

Дремов Никита

Комиссарова Арина (6)

Кудрявцева Лидия (7)

Лукьянова Анна

Ляховец Надежда

Маликова Анна

Март Мишель

Никорук Михаил

Полежаев Леонид

Полинский Алексей (6)

Пэн Цзинни

Рафиков Тимур

Стрижкова Алиса

Сунцов Павел

Ушакова Ульяна (7)

Фетисова София

Филатова Наталья

Хома Кирилл

Чебанова Полина 

Янышев Егор

Артамонов Максим

Белова Мария (7)

Бочарова Ольга

Быков Степан

Гладун Владимир

Голомыслова Мария (6)

Гутник Петр

Дудка Варвара (6)

Зотова Вероника

Кошелева Юлия (7)

Крючков Илья

Кушнир Алексей (6)

Любченко Анастасия

Максимова Софья

Овчаренко Елизавета

Осин Иван

Паленова Ульяна

Парфенова Дарья

Пищелко Полина

Прокошева Зоя

Рахимов Амир

Симонов Михаил

Синкин Роман

Старых Елизавета

Тимофеева Софья (6)

Трофименко Алена

Харитонов Дмитрий

Чиджиева Бадма

Чиркина Александра
'''

    for i in friends_list:
        schools = []
        if 'deactivated' not in i.keys():
            if not i['is_closed']:
                if 'occupation' in i.keys():
                    schools += [i['occupation']['name']]

                if 'schools' in i.keys():
                    schools += [j['name'] for j in i['schools']]

                schools = ', '.join(schools)

                if '1543' in schools if flag else True:
                    print('{}. [https://vk.com/id{}] {} - [{}] - {}'.format(count, i['id'],
                        '\033[33m'+i['last_name']+' '+i['first_name']+'\033[0m' if i['last_name']+' ' in s else i['last_name']+' '+i['first_name'], schools, i['id']))
                    count+=1

if __name__ == '__main__':
    main()