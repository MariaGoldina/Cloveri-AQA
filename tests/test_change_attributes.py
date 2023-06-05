import pytest
# from ..settings import *
# from ..methods import *
from nodes import *


# Базовые тесты на изменение атрибутов узлов всех уровней
@pytest.mark.high
@pytest.mark.parametrize(('get_node', 'path', 'order', 'level'),
                         [(id_root1, path_root1, order_root1, 1),
                          (id_child2lvl, path_child2lvl, order_child2lvl, 2),
                          (id_child3lvl, path_child3lvl, order_child3lvl, 3),
                          (id_child4lvl, path_child4lvl, order_child4lvl, 4)],
                         ids=["change node 1lvl", "change node 2lvl", "change node 3lvl", "change node 4lvl"])
def test_change_attributes_positive(get_node, path, order, level):
    status, response, res_headers = org.change_attributes(attributes={"name": "new name",
                                                                      "description": "new description"},
                                                          node_id=get_node)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == get_node
    assert response[0]['path'] == path
    assert response[0]['inner_order'] == order
    assert response[0]['level_node'] == level
    assert response[0]['attributes'] == '{"name": "new name", "description": "new description"}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тесты на отправку запросов с заголовками в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [upper_headers,
                                           upper_and_low_headers],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_change_attributes_upper_headers(headers_upper):
    status, response, res_headers = org.change_attributes(attributes={"name": "name1", "description": "description1"},
                                                          node_id=id_child4lvl, wrong_id=None, wrong_url=None,
                                                          wrong_headers=headers_upper, wrong_params=None,
                                                          wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] == id_child4lvl
    assert response[0]['attributes'] == '{"name": "name1", "description": "description1"}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с url в верхнем регистре
@pytest.mark.medium
def test_change_attributes_upper_url():
    status, response, res_headers = org.change_attributes(attributes={"name": "name2", "description": "description2"},
                                                          node_id=None, wrong_headers=None, wrong_params=None,
                                                          wrong_url=upper_url_node+f'{id_child4lvl}/attributes/')
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] == id_child4lvl
    assert response[0]['attributes'] == '{"name": "name2", "description": "description2"}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с переменой местами полей в json в теле запроса
@pytest.mark.medium
def test_change_attributes_move_body_fields():
    status, response, res_headers = org.change_attributes(attributes=None, node_id=id_child4lvl, wrong_id=None,
                                                          wrong_url=None, wrong_headers=None,
                                                          wrong_params=None,
                                                          wrong_data={
                                                              'item_type': item_type,
                                                              'project_id': project_id,
                                                              'attributes': json.dumps({"name": "name3",
                                                                                        "description": "description3"},
                                                                                       ensure_ascii=False),
                                                              'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_child4lvl
    assert response[0]['path'] == path_child4lvl
    assert response[0]['inner_order'] == order_child4lvl
    assert response[0]['level_node'] == 4
    assert response[0]['attributes'] == '{"name": "name3", "description": "description3"}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тесты на отправку запросов с разным наполнением поля attributes
@pytest.mark.medium
@pytest.mark.parametrize('other_attributes', ['{}',
                                              '{"name": "name", "description": "description", "tag": "tag"}',
                                              '{"name": "", "description": ""}',
                                              '{"name": "some_name", "description": ""}'],
                         ids=["empty json",
                              "new field in attributes",
                              "empty name and description",
                              "with name and empty description"])
def test_change_attributes_other_attributes(other_attributes):
    status, response, res_headers = org.change_attributes(attributes=None, node_id=id_child4lvl, wrong_id=None,
                                                          wrong_url=None, wrong_headers=None, wrong_params=None,
                                                          wrong_data={
                                                              'project_id': project_id,
                                                              'item_type': item_type,
                                                              'item': item,
                                                              'attributes': other_attributes
                                                          })
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] == id_child4lvl
    assert response[0]['attributes'] == f'{other_attributes}'
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на проверку отображения измененного значения поля attributes get методами
@pytest.mark.medium
def test_change_attributes_check_get_methods():
    status_get_node, response_get_node, _ = org.get_node(node_id=id_child4lvl)
    get_node_attributes_before = response_get_node[0]['attributes']
    status_get_tree, response_get_tree, _ = org.get_tree()
    get_tree_attributes_before = ""
    for node in response_get_tree[0]:
        if node['id'] == id_child4lvl:
            get_tree_attributes_before = node['attributes']
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child3lvl)
    get_children_attributes_before = ""
    for node in response_get_children[0]:
        if node['id'] == id_child4lvl:
            get_children_attributes_before = node['attributes']
    print(get_node_attributes_before, get_tree_attributes_before, get_children_attributes_before)
    assert get_node_attributes_before == get_tree_attributes_before == get_children_attributes_before
    status, response, res_headers = org.change_attributes(attributes={"name": "new name2",
                                                                      "description": "new description2"},
                                                          node_id=id_child4lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    assert response[0]['id'] == id_child4lvl
    changed_attributes = response[0]['attributes']
    assert changed_attributes == '{"name": "new name2", "description": "new description2"}'
    status_get_node, response_get_node, _ = org.get_node(node_id=id_child4lvl)
    get_node_attributes_after = response_get_node[0]['attributes']
    status_get_tree, response_get_tree, _ = org.get_tree()
    get_tree_attributes_after = ""
    for node in response_get_tree[0]:
        if node['id'] == id_child4lvl:
            get_tree_attributes_after = node['attributes']
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child3lvl)
    get_children_attributes_after = ""
    for node in response_get_children[0]:
        if node['id'] == id_child4lvl:
            get_children_attributes_after = node['attributes']
    print(get_node_attributes_after, get_tree_attributes_after, get_children_attributes_after)
    assert get_node_attributes_after == get_tree_attributes_after == get_children_attributes_after == changed_attributes


