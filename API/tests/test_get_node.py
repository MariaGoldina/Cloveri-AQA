import pytest
# from ..settings import *
# from ..methods import *
from ..nodes import *


# Базовый тест на получение узла любого уровня
# OS-API-Gn-4, OS-API-Gn-5, OS-API-Gn-6, OS-API-Gn-7
@pytest.mark.high
@pytest.mark.parametrize(('get_node', 'path', 'order', 'level'),
                         [(id_root1, path_root1, order_root1, 1),
                          (id_child2lvl, path_child2lvl, order_child2lvl, 2),
                          (id_child3lvl, path_child3lvl, order_child3lvl, 3),
                          (id_child4lvl, path_child4lvl, order_child4lvl, 4)],
                         ids=["get node 1lvl", "get node 2lvl", "get node 3lvl",
                              "get node 4lvl"])
def test_get_node_positive(get_node, path, order, level):
    status, response, res_headers = org.get_node(node_id=get_node)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == get_node
    assert response[0]['path'] == path
    assert response[0]['inner_order'] == order
    assert response[0]['level_node'] == level
    assert response[0]['attributes'] == '{}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с заголовками в верхнем регистре
# OS-API-Gn-4а, OS-API-Gn-5а
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [{'ACCEPT': 'APPLICATION/JSON'},
                                           {'ACCept': 'APPLICATION/json'}],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_get_node_upper_headers(headers_upper):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_id=None, wrong_url=None, wrong_headers=headers_upper,
                                                 wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_root1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с url в верхнем регистре
# OS-API-Gn-6а
@pytest.mark.medium
def test_get_node_upper_url():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_id=None, wrong_params=None, wrong_data=None,
                                                 wrong_url=upper_url_node+f'{id_root1}/', wrong_headers=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_root1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Негативные тесты!!!


# Тесты на отправку запросов с неверным url и эндпоинтом и без id в url
# OS-API-Gn-9, OS-API-Gn-10, OS-API-Gn-43
@pytest.mark.medium
@pytest.mark.parametrize("urls", [f"https://skroy.ru/api/v1/node/{id_root1}/",
                                  f"https://api.cloveri.skroy.ru/api/v2/node/{id_root1}/",
                                  f"https://api.cloveri.skroy.ru/api/v1/nod/{id_root1}/",
                                  f"{url_node}"],
                         ids=['wrong url', 'wrong api version', 'wrong endpoint', 'without id in url'])
def test_get_node_wrong_urls(urls):
    status, response, res_headers = org.get_node(node_id=None, wrong_url=urls, wrong_headers=None, wrong_data=None,
                                                 wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов неверным методом
# OS-API-Gn-8
@pytest.mark.medium
def test_get_node_wrong_method():
    headers = {'Accept': 'application/json'}
    params = {'project_id': project_id, 'item_type': item_type, 'item': item}
    res = requests.patch(url_node+f'{id_root1}/', headers=headers, params=params, json={})
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 405
    assert "'id': " not in str(response[0])
    res = requests.put(url_node + f'{id_root1}/', headers=headers, params=params, json={})
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 405
    assert "'id': " not in str(response[0])
    res = requests.delete(url_node + f'{id_root1}/', headers=headers, params=params, json={})
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 405
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
# OS-API-Gn-25, OS-API-Gn-26, OS-API-Gn-12
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': 123, 'item_type': item_type, 'item': item},
                                    {'project_id': 'abc', 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': 123, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': 123}],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_get_node_with_incorrect_format_in_fields(fields):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422 or status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверным форматом id в url
# OS-API-Gn-30
@pytest.mark.medium
def test_get_node_with_incorrect_format_in_id():
    status, response, res_headers = org.get_node(node_id='abc', wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверными заголовками и без заголовков
# OS-API-Gn-17, OS-API-Gn-18
@pytest.mark.medium
@pytest.mark.parametrize("header", [{'Accept': 'application/xml'},
                                    {}],
                         ids=['wrong_media_type_in_headers',
                              'without headers'])
def test_get_node_wrong_headers(header):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=header,
                                                 wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200 or status == 415


# Тесты на отправку запросов с неверным протоколом http
# OS-API-Gn-52
@pytest.mark.medium
def test_get_node_wrong_protocol():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_headers=None, wrong_params=None,
                                                 wrong_url=f"http://api.cloveri.skroy.ru/api/v1/node/{id_root1}/")
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422


# Тесты на отправку запросов с дублированием обязательных полей
# OS-API-Gn-53, OS-API-Gn-54
@pytest.mark.medium
@pytest.mark.parametrize("fields",
                         [{'project_id': project_id, 'item_type': item_type, 'item': item,
                           'project_id': project_id, 'item_type': item_type, 'item': item},
                          {'project_id': project_id, 'item_type': item_type, 'item': item,
                           'project_id': other_project_id, 'item_type': other_item_type, 'item': other_item}],
                         ids=['double fields with same values', 'double fields with different values'])
