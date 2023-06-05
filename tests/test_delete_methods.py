import pytest
# from ..settings import *
# from ..methods import *
from nodes import *


# Базовый тест на удаление/скрытие узлов всех уровней
@pytest.mark.high
@pytest.mark.parametrize('get_node', [id_root1, id_child2lvl, id_child3lvl, id_child4lvl],
                         ids=["delete node 1lvl", "delete node 2lvl", "delete node 3lvl",
                              "delete node 4lvl without children"])
def test_delete_node_positive(get_node):
    status, response, res_headers = org.change_hidden_attr(node_id=get_node, hidden=True)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_hidden_attr(node_id=get_node, hidden=None)


# Проверка невозможности получения удаленного/скрытого узла
@pytest.mark.high
def test_delete_node_check_get_unavailable():
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_child4lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response)
    org.change_hidden_attr(node_id=id_child4lvl, hidden=None)


# Проверка невозможности повторного удаления/скрытия узла (double click)
@pytest.mark.high
def test_delete_node_check_double_click():
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    sec_status, sec_response, _ = org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    print(f"\nSecond request code: {sec_status}")
    print(f"Second request response: {sec_response}")
    assert sec_status == 400
    assert "{'error': 'hidden is already set to True'}" in str(sec_response)
    org.change_hidden_attr(node_id=id_child4lvl, hidden=None)


# Тест на отправку запроса с заголовками в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [upper_headers,
                                           upper_and_low_headers],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_delete_node_upper_headers(headers_upper):
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=True, wrong_id=None,
                                                           wrong_headers=headers_upper, wrong_params=None,
                                                           wrong_data=None, wrong_url=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_hidden_attr(node_id=id_child4lvl, hidden=None)


# Тест на отправку запроса с url в верхнем регистре
@pytest.mark.medium
def test_delete_node_upper_url():
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=True, wrong_url=upper_url_node,
                                                           wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_hidden_attr(node_id=id_child4lvl, hidden=None)


# Тест на отправку запроса с переменой местами полей в json в теле запроса
@pytest.mark.medium
def test_delete_node_move_body_fields():
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=True, wrong_id=None,
                                                           wrong_url=None, wrong_headers=None, wrong_params=None,
                                                           wrong_data={'item_type': item_type,
                                                                       'project_id': project_id,
                                                                       'hidden': True,
                                                                       'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    org.change_hidden_attr(node_id=id_child4lvl, hidden=None)


# Тест на удаление узла с дочками (с полем affect_descendants)
@pytest.mark.high
def test_delete_node_with_affect_descendants_is_true():
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=True,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': True,
                                                                       'affect_descendants': True})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    org.change_hidden_attr(node_id=id_root1, hidden=None, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': True})


# Тест на удаление узла без дочек (с полем affect_descendants)
@pytest.mark.high
def test_delete_node_with_affect_descendants_is_false():
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=True,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': False})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)
    org.change_hidden_attr(node_id=id_root1, hidden=None, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': False})


# Тест на удаление узла без уже удаленных дочек (с полем affect_descendants)
@pytest.mark.high
def test_delete_node_without_deleted_children():
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id,
                                                                          'item_type': item_type,
                                                                          'item': item, 'hidden': True,
                                                                          'affect_descendants': False})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=True,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': True,
                                                                       'affect_descendants': False})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert str(id_child2lvl) not in str(get_response)
    org.change_hidden_attr(node_id=id_root1, hidden=None, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': None,
                                                                      'affect_descendants': False})
    org.change_hidden_attr(node_id=id_child2lvl, hidden=None, wrong_data={'project_id': project_id,
                                                                          'item_type': item_type,
                                                                          'item': item, 'hidden': None,
                                                                          'affect_descendants': False})


# Тест на удаление узла с уже удаленными дочками (с полем affect_descendants)
@pytest.mark.high
def test_delete_node_with_deleted_children():
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id,
                                                                          'item_type': item_type,
                                                                          'item': item, 'hidden': True,
                                                                          'affect_descendants': False})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=True,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': True,
                                                                       'affect_descendants': True})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) deleted"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert "{'error': 'does not exist object(s)'}" in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert str(id_child2lvl) not in str(get_response)
    org.change_hidden_attr(node_id=id_root1, hidden=None, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': None,
                                                                      'affect_descendants': True})


# Базовый тест на восстановление узлов всех уровней
@pytest.mark.high
@pytest.mark.parametrize(('get_node', 'path', 'order', 'level'),
                         [(id_root1, path_root1, order_root1, 1),
                          (id_child2lvl, path_child2lvl, order_child2lvl, 2),
                          (id_child3lvl, path_child3lvl, order_child3lvl, 3),
                          (id_child4lvl, path_child4lvl, order_child4lvl, 4)],
                         ids=["restore node 1lvl", "restore node 2lvl", "restore node 3lvl", "restore node 4lvl"])
