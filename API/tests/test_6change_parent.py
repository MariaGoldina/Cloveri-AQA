import pytest
from ..nodes import *


# Базовый тест на изменение родителя узлов 2-4 уровней (в т.ч. узла без дочек, перемещение к родителю без дочек)
# OS-API-Up-1, OS-API-Up-3, OS-API-Up-5
@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.parametrize(('node_out', 'node_in', 'node_back', 'path', 'order', 'level'),
                         [(id_fourth_child4lvl, id_sec_child3lvl, id_child3lvl, path_sec_child3lvl,
                           order_sec_child3lvl, 4),
                          (id_sec_child3lvl, id_sec_child2lvl, id_child2lvl, path_sec_child2lvl,
                           order_sec_child2lvl, 3),
                          (id_sec_child2lvl, id_root2, id_root1, path_root2, order_root2, 2)],
                         ids=["change up parent for node 4lvl", "change up parent for node 3lvl",
                              "change up parent for node 2lvl"])
def test_change_parent_positive(node_out, node_in, node_back, path, order, level):
    # _, changing_node_out, _ = org.get_node(node_id=node_out)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=node_in)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=node_in)
    child_nodes_for_new_parent = []
    for node in response_get_descendants[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path and node['level_node'] == level:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=node_out, node_id_in=node_in)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=node_out)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == node_out
    assert response[0]['path'] == path + ('0' * (10 - len(str(node_out))) + str(node_out))
    # assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == level
    assert response[0]['inner_order'] == \
           order + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=node_out, node_id_in=node_back)
    # _, changed_node_out, _ = org.get_node(node_id=node_out)
    # print(changed_node_out)
    # _, changed_node_back, _ = org.get_node(node_id=node_back)
    # print(changed_node_back)
    # _, changed_node_in, _ = org.get_node(node_id=node_in)
    # print(changed_node_in)


# Базовый тест на изменение родителя узла без дочек под нового родителя выше и ниже по inner_order
# OS-API-Up-79, OS-API-Up-80, OS-API-Up-11
@pytest.mark.high
# @pytest.mark.smoke
@pytest.mark.parametrize(('node_in', 'node_back', 'path', 'order', 'level'),
                         [(id_child4lvl, id_third_child4lvl, path_child4lvl, order_child4lvl, 5),
                          (id_fourth_child4lvl, id_third_child4lvl, path_fourth_child4lvl, order_fourth_child4lvl, 5)],
                         ids=["parent up in order", "parent down in order"])
def test_change_parent_with_order_up_and_down(node_in, node_back, path, order, level):
    _, child5lvl, _ = org.create_child(node_id=node_back, attributes={})
    id_child5lvl = child5lvl[0]['id']
    # print(child5lvl)
    # _, changing_node_in, _ = org.get_node(node_id=node_in)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=node_in)
    child_nodes_for_new_parent = []
    for node in response_get_descendants[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path and node['level_node'] == level:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_child5lvl, node_id_in=node_in)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_child5lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_child5lvl
    assert response[0]['path'] == path + ('0' * (10 - len(str(id_child5lvl))) + str(id_child5lvl))
    # assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == level
    assert response[0]['inner_order'] == \
           order + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=id_child5lvl, node_id_in=node_back)
    # _, changed_node_out, _ = org.get_node(node_id=id_child5lvl)
    # print(changed_node_out)
    # _, changing_node_back, _ = org.get_node(node_id=node_back)
    # print(changing_node_back)


# Тест на перемещение узла под нового родителя на несколько уровней выше по иерархии
# OS-API-Up-7
@pytest.mark.high
# @pytest.mark.smoke
def test_change_parent_to_several_levels_up():
    # _, changing_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_root1)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_root1)
    child_nodes_for_new_parent = []
    for node in response_get_descendants[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_root1 and node['level_node'] == 2:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_root1)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_fourth_child4lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_fourth_child4lvl
    assert response[0]['path'] == path_root1 + ('0' * (10 - len(str(id_fourth_child4lvl))) + str(id_fourth_child4lvl))
    # assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 2
    assert response[0]['inner_order'] == \
           order_root1 + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_child3lvl)
    # _, changed_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(changed_node_out)
    # _, changed_node_back, _ = org.get_node(node_id=id_child3lvl)
    # print(changed_node_back)


