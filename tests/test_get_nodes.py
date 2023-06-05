import pytest
# from ..settings import *
# from ..methods import *
from nodes import *


# Позитивные тесты по get-tree

# Базовый тест на получение пустого списка по несозданному дереву
# OS-API-Gt-1
@pytest.mark.high
def test_get_empty_tree():
    status, response, res_headers = org.get_tree(wrong_params={'project_id': project_id,
                                                               'item_type': item_type,
                                                               'item': other_item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) == 0
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Базовый тест на получение созданного дерева
# OS-API-Gt-2
@pytest.mark.high
def test_get_tree_positive():
    status, response, res_headers = org.get_tree()
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    nodes = []
    for node in response[0]:
        nodes.append(node)
    for s in nodes:
        assert 'project_id' in s
        assert 'item_type' in s
        assert 'item' in s
        assert 'id' in s
        assert 'path' in s
        assert 'inner_order' in s
        assert 'attributes' in s
        assert 'level_node' in s
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Проверка сортировки узлов при получении созданного дерева
# OS-API-Gt-2
@pytest.mark.high
def test_get_tree_check_default_sorted_tree():
    status, response, res_headers = org.get_tree()
    print(f"\nCode: {status}")
    # print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    new_nodes = []
    id_new_nodes_sorted = [id_root1, id_child2lvl, id_child3lvl, id_child4lvl, id_sec_child4lvl,
                           id_third_child4lvl, id_fourth_child4lvl, id_sec_child3lvl, id_child4lvl_for_sec_child3lvl,
                           id_sec_child2lvl, id_root2]
    for i in response[0]:
        if i['id'] in id_new_nodes_sorted:
            new_nodes.append(i)
    print(new_nodes)
    id_resp_nodes = []
    for i in new_nodes:
        id_resp_nodes.append(i['id'])
    assert id_resp_nodes == id_new_nodes_sorted


# Тест на получение дерева с сортировкой узлов по id
# OS-API-Gt-38
@pytest.mark.high
def test_get_tree_sorted_by_id():
    status, response, res_headers = org.get_tree(wrong_params={'project_id': project_id, 'item_type': item_type,
                                                               'item': item, 'sort_by_id': True})
    print(f"\nCode: {status}")
    # print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    new_nodes = []
    id_new_nodes_sorted = [id_root1, id_root2, id_child2lvl, id_sec_child2lvl, id_child3lvl, id_sec_child3lvl,
                           id_child4lvl, id_sec_child4lvl, id_third_child4lvl, id_fourth_child4lvl,
                           id_child4lvl_for_sec_child3lvl]
    for i in response[0]:
        if i['id'] in id_new_nodes_sorted:
            new_nodes.append(i)
    print(new_nodes)
    id_resp_nodes = []
    for i in new_nodes:
        id_resp_nodes.append(i['id'])
    assert id_resp_nodes == id_new_nodes_sorted


# Тест на получение дерева с параметром sorted_by_id не равным True
# OS-API-Gt-39
@pytest.mark.high
def test_get_tree_sort_by_id_is_none():
    status, response, res_headers = org.get_tree(wrong_params={'project_id': project_id, 'item_type': item_type,
                                                               'item': item, 'sort_by_id': None})
    print(f"\nCode: {status}")
    # print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    new_nodes = []
    id_new_nodes_sorted = [id_root1, id_child2lvl, id_child3lvl, id_child4lvl, id_sec_child4lvl,
                           id_third_child4lvl, id_fourth_child4lvl, id_sec_child3lvl, id_child4lvl_for_sec_child3lvl,
                           id_sec_child2lvl, id_root2]
    for i in response[0]:
        if i['id'] in id_new_nodes_sorted:
            new_nodes.append(i)
    print(new_nodes)
    id_resp_nodes = []
    for i in new_nodes:
        id_resp_nodes.append(i['id'])
    assert id_resp_nodes == id_new_nodes_sorted


# Позитивные тесты по get-children

# Базовый тест на получение пустого списка при отсутствии дочек у узла
# OS-API-Gc-1
@pytest.mark.high
def test_get_children_empty():
    status, response, res_headers = org.get_children(node_id=id_sec_child2lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) == 0
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Базовый тест на получение всех дочек узлов разных уровней
# OS-API-Gc-2, OS-API-Gc-3, OS-API-Gc-4
@pytest.mark.high
@pytest.mark.parametrize(('parent', 'level', 'path'), [(id_root1, 1, path_root1), (id_child2lvl, 2, path_child2lvl),
                                                       (id_child3lvl, 3, path_child3lvl)],
                         ids=["get children for node 1lvl", "get children for node 2lvl", "get children for node 3lvl"])
def test_get_children_positive(parent, level, path):
    _, get_parent, _ = org.get_node(parent)
    print(get_parent)
    status, response, res_headers = org.get_children(node_id=parent)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    nodes = []
    for node in response[0]:
        nodes.append(node)
    for s in nodes:
        assert 'project_id' in s
        assert 'item_type' in s
        assert 'item' in s
        assert 'id' in s
        assert 'path' in s
        assert 'inner_order' in s
        assert 'attributes' in s
        assert 'level_node' in s
        if s['level_node'] >= level:
            assert s['path'][:level * 10] == path
        assert s['id'] != parent
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Проверка сортировки узлов при get_children
# OS-API-Gc-2
@pytest.mark.high
def test_get_children_check_default_sorted():
    status, response, res_headers = org.get_children(node_id=id_root1)
    print(f"\nCode: {status}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    child_nodes = []
    id_child_nodes_sorted = [id_child2lvl, id_child3lvl, id_child4lvl, id_sec_child4lvl, id_third_child4lvl,
                             id_fourth_child4lvl, id_sec_child3lvl, id_child4lvl_for_sec_child3lvl, id_sec_child2lvl]
    for i in response[0]:
        if i['id'] in id_child_nodes_sorted:
            child_nodes.append(i)
    print(child_nodes)
    id_resp_nodes = []
    for i in child_nodes:
        id_resp_nodes.append(i['id'])
    assert id_resp_nodes == id_child_nodes_sorted


# Тест на отправку запроса с полем sort_by_id и указание id в url (get_children с параметром sort_by_id)
# OS-API-Gt-43
@pytest.mark.medium
def test_get_children_with_sort_by_id():
    status, response, res_headers = org.get_children(node_id=id_root1, wrong_params={'project_id': project_id,
                                                                                     'item_type': item_type,
                                                                                     'item': item, 'sort_by_id': True})
    print(f"\nCode: {status}")
    # print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    child_nodes = []
    id_child_nodes_sorted = [id_child2lvl, id_sec_child2lvl, id_child3lvl, id_sec_child3lvl, id_child4lvl,
                             id_sec_child4lvl, id_third_child4lvl, id_fourth_child4lvl, id_child4lvl_for_sec_child3lvl]
    for i in response[0]:
        if i['id'] in id_child_nodes_sorted:
            child_nodes.append(i)
    print(child_nodes)
    id_resp_nodes = []
    for i in child_nodes:
        id_resp_nodes.append(i['id'])
    assert id_resp_nodes == id_child_nodes_sorted


# Тест на отправку запроса с полем sort_by_id и указание id в url (get_children с параметром sort_by_id=None)
# OS-API-Gt-44
@pytest.mark.medium
def test_get_children_with_sort_by_id_is_none():
    status, response, res_headers = org.get_children(node_id=id_root1, wrong_params={'project_id': project_id,
                                                                                     'item_type': item_type,
                                                                                     'item': item, 'sort_by_id': None})
    print(f"\nCode: {status}")
    # print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    child_nodes = []
    id_child_nodes_sorted = [id_child2lvl, id_child3lvl, id_child4lvl, id_sec_child4lvl, id_third_child4lvl,
                             id_fourth_child4lvl, id_sec_child3lvl, id_child4lvl_for_sec_child3lvl, id_sec_child2lvl]
    for i in response[0]:
        if i['id'] in id_child_nodes_sorted:
            child_nodes.append(i)
    print(child_nodes)
    id_resp_nodes = []
    for i in child_nodes:
        id_resp_nodes.append(i['id'])
    assert id_resp_nodes == id_child_nodes_sorted


# Общие позитивные тесты

# Тест на отправку запроса с заголовками в верхнем регистре
# OS-API-Gt-3, OS-API-Gt-4
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [{'ACCEPT': 'APPLICATION/JSON'},
                                           {'ACCept': 'APPLICATION/json'}],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_get_nodes_upper_headers(headers_upper):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=headers_upper, wrong_params=None,
                                                 wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с url в верхнем регистре
# OS-API-Gt-5
@pytest.mark.medium
def test_get_nodes_upper_url():
    status, response, res_headers = org.get_tree(wrong_url=upper_url_nodes, wrong_headers=None, wrong_params=None,
                                                 wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert len(response[0]) != 0
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Негативные тесты!!!


# Проверки на параметр parent id в get_children

# Тесты на отправку запросов с неверным форматом id в url
# OS-API-Gc-13
@pytest.mark.medium
def test_get_children_with_incorrect_format_in_id():
    status, response, res_headers = org.get_children(node_id='abc', wrong_url=None, wrong_headers=None, wrong_data=None,
                                                     wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с несуществующим id в url
# OS-API-Gc-14
@pytest.mark.high
# @pytest.mark.skip
def test_get_children_with_nonexistent_id_node():
    status, response, res_headers = org.get_children(node_id=100000, wrong_url=None, wrong_headers=None, wrong_data=None,
                                                     wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с пустым значением id в url
# OS-API-Gc-36, OS-API-Gc-37
@pytest.mark.medium
@pytest.mark.parametrize("id_node", [" ", None],
                         ids=['id is empty', 'id is Null'])
def test_get_children_with_empty_value_in_id(id_node):
    status, response, res_headers = org.get_children(node_id=id_node, wrong_url=None, wrong_headers=None,
                                                     wrong_data=None, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 400
    assert "'id': " not in str(response[0])


# Общие негативные проверки

# Тесты на отправку запросов с неверным url и эндпоинтом
# OS-API-Gt-8, OS-API-Gt-9
@pytest.mark.medium
@pytest.mark.parametrize("urls", ["https://skroy.ru/api/v1/nodes/",
                                  "https://api.cloveri.skroy.ru/api/v2/nodes/",
                                  "https://api.cloveri.skroy.ru/api/v1/nod/"],
                         ids=['wrong url', 'wrong api version', 'wrong endpoint'])
def test_get_nodes_wrong_urls(urls):
    status, response, res_headers = org.get_tree(wrong_url=urls, wrong_headers=None, wrong_params=None,
                                                 wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов неверным методом
# OS-API-Gt-7
@pytest.mark.medium
def test_get_nodes_wrong_method():
    headers = {'Accept': 'application/json'}
    params = {'project_id': project_id, 'item_type': item_type, 'item': item}
    res = requests.post(url_nodes, headers=headers, params=params, json={})
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
    res2 = requests.put(url_nodes, headers=headers, params=params, json={})
    status2 = res2.status_code
    res_headers2 = res2.headers
    try:
        response2 = res2.json(),
    except json.decoder.JSONDecodeError:
        response2 = res2.text
    print(f"\nCode: {status2}")
    print(f"Response: {response2}")
    print(f'Response headers: {res_headers2}')
    assert status2 != 200
    assert status2 == 405
    assert "'id': " not in str(response2[0])
    res3 = requests.delete(url_nodes, headers=headers, params=params, json=None)
    status3 = res3.status_code
    res_headers3 = res3.headers
    try:
        response3 = res3.json(),
    except json.decoder.JSONDecodeError:
        response3 = res3.text
    print(f"\nCode: {status3}")
    print(f"Response: {response3}")
    print(f'Response headers: {res_headers3}')
    assert status3 != 200
    assert status3 == 405
    assert "'id': " not in str(response3[0])
    res4 = requests.patch(url_nodes, headers=headers, params=params, json=None)
    status4 = res4.status_code
    res_headers4 = res4.headers
    try:
        response4 = res4.json(),
    except json.decoder.JSONDecodeError:
        response4 = res4.text
    print(f"\nCode: {status4}")
    print(f"Response: {response4}")
    print(f'Response headers: {res_headers4}')
    assert status4 != 200
    assert status4 == 405
    assert "'id': " not in str(response4[0])


# Тесты на отправку запросов с неверными заголовками и без заголовков
# OS-API-Gt-16, OS-API-Gt-11
@pytest.mark.medium
@pytest.mark.parametrize("header", [{'Accept': 'application/xml'},
                                    {}],
                         ids=['wrong_media_type_in_headers',
                              'without headers'])
def test_get_nodes_wrong_headers(header):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=header,
                                                 wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200 or status == 415


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
# OS-API-Gt-16, OS-API-Gt-17, OS-API-Gt-18
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': 123, 'item_type': item_type, 'item': item},
                                    {'project_id': 'abc', 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': 123, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': 123}],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_get_nodes_with_incorrect_format_in_fields(fields):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422 or status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверным протоколом http и без parent id в url
# OS-API-Gt-34
@pytest.mark.medium
def test_get_tree_wrong_protocol():
    status, response, res_headers = org.get_tree(wrong_url="http://api.cloveri.skroy.ru/api/v1/nodes/",
                                                 wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422


# Тесты на отправку запросов с неверным протоколом http с parent id в url
# OS-API-Gc-49
@pytest.mark.medium
def test_get_children_wrong_protocol():
    status, response, res_headers = org.get_children(node_id=id_root1, wrong_headers=None, wrong_params=None,
                                                     wrong_data=None,
                                                     wrong_url=f"http://api.cloveri.skroy.ru/api/v1/nodes/{id_root1}/")
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422


# Тесты на отправку запросов с дублированием обязательных полей
# OS-API-Gt-35, OS-API-Gt-36
@pytest.mark.medium
@pytest.mark.parametrize("fields",
                         [{'project_id': project_id, 'item_type': item_type, 'item': item,
                           'project_id': project_id, 'item_type': item_type, 'item': item},
                          {'project_id': project_id, 'item_type': item_type, 'item': item,
                           'project_id': other_project_id, 'item_type': other_item_type, 'item': other_item}],
                         ids=['double fields with same values', 'double fields with different values'])
def test_get_nodes_with_double_fields(fields):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None,
                                                 wrong_params=fields, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 404 or status == 422 or status == 200


# Тесты на отправку запросов с ключами обязательных полей в верхнем регистре
# OS-API-Gt-37
@pytest.mark.medium
def test_get_nodes_upper_fields():
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None,
                                                 wrong_params={'PROJECT_ID': project_id, 'ITEM_TYPE': item_type,
                                                               'ITEM': item}, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тест на отправку запроса с полем sort_by_id в верхнем регистре
# OS-API-Gt-40
@pytest.mark.medium
def test_get_nodes_with_sort_by_id_upper():
    status, response, res_headers = org.get_tree(wrong_params={'project_id': project_id, 'item_type': item_type,
                                                               'item': item, 'SORT_BY_ID': True})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с пустыми значениями в обязательных полях
# OS-API-Gt-19, OS-API-Gt-20, OS-API-Gt-21, OS-API-Gt-22, OS-API-Gt-23, OS-API-Gt-24
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': "", 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': "", 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': ""},
                                    {'project_id': None, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': None, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': None}],
                         ids=['project_id empty', 'item_type empty', 'item empty', 'project_id Null',
                              'item_type Null', 'item Null'])
def test_get_nodes_with_empty_value_in_fields(fields):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с несуществующими значениями в обязательных полях
# OS-API-Gt-27, OS-API-Gt-28, OS-API-Gt-29
@pytest.mark.high
@pytest.mark.skip
@pytest.mark.parametrize("fields", [{'project_id': nonexistent_project_id, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': nonexistent_item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': nonexistent_item}],
                         ids=['project_id dont exist', 'item_type dont exist', 'item dont exist'])
def test_get_nodes_with_nonexistent_value_in_fields(fields):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с разными значениями в опциональном поле sort_by_id
# OS-API-Gt-42, OS-API-Gt-41
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': project_id, 'item_type': item_type, 'item': item, 'sort_by_id': ""},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item, 'sort_by_id': False},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item, 'sort_by_id': 123},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'sort_by_id': "abc"}],
                         ids=['empty string', 'False in value', 'int in value', 'string in value'])
def test_get_nodes_with_different_value_in_sort_by_id(fields):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов без обязательных полей и с непредусмотренными полями
# OS-API-Gt-13, OS-API-Gt-14, OS-API-Gt-15, OS-API-Gt-26, OS-API-Gt-33
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type},
                                    {'project_ids': project_id, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item, 'new_field': ''}],
                         ids=['without project_id', 'without item_type', 'without item', 'with projest_ids',
                              'with new field'])
def test_get_nodes_without_required_fields(fields):
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с обязательными полями в url
# OS-API-Gt-30
@pytest.mark.min
def test_get_nodes_fields_in_path():
    status, response, res_headers = org.get_tree(
        wrong_url=url_nodes + f"project_id/{project_id}/item_type/{item_type}/item/{item}/",
        wrong_headers=None, wrong_params={}, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404


# Тест на отправку запроса с обязательными полями в теле
# OS-API-Gt-31
@pytest.mark.min
def test_get_nodes_fields_in_body():
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_params={},
                                                 wrong_data={"project_id": project_id, "item_type": item_type,
                                                             "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тест на отправку запроса с text в теле
# OS-API-Gt-12
@pytest.mark.min
def test_get_nodes_text_in_body():
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_params=None,
                                                 wrong_data=f'"project_id": {project_id}, "item_type": {item_type}, "item": {item}')
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status == 200 or status == 422


# Тесты на отправку запросов с обязательными полями в заголовках
# OS-API-Gt-32
@pytest.mark.min
def test_get_nodes_fields_in_headers():
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_params={}, wrong_data=None,
                                                 wrong_headers={"project_id": project_id, "item_type": item_type,
                                                                "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тесты на указание parent id не в url, а в других местах

# Тест на отправку запроса с id в query params
# OS-API-Gc-44
@pytest.mark.min
def test_get_children_id_in_query_params():
    status, response, res_headers = org.get_children(node_id=None, wrong_url=url_nodes, wrong_headers=None,
                                                     wrong_params={'id': id_root1, 'project_id': project_id,
                                                                   'item_type': item_type, 'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404 or status == 422


# Тесты на отправку запросов с id в теле запроса
# OS-API-Gc-45
@pytest.mark.min
def test_get_children_id_in_body():
    status, response, res_headers = org.get_children(node_id=None, wrong_url=url_nodes, wrong_params=None,
                                                     wrong_headers=None, wrong_data={"id": id_root1})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200 or status == 422


# Тесты на отправку запросов с id в заголовках
# OS-API-Gc-46
@pytest.mark.min
def test_get_children_id_in_headers():
    status, response, res_headers = org.get_children(node_id=None, wrong_url=url_nodes, wrong_params=None,
                                                     wrong_data=None,
                                                     wrong_headers={"id": str(id_root1)})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status == 200 or status == 422
