import pytest
from ..nodes import *


# Позитивные тесты на create_root

# Базовые тесты на создание корневых узлов
# OS-API-Cr-1, OS-API-Cr-2
@pytest.mark.high
@pytest.mark.smoke
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
# OS-API-Cr-1
@pytest.mark.high
@pytest.mark.smoke
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
# OS-API-Cr-3, OS-API-Cr-3а, OS-API-Cr-3б
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

# Базовые тесты на создание дочек разных уровней
# OS-API-Cc-1, OS-API-Cc-2, OS-API-Cc-3, OS-API-Cc-4, OS-API-Cc-5, OS-API-Cc-6, OS-API-Cc-37
@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.parametrize(('parent', 'attr', 'path', 'level', 'parent_order'),
                         [(id_root1, '{"name": "1 child 2lvl"}', path_root1, 2, order_root1),
                          (id_root1, '{"name": "2 child 2lvl"}', path_root1, 2, order_root1),
                          (id_child2lvl, '{"name": "1 child 3lvl"}', path_child2lvl, 3, order_child2lvl),
                          (id_child2lvl, '{"name": "2 child 3lvl"}', path_child2lvl, 3, order_child2lvl),
                          (id_child3lvl, '{"name": "1 child 4lvl"}', path_child3lvl, 4, order_child3lvl),
                          (id_child3lvl, '{"name": "2 child 4lvl"}', path_child3lvl, 4, order_child3lvl)],
                         ids=["create child 2lvl", "create second child 2lvl", "create child 3lvl",
                              "create second child 3lvl", "create child 4lvl", "create second child 4lvl"])
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


# Тест на создание дочки 5 уровня
# OS-API-Cc-37
@pytest.mark.medium
def test_create_child_5_level():
    status, response, res_headers = org.create_child(attributes=None, node_id=id_child4lvl,
                                                     wrong_data={'project_id': project_id,
                                                                 'item_type': item_type, 'item': item,
                                                                 'attributes': '{"name": "child 5lvl"}'})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    id_node = response[0]['id']
    assert status == 201
    assert response[0]['project_id'] == project_id
    assert response[0]['item_type'] == item_type
    assert response[0]['item'] == item
    assert response[0]['id'] != 0
    assert response[0]['path'] == path_child4lvl + ('0' * (10 - len(str(id_node))) + str(id_node))
    assert response[0]['attributes'] == '{"name": "child 5lvl"}'
    assert response[0]['level_node'] == 5
    assert "'Content-Type': 'application/json'" in str(res_headers)
    assert 'inner_order' in str(response[0])


# Тест на проверку inner_order при создании дочерних узлов
# OS-API-Cc-1, OS-API-Cc-3, OS-API-Cc-5
@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.parametrize(('parent', 'parent_path', 'parent_order', 'child_level'),
                         [(id_root1, path_root1, order_root1, 2),
                          (id_child2lvl, path_child2lvl, order_child2lvl, 3),
                          (id_child3lvl, path_child3lvl, order_child3lvl, 4)],
                         ids=["create child 2lvl", "create child 3lvl", "create child 4lvl"])
def test_create_child_check_inner_order(parent, parent_order, parent_path, child_level):
    status_get_descendants, response_get_descendants, _ = org.get_descendants(node_id=parent)
    child_nodes_for_parent = []
    for node in response_get_descendants[0]:
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
# OS-API-Cr-53
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
# OS-API-Cr-29, OS-API-Cr-52, OS-API-Cr-30, OS-API-Cr-54, OS-API-Cr-55, OS-API-Cr-56, OS-API-Cr-57
@pytest.mark.medium
@pytest.mark.parametrize('other_attributes', ['{}',
                                              '{"name": "", "description": ""}',
                                              None,
                                              '{"name": "name"}',
                                              '{"description": "description"}',
                                              '{"name": "None"}',
                                              '{"description": "None"}'],
                         ids=["empty json", "empty string - name, description", "None instead attributes",
                              "only name", "only description", "None in name", "None in description"])
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
# OS-API-Cr-4, OS-API-Cr-5
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
# OS-API-Cr-8
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
# OS-API-Cr-66
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

# Тесты на отправку запросов с неверным форматом в поле parent_id
# OS-API-Cc-17
@pytest.mark.medium
def test_create_child_with_incorrect_format_parent_id():
    status, response, res_headers = org.create_child(node_id='abc', attributes={}, wrong_url=None,
                                                     wrong_data=None, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)


# Тесты на отправку запросов с несуществующим значением в поле parent_id
# OS-API-Cc-18
@pytest.mark.medium
def test_create_child_with_nonexistent_parent_id():
    status, response, res_headers = org.create_child(node_id=100000, attributes={}, wrong_url=None,
                                                     wrong_data=None, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "Objects for verification not received" in str(response[0])


# Тест на проверку обязательных полей у дочки и родителя в create_child

# Тесты на отправку запросов с несовпадением обязательных полей с родителем
# OS-API-Cc-25, OS-API-Cc-26, OS-API-Cc-27
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
    assert 'error' in str(response[0])
    assert "Objects for verification not received" in str(response[0])


# Общие негативные тесты

# Тесты на отправку запросов без обязательных полей
# OS-API-Cr-18, OS-API-Cr-19, OS-API-Cr-20
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'field'),
                         [({'item_type': item_type, 'item': item, 'attributes': {}}, 'project_id'),
                          ({'project_id': project_id, 'item': item, 'attributes': {}}, 'item_type'),
                          ({'project_id': project_id, 'item_type': item_type, 'attributes': {}}, 'item'),
                          ({'project_ids': project_id, 'item_type': item_type, 'item': item, 'attributes': {}},
                           'project_id')],
                         ids=['without project_id', 'without item_type', 'without item', 'mistake in projest_id'])