def test_restore_node_positive(get_node, path, order, level):
    org.change_hidden_attr(node_id=get_node, hidden=True)
    status, response, res_headers = org.change_hidden_attr(node_id=get_node, hidden=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    status, response, res_headers = org.get_node(node_id=get_node)
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] == get_node
    assert response[0]['path'] == path
    # assert response[0]['inner_order'] == order
    assert response[0]['attributes'] == '{}'
    assert response[0]['level_node'] == level
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Проверка доступности для получения восстановленного узла
@pytest.mark.high
def test_restore_node_check_get_available():
    org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_child4lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert get_response[0]['id'] == id_child4lvl


# Проверка невозможности повторного восстановления узла (double click)
@pytest.mark.high
def test_restore_node_check_double_click():
    org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)
    sec_status, sec_response, _ = org.change_hidden_attr(node_id=id_child4lvl, hidden=None)
    print(f"\nSecond request code: {sec_status}")
    print(f"Second request response: {sec_response}")
    assert sec_status == 400
    assert "{'error': 'hidden is already set to None'}" in str(sec_response)


# Тест на отправку запроса с заголовками в верхнем регистре
@pytest.mark.medium
@pytest.mark.parametrize('headers_upper', [upper_headers,
                                           upper_and_low_headers],
                         ids=["upper headers",
                              "upper and lower headers"])
def test_restore_node_upper_headers(headers_upper):
    org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=None, wrong_id=None,
                                                           wrong_headers=headers_upper, wrong_params=None,
                                                           wrong_data=None, wrong_url=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с url в верхнем регистре
@pytest.mark.medium
def test_restore_node_upper_url():
    org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=None, wrong_url=upper_url_node,
                                                           wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на отправку запроса с переменой местами полей в json в теле запроса
@pytest.mark.medium
def test_restore_node_move_body_fields():
    org.change_hidden_attr(node_id=id_child4lvl, hidden=True)
    status, response, res_headers = org.change_hidden_attr(node_id=id_child4lvl, hidden=None, wrong_id=None,
                                                           wrong_url=None, wrong_headers=None, wrong_params=None,
                                                           wrong_data={'item_type': item_type,
                                                                       'project_id': project_id,
                                                                       'hidden': None,
                                                                       'item': item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0]['id'] == id_child4lvl
    assert "'Content-Type': 'application/json'" in str(res_headers)


# Тест на восстановление узла с дочками (с полем affect_descendants)
@pytest.mark.high
def test_restore_node_with_affect_descendants_is_true():
    org.change_hidden_attr(node_id=id_root1, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': True,
                                                                      'affect_descendants': True})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=None,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': True})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_root1}") in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)


# Тест на восстановление узла без дочек (с полем affect_descendants)
@pytest.mark.high
def test_restore_node_with_affect_descendants_is_false():
    org.change_hidden_attr(node_id=id_root1, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': True,
                                                                      'affect_descendants': False})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=None,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': False})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_root1}") in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)


# Тест на восстановление узла без уже удаленных дочек (с полем affect_descendants)
@pytest.mark.high
def test_restore_node_without_deleted_children():
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id,
                                                                          'item_type': item_type,
                                                                          'item': item, 'hidden': True,
                                                                          'affect_descendants': False})
    org.change_hidden_attr(node_id=id_root1, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': True,
                                                                      'affect_descendants': False})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=None,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': False})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_root1}") in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") not in str(get_response)
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 404
    assert str(f"'id': {id_child2lvl}") not in str(get_response)
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id,
                                                                          'item_type': item_type,
                                                                          'item': item, 'hidden': None,
                                                                          'affect_descendants': False})


# Тест на восстановление узла с уже удаленнми дочками (с полем affect_descendants)
@pytest.mark.high
def test_restore_node_with_deleted_children():
    org.change_hidden_attr(node_id=id_child2lvl, hidden=True, wrong_data={'project_id': project_id,
                                                                          'item_type': item_type,
                                                                          'item': item, 'hidden': True,
                                                                          'affect_descendants': False})
    org.change_hidden_attr(node_id=id_root1, hidden=True, wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                      'item': item, 'hidden': True,
                                                                      'affect_descendants': False})
    status, response, res_headers = org.change_hidden_attr(node_id=id_root1, hidden=None,
                                                           wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                       'item': item, 'hidden': None,
                                                                       'affect_descendants': True})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200
    assert response[0] == "Node(s) restored"
    assert "'Content-Type': 'application/json'" in str(res_headers)
    get_status, get_response, _ = org.get_node(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_root1}") in str(get_response)
    get_status, get_response, _ = org.get_children(node_id=id_root1)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)
    get_status, get_response, _ = org.get_node(node_id=id_child2lvl)
    print(f"\nGet code: {get_status}")
    print(f"Get response: {get_response}")
    assert get_status == 200
    assert str(f"'id': {id_child2lvl}") in str(get_response)
