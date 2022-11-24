import requests
import networkx as nx
import matplotlib.pyplot as plt

# nVuts2gGgNYmXX7esbRb
# 3b49eb533b49eb533b49eb53a13859335633b493b49eb5358781df12623abddaabc4d40

friends_address = 'https://api.vk.com/method/{}'.format('friends.get')
users_address = 'https://api.vk.com/method/{}'.format('users.get')

key = '3b49eb533b49eb533b49eb53a13859335633b493b49eb5358781df12623abddaabc4d40'


def my_request(friends_id):
    response = requests.get(
        url=friends_address, params={
            'user_id': friends_id,
            'access_token': key,
            'fields': 'nickname',
            'v': 5.131,
            'lang': 'ru'
        }
    ).json()['response']['items']

    friends_dict = {i['id']: i['last_name']+' '+i['first_name'] for i in response}

    return friends_dict


# print(my_request(523153163))

friends_dict = {}
friends_list = my_request(requests.get(url=users_address, params={
                'access_token': key,
                'user_ids': input(),
                'v': 5.131
            }).json()['response'][0]['id'])

for i in friends_list.keys():
    try:
        friends_dict[i] = my_request(i)
    except:
        pass

graph = nx.Graph()
graph.add_nodes_from(friends_list.values())

for i in friends_list.keys():
    if i in friends_dict.keys():
        for j in friends_list.keys():
            if j in friends_dict[i]:
                graph.add_edge(friends_list[i], friends_list[j])

nx.draw(graph, with_labels=True)
plt.show()
