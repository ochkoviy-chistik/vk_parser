import requests
import json

# https://oauth.vk.com/authorize?client_id=51435525&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131

class Color:
    def __init__(self, string):
        self.string = string

    def yellow(self):
        return '\033[38;2;255;255;0m'+self.string+'\033[0;0m'

    def green(self):
        return '\033[38;2;0;255;0m'+self.string+'\033[0;0m'

    def blue(self):
        return '\033[38;2;0;255;255m'+self.string+'\033[0;0m'

    def red(self):
        return '\033[38;2;255;0;0m'+self.string+'\033[0;0m'


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

    for i in range(len(friends_list)):
        for j in range(i, len(friends_list)):
            if friends_list[i]['last_name'] > friends_list[j]['last_name']:
                friends_list[i], friends_list[j] = friends_list[j], friends_list[i]

    count = 1
    flag = False

    with open('marked.json', 'r') as f:
        s = json.load(f)

    for i in friends_list:
        schools = []
        if 'deactivated' not in i.keys():
            if True:
                if 'occupation' in i.keys():
                    schools += [i['occupation']['name'].strip()]

                if 'schools' in i.keys():
                    schools += [j['name'].strip() for j in i['schools']]

                schools = ', '.join(schools)

                if '1543' in schools if flag else True:
                    if i['last_name'] in s.keys():
                        if i['first_name'] == s[i['last_name']]:
                            marked = Color(i['last_name'] + ' ' + i['first_name']).yellow()
                        else:
                            marked = Color(i['last_name'] + ' ' + i['first_name']).blue()
                    else:
                        marked = Color(i['last_name'] + ' ' + i['first_name']).string

                    print('{}. [https://vk.com/id{} - {}] {} - [{}] - {}'.format(count, i['id'], Color('Закрытый').red() if i['is_closed'] else Color('Открытый').green(),
                         marked, schools, i['id']))
                    count+=1

if __name__ == '__main__':
    main()
