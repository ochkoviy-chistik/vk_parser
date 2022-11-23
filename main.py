import requests
import networkx as nx
import matplotlib.pyplot as plt

# nVuts2gGgNYmXX7esbRb
# 3b49eb533b49eb533b49eb53a13859335633b493b49eb5358781df12623abddaabc4d40

address = 'https://api.vk.com/method/{}'.format('friends.get')
key = '3b49eb533b49eb533b49eb53a13859335633b493b49eb5358781df12623abddaabc4d40'


def my_request(friends_id):
    response = requests.get(
        url=address, params={
            'user_id': friends_id,
            'access_token': key,
            'fields': 'nickname',
            'v': 5.131
        }
    ).json()['response']['items']

    friends_dict = {i['id']: i['last_name']+' '+i['first_name'] for i in response}

    return friends_dict


# print(my_request(523153163))

friends_dict = {}
friends_list = my_request(input())

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