# Тест на перемещение узла под нового родителя без дочек на несколько уровней ниже по иерархии
# OS-API-Up-8a, OS-API-Up-13
@pytest.mark.high
# @pytest.mark.smoke
def test_change_parent_to_several_levels_down():
    # _, changing_node_out, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_child4lvl)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=id_child4lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_child4lvl and node['level_node'] == 5:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child4lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_sec_child2lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_sec_child2lvl
    assert response[0]['path'] == path_child4lvl + ('0' * (10 - len(str(id_sec_child2lvl))) + str(id_sec_child2lvl))
    # assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 5
    assert response[0]['inner_order'] == \
           order_child4lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)
    # _, changed_node_out, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changed_node_out)
    # _, changed_node_back, _ = org.get_node(node_id=id_root1)
    # print(changed_node_back)


# Тест на перемещение узла с дочками под нового родителя
# OS-API-Up-12
@pytest.mark.high
def test_change_parent_for_node_with_children():
    # _, changing_node_out, _ = org.get_node(node_id=id_sec_child3lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_in)
    org.create_child(node_id=id_sec_child3lvl, attributes={})
    org.create_child(node_id=id_child4lvl_for_sec_child3lvl, attributes={})
    status_get_descendants, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_sec_child2lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_sec_child2lvl and node['level_node'] == 3:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child3lvl, node_id_in=id_sec_child2lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_sec_child3lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_sec_child3lvl
    assert response[0]['path'] == path_sec_child2lvl + ('0' * (10 - len(str(id_sec_child3lvl))) + str(id_sec_child3lvl))
    # assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 3
    assert response[0]['inner_order'] == \
           order_sec_child2lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    _, response_get_descendants_for_node, _ = org.get_descendants(node_id=id_sec_child3lvl)
    for node in response_get_descendants_for_node[0]:
        assert node['path'][:30] == path_sec_child2lvl + ('0' * (10 - len(str(id_sec_child3lvl))) + str(id_sec_child3lvl))
        assert node['inner_order'][:30] == \
               order_sec_child2lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    org.change_parent(node_id_out=id_sec_child3lvl, node_id_in=id_child2lvl)
    # _, changed_node_out, _ = org.get_node(node_id=id_sec_child3lvl)
    # print(changed_node_out)
    # _, changed_node_back, _ = org.get_node(node_id=id_child2lvl)
    # print(changed_node_back)


# Тест на перемещение узла под нового родителя с дочками
# OS-API-Up-14
@pytest.mark.high
def test_change_parent_to_parent_with_children():
    # _, changing_node_out, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_child2lvl)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_child2lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_child2lvl and node['level_node'] == 3:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child2lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_sec_child2lvl)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == id_sec_child2lvl
    assert response[0]['path'] == path_child2lvl + ('0' * (10 - len(str(id_sec_child2lvl))) + str(id_sec_child2lvl))
    # assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == 3
    assert response[0]['inner_order'] == \
           order_child2lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    _, response_get_descendants_for_new_parent, _ = org.get_tree()
    child_orders_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if node['path'][0:20] == path_child2lvl and node['level_node'] > 2:
            child_orders_for_new_parent.append(node['inner_order'])
    assert child_orders_for_new_parent == sorted(child_orders_for_new_parent)
    # print(child_orders_for_new_parent)
    org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)
    # _, changed_node_out, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changed_node_out)
    # _, changed_node_back, _ = org.get_node(node_id=id_root1)
    # print(changed_node_back)


# Тесты на отправку запросов с заголовками в верхнем регистре
# OS-API-Up-15, OS-API-Up-16
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [upper_headers,
                                           upper_and_low_headers],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_change_parent_upper_headers(headers_upper):
    # _, changing_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_sec_child2lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_sec_child2lvl and node['level_node'] == 3:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_sec_child2lvl,
                                                      wrong_url=None, wrong_headers=headers_upper, wrong_params=None,
                                                      wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_fourth_child4lvl)
    assert response[0]['id'] == id_fourth_child4lvl
    assert response[0]['path'] == \
           path_sec_child2lvl + ('0' * (10 - len(str(id_fourth_child4lvl))) + str(id_fourth_child4lvl))
    assert response[0]['inner_order'] == \
           order_sec_child2lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_child3lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_child3lvl)
    # print(back_node_in)


# Тест на отправку запроса с url в верхнем регистре
# OS-API-Up-18
@pytest.mark.medium
def test_change_parent_upper_url():
    # _, changing_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_sec_child2lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_sec_child2lvl and node['level_node'] == 3:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_sec_child2lvl,
                                                      wrong_headers=None, wrong_params=None,
                                                      wrong_url=upper_url_node + f'{id_fourth_child4lvl}/parent/')
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_fourth_child4lvl)
    assert response[0]['id'] == id_fourth_child4lvl
    assert response[0]['path'] == \
           path_sec_child2lvl + ('0' * (10 - len(str(id_fourth_child4lvl))) + str(id_fourth_child4lvl))
    assert response[0]['inner_order'] == \
           order_sec_child2lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_child3lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_child3lvl)
    # print(back_node_in)