# Негативные тесты!!!


# Тесты на отправку запросов с ключами обязательных полей в теле в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                                     'attributes': '{"name": "new_name3"}'},
                                    {'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                                     'ATTRIBUTES': '{"name": "new_name3"}'},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'ATTRIBUTES': '{"name": "new_name3"}'}],
                         ids=['only 3 fields UPPER', 'all fields UPPER', 'only attributes UPPER'])
def test_change_attributes_upper_fields(fields):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запроса со всеми характеристиками узла в теле
@pytest.mark.medium
def test_change_attributes_all_fields_in_body():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_params=None,
                                                          wrong_data={'id': id_child4lvl, 'path': path_child4lvl,
                                                                      'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'inner_order': order_child4lvl,
                                                                      'attributes': '{"name": "name1"}', 'level_node': 4})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запросов неверными методами
@pytest.mark.medium
def test_change_attributes_wrong_method():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': '{"name": "name3"}'}
    res1 = requests.put(url_node+f'{id_child4lvl}/attributes/', headers=headers, params=None, json=data)
    status1 = res1.status_code
    res_headers1 = res1.headers
    try:
        response1 = res1.json(),
    except json.decoder.JSONDecodeError:
        response1 = res1.text
    print(f"\nCode: {status1}")
    print(f"Response: {response1}")
    print(f'Response headers: {res_headers1}')
    assert status1 != 201
    assert status1 == 405
    assert "'id': " not in str(response1[0])
    res2 = requests.post(url_node+f'{id_child4lvl}/attributes/', headers=headers, params=None, json=data)
    status2 = res2.status_code
    res_headers2 = res2.headers
    try:
        response2 = res2.json(),
    except json.decoder.JSONDecodeError:
        response2 = res2.text
    print(f"\nCode: {status2}")
    print(f"Response: {response2}")
    print(f'Response headers: {res_headers2}')
    assert status2 != 201
    assert status2 == 405
    assert "'id': " not in str(response2[0])
    res3 = requests.get(url_node+f'{id_child4lvl}/attributes/', headers=headers, params=None, json=data)
    status3 = res3.status_code
    res_headers3 = res3.headers
    try:
        response3 = res3.json(),
    except json.decoder.JSONDecodeError:
        response3 = res3.text
    print(f"\nCode: {status3}")
    print(f"Response: {response3}")
    print(f'Response headers: {res_headers3}')
    assert status3 != 201
    assert status3 == 405
    assert "'id': " not in str(response3[0])
    res4 = requests.delete(url_node+f'{id_child4lvl}/attributes/', headers=headers, params=None, json=data)
    status4 = res4.status_code
    res_headers4 = res4.headers
    try:
        response4 = res4.json(),
    except json.decoder.JSONDecodeError:
        response4 = res4.text
    print(f"\nCode: {status4}")
    print(f"Response: {response4}")
    print(f'Response headers: {res_headers4}')
    assert status4 != 201
    assert status4 == 405
    assert "'id': " not in str(response4[0])


