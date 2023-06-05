import pytest
# from ..settings import *
# from ..methods import *
from nodes import *


# Базовый тест на изменение порядка узлов всех уровней
@pytest.mark.high
@pytest.mark.parametrize(('node_out', 'node_in', 'path', 'order', 'level'),
                         [(id_root1, id_root2, path_root1, order_root2, 1),
                          (id_child2lvl, id_sec_child2lvl, path_child2lvl, order_sec_child2lvl, 2),
                          (id_child3lvl, id_sec_child3lvl, path_child3lvl, order_sec_child3lvl, 3),
                          (id_child4lvl, id_sec_child4lvl, path_child4lvl, order_sec_child4lvl, 4)],
                         ids=["change order for node 1lvl", "change order for node 2lvl",
                              "change order for node 3lvl", "change order for node 4lvl"])
def test_change_order_positive(node_out, node_in, path, order, level):
    # _, changing_node_out, _ = org.get_node(node_id=node_out)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=node_in)
    # print(changing_node_in)
    status, response, res_headers = org.change_order(node_id_out=node_out, node_id_in=node_in)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=node_out)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == node_out
    assert response[0]['path'] == path
    assert response[0]['inner_order'] == order
    assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == level
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=node_out)
    # print(changed_node_out)
    # _, changed_node_in, _ = org.get_node(node_id=node_in)
    # print(changed_node_in)
    org.change_order(node_id_out=node_in, node_id_in=node_out)


# Тест на изменение порядка узла без дочек
@pytest.mark.high
def test_change_order_for_node_without_children():
    # _, changing_node_out, _ = org.get_node(node_id=id_sec_child4lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_child4lvl)
    # print(changing_node_in)
    status, response, res_headers = org.change_order(node_id_out=id_sec_child4lvl, node_id_in=id_child4lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_sec_child4lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_sec_child4lvl
    assert response[0]['path'] == path_sec_child4lvl
    assert response[0]['inner_order'] == order_child4lvl
    assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 4
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=id_sec_child4lvl)
    # print(changed_node_out)
    # _, changed_node_in, _ = org.get_node(node_id=id_child4lvl)
    # print(changed_node_in)
    org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на изменение порядка узла с дочками
@pytest.mark.high
def test_change_order_for_node_with_children():
    # _, changing_node_out, _ = org.get_node(node_id=id_child3lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_sec_child3lvl)
    # print(changing_node_in)
    status, response, res_headers = org.change_order(node_id_out=id_child3lvl, node_id_in=id_sec_child3lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child3lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_child3lvl
    assert response[0]['path'] == path_child3lvl
    assert response[0]['inner_order'] == order_sec_child3lvl
    assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 3
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=id_child3lvl)
    # print(changed_node_out)
    # _, changed_node_in, _ = org.get_node(node_id=id_sec_child3lvl)
    # print(changed_node_in)
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child3lvl)
    print(response_get_children)
    all_children = []
    for node in response_get_children[0]:
        if node['path'][0:-10] == path_child3lvl and node['level_node'] == 4:
            all_children.append(node)
    for s in all_children:
        assert s['inner_order'][:-10] == order_sec_child3lvl
    org.change_order(node_id_out=id_sec_child3lvl, node_id_in=id_child3lvl)


# Тест на изменение порядка на разное количество шагов
@pytest.mark.high
@pytest.mark.parametrize(('node_out', 'node_in', 'node_back', 'path', 'order', 'level'),
                         [(id_child4lvl, id_sec_child4lvl, id_sec_child4lvl, path_child4lvl, order_sec_child4lvl, 4),
                          (id_child4lvl, id_third_child4lvl, id_sec_child4lvl, path_child4lvl,
                           order_third_child4lvl, 4),
                          (id_child4lvl, id_fourth_child4lvl, id_sec_child4lvl, path_child4lvl,
                           order_fourth_child4lvl, 4),
                          (id_fourth_child4lvl, id_third_child4lvl, id_third_child4lvl, path_fourth_child4lvl,
                           order_third_child4lvl, 4),
                          (id_fourth_child4lvl, id_sec_child4lvl, id_third_child4lvl, path_fourth_child4lvl,
                           order_sec_child4lvl, 4),
                          (id_fourth_child4lvl, id_child4lvl, id_third_child4lvl, path_fourth_child4lvl,
                           order_child4lvl, 4)],
                         ids=["1 step down", "2 steps down", "down to the end", "1 step up", "2 steps up",
                              "up to the start"])