# Тест на отправку запроса с переменой местами полей в json в теле запроса
# OS-API-Up-17
@pytest.mark.medium
def test_change_parent_move_body_fields():
    # _, changing_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(changing_node_out)
    # _, changing_node_in, _ = org.get_node(node_id=id_sec_child2lvl)
    # print(changing_node_in)
    status_get_descendants, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_sec_child2lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if status_get_descendants == 200:
            if node['path'][0:-10] == path_sec_child2lvl and node['level_node'] == 3:
                child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_sec_child2lvl,
                                                      wrong_id=None, wrong_url=None, wrong_headers=None,
                                                      wrong_params=None, wrong_data={'item_type': item_type,
                                                                                     'project_id': project_id,
                                                                                     'new_parent_id': id_sec_child2lvl,
                                                                                     'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_fourth_child4lvl)
    assert response[0]['id'] == id_fourth_child4lvl
    assert response[0]['path'] == \
           path_sec_child2lvl + ('0' * (10 - len(str(id_fourth_child4lvl))) + str(id_fourth_child4lvl))
    assert response[0]['inner_order'] == \
           order_sec_child2lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_child3lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_child3lvl)
    # print(back_node_in)


# Тест на проверку отображения get методами измененного значения полей path, inner_order у узла без дочек
# OS-API-Up-79
@pytest.mark.medium
def test_change_parent_without_children_check_get_methods():
    _, response_get_node, _ = org.get_node(node_id=id_fourth_child4lvl)
    get_node_path_before = response_get_node[0]['path']
    get_node_order_before = response_get_node[0]['inner_order']
    _, response_get_tree, _ = org.get_tree()
    get_tree_path_before = ""
    get_tree_order_before = ""
    for node in response_get_tree[0]:
        if node['id'] == id_fourth_child4lvl:
            get_tree_path_before = node['path']
            get_tree_order_before = node['inner_order']
    _, response_get_descendants, _ = org.get_descendants(node_id=id_child3lvl)
    get_descendants_path_before = ""
    get_descendants_order_before = ""
    for node in response_get_descendants[0]:
        if node['id'] == id_fourth_child4lvl:
            get_descendants_path_before = node['path']
            get_descendants_order_before = node['inner_order']
    print(get_node_path_before, get_tree_path_before, get_descendants_path_before)
    print(get_node_order_before, get_tree_order_before, get_descendants_order_before)
    assert get_node_path_before == get_tree_path_before == get_descendants_path_before
    assert get_node_order_before == get_tree_order_before == get_descendants_order_before
    _, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_sec_child3lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if node['path'][0:-10] == path_sec_child3lvl and node['level_node'] == 4:
            child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_sec_child3lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_fourth_child4lvl)
    assert response[0]['id'] == id_fourth_child4lvl
    assert response[0]['path'] == \
           path_sec_child3lvl + ('0' * (10 - len(str(id_fourth_child4lvl))) + str(id_fourth_child4lvl))
    assert response[0]['inner_order'] == \
           order_sec_child3lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    _, response_get_node, _ = org.get_node(node_id=id_fourth_child4lvl)
    get_node_path_after = response_get_node[0]['path']
    get_node_order_after = response_get_node[0]['inner_order']
    _, response_get_tree, _ = org.get_tree()
    get_tree_path_after = ""
    get_tree_order_after = ""
    for node in response_get_tree[0]:
        if node['id'] == id_fourth_child4lvl:
            get_tree_path_after = node['path']
            get_tree_order_after = node['inner_order']
    _, response_get_descendants, _ = org.get_descendants(node_id=id_sec_child3lvl)
    get_descendants_path_after = ""
    get_descendants_order_after = ""
    for node in response_get_descendants[0]:
        if node['id'] == id_fourth_child4lvl:
            get_descendants_path_after = node['path']
            get_descendants_order_after = node['inner_order']
    # print(get_node_path_after, get_tree_path_after, get_descendants_path_after)
    # print(get_node_order_after, get_tree_order_after, get_descendants_order_after)
    assert get_node_path_after == get_tree_path_after == get_descendants_path_after == \
           path_sec_child3lvl + ('0' * (10 - len(str(id_fourth_child4lvl))) + str(id_fourth_child4lvl))
    assert get_node_order_after == get_tree_order_after == get_descendants_order_after == \
           order_sec_child3lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    relatives = []
    for node in response_get_tree[0]:
        if node['path'][0:-10] == path_sec_child3lvl and node['level_node'] == 4:
            relatives.append(node)
    relatives_orders = [i['inner_order'] for i in relatives]
    # print(relatives_orders)
    assert relatives_orders == sorted(relatives_orders)
    org.change_parent(node_id_out=id_fourth_child4lvl, node_id_in=id_child3lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_fourth_child4lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_child3lvl)
    # print(back_node_in)


