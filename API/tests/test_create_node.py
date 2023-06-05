# import json
import pytest
# from ..settings import *
# from ..methods import *
from ..nodes import *


# Позитивные тесты на create_root

# Базовые тесты на создание корневых узлов
@pytest.mark.high
@pytest.mark.parametrize('other_attributes', ['{"name": "Компания Ромашка", "description": "ПО"}',
                                              '{"name": "Company2", "description": "software"}'],
                         ids=["create root 1", "create root 2"])
def test_create_root_positive(other_attributes):
    status, response, res_headers = org.create_root(attributes=None, wrong_data={'project_id': project_id,
                                                                                 'item_type': item_type, 'item': item,
                                                                                 'attributes': other_attributes})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == '0' * (10 - len(str(id_node))) + str(id_node)
    assert 'inner_order' in str(response[0])
    assert response[0]['attributes'] == f'{other_attributes}'
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на проверку inner_order при создании корневого узла
@pytest.mark.high
def test_create_root_check_inner_order():
    status_get_tree, response_get_tree, _ = org.get_tree()
    all_nodes = []
    root_nodes = []
    for node in response_get_tree[0]:
        all_nodes.append(node)
    for s in all_nodes:
        if s['level_node'] == 1 or 'level_node' not in str(s):
            root_nodes.append(s)
    amount_root_nodes = len(root_nodes)
    status, response, res_headers = org.create_root(attributes={})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] != 0
    assert response[0]['inner_order'] == '0' * (10 - len(str(amount_root_nodes + 1))) + str(amount_root_nodes + 1)


# Тест на отправку запроса с другими значениями обязательных 3 полей
@pytest.mark.high
def test_create_root_other_value_in_fields():
    status, response, res_headers = org.create_root(attributes=None, wrong_data={'project_id': other_project_id,
                                                                                 'item_type': other_item_type,
                                                                                 'item': other_item,
                                                                                 'attributes': '{}'})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == other_project_id
    assert response[0]['item_type'] == other_item_type
    assert response[0]['item'] == other_item
    assert response[0]['id'] != 0
    assert response[0]['path'] == '0' * (10 - len(str(id_node))) + str(id_node)
    assert 'inner_order' in str(response[0])
    assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Позитивные тесты на create_child

# Базове тесты на создание дочек разных уровней
@pytest.mark.high
@pytest.mark.parametrize(('parent', 'attr', 'path', 'level', 'parent_order'),
                         [(id_root1, '{"name": "1 child 2lvl"}', path_root1, 2, order_root1),
                          (id_root1, '{"name": "2 child 2lvl"}', path_root1, 2, order_root1),
                          (id_child2lvl, '{"name": "1 child 3lvl"}', path_child2lvl, 3, order_child2lvl),
                          (id_child2lvl, '{"name": "2 child 3lvl"}', path_child2lvl, 3, order_child2lvl),
                          (id_child3lvl, '{"name": "1 child 4lvl"}', path_child3lvl, 4, order_child3lvl),
                          (id_child3lvl, '{"name": "2 child 4lvl"}', path_child3lvl, 4, order_child3lvl),
                          (id_child4lvl, '{"name": "child 5lvl"}', path_child4lvl, 5, order_child3lvl)],
                         ids=["create child 2lvl", "create second child 2lvl", "create child 3lvl",
                              "create second child 3lvl", "create child 4lvl", "create second child 4lvl",
                              "create child 5lvl"])
def test_create_child_positive(parent, attr, path, level, parent_order):
    status, response, res_headers = org.create_child(attributes=None, node_id=parent,
                                                     wrong_data={'project_id': project_id,
                                                                 'item_type': item_type, 'item': item,
                                                                 'attributes': attr})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == path + ('0' * (10 - len(str(id_node))) + str(id_node))
    assert response[0]['attributes'] == attr
    assert response[0]['level_node'] == level
    assert "'Content-Type': 'application/json'" in str(res_headers)
    assert 'inner_order' in str(response[0])


# Тест на проверку inner_order при создании дочерних узлов
@pytest.mark.high
@pytest.mark.parametrize(('parent', 'parent_path', 'parent_order', 'child_level'),
                         [(id_root1, path_root1, order_root1, 2),
                          (id_child2lvl, path_child2lvl, order_child2lvl, 3),
                          (id_child3lvl, path_child3lvl, order_child3lvl, 4)],
                         ids=["create child 2lvl", "create child 3lvl", "create child 4lvl"])
def test_create_child_check_inner_order(parent, parent_order, parent_path, child_level):
    status_get_children, response_get_children, _ = org.get_children(node_id=parent)
    child_nodes_for_parent = []
    for node in response_get_children[0]:
        if node['path'][0:-10] == parent_path and node['level_node'] == child_level:
            child_nodes_for_parent.append(node)
    amount_child_nodes = len(child_nodes_for_parent)
    status, response, res_headers = org.create_child(node_id=parent, attributes=None,
                                                     wrong_data={'project_id': project_id,
                                                                 'item_type': item_type, 'item': item,
                                                                 'attributes': '{}'})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] != 0

    assert response[0]['inner_order'] == \
           parent_order + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)