def test_change_order_remove_on_different_steps(node_out, node_in, node_back, path, order, level):
    # _, changing_node_out, _ = org.get_node(node_id=node_out)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=node_in)
    # print(changing_node_in)
    status, response, res_headers = org.change_order(node_id_out=node_out, node_id_in=node_in)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=node_out)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == node_out
    assert response[0]['path'] == path
    assert response[0]['inner_order'] == order
    assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == level
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=node_out)
    # print(changed_node_out)
    # _, changed_node_in, _ = org.get_node(node_id=node_in)
    # print(changed_node_in)
    org.change_order(node_id_out=node_out, node_id_in=node_back)
    # _, back_node_out, _ = org.get_node(node_id=node_out)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=node_in)
    # print(back_node_in)


# Тест на изменение порядка узла с переходом разряда в inner_order (с 9 места на 10 и назад)
@pytest.mark.high
def test_change_order_with_change_numbers_9_and_10_in_inner_order():
    _, fifth_child4lvl, _ = org.create_child(node_id=id_child3lvl, attributes={})
    _, sixth_child4lvl, _ = org.create_child(node_id=id_child3lvl, attributes={})
    _, seventh_child4lvl, _ = org.create_child(node_id=id_child3lvl, attributes={})
    _, eighth_child4lvl, _ = org.create_child(node_id=id_child3lvl, attributes={})
    _, ninth_child4lvl, _ = org.create_child(node_id=id_child3lvl, attributes={})
    id_ninth_child4lvl = ninth_child4lvl[0]['id']
    _, tenth_child4lvl, _ = org.create_child(node_id=id_child3lvl, attributes={})
    id_tenth_child4lvl = tenth_child4lvl[0]['id']
    # _, changing_node_out, _ = org.get_node(node_id=id_ninth_child4lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_tenth_child4lvl)
    # print(changing_node_in)
    status, response, res_headers = org.change_order(node_id_out=id_ninth_child4lvl, node_id_in=id_tenth_child4lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_ninth_child4lvl)
    assert response[0]['id'] == id_ninth_child4lvl
    assert response[0]['inner_order'] == tenth_child4lvl[0]['inner_order']
    assert "'Content-Type': 'application/json'" in str(res_headers)
    # _, changed_node_out, _ = org.get_node(node_id=id_ninth_child4lvl)
    # print(changed_node_out)
    # _, changed_node_in, _ = org.get_node(node_id=id_tenth_child4lvl)
    # print(changed_node_in)
    status, response, res_headers = org.change_order(node_id_out=id_ninth_child4lvl, node_id_in=id_tenth_child4lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_ninth_child4lvl)
    assert response[0]['id'] == id_ninth_child4lvl
    assert response[0]['inner_order'] == ninth_child4lvl[0]['inner_order']
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тесты на отправку запросов с заголовками в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [upper_headers,
                                           upper_and_low_headers],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_change_order_upper_headers(headers_upper):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=headers_upper, wrong_params=None,
                                                     wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child4lvl)
    assert response[0]['id'] == id_child4lvl
    assert response[0]['inner_order'] == order_sec_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_sec_child4lvl)
    # print(back_node_in)


# Тест на отправку запроса с url в верхнем регистре
@pytest.mark.medium
def test_change_order_upper_url():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_headers=None, wrong_params=None,
                                                     wrong_url=upper_url_node + f'{id_child4lvl}/order/')
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child4lvl)
    assert response[0]['id'] == id_child4lvl
    assert response[0]['inner_order'] == order_sec_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_sec_child4lvl)
    # print(back_node_in)