# Тест на проверку отображения get методами измененного значения поля path, inner_order у узла с дочками и у всех дочек
# OS-API-Up-80
@pytest.mark.medium
def test_change_parent_with_children_check_get_methods():
    _, response_get_node, _ = org.get_node(node_id=id_sec_child3lvl)
    get_node_path_before = response_get_node[0]['path']
    get_node_order_before = response_get_node[0]['inner_order']
    _, response_get_tree, _ = org.get_tree()
    get_tree_path_before = ""
    get_tree_order_before = ""
    for node in response_get_tree[0]:
        if node['id'] == id_sec_child3lvl:
            get_tree_path_before = node['path']
            get_tree_order_before = node['inner_order']
    _, response_get_descendants, _ = org.get_descendants(node_id=id_child2lvl)
    get_descendants_path_before = ""
    get_descendants_order_before = ""
    for node in response_get_descendants[0]:
        if node['id'] == id_sec_child3lvl:
            get_descendants_path_before = node['path']
            get_descendants_order_before = node['inner_order']
    print(get_node_path_before, get_tree_path_before, get_descendants_path_before)
    print(get_node_order_before, get_tree_order_before, get_descendants_order_before)
    assert get_node_path_before == get_tree_path_before == get_descendants_path_before
    assert get_node_order_before == get_tree_order_before == get_descendants_order_before
    _, response_get_descendants_for_new_parent, _ = org.get_descendants(node_id=id_child3lvl)
    child_nodes_for_new_parent = []
    for node in response_get_descendants_for_new_parent[0]:
        if node['path'][0:-10] == path_child3lvl and node['level_node'] == 4:
            child_nodes_for_new_parent.append(node)
    amount_child_nodes = len(child_nodes_for_new_parent)
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child3lvl, node_id_in=id_child3lvl)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201
    status, response, res_headers = org.get_node(node_id=id_sec_child3lvl)
    assert response[0]['id'] == id_sec_child3lvl
    assert response[0]['path'] == \
           path_child3lvl + ('0' * (10 - len(str(id_sec_child3lvl))) + str(id_sec_child3lvl))
    assert response[0]['inner_order'] == \
           order_child3lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    assert "'Content-Type': 'application/json'" in str(res_headers)
    _, response_get_node, _ = org.get_node(node_id=id_sec_child3lvl)
    get_node_path_after = response_get_node[0]['path']
    get_node_order_after = response_get_node[0]['inner_order']
    _, response_get_tree, _ = org.get_tree()
    get_tree_path_after = ""
    get_tree_order_after = ""
    for node in response_get_tree[0]:
        if node['id'] == id_sec_child3lvl:
            get_tree_path_after = node['path']
            get_tree_order_after = node['inner_order']
    _, response_get_descendants, _ = org.get_descendants(node_id=id_child3lvl)
    get_descendants_path_after = ""
    get_descendants_order_after = ""
    for node in response_get_descendants[0]:
        if node['id'] == id_sec_child3lvl:
            get_descendants_path_after = node['path']
            get_descendants_order_after = node['inner_order']
    # print(get_node_path_after, get_tree_path_after, get_descendants_path_after)
    # print(get_node_order_after, get_tree_order_after, get_descendants_order_after)
    assert get_node_path_after == get_tree_path_after == get_descendants_path_after == \
           path_child3lvl + ('0' * (10 - len(str(id_sec_child3lvl))) + str(id_sec_child3lvl))
    assert get_node_order_after == get_tree_order_after == get_descendants_order_after == \
           order_child3lvl + '0' * (10 - len(str(amount_child_nodes + 1))) + str(amount_child_nodes + 1)
    relatives_for_node = []
    get_tree_children_for_node = []
    for node in response_get_tree[0]:
        if node['path'][0:-10] == path_child3lvl and node['level_node'] == 4:
            relatives_for_node.append(node)
        if node['path'][:40] == get_tree_path_after and node['level_node'] > 4:
            get_tree_children_for_node.append(node)
    relatives_orders = [i['inner_order'] for i in relatives_for_node]
    # print(relatives_orders)
    assert relatives_orders == sorted(relatives_orders)
    for i in get_tree_children_for_node:
        assert i['inner_order'][:40] == get_tree_order_after
    _, response_get_descendants_for_node, _ = org.get_descendants(node_id=id_sec_child3lvl)
    for node in response_get_descendants_for_node[0]:
        if node['level_node'] > 4:
            assert node['path'][0:40] == get_tree_path_after
            assert node['inner_order'][0:40] == get_tree_order_after
    org.change_parent(node_id_out=id_sec_child3lvl, node_id_in=id_child2lvl)
    # _, back_node_out, _ = org.get_node(node_id=id_sec_child3lvl)
    # print(back_node_out)
    # _, back_node_in, _ = org.get_node(node_id=id_child2lvl)
    # print(back_node_in)