# Тесты на отправку запросов с неверным url и эндпоинтом
@pytest.mark.medium
@pytest.mark.parametrize("urls", [
                                  # f"https://api.cloveri.ru/api/v1/node/{id_child4lvl}/attributes/",
                                  f"https://api.cloveri.skroy.ru/api/v2/node/{id_child4lvl}/attributes/",
                                  f"https://api.cloveri.skroy.ru/api/v1/nod/{id_child4lvl}/attributes/"],
                         ids=[
                             # 'wrong url',
                             'wrong api version', 'wrong endpoint'])
def test_change_attributes_wrong_urls(urls):
    status, response, res_headers = org.change_attributes(node_id=None, attributes={"name": "name2"},
                                                          wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с неверными заголовками
@pytest.mark.medium
def test_change_attributes_wrong_media_type_in_headers():
    headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': '{"name": "name4"}'}
    res = requests.patch(url_node + f'{id_child4lvl}/attributes/', headers=headers, params=None, json=data)
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 415


# Тест на отправку запроса без заголовков
@pytest.mark.medium
def test_change_attributes_without_headers():
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': '{"name": "name5"}'}
    res = requests.patch(url_node + f'{id_child4lvl}/attributes/', headers=None, params=None, data=data)
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 415


# Тесты на отправку запросов с неверным id в url
@pytest.mark.medium
@pytest.mark.parametrize("urls", [f"{url_node}/abc/attributes/",
                                  f"{url_node} /attributes/",
                                  f"{url_node}None/attributes/",
                                  f"{url_node}attributes/",
                                  f"{url_node}100000/attributes/"],
                         ids=['incorrect format', 'empty id', 'id is None', 'without id', 'nonexistent id'])
def test_change_attributes_with_incorrect_id_in_url(urls):
    status, response, res_headers = org.change_attributes(node_id=None, attributes={"name": "name3"},
                                                          wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с телом запроса в формате text
@pytest.mark.medium
def test_change_attributes_with_text_in_body():
    res = requests.patch(url_node + f'{id_child4lvl}/attributes/', headers=None, params=None,
                         data=f"'project_id': {project_id}, 'item_type': {item_type}, 'item': {item}, "
                              f"'attributes': 'name': 'name1'")
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


# Тест на отправку запроса со строкой в поле attributes
@pytest.mark.medium
@pytest.mark.parametrize("string", ['name: new_name', ''],
                         ids=['string in attributes', 'empty string in attributes'])
def test_change_attributes_string_in_attributes(string):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_params=None,
                                                          wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'attributes': string})

    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422


# Тест на отправку запросов с измененными значениями в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': other_project_id, 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name1"}'},
                                    {'project_id': project_id, 'item_type': other_item_type,
                                     'item': item, 'attributes': '{"name": "new_name1"}'},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': other_item, 'attributes': '{"name": "new_name1"}'}],
                         ids=['changed project_id', 'changed item_type', 'changed item'])
def test_change_attributes_with_changed_value_in_fields(fields):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': 123, 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name2"}'},
                                    {'project_id': 'abc', 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name2"}'},
                                    {'project_id': project_id, 'item_type': 123, 'item': item,
                                     'attributes': '{"name": "new_name2"}'},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': 123, 'attributes': '{"name": "new_name2"}'}],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_change_attributes_with_incorrect_format_in_fields(fields):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с полем attributes в формате dict
@pytest.mark.medium
def test_change_attributes_dict_in_attributes():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(url_node + f'{id_child4lvl}/attributes/', headers=headers, params=None,
                         json={'project_id': project_id, 'item_type': item_type, 'item': item,
                               'attributes': {'name': 'new_name2'}})
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


# Тест на отправку запроса с неверным протоколом http
@pytest.mark.medium
def test_change_attributes_wrong_protocol():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(f"http://api.cloveri.skroy.ru/api/v1/node/{id_child4lvl}/attributes/", headers=headers,
                         params=None, json={'project_id': project_id, 'item_type': item_type, 'item': item,
                                            'attributes': '{"name": "name2"}'})
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
    assert status == 422 or status == 404
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с дублированием обязательных полей в теле
@pytest.mark.medium
@pytest.mark.parametrize("fields",
                         [{'project_id': project_id, 'item_type': item_type, 'item': item,
                           'attributes': '{"name": "new_name"}', 'project_id': project_id, 'item_type': item_type,
                           'item': item, 'attributes': '{"name": "new_name"}'},
                          {'project_id': other_project_id, 'item_type': other_item_type, 'item': other_item,
                           'attributes': '{"name": "other_new_name"}', 'project_id': project_id, 'item_type': item_type,
                           'item': item, 'attributes': '{"name": "new_name"}'}],
                         ids=['double fields with same values', 'double fields with different values'])
def test_change_attributes_with_double_fields(fields):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 422 or status == 404


# Тесты на отправку запросов без обязательных полей и с непредусмотренными полями
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'item_type': item_type, 'item': item, 'attributes': '{"name": "new_name3"}'},
                                    {'project_id': project_id, 'item': item, 'attributes': '{"name": "new_name3"}'},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'attributes': '{"name": "new_name3"}'},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item},
                                    {'project_ids': project_id, 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name3"}'},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name3"}', 'new_field': ''}],
                         ids=['without project_id', 'without item_type', 'without item', 'without attributes',
                              'with projest_ids', 'with new field'])