# Тест на отправку запроса с переменой местами полей в json в теле запроса
@pytest.mark.medium
def test_change_order_move_body_fields():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_id=None, wrong_url=None, wrong_headers=None,
                                                     wrong_params=None, wrong_data={'item_type': item_type,
                                                                                    'project_id': project_id,
                                                                                    'destination_node_id': id_sec_child4lvl,
                                                                                    'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child4lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_child4lvl
    assert response[0]['inner_order'] == order_sec_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_sec_child4lvl)
    # print(back_node_in)


# Тест на проверку отображения get методами измененного значения поля inner_order у узла без дочек
@pytest.mark.medium
def test_change_order_without_children_check_get_methods():
    status_get_node, response_get_node, _ = org.get_node(node_id=id_child4lvl)
    get_node_order_before = response_get_node[0]['inner_order']
    status_get_tree, response_get_tree, _ = org.get_tree()
    get_tree_order_before = ""
    for node in response_get_tree[0]:
        if node['id'] == id_child4lvl:
            get_tree_order_before = node['inner_order']
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child3lvl)
    get_children_order_before = ""
    for node in response_get_children[0]:
        if node['id'] == id_child4lvl:
            get_children_order_before = node['inner_order']
    print(get_node_order_before, get_tree_order_before, get_children_order_before)
    assert get_node_order_before == get_tree_order_before == get_children_order_before
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child4lvl)
    assert response[0]['id'] == id_child4lvl
    assert response[0]['inner_order'] == order_sec_child4lvl
    status_get_node, response_get_node, _ = org.get_node(node_id=id_child4lvl)
    get_node_order_after = response_get_node[0]['inner_order']
    status_get_tree, response_get_tree, _ = org.get_tree()
    get_tree_order_after = ""
    for node in response_get_tree[0]:
        if node['id'] == id_child4lvl:
            get_tree_order_after = node['inner_order']
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child3lvl)
    get_children_order_after = ""
    for node in response_get_children[0]:
        if node['id'] == id_child4lvl:
            get_children_order_after = node['inner_order']
    print(get_node_order_after, get_tree_order_after, get_children_order_after)
    assert get_node_order_after == get_tree_order_after == get_children_order_after == order_sec_child4lvl
    relatives = []
    must_be_relatives = [id_child4lvl, id_sec_child4lvl, id_third_child4lvl, id_fourth_child4lvl]
    for node in response_get_tree[0]:
        if node['id'] in must_be_relatives:
            relatives.append(node)
    print(relatives)
    relatives_ids = [i['id'] for i in relatives]
    assert relatives_ids == [id_sec_child4lvl, id_child4lvl, id_third_child4lvl, id_fourth_child4lvl]
    org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_sec_child4lvl)
    # print(back_node_in)


# Тест на проверку отображения get методами измененного значения поля inner_order у узла с дочками и у всех дочек
@pytest.mark.medium
def test_change_order_with_children_check_get_methods():
    status_get_node, response_get_node, _ = org.get_node(node_id=id_child3lvl)
    get_node_order_before = response_get_node[0]['inner_order']
    status_get_tree, response_get_tree, _ = org.get_tree()
    get_tree_order_before = ""
    for node in response_get_tree[0]:
        if node['id'] == id_child3lvl:
            get_tree_order_before = node['inner_order']
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child2lvl)
    get_children_order_before = ""
    for node in response_get_children[0]:
        if node['id'] == id_child3lvl:
            get_children_order_before = node['inner_order']
    print(get_node_order_before, get_tree_order_before, get_children_order_before)
    assert get_node_order_before == get_tree_order_before == get_children_order_before
    status, response, res_headers = org.change_order(node_id_out=id_child3lvl, node_id_in=id_sec_child3lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child3lvl)
    assert response[0]['id'] == id_child3lvl
    assert response[0]['inner_order'] == order_sec_child3lvl
    status_get_node, response_get_node, _ = org.get_node(node_id=id_child3lvl)
    get_node_order_after = response_get_node[0]['inner_order']
    status_get_tree, response_get_tree, _ = org.get_tree()
    get_tree_order_after = ""
    for node in response_get_tree[0]:
        if node['id'] == id_child3lvl:
            get_tree_order_after = node['inner_order']
    status_get_children, response_get_children, _ = org.get_children(node_id=id_child2lvl)
    get_children_order_after = ""
    for node in response_get_children[0]:
        if node['id'] == id_child3lvl:
            get_children_order_after = node['inner_order']
    print(get_node_order_after, get_tree_order_after, get_children_order_after)
    assert get_node_order_after == get_tree_order_after == get_children_order_after == order_sec_child3lvl
    relatives = []
    for node in response_get_tree[0]:
        if node['path'][0:-10] == path_child2lvl and node['level_node'] == 3:
            relatives.append(node)
    print(relatives)
    relatives_ids = [i['id'] for i in relatives]
    assert relatives_ids == [id_sec_child3lvl, id_child3lvl]
    for node in response_get_children[0]:
        if node['path'][0:-10] == path_child3lvl:
            assert node['inner_order'][0:-10] == order_sec_child3lvl
    org.change_order(node_id_out=id_child3lvl, node_id_in=id_sec_child3lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_child3lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_sec_child3lvl)
    # print(back_node_in)