# Негативные тесты!!!


# Тесты на отправку запросов с ключами обязательных полей в теле в верхнем регистре
# OS-API-Up-19, OS-API-Up-20
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field'),
                         [({'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                            'new_parent_id': id_child3lvl}, ['project_id', 'item_type', 'item']),
                          ({'PROJECT_ID': project_id, 'ITEM_TYPE': item_type, 'ITEM': item,
                           'NEW_PARENT_ID': id_child3lvl}, ['project_id', 'item_type', 'item', 'new_parent_id']),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'NEW_PARENT_ID': id_child3lvl}, ['new_parent_id'])],
                         ids=['only 3 fields UPPER', 'all fields UPPER', 'only new_parent_id UPPER'])
def test_change_parent_upper_fields(fields, field):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    for s in field:
        assert f'field {s} is required' in str(response[0])
        assert f'field {s.upper()} not allowed' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса со всеми характеристиками узла в теле
# OS-API-Up-21
@pytest.mark.medium
def test_change_parent_all_fields_in_body():
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_params=None,
                                                      wrong_data={'id': id_sec_child2lvl, 'path': path_sec_child2lvl,
                                                                 'project_id': project_id, 'item_type': item_type,
                                                                 'item': item, 'inner_order': order_sec_child2lvl,
                                                                 'attributes': '{}', 'level_node': 2,
                                                                 'new_parent_id': id_child3lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field id not allowed' in str(response[0]) and 'field path not allowed' in str(response[0]) \
           and 'field inner_order not allowed' in str(response[0]) \
           and 'field level_node not allowed' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с полем path вместо new_parent_id
# OS-API-Up-24
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'path': id_child3lvl},
                                    {'project_id': project_id, 'item_type': item_type, 'item': item,
                                     'path': path_child3lvl}],
                         ids=['key path instead new_parent_id', 'key and value path instead new_parent_id'])
def test_change_parent_with_path_instead_new_parent_id(fields):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_params=None,
                                                      wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field path not allowed' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запросов неверными методами
# OS-API-Up-25
@pytest.mark.medium
def test_change_parent_wrong_method():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'new_parent_id': id_child3lvl}
    res1 = requests.put(url_node + f'{id_sec_child2lvl}/parent/', headers=headers, params=None, json=data)
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
    res2 = requests.post(url_node + f'{id_sec_child2lvl}/parent/', headers=headers, params=None, json=data)
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
    res3 = requests.get(url_node + f'{id_sec_child2lvl}/parent/', headers=headers, params=None, json=data)
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
    res4 = requests.delete(url_node + f'{id_sec_child2lvl}/parent/', headers=headers, params=None, json=data)
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
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с неверным url и эндпоинтом
# OS-API-Up-26, OS-API-Up-26a, OS-API-Up-27
@pytest.mark.medium
@pytest.mark.parametrize("urls", [
                                  # f"https://skroy.ru/api/v1/node/{id_sec_child2lvl}/parent/",
                                  f"https://api.cloveri.skroy.ru/api/v2/node/{id_sec_child2lvl}/parent/",
                                  f"https://api.cloveri.skroy.ru/api/v1/node/{id_sec_child2lvl}/paren/"],
                         ids=[
                             # 'wrong url',
                             'wrong api version', 'wrong endpoint'])
