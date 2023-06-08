import pytest
# from ..settings import *
# from ..methods import *
from ..nodes import *


# Базовые тесты на изменение атрибутов узлов всех уровней
# OS-API-Ua-1, OS-API-Ua-2, OS-API-Ua-3, OS-API-Ua-4
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
# OS-API-Ua-8, OS-API-Ua-9
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
# OS-API-Ua-11
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
# OS-API-Ua-10
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
# OS-API-Ua-12, OS-API-Ua-66a, OS-API-Ua-67, OS-API-Ua-68
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
# OS-API-Ua-73
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
# OS-API-Ua-13, OS-API-Ua-14
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field'),
                         [({'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                           'attributes': '{"name": "new_name3"}'}, ['project_id', 'item_type', 'item']),
                          ({'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                           'ATTRIBUTES': '{"name": "new_name3"}'}, ['project_id', 'item_type', 'item', 'attributes']),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'ATTRIBUTES': '{"name": "new_name3"}'}, ['attributes'])],
                         ids=[
                             'only 3 fields UPPER',
                             'all fields UPPER', 'only attributes UPPER'])
def test_change_attributes_upper_fields(fields, field):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    for s in field:
        assert f'field {s} is required' in str(response[0])
        assert f'field {s.upper()} not allowed' in str(response[0])


# Тест на отправку запроса со всеми характеристиками узла в теле
# OS-API-Ua-5
@pytest.mark.medium
def test_change_attributes_all_fields_in_body():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_params=None,
                                                          wrong_data={'id': id_child4lvl, 'path': path_child4lvl,
                                                                      'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'inner_order': order_child4lvl,
                                                                      'attributes': '{"name": "name1"}',
                                                                      'level_node': 4})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert 'field id not allowed' in str(response[0]) and 'field path not allowed' in str(response[0]) \
           and 'field inner_order not allowed' in str(response[0]) \
           and 'field level_node not allowed' in str(response[0])


# Тест на отправку запросов неверными методами
# OS-API-Ua-15
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
# OS-API-Ua-16, OS-API-Ua-16a, OS-API-Ua-17
@pytest.mark.medium
@pytest.mark.parametrize("urls", [
                                  # f"https://api.cloveri.ru/api/v1/node/{id_child4lvl}/attributes/",
                                  f"https://api.cloveri.skroy.ru/api/v2/node/{id_child4lvl}/attributes/",
                                  f"https://api.cloveri.skroy.ru/api/v1/node/{id_child4lvl}/attributs/"],
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
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)


# Тест на отправку запроса с неверными заголовками
# OS-API-Ua-23
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
# OS-API-Ua-24
@pytest.mark.medium
def test_change_attributes_without_headers():
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'attributes': '{"name": "name5"}'}
    res = requests.patch(url_node + f'{id_child4lvl}/attributes/', params=None, data=data)
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
# OS-API-Ua-18, OS-API-Ua-19, OS-API-Ua-20, OS-API-Ua-64
@pytest.mark.medium
@pytest.mark.parametrize("urls", [f"{url_node}/abc/attributes/",
                                  f"{url_node} /attributes/",
                                  f"{url_node}None/attributes/",
                                  f"{url_node}attributes/"],
                         ids=['incorrect format', 'empty id', 'id is None', 'without id'])
def test_change_attributes_with_incorrect_id_in_url(urls):
    status, response, res_headers = org.change_attributes(node_id=None, attributes={"name": "name3"},
                                                          wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)


# Тесты на отправку запросов с несуществующим id в url
# OS-API-Ua-60
@pytest.mark.medium
def test_change_attributes_with_nonexistent_id_in_url():
    status, response, res_headers = org.change_attributes(node_id=None, attributes={"name": "name3"},
                                                          wrong_url=f"{url_node}100000/attributes/",
                                                          wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "does not exist object(s)" in str(response[0])


# Тест на отправку запроса с телом запроса в формате text
# OS-API-Ua-31
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
# OS-API-Ua-34
@pytest.mark.medium
def test_change_attributes_string_in_attributes():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_params=None,
                                                          wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'attributes': 'name: new_name'})

    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert 'attributes has wrong format, must be json' in str(response[0])


# Тест на отправку запроса с пустой строкой в поле attributes
# OS-API-Ua-35
@pytest.mark.medium
def test_change_attributes_empty_string_in_attributes():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_params=None,
                                                          wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'attributes': ''})

    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert 'field attributes must not be empty' in str(response[0]) \
           or 'attributes has wrong format, must be json' in str(response[0])


# Тест на отправку запросов с измененными значениями в обязательных полях
# OS-API-Ua-36, OS-API-Ua-37, OS-API-Ua-38
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
    assert status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "does not exist object(s)" in str(response[0])


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
# OS-API-Ua-45, OS-API-Ua-46, OS-API-Ua-47
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field', 'formats'),
                         [({'project_id': 123, 'item_type': item_type, 'item': item,
                           'attributes': '{"name": "new_name2"}'}, 'project_id', 'uuid'),
                          ({'project_id': 'abc', 'item_type': item_type, 'item': item,
                           'attributes': '{"name": "new_name2"}'}, 'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': 123, 'item': item,
                           'attributes': '{"name": "new_name2"}'}, 'item_type', 'str'),
                          ({'project_id': project_id, 'item_type': item_type,
                           'item': 123, 'attributes': '{"name": "new_name2"}'}, 'item', 'str')],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_change_attributes_with_incorrect_format_in_fields(fields, field, formats):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f"['{field} has wrong format, must be {formats}']" in str(response[0])