# Негативные тесты!!!


# Тесты на отправку запросов с ключами обязательных полей в теле в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                                     'DESTINATION_NODE_ID': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'DESTINATION_NODE_ID': id_sec_child4lvl}],
                         ids=['only 3 fields UPPER', 'all fields UPPER', 'only destination_node_id UPPER'])
def test_change_order_upper_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса со всеми характеристиками узла в теле
@pytest.mark.medium
def test_change_order_all_fields_in_body():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_params=None,
                                                     wrong_data={'id': id_child4lvl, 'path': path_child4lvl,
                                                                 'project_id': project_id, 'item_type': item_type,
                                                                 'item': item, 'inner_order': order_child4lvl,
                                                                 'attributes': '{}', 'level_node': 4,
                                                                 'destination_node_id': id_sec_child4lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с полем inner_order вместо destination_node_id
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': project_id, 'item_type': item_type,
                                    'item': item, 'inner_order': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': item, 'destination_node_id': id_sec_child4lvl,
                                     'inner_order': id_sec_child4lvl}],
                         ids=['inner_order instead destination_node_id', 'inner_order and destination_node_id in body'])
def test_change_order_with_inner_order_instead_destination_node_id(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_params=None,
                                                     wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запросов неверными методами
@pytest.mark.medium
def test_change_order_wrong_method():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'destination_node_id': id_sec_child4lvl}
    res1 = requests.put(url_node + f'{id_child4lvl}/order/', headers=headers, params=None, json=data)
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
    # assert "'id': " not in str(response1[0])
    res2 = requests.post(url_node + f'{id_child4lvl}/order/', headers=headers, params=None, json=data)
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
    # assert "'id': " not in str(response2[0])
    res3 = requests.get(url_node + f'{id_child4lvl}/order/', headers=headers, params=None, json=data)
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
    # assert "'id': " not in str(response3[0])
    res4 = requests.delete(url_node + f'{id_child4lvl}/order/', headers=headers, params=None, json=data)
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
    # assert "'id': " not in str(response4[0])
    if status1 == 201 or status2 == 201 or status3 == 201 or status4 == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов с неверным url и эндпоинтом
@pytest.mark.medium
@pytest.mark.parametrize("urls", [
                                  # f"https://skroy.ru/api/v1/node/{id_child4lvl}/order/",
                                  f"https://api.cloveri.skroy.ru/api/v2/node/{id_child4lvl}/order/",
                                  f"https://api.cloveri.skroy.ru/api/v1/nod/{id_child4lvl}/order/"],
                         ids=[
                             # 'wrong url',
                             'wrong api version', 'wrong endpoint'])