def test_change_parent_wrong_urls(urls):
    status, response, res_headers = org.change_parent(node_id_out=None, node_id_in=id_child3lvl,
                                                      wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с неверными заголовками
# OS-API-Up-29
@pytest.mark.medium
def test_change_parent_wrong_media_type_in_headers():
    headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=headers, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 415
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса без заголовков
# OS-API-Up-64
@pytest.mark.medium
@pytest.mark.skip
def test_change_parent_without_headers():
    data = {'project_id': project_id, 'item_type': item_type, 'item': item, 'new_parent_id': id_child3lvl}
    res = requests.patch(url_node + f'{id_sec_child2lvl}/parent/', headers=None, params=None, data=data)
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
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с неверным id в url
# OS-API-Up-28, OS-API-Up-47, OS-API-Up-48, OS-API-Up-70
@pytest.mark.medium
@pytest.mark.parametrize("urls", [f"{url_node}abc/parent/",
                                  f"{url_node} /parent/",
                                  f"{url_node}None/parent/",
                                  f"{url_node}parent/"],
                         ids=['incorrect format', 'empty id', 'id is None', 'without id'])
def test_change_parent_with_incorrect_id_in_url(urls):
    status, response, res_headers = org.change_parent(node_id_out=None, node_id_in=id_child3lvl,
                                                      wrong_url=urls, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с несуществующим id в url
# OS-API-Up-46
@pytest.mark.medium
def test_change_parent_with_nonexistent_id_in_url():
    status, response, res_headers = org.change_parent(node_id_out=None, node_id_in=id_child3lvl,
                                                      wrong_url=f"{url_node}100000/parent/",
                                                      wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 200
    assert status == 404
    assert 'error' in str(response[0])
    assert "does not exist object with id" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с телом запроса в формате text
# OS-API-Up-30
@pytest.mark.medium
def test_change_parent_with_text_in_body():
    res = requests.patch(url_node + f'{id_sec_child2lvl}/parent/', headers=None, params=None,
                       data=f"'project_id': {project_id}, 'item_type': {item_type}, 'item': {item}, "
                            f"'new_parent_id': {id_child3lvl}")
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
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с разными значениями в поле new_parent_id
# OS-API-Up-32, OS-API-Up-58, OS-API-Up-60, OS-API-Up-61
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'answer'),
                         [({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': 'abc'}, 'new_parent_id has wrong format, must be int'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': str(id_child3lvl)}, 'new_parent_id has wrong format, must be int'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': ''}, 'field new_parent_id must not be empty'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': None}, 'new_parent_id has wrong format, must be int'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                            'new_parent_id': float(id_child3lvl)}, 'new_parent_id has wrong format, must be int'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': 0}, 'new_parent_id must be positive number'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': -id_child3lvl}, 'new_parent_id must be positive number')],
                         ids=['string in value', 'number in string in value',
                              'empty value',
                              'None in value', 'float in value', '0 in value', 'negative number in value'])
def test_change_parent_different_value_in_new_parent_id(fields, answer):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert answer in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с несуществующим id в поле destination_node_id
# OS-API-Up-59
@pytest.mark.medium
def test_change_parent_nonexistent_id_in_new_parent_id():
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=100000,
                                                      wrong_url=None, wrong_headers=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert 'error' in str(response[0])
    assert "does not exist object with id" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запросов с измененными значениями в обязательных полях
# OS-API-Up-33, OS-API-Up-34, OS-API-Up-35
@pytest.mark.medium
@pytest.mark.parametrize("fields", [{'project_id': other_project_id, 'item_type': item_type, 'item': item,
                                     'new_parent_id': id_child3lvl},
                                    {'project_id': project_id, 'item_type': other_item_type,
                                     'item': item, 'new_parent_id': id_child3lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': other_item, 'new_parent_id': id_child3lvl}],
                         ids=['changed project_id', 'changed item_type', 'changed item'])
def test_change_parent_with_changed_value_in_fields(fields):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404 or status == 422
    assert 'error' in str(response[0])
    assert "does not exist object with id" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
# OS-API-Up-38, OS-API-Up-39, OS-API-Up-40
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field', 'formats'),
                         [({'project_id': 123, 'item_type': item_type, 'item': item,
                           'new_parent_id': id_child3lvl}, 'project_id', 'uuid'),
                          ({'project_id': 'abc', 'item_type': item_type, 'item': item,
                            'new_parent_id': id_child3lvl}, 'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': 123, 'item': item,
                           'new_parent_id': id_child3lvl}, 'item_type', 'str'),
                          ({'project_id': project_id, 'item_type': item_type,
                            'item': 123, 'new_parent_id': id_child3lvl}, 'item', 'str')],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_change_parent_with_incorrect_format_in_fields(fields, field, formats):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert f"['{field} has wrong format, must be {formats}']" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с неверным протоколом http
# OS-API-Up-43
@pytest.mark.medium
@pytest.mark.skip
def test_change_parent_wrong_protocol():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(f"http://api.cloveri.skroy.ru/api/v1/node/{id_sec_child2lvl}/parent/", headers=headers,
                       params=None, json={'project_id': project_id, 'item_type': item_type, 'item': item,
                                          'new_parent_id': id_child3lvl})
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
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с дублированием обязательных полей в теле
# OS-API-Up-44, OS-API-Up-45
@pytest.mark.medium
@pytest.mark.parametrize("fields",
                         [{'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': id_child3lvl, 'project_id': project_id, 'item_type': item_type,
                           'item': item, 'new_parent_id': id_child3lvl},
                          {'project_id': other_project_id, 'item_type': other_item_type, 'item': other_item,
                           'new_parent_id': id_child3lvl, 'project_id': project_id, 'item_type': item_type,
                           'item': item, 'new_parent_id': id_child3lvl}],
                         ids=['double fields with same values', 'double fields with different values'])
def test_change_parent_with_double_fields(fields):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 422 or status == 404
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов без обязательных полей
# OS-API-Up-65, OS-API-Up-66, OS-API-Up-67, OS-API-Up-68
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'field'),
                         [({'item_type': item_type, 'item': item, 'new_parent_id': id_child3lvl},
                           'project_id'),
                          ({'project_id': project_id, 'item': item, 'new_parent_id': id_child3lvl},
                           'item_type'),
                          ({'project_id': project_id, 'item_type': item_type, 'new_parent_id': id_child3lvl},
                           'item'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item},
                           'new_parent_id'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                            'new_parent_ids': id_child3lvl}, 'new_parent_id')],
                         ids=['without project_id', 'without item_type', 'without item', 'without new_parent_id',
                              'mistake in new_parent_id'])