# Общие позитивные тесты

# Тест на отправку запроса без поля attributes
@pytest.mark.medium
def test_create_node_without_attributes():
    status, response, res_headers = org.create_root(attributes=None, wrong_data={'project_id': project_id,
                                                                                 'item_type': item_type,
                                                                                 'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == '0' * (10 - len(str(id_node))) + str(id_node)
    assert 'inner_order' in str(response[0])
    assert response[0]['attributes'] is None
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тесты на отправку запросов с разным наполнением поля attributes
@pytest.mark.medium
@pytest.mark.parametrize('other_attributes', ['{}',
                                              '{"name": "", "description": ""}',
                                              None,
                                              '{"name": "name"}',
                                              '{"description": "description"}',
                                              '{"name": "None"}',
                                              '{"description": "None"}',
                                              ''],
                         ids=["empty json", "empty string - name, description", "None instead attributes",
                              "only name", "only description", "None in name", "None in description",
                              "empty string in attributes"])
def test_create_node_with_other_attributes(other_attributes):
    status, response, res_headers = org.create_root(attributes=None, wrong_data={'project_id': project_id,
                                                                                 'item_type': item_type, 'item': item,
                                                                                 'attributes': other_attributes})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == '0' * (10 - len(str(id_node))) + str(id_node)
    assert 'inner_order' in str(response[0])
    assert response[0]['attributes'] == other_attributes
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с заголовками в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [upper_headers,
                                           upper_and_low_headers],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_create_node_upper_headers(headers_upper):
    status, response, res_headers = org.create_root(attributes={}, wrong_url=None, wrong_headers=headers_upper,
                                                    wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] != 0
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с url в верхнем регистре
@pytest.mark.medium
def test_create_node_upper_url():
    status, response, res_headers = org.create_root(attributes={}, wrong_url=upper_url_node,
                                                    wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] != 0
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с переменой местами полей в json в теле запроса
@pytest.mark.medium
def test_create_node_move_body_fields():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_params=None, wrong_data={'item_type': item_type,
                                                                                   'project_id': project_id,
                                                                                   'attributes': {},
                                                                                   'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] != 0
    assert response[0]['level_node'] == 1
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Негативные тесты!!!


# Проверки на параметр parent id в create_child

# Тесты на отправку запросов с неверным форматом и неверными значениями в поле parent_id
@pytest.mark.medium
@pytest.mark.parametrize("parent", ['abc', 100000],
                         ids=['incorrect format in parent_id', 'nonexistent parent_id'])
def test_create_child_with_different_parent_id(parent):
    status, response, res_headers = org.create_child(node_id=parent, attributes={}, wrong_url=None,
                                                     wrong_data=None, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422 or status == 404
    assert "'id': " not in str(response[0])


# Тест на проверку обязательных полей у дочки и родителя в create_child

# Тесты на отправку запросов с несовпадением обязательных полей с родителем
@pytest.mark.high
@pytest.mark.parametrize("fields",
                         [{'project_id': other_project_id, 'item_type': item_type,
                           'item': item, 'attributes': {}},
                          {'project_id': project_id, 'item_type': other_item_type,
                           'item': item, 'attributes': {}},
                          {'project_id': project_id, 'item_type': item_type,
                           'item': other_item, 'attributes': {}}],
                         ids=['project_id dont equal parent', 'item_type dont equal parent', 'item dont equal parent'])
def test_create_child_value_in_fields_not_equal_parent(fields):
    status, response, res_headers = org.create_child(node_id=id_root1, attributes=None, wrong_url=None,
                                                     wrong_data=fields, wrong_headers=None, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])


# Общие негативные тесты

# Тесты на отправку запросов без обязательных полей и с непредусмотренными полями
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'item_type': item_type, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': item_type, 'attributes': {}},
                                    {'project_ids': project_id, 'item_type': item_type, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item, 'new_field': '',
                                     'attributes': {}}],
                         ids=['without project_id', 'without item_type', 'without item', 'with projest_ids',
                              'with new field'])
def test_create_node_without_required_fields(fields):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с несуществующими значениями в обязательных полях
@pytest.mark.high
@pytest.mark.skip
@pytest.mark.parametrize("fields",
                         [{'project_id': nonexistent_project_id, 'item_type': item_type, 'item': item,
                           'attributes': {}},
                          {'project_id': project_id, 'item_type': nonexistent_item_type, 'item': item,
                           'attributes': {}},
                          {'project_id': project_id, 'item_type': item_type, 'item': nonexistent_item,
                           'attributes': {}}],
                         ids=['project_id dont exist', 'item_type dont exist', 'item dont exist'])
def test_create_node_with_nonexistent_value_in_fields(fields):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с дублированием обязательных полей в теле
@pytest.mark.medium
@pytest.mark.parametrize("fields",
                         [{'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': {},
                           'project_id': project_id, 'item_type': item_type, 'item': item},
                          {'project_id': other_project_id, 'item_type': other_item_type, 'item': other_item,
                           'attributes': {}, 'project_id': project_id, 'item_type': item_type, 'item': item, }],
                         ids=['double fields with same values', 'double fields with different values'])
def test_create_node_with_double_fields(fields):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 422


# Тесты на отправку запросов с пустыми значениями в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': "", 'item_type': item_type, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': "", 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': item_type, 'item': "", 'attributes': {}},
                                    {'project_id': None, 'item_type': item_type, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': None, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': item_type, 'item': None, 'attributes': {}}],
                         ids=['project_id empty', 'item_type empty', 'item empty',
                              'project_id Null', 'item_type Null', 'item Null'])
