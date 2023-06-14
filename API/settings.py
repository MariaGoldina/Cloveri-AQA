import os


url_node = os.environ.get('URL_NODE')
url_nodes = os.environ.get('URL_NODES')


# Локальный сервер
# url_node = "http://127.0.0.1:8000/api/v1/node/"
# url_nodes = "http://127.0.0.1:8000/api/v1/nodes/"
# Тестовый сервер
# url_node = "https://api.cloveri.skroy.ru/api/v1/node/"
# url_nodes = "https://api.cloveri.skroy.ru/api/v1/nodes/"
project_id = '3e3028cd-3849-461b-a32b-90c0d6411daa'
item_type = 'orgstructureM'
item = 'pytest'
other_project_id = '00000000-0000-0000-0000-0000000000ba'
other_item_type = 'note'
other_item = 'project1'
nonexistent_project_id = '11111111-3849-461b-a32b-11111111111a'
nonexistent_item_type = 'tasks'
nonexistent_item = 'project3'
upper_and_low_headers = {'CONTENT-type': 'APPLICATION/json', 'ACCept': 'APPLICATION/json'}
upper_headers = {'CONTENT-TYPE': 'APPLICATION/JSON', 'ACCEPT': 'APPLICATION/JSON'}
upper_url_node = "https://API.CLOVERI.SKROY.ru/api/v1/node/"
upper_url_nodes = "https://API.CLOVERI.SKROY.ru/api/v1/nodes/"