def test_change_order_wrong_urls(urls):
    status, response, res_headers = org.change_order(node_id_out=None, node_id_in=id_sec_child4lvl,
                                                     wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с неверными заголовками
@pytest.mark.medium
def test_change_order_wrong_media_type_in_headers():
    headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=headers, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 415
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса без заголовков
@pytest.mark.medium
@pytest.mark.skip
def test_change_order_without_headers():
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'destination_node_id': id_sec_child4lvl}
    res = requests.patch(url_node + f'{id_child4lvl}/order/', headers=None, params=None, data=data)
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
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов с неверным id в url
@pytest.mark.medium
@pytest.mark.parametrize("urls", [f"{url_node}abc/order/",
                                  f"{url_node} /order/",
                                  f"{url_node}None/order/",
                                  f"{url_node}order/",
                                  f"{url_node}100000/order/"],
                         ids=['incorrect format', 'empty id', 'id is None', 'without id', 'nonexistent id'])
def test_change_order_with_incorrect_id_in_url(urls):
    status, response, res_headers = org.change_order(node_id_out=None, node_id_in=id_sec_child4lvl,
                                                     wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с телом запроса в формате text
@pytest.mark.medium
def test_change_order_with_text_in_body():
    res = requests.patch(url_node + f'{id_child4lvl}/order/', headers=None, params=None,
                       data=f"'project_id': {project_id}, 'item_type': {item_type}, 'item': {item}, "
                            f"'destination_node_id': {id_sec_child4lvl}")
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
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов с разными значениями в поле destination_node_id
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': 'abc'},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': str(id_sec_child4lvl)},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': 100000},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': ''},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': None},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': float(id_sec_child4lvl)},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': 0},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': -id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_child4lvl}],
                         ids=['string in value', 'number in string in value', 'nonexistent value', 'empty value',
                              'None in value', 'float in value', '0 in value', 'negative number in value',
                              'id remove node in value'])
def test_change_order_different_value_in_destination_node_id(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422 or status == 404 or status == 400
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запросов с измененными значениями в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': other_project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': other_item_type,
                                     'item': item, 'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': other_item, 'destination_node_id': id_sec_child4lvl}],
                         ids=['changed project_id', 'changed item_type', 'changed item'])
def test_change_order_with_changed_value_in_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': 123, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': 'abc', 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': 123, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': 123, 'destination_node_id': id_sec_child4lvl}],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_change_order_with_incorrect_format_in_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с неверным протоколом http
@pytest.mark.medium
def test_change_order_wrong_protocol():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(f"http://api.cloveri.skroy.ru/api/v1/node/{id_child4lvl}/order/", headers=headers,
                       params=None, json={'project_id': project_id, 'item_type': item_type, 'item': item,
                                          'destination_node_id': id_sec_child4lvl})
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
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов с дублированием обязательных полей в теле
@pytest.mark.medium
@pytest.mark.parametrize("fields",
                         [{'project_id': project_id, 'item_type': item_type, 'item': item,
                           'destination_node_id': id_sec_child4lvl, 'project_id': project_id, 'item_type': item_type,
                           'item': item, 'destination_node_id': id_sec_child4lvl},
                          {'project_id': other_project_id, 'item_type': other_item_type, 'item': other_item,
                           'destination_node_id': id_third_child4lvl, 'project_id': project_id, 'item_type': item_type,
                           'item': item, 'destination_node_id': id_sec_child4lvl}],
                         ids=['double fields with same values', 'double fields with different values'])
def test_change_order_with_double_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 422 or status == 404
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов без обязательных полей и с непредусмотренными полями
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'item_type': item_type, 'item': item, 'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item': item, 'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_ids': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl, 'new_field': ''}],
                         ids=['without project_id', 'without item_type', 'without item', 'without destination_node_id',
                              'with destination_node_ids', 'with new field'])
def test_change_order_without_required_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запросов с несуществующими значениями в обязательных полях
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'project_id': nonexistent_project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': nonexistent_item_type,
                                     'item': item, 'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': nonexistent_item, 'destination_node_id': id_sec_child4lvl}],
                         ids=['nonexistent project_id', 'nonexistent item_type', 'nonexistent item'])
def test_change_order_with_nonexistent_value_in_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты на отправку запросов с пустыми значениями в обязательных полях
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': "", 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': "", 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': "", 'destination_node_id': id_sec_child4lvl},
                                    {'project_id': None, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': None, 'item': item,
                                     'destination_node_id': id_sec_child4lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': None, 'destination_node_id': id_sec_child4lvl}],
                         ids=['project_id empty', 'item_type empty', 'item empty',
                              'project_id Null', 'item_type Null', 'item Null'])