# Тест на отправку запроса с полем attributes в формате dict
# OS-API-Ua-66
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
    assert 'error' in str(response[0])
    assert 'attributes has wrong format, must be json' in str(response[0])


# Тест на отправку запроса с неверным протоколом http
# OS-API-Ua-70
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
# OS-API-Ua-71, OS-API-Ua-72
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


# Тесты на отправку запросов без обязательных полей
# OS-API-Ua-26, OS-API-Ua-27, OS-API-Ua-28, OS-API-Ua-30, OS-API-Ua-60
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'field'),
                         [({'item_type': item_type, 'item': item, 'attributes': '{"name": "new_name3"}'}, 'project_id'),
                          ({'project_id': project_id, 'item': item, 'attributes': '{"name": "new_name3"}'},
                           'item_type'),
                          ({'project_id': project_id, 'item_type': item_type, 'attributes': '{"name": "new_name3"}'},
                           'item'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item}, 'attributes'),
                          ({'project_ids': project_id, 'item_type': item_type, 'item': item,
                            'attributes': '{"name": "new_name3"}'}, 'project_id')],
                         ids=['without project_id', 'without item_type', 'without item', 'without attributes',
                              'mistake in project_id'])
def test_change_attributes_without_required_fields(fields, field):
    status, response, res_headers = org.change_attributes(attributes=None, node_id=id_child4lvl,
                                                          wrong_url=None, wrong_headers=None, wrong_data=fields,
                                                          wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f'field {field} is required' in str(response[0])


# Тесты на отправку запросов с непредусмотренными полями
# OS-API-Ua-60
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'field'),
                         [({'project_ids': project_id, 'item_type': item_type, 'item': item,
                           'attributes': '{"name": "new_name3"}'}, 'project_ids'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'attributes': '{"name": "new_name3"}', 'new_field': ''}, 'new_field')],
                         ids=['with projest_ids', 'with new field'])
def test_change_attributes_with_not_allowed_fields(fields, field):
    status, response, res_headers = org.change_attributes(attributes=None, node_id=id_child4lvl,
                                                          wrong_url=None, wrong_headers=None, wrong_data=fields,
                                                          wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f"field {field} not allowed" in str(response[0])


# Тест на отправку запросов с несуществующими значениями в обязательных полях
# OS-API-Ua-61, OS-API-Ua-62, OS-API-Ua-63
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
    assert status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "does not exist object(s)" in str(response[0])


# Тесты на отправку запросов с пустыми значениями в обязательных полях
# OS-API-Ua-48, OS-API-Ua-49, OS-API-Ua-50, OS-API-Ua-54, OS-API-Ua-55, OS-API-Ua-56
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field', 'formats'),
                         [({'project_id': "", 'item_type': item_type, 'item': item,
                           'attributes': '{"name": "new_name1"}'}, 'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': "", 'item': item,
                           'attributes': '{"name": "new_name1"}'}, 'item_type', 'str'),
                          ({'project_id': project_id, 'item_type': item_type,
                           'item': "", 'attributes': '{"name": "new_name1"}'}, 'item', 'str'),
                          ({'project_id': None, 'item_type': item_type, 'item': item,
                            'attributes': '{"name": "new_name1"}'}, 'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': None, 'item': item,
                            'attributes': '{"name": "new_name1"}'}, 'item_type', 'str'),
                          ({'project_id': project_id, 'item_type': item_type,
                           'item': None, 'attributes': '{"name": "new_name1"}'}, 'item', 'str')],
                         ids=['project_id empty', 'item_type empty', 'item empty',
                              'project_id Null', 'item_type Null', 'item Null'])
def test_change_attributes_with_empty_value_in_fields(fields, field, formats):
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f"['field {field} must not be empty']" in str(response[0]) \
           or f"['{field} has wrong format, must be {formats}']" in str(response[0])


# Тест на отправку запроса без тела
# OS-API-Ua-32
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
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0]) and 'field attributes is required' in str(response[0])


# Тест на отправку запроса с обязательными полями в url
# OS-API-Ua-22
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
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)


# Тест на отправку запроса с обязательными полями в query params
# OS-API-Ua-69
@pytest.mark.min
def test_change_attributes_fields_in_query_params():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_headers=None, wrong_data={},
                                                          wrong_params={"project_id": project_id, "item_type": item_type,
                                                                        "item": item, 'attributes': '{"name": "name5"}'})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0]) and 'field attributes is required' in str(response[0])


# Тест на отправку запроса с обязательными полями в заголовках
# OS-API-Ua-25
@pytest.mark.min
def test_change_attributes_fields_in_headers():
    status, response, res_headers = org.change_attributes(node_id=id_child4lvl, attributes=None, wrong_url=None,
                                                          wrong_params=None, wrong_data={},
                                                          wrong_headers={"project_id": project_id, "item_type": item_type,
                                                                         "item": item, 'attributes': '{"name": "name1"}'})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0]) and 'field attributes is required' in str(response[0])


# Тест на отправку запроса с id в query params
# OS-API-Ua-21
@pytest.mark.min
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
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)


# Тест на отправку запроса с id в headers
# OS-API-Ua-65
@pytest.mark.min
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
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)