def test_change_parent_without_required_fields(fields, field):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert f'field {field} is required' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с непредусмотренными полями
# OS-API-Up-41, OS-API-Up-42
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'field'),
                         [({'project_id': project_id, 'item_type': item_type, 'item': item,
                            'new_parent_ids': id_child3lvl}, 'new_parent_ids'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                            'new_parent_id': id_child3lvl, 'new_field': ''}, 'new_field')],
                         ids=['with new_parent_ids', 'with new field'])
def test_change_parent_with_not_allowed_fields(fields, field):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert f"field {field} not allowed" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запросов с несуществующими значениями в обязательных полях
# OS-API-Up-55, OS-API-Up-56, OS-API-Up-57
@pytest.mark.high
@pytest.mark.parametrize("fields", [{'project_id': nonexistent_project_id, 'item_type': item_type, 'item': item,
                                     'new_parent_id': id_child3lvl},
                                    {'project_id': project_id, 'item_type': nonexistent_item_type,
                                     'item': item, 'new_parent_id': id_child3lvl},
                                    {'project_id': project_id, 'item_type': item_type,
                                     'item': nonexistent_item, 'new_parent_id': id_child3lvl}],
                         ids=['nonexistent project_id', 'nonexistent item_type', 'nonexistent item'])
def test_change_parent_with_nonexistent_value_in_fields(fields):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert 'error' in str(response[0])
    assert "does not exist object with id" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тесты на отправку запросов с пустыми значениями в обязательных полях
# OS-API-Up-49, OS-API-Up-50, OS-API-Up-51, OS-API-Up-52, OS-API-Up-53, OS-API-Up-54
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field', 'value', 'formats'),
                         [({'project_id': "", 'item_type': item_type, 'item': item,
                           'new_parent_id': id_child3lvl}, 'project_id', 'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': "", 'item': item,
                            'new_parent_id': id_child3lvl}, 'item_type', 'item_type_empty', 'str'),
                          ({'project_id': project_id, 'item_type': item_type,
                            'item': "", 'new_parent_id': id_child3lvl}, 'item', 'item_empty', 'str'),
                          ({'project_id': None, 'item_type': item_type, 'item': item,
                           'new_parent_id': id_child3lvl}, 'project_id', 'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': None, 'item': item,
                           'new_parent_id': id_child3lvl}, 'item_type', 'item_type_none', 'str'),
                          ({'project_id': project_id, 'item_type': item_type,
                            'item': None, 'new_parent_id': id_child3lvl}, 'item', 'item_none', 'str')],
                         ids=['project_id empty', 'item_type empty', 'item empty',
                              'project_id Null', 'item_type Null', 'item Null'])
def test_change_parent_with_empty_value_in_fields(fields, field, value, formats):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    if value == 'project_id' or value == 'item_type_none' or value == 'item_none':
        assert f"['{field} has wrong format, must be {formats}']" in str(response[0])
    if value == 'item_type_empty' or value == 'item_empty':
        assert f"['field {field} must not be empty']" in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на перемещение узла к неправильному родителю