def test_change_order_with_empty_value_in_fields(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тесты с id узла в destination_node_id, у которого level_node, path  отличаются от перемещаемого узла
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_sec_child3lvl},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'destination_node_id': id_child4lvl_for_sec_child3lvl}],
                         ids=['to node with other path, level_node', 'to node with other path'])
def test_change_order_remove_to_node_with_other_path_and_level(fields):
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=None,
                                                     wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])


# Тест на отправку запроса без тела
@pytest.mark.medium
def test_change_order_without_body():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(url_node + f'{id_child4lvl}/order/', headers=headers, params=None, data=None)
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
    # assert "'id': " not in str(response[0])


# Тест на отправку запроса с обязательными полями в url
@pytest.mark.min
def test_change_order_fields_in_path():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'destination_node_id': id_sec_child4lvl}
    res = requests.patch(
        url_node + f'project_id/{project_id}/item_type/{item_type}/item/{item}/{id_child4lvl}/order/',
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
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с обязательными полями в теле + с отправкой text в теле
@pytest.mark.min
def test_change_order_fields_in_query_params():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_headers=None,
                                                     wrong_data={'destination_node_id': id_sec_child4lvl},
                                                     wrong_params={"project_id": project_id,
                                                                   "item_type": item_type,
                                                                   "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с обязательными полями в заголовках
@pytest.mark.min
def test_change_order_fields_in_headers():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_url=None, wrong_params=None,
                                                     wrong_data={'destination_node_id': id_sec_child4lvl},
                                                     wrong_headers={"project_id": project_id,
                                                                    "item_type": item_type,
                                                                    "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с id в query params
@pytest.mark.medium
def test_change_order_id_in_query_params():
    status, response, res_headers = org.change_order(node_id_out=None, node_id_in=id_sec_child4lvl, wrong_headers=None,
                                                     wrong_url=f"{url_node}order/",
                                                     wrong_data=None, wrong_params={"id": id_child4lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с id в headers
@pytest.mark.medium
def test_change_order_id_in_headers():
    status, response, res_headers = org.change_order(node_id_out=None, node_id_in=id_sec_child4lvl, wrong_params=None,
                                                     wrong_url=f"{url_node}order/",
                                                     wrong_data=None, wrong_headers={"id": str(id_child4lvl)})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с id в body
@pytest.mark.medium
def test_change_order_id_in_body():
    status, response, res_headers = org.change_order(node_id_out=None, node_id_in=id_sec_child4lvl, wrong_headers=None,
                                                     wrong_url=f"{url_node}order/",
                                                     wrong_data={"project_id": project_id, "item_type": item_type,
                                                                 "item": item, "id": id_child4lvl,
                                                                 "destination_node_id": id_sec_child4lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с destination_node_id в url
@pytest.mark.medium
def test_change_order_destination_node_id_in_url():
    status, response, res_headers = \
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                         wrong_url=f"{url_node}{id_child4lvl}/order/{id_sec_child4lvl}",
                         wrong_data={"project_id": project_id, "item_type": item_type, "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с destination_node_id в headers
@pytest.mark.medium
def test_change_order_destination_node_id_in_headers():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_headers={"destination_node_id": str(id_sec_child4lvl)},
                                                     wrong_url=None, wrong_data={"project_id": project_id,
                                                                                 "item_type": item_type,
                                                                                 "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)


# Тест на отправку запроса с destination_node_id в query params
@pytest.mark.medium
def test_change_order_destination_node_id_in_query_params():
    status, response, res_headers = org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl,
                                                     wrong_params={"destination_node_id": id_sec_child4lvl},
                                                     wrong_url=None, wrong_data={"project_id": project_id,
                                                                                 "item_type": item_type,
                                                                                 "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    # assert "'id': " not in str(response[0])
    if status == 201:
        org.change_order(node_id_out=id_child4lvl, node_id_in=id_sec_child4lvl)