def test_create_node_with_empty_value_in_fields(fields):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': 123, 'item_type': item_type, 'item': item, 'attributes': {}},
                                    {'project_id': 'abc', 'item_type': item_type, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': 123, 'item': item, 'attributes': {}},
                                    {'project_id': project_id, 'item_type': item_type, 'item': 123, 'attributes': {}}],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_create_node_with_incorrect_format_in_fields(fields):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с ключами обязательных полей в теле в верхнем регистре
@pytest.mark.medium
def test_create_node_upper_fields():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data={'PROJECT_ID': project_id, 'ITEM_TYPE': item_type,
                                                                'ITEM': item, 'ATTRIBUTES': {}}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422


# Тест на отправку запроса с телом запроса в формате text
@pytest.mark.medium
def test_create_node_with_text_in_body():
    res = requests.post(url_node, headers=None, params=None,
                        data="'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': {}")
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422 or status == 415
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с телом запроса в формате dict
@pytest.mark.medium
def test_create_node_with_dict_in_body():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.post(url_node, headers=headers, params=None,
                        data={"project_id": project_id, "item_type": item_type, "item": item, 'attributes': "{}"})
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запроса без тела
@pytest.mark.medium
def test_create_node_without_body():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.post(url_node, headers=headers, params=None,
                        data=None)
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запроса со строкой в поле attributes
@pytest.mark.medium
def test_create_node_string_in_attributes():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                'item': item, 'attributes': 'name'}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422


# Тест на отправку запроса с телом запроса в формате dict
@pytest.mark.medium
def test_create_node_dict_in_attributes():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.post(url_node, headers=headers, params=None,
                        json={'project_id': project_id, 'item_type': item_type, 'item': item,
                              'attributes': {'name': 'some_name', 'description': 'some_description'}})
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверным url и эндпоинтом
@pytest.mark.medium
@pytest.mark.parametrize("urls", ["https://skroy.ru/api/v1/node/",
                                  "https://api.cloveri.skroy.ru/api/v2/node/",
                                  "https://api.cloveri.skroy.ru/api/v1/nod/"],
                         ids=['wrong url', 'wrong api version', 'wrong endpoint'])
def test_create_node_wrong_urls(urls):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=urls, wrong_headers=None,
                                                    wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                'item': item, 'attributes': {}}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])


# Тест на отправку запроса неверным методом
@pytest.mark.medium
def test_create_node_wrong_method():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': {}}
    res = requests.patch(url_node, headers=headers, params=None, json=data)
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 405
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверными заголовками и без заголовков
@pytest.mark.medium
@pytest.mark.parametrize("header", [{'Content-Type': 'application/xml', 'Accept': 'application/xml'},
                                    {}],
                         ids=['wrong_media_type_in_headers',
                              'without headers'])
def test_create_node_wrong_headers(header):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=header,
                                                    wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                'item': item, 'attributes': {}}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 415


# Тест на отправку запроса с неверным протоколом http
@pytest.mark.medium
def test_create_node_wrong_protocol():
    status, response, res_headers = org.create_root(attributes=None,
                                                    wrong_url="http://api.cloveri.skroy.ru/api/v1/node/",
                                                    wrong_headers=None, wrong_params=None,
                                                    wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                'item': item, 'attributes': {}})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422


# Тест на отправку запроса с обязательными полями в url
@pytest.mark.min
def test_create_node_fields_in_path():
    status, response, res_headers = org.create_root(attributes=None,
                                                    wrong_url=url_node + f"project_id/{project_id}/item_type/{item_type}/item/{item}/",
                                                    wrong_headers=None, wrong_params=None, wrong_data={})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404


# Тест на отправку запроса с обязательными полями в теле
@pytest.mark.min
def test_create_node_fields_in_query_params():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None, wrong_data={},
                                                    wrong_params={"project_id": project_id, "item_type": item_type,
                                                                  "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тест на отправку запроса с обязательными полями в заголовках
@pytest.mark.min
def test_create_node_fields_in_headers():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_params=None, wrong_data={},
                                                    wrong_headers={"project_id": project_id, "item_type": item_type,
                                                                   "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 422


# Тест на отправку запроса с id в body
@pytest.mark.medium
# @pytest.mark.skip
def test_create_node_id_in_body():
    status, response, res_headers = org.create_child(attributes=None, node_id=None, wrong_headers=None,
                                                    wrong_url=f"https://api.cloveri.skroy.ru/api/v1/node/",
                                                    wrong_data={'parent_id': id_root1, 'project_id': project_id, 'item_type': item_type,
                                                                'item': item, 'attributes': {}}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422
    assert "'id': " not in str(response[0])