# OS-API-Up-63, OS-API-Up-62, OS-API-Up-79
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'answer'),
                         [({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': id_sec_child3lvl}, "New parent can't be movable instance itself"),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': id_child4lvl_for_sec_child3lvl},
                           "New parent can't be movable instance's descendant"),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item,
                           'new_parent_id': id_child2lvl}, 'This parent is already set')],
                         ids=['id remove id node in new_parent', 'id descendant for node in new_parent',
                              'id current parent for node in new_parent'])
def test_change_parent_remove_to_wrong_parent(fields, answer):
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child3lvl, wrong_url=None, wrong_headers=None,
                                                      node_id_in=None, wrong_data=fields)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 400
    assert 'error' in str(response[0])
    assert answer in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child3lvl, node_id_in=id_child2lvl)


# Тест на отправку запроса без тела
# OS-API-Up-69
@pytest.mark.medium
def test_change_parent_without_body():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    res = requests.patch(url_node + f'{id_sec_child2lvl}/parent/', headers=headers, params=None, data=None)
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
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0]) and 'field new_parent_id is required' in str(response[0])


# Тест на отправку запроса с обязательными полями в url
# OS-API-Up-73
@pytest.mark.min
def test_change_parent_fields_in_path():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'new_parent_id': id_child3lvl}
    res = requests.patch(
        url_node + f'project_id/{project_id}/item_type/{item_type}/item/{item}/{id_sec_child2lvl}/parent/',
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
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с обязательными полями в query params
# OS-API-Up-75
@pytest.mark.min
def test_change_parent_fields_in_query_params():
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_headers=None,
                                                      wrong_data={'new_parent_id': id_child3lvl},
                                                      wrong_params={"project_id": project_id,
                                                                    "item_type": item_type,
                                                                    "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с обязательными полями в заголовках
# OS-API-Up-74
@pytest.mark.min
def test_change_parent_fields_in_headers():
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_url=None, wrong_params=None,
                                                      wrong_data={'new_parent_id': id_child3lvl},
                                                      wrong_headers={"project_id": project_id,
                                                                     "item_type": item_type,
                                                                     "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с id в query params
# OS-API-Up-71
@pytest.mark.min
def test_change_parent_id_in_query_params():
    status, response, res_headers = org.change_parent(node_id_out=None, node_id_in=id_child3lvl, wrong_headers=None,
                                                      wrong_url=f"{url_node}parent/",
                                                      wrong_data=None, wrong_params={"id": id_sec_child2lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с id в headers
# OS-API-Up-72
@pytest.mark.min
def test_change_parent_id_in_headers():
    status, response, res_headers = org.change_parent(node_id_out=None, node_id_in=id_child3lvl, wrong_params=None,
                                                      wrong_url=f"{url_node}parent/",
                                                      wrong_data=None, wrong_headers={"id": str(id_sec_child2lvl)})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с id в body
@pytest.mark.min
def test_change_parent_id_in_body():
    status, response, res_headers = org.change_parent(node_id_out=None, node_id_in=id_child3lvl, wrong_headers=None,
                                                      wrong_url=f"{url_node}parent/",
                                                      wrong_data={"project_id": project_id, "item_type": item_type,
                                                                  "item": item, "id": id_sec_child2lvl,
                                                                  "new_parent_id": id_child3lvl})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с new_parent_id в url
# OS-API-Up-76
@pytest.mark.min
def test_change_parent_new_parent_id_in_url():
    status, response, res_headers = \
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                          wrong_url=f"{url_node}{id_sec_child2lvl}/parent/{id_child3lvl}",
                          wrong_data={"project_id": project_id, "item_type": item_type, "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'Content-Type': 'text/html; charset=utf-8'" in str(res_headers)
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с new_parent_id в headers
# OS-API-Up-77
@pytest.mark.min
def test_change_parent_new_parent_id_in_headers():
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_headers={"new_parent_id": str(id_child3lvl)},
                                                      wrong_url=None, wrong_data={"project_id": project_id,
                                                                                  "item_type": item_type,
                                                                                  "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field new_parent_id is required' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)


# Тест на отправку запроса с new_parent_id в query params
# OS-API-Up-78
@pytest.mark.min
def test_change_parent_new_parent_id_in_query_params():
    status, response, res_headers = org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_child3lvl,
                                                      wrong_params={"new_parent_id": id_child3lvl},
                                                      wrong_url=None, wrong_data={"project_id": project_id,
                                                                                  "item_type": item_type,
                                                                                  "item": item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert 'error' in str(response[0])
    assert 'field new_parent_id is required' in str(response[0])
    if status == 201:
        org.change_parent(node_id_out=id_sec_child2lvl, node_id_in=id_root1)