def test_get_node_with_double_fields(fields):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None,
                                                 wrong_params=fields, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 404 or status == 422 or status == 200


# Тесты на отправку запросов с ключами обязательных полей в верхнем регистре
# OS-API-Gn-55
@pytest.mark.medium
def test_get_node_upper_fields():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None,
                                                 wrong_params={'PROJECT_ID': project_id, 'ITEM_TYPE': item_type,
                                                               'ITEM': item}, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тесты на отправку запросов с несуществующим id в url
# OS-API-Gn-31
@pytest.mark.high
def test_get_node_with_nonexistent_id_node():
    status, response, res_headers = org.get_node(node_id=100000, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с несуществующими значениями в обязательных полях
# OS-API-Gn-38, OS-API-Gn-39, OS-API-Gn-13
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'project_id': nonexistent_project_id, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': nonexistent_item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': nonexistent_item}],
                         ids=['project_id dont exist', 'item_type dont exist', 'item dont exist'])
def test_get_node_with_nonexistent_value_in_fields(fields):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с пустыми значениями в обязательных полях
# OS-API-Gn-27, OS-API-Gn-28, OS-API-Gn-14, OS-API-Gn-40, OS-API-Gn-41, OS-API-Gn-42
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': "", 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': "", 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': ""},
                                    {'project_id': None, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': None, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': None}],
                         ids=['project_id empty', 'item_type empty', 'item empty', 'project_id Null',
                              'item_type Null', 'item Null'])
def test_get_node_with_empty_value_in_fields(fields):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с пустым значением id в url
# OS-API-Gn-32, OS-API-Gn-44
@pytest.mark.medium
@pytest.mark.parametrize("id_node", [" ", None],
                         ids=['id is empty', 'id is Null'])
def test_get_node_with_empty_value_in_id(id_node):
    status, response, res_headers = org.get_node(node_id=id_node, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов без обязательных полей и с непредусмотренными полями
# OS-API-Gn-33, OS-API-Gn-34, OS-API-Gn-35, OS-API-Gn-36, OS-API-Gn-37
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type},
                                    {'project_ids': project_id, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item, 'new_field': ''}],
                         ids=['without project_id', 'without item_type', 'without item', 'with projest_ids',
                              'with new field'])
def test_get_node_without_required_fields(fields):
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с обязательными полями в url
# OS-API-Gn-45
@pytest.mark.min
def test_get_node_fields_in_path():
    status, response, res_headers = org.get_node(node_id=None, wrong_headers=None, wrong_params={}, wrong_data=None,
                                                 wrong_url=url_node+f"{id_root1}/project_id/{project_id}/item_type/{item_type}/item/{item}/")
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404


# Тесты на отправку запросов с обязательными полями в теле
# OS-API-Gn-46
@pytest.mark.min
def test_get_node_fields_in_body():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_params={},
                                                 wrong_data={"project_id": project_id, "item_type": item_type,
                                                             "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тесты на отправку запросов с text в теле
# OS-API-Gn-20
@pytest.mark.min
def test_get_node_text_in_body():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_params=None,
                                                 wrong_data=f'"project_id": {project_id}, "item_type": {item_type}, "item": {item}')
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200 or status == 422


# Тесты на отправку запросов с обязательными полями в заголовках
# OS-API-Gn-47
@pytest.mark.min
def test_get_node_fields_in_headers():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_params={}, wrong_data=None,
                                                 wrong_headers={"project_id": project_id, "item_type": item_type, "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тест на отправку запроса с id в query params
# OS-API-Gn-49
@pytest.mark.min
def test_get_node_id_in_query_params():
    status, response, res_headers = org.get_node(node_id=None, wrong_url=url_node, wrong_headers=None,
                                                 wrong_params={'id': id_root1, 'project_id': project_id,
                                                               'item_type': item_type, 'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422


# Тест на отправку запросов с path в query params
# OS-API-Gn-48
@pytest.mark.min
def test_get_node_path_in_query_params():
    status, response, res_headers = org.get_node(node_id=id_root1, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params={'project_id': project_id, 'item_type': item_type,
                                                               'item': item, 'path': path_root1})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тесты на отправку запросов с id в теле запроса
# OS-API-Gn-50
@pytest.mark.min
def test_get_node_id_in_body():
    status, response, res_headers = org.get_node(node_id=None, wrong_url=url_node, wrong_params=None,
                                                 wrong_headers=None, wrong_data={"id": id_root1})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422


# Тесты на отправку запросов с id в заголовках
# OS-API-Gn-51
@pytest.mark.min
def test_get_node_id_in_headers():
    status, response, res_headers = org.get_node(node_id=None, wrong_url=url_node, wrong_params=None, wrong_data=None,
                                                 wrong_headers={"id": str(id_root1)})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422