def test_create_node_without_required_fields(fields, field):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f'field {field} is required' in str(response[0])


# Тесты на отправку запросов с непредусмотренными полями
# OS-API-Cr-45
@pytest.mark.high
@pytest.mark.parametrize(("fields", 'field'),
                         [({'project_ids': project_id, 'item_type': item_type, 'item': item, 'attributes': {}},
                           'project_ids'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': item, 'new_field': '',
                            'attributes': {}}, 'new_field')],
                         ids=['with projest_ids', 'with new field'])
def test_create_node_with_not_allowed_fields(fields, field):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f"field {field} not allowed" in str(response[0])


# Тесты на отправку запросов с несуществующими значениями в обязательных полях
# OS-API-Cr-41, OS-API-Cr-42, OS-API-Cr-43
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
    assert status == 422 or status == 404
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert "Objects for verification not received" in str(response[0])


# Тесты на отправку запросов с дублированием обязательных полей в теле
# OS-API-Cr-61, OS-API-Cr-62
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
# OS-API-Cr-34, OS-API-Cr-24, OS-API-Cr-35, OS-API-Cr-25, OS-API-Cr-26, OS-API-Cr-36
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


# Тест на отправку запросa с пустой строкой в поле attributes
@pytest.mark.medium
def test_create_node_with_empty_value_in_attributes():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                'item': item, 'attributes': ''}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert 'field attributes must not be empty' in str(response[0])


# Тесты на отправку запросов с неверным форматом значений в обязательных полях
# OS-API-Cr-21, OS-API-Cr-63, OS-API-Cr-64
@pytest.mark.medium
@pytest.mark.parametrize(("fields", 'field', 'formats'),
                         [({'project_id': 123, 'item_type': item_type, 'item': item, 'attributes': {}},
                           'project_id', 'uuid'),
                          ({'project_id': 'abc', 'item_type': item_type, 'item': item, 'attributes': {}},
                           'project_id', 'uuid'),
                          ({'project_id': project_id, 'item_type': 123, 'item': item, 'attributes': {}},
                           'item_type', 'str'),
                          ({'project_id': project_id, 'item_type': item_type, 'item': 123, 'attributes': {}},
                           'item', 'str')],
                         ids=['project_id int', 'project_id str', 'item_type int', 'item int'])
def test_create_node_with_incorrect_format_in_fields(fields, field, formats):
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_data=fields, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert f"['{field} has wrong format, must be {formats}']" in str(response[0])


# Тест на отправку запроса с ключами обязательных полей в теле в верхнем регистре
# OS-API-Cr-7
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
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0])
    assert 'field PROJECT_ID not allowed' in str(response[0]) and 'field ITEM_TYPE not allowed' in str(response[0]) \
           and 'field ITEM not allowed' in str(response[0]) and 'field ATTRIBUTES not allowed' in str(response[0])


# Тест на отправку запроса с телом запроса в формате text
# OS-API-Cr-32
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
# OS-API-Cr-65
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
    assert status == 422 or status == 400
    assert "'id': " not in str(response[0])


# Тест на отправку запроса без тела
# OS-API-Cr-33
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
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0])


# Тест на отправку запроса со строкой в поле attributes
# OS-API-Cr-44
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
    assert 'error' in str(response[0])
    assert "['attributes has wrong format, must be json']" in str(response[0])


# Тест на отправку запроса с полем attributes в формате dict
# OS-API-Cr-51
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
    assert 'error' in str(response[0])
    assert "['attributes has wrong format, must be json']" in str(response[0])


# Тесты на отправку запросов с неверным url и эндпоинтом
# OS-API-Cr-11, OS-API-Cr-12
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
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)



# Тест на отправку запроса неверным методом
# OS-API-Cr-10
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
    res = requests.put(url_node, headers=headers, params=None, json=data)
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
    res = requests.delete(url_node, headers=headers, params=None, json=data)
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
# OS-API-Cr-15, OS-API-Cr-16
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
# OS-API-Cr-60
@pytest.mark.medium
@pytest.mark.skip
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
    assert "'Content-Type': 'text/html'" in str(res_headers) or "'Content-Type': 'text/html; charset=utf-8'" \
           in str(res_headers)


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
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0])


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
    assert 'error' in str(response[0])
    assert 'field project_id is required' in str(response[0]) and 'field item_type is required' in str(response[0]) \
           and 'field item is required' in str(response[0])


# Тест на отправку запроса с id в body
# OS-API-Cc-73
@pytest.mark.min
# @pytest.mark.skip
def test_create_node_id_in_body():
    status, response, res_headers = org.create_child(attributes=None, node_id=None, wrong_headers=None,
                                                     wrong_url=f"https://api.cloveri.skroy.ru/api/v1/node/",
                                                     wrong_data={'parent_id': id_root1, 'project_id': project_id,
                                                                 'item_type': item_type,
                                                                 'item': item, 'attributes': {}}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status != 201
    assert status == 422
    assert "'id': " not in str(response[0])
    assert 'error' in str(response[0])
    assert 'field parent_id not allowed' in str(response[0])


# Тест на отправку запроса с id в headers
# OS-API-Cc-74
@pytest.mark.min
# @pytest.mark.skip
def test_create_node_id_in_headers():
    status, response, res_headers = org.create_child(attributes=None, node_id=None,
                                                     wrong_headers={'parent_id': str(id_root1)},
                                                     wrong_url=f"https://api.cloveri.skroy.ru/api/v1/node/",
                                                     wrong_data={'project_id': project_id, 'item_type': item_type,
                                                                 'item': item, 'attributes': {}}, wrong_params=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201 or status == 404 or status == 422