def test_change_attributes_without_required_fields(fields):
    status, response, res_headers = org.change_attributes(attributes=None, node_id=id_child4lvl,
                                                          wrong_url=None, wrong_headers=None, wrong_data=fields,
                                                          wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запросов с несуществующими значениями в обязательных полях
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'project_id': nonexistent_project_id, 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name4"}'},
                                    {'project_id': project_id, 'item_type': nonexistent_item_type,
                                     'item': item, 'attributes': '{"name": "new_name4"}'},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': nonexistent_item, 'attributes': '{"name": "new_name4"}'}],
                         ids=['nonexistent project_id', 'nonexistent item_type', 'nonexistent item'])
def test_change_attributes_with_nonexistent_value_in_fields(fields):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422
    assert "'id': " not in str(response[0])


# Тесты на отправку запросов с пустыми значениями в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': "", 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name1"}'},
                                    {'project_id': project_id, 'item_type': "", 'item': item,
                                     'attributes': '{"name": "new_name1"}'},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': "", 'attributes': '{"name": "new_name1"}'},
                                    {'project_id': None, 'item_type': item_type, 'item': item,
                                     'attributes': '{"name": "new_name1"}'},
                                    {'project_id': project_id, 'item_type': None, 'item': item,
                                     'attributes': '{"name": "new_name1"}'},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': None, 'attributes': '{"name": "new_name1"}'}],
                         ids=['project_id empty', 'item_type empty', 'item empty',
                              'project_id Null', 'item_type Null', 'item Null'])
def test_change_attributes_with_empty_value_in_fields(fields):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])


# Тест на отправку запроса без тела
@pytest.mark.medium
def test_change_attributes_without_body():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(url_node+f'{id_child4lvl}/attributes/', headers=headers, params=None, data=None)
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


# Тест на отправку запроса с обязательными полями в url
@pytest.mark.min
def test_change_attributes_fields_in_path():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'attributes': '{"name": "new_name5"}'}
    res = requests.patch(url_node + f'project_id/{project_id}/item_type/{item_type}/item/{item}/{id_child4lvl}/attributes/',
                         headers=headers, params=None, json=data)
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
    assert status == 404
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с обязательными полями в теле + с отправкой text в теле
@pytest.mark.min
def test_change_attributes_fields_in_query_params():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data={'attributes': '{"name": "name5"}'},
                                                          wrong_params={"project_id": project_id, "item_type": item_type,
                                                                        "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422


# Тест на отправку запроса с обязательными полями в заголовках
@pytest.mark.min
def test_change_attributes_fields_in_headers():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_params=None, wrong_data={'attributes': '{"name": "name1"}'},
                                                          wrong_headers={"project_id": project_id, "item_type": item_type,
                                                                         "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422


# Тест на отправку запроса с id в query params
@pytest.mark.medium
# @pytest.mark.skip
def test_change_attributes_id_in_query_params():
    status, response, res_headers = org.change_attributes(node_id=None, attributes=None, wrong_headers=None,
                                                          wrong_url=f"https://api.cloveri.skroy.ru/api/v1/node/attributes/",
                                                          wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'attributes': '{"name": "name2"}'},
                                                          wrong_params={"id": id_child4lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])


# Тест на отправку запроса с id в headers
@pytest.mark.medium
# @pytest.mark.skip
def test_change_attributes_id_in_headers():
    status, response, res_headers = org.change_attributes(node_id=None, attributes=None, wrong_params=None,
                                                          wrong_url=f"https://api.cloveri.skroy.ru/api/v1/node/attributes/",
                                                          wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'attributes': '{"name": "name2"}'},
                                                          wrong_headers={"id": str(id_child4lvl)})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])
