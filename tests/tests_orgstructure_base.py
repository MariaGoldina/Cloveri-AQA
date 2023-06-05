from methods import *


def test_get_empty_tree():
    status, response, res_headers = org.get_tree()
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200


def test_get_tree_positive():
    status, response, res_headers = org.get_tree()
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200


def test_get_node_positive():
    status, response, res_headers = org.get_node(node_id=1110)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200


def test_get_children_positive():
    status, response, res_headers = org.get_children(node_id=11)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200


def test_create_root_positive():
    status, response, res_headers = org.create_root(attributes={"name": "Компания 1", "description": "ПО"})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201


def test_create_child_positive():
    status, response, res_headers = org.create_child(attributes={"name": "Отдел 1",
                                                                 "description": "разработка"},
                                                     node_id=9999999999999999999999)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201


def test_change_attributes_positive():
    status, response, res_headers = org.change_attributes(attributes={"name": "new name",
                                                                      "description": "new description"},
                                                          node_id=9999999999999999999999)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201


def test_delete_node_positive():
    status, response, res_headers = org.change_hidden_attr(node_id=11, hidden=True, wrong_data={
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'hidden': True,
        'affect_descendants': None
                })
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200


def test_restore_node_positive():
    status, response, res_headers = org.change_hidden_attr(node_id=1, hidden=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 200


def test_change_order_positive():
    status, response, res_headers = org.change_order(node_id_out=11, node_id_in=12)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201


def test_change_parent_positive():
    status, response, res_headers = org.change_parent(node_id_out=1110, node_id_in=1111)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201


def test_get_tree_negative():
    status, response, res_headers = org.get_tree(wrong_url=None, wrong_headers=None, wrong_data=None,
                                                 wrong_params={'project_id': project_id,
                                                               'item_type': other_item_type,
                                                               'item': other_item})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_get_node_negative():
    status, response, res_headers = org.get_node(node_id=None, wrong_id=None, wrong_url=None, wrong_headers=None,
                                                 wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_get_children_negative():
    status, response, res_headers = org.get_children(node_id=1, wrong_id=None, wrong_url=None, wrong_headers=None,
                                                     wrong_params={'project_id': project_id,
                                                                   'item_type': other_item_type,
                                                                   'item': other_item}, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_create_root_negative():
    status, response, res_headers = org.create_root(attributes=None, wrong_url=None, wrong_headers=None,
                                                    wrong_params=None,
                                                    wrong_data={'project_id': '3e3028cd-3849-461b-a32b-90c0d6411dbd',
                                                                'item_type': 'orgstructureM2', 'item': 'start_project',
                                                                'attributes': json.dumps({'name': 'Компания 1'},
                                                                                         ensure_ascii=False)})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')
    assert status == 201


def test_create_child_negative():
    status, response, res_headers = org.create_child(attributes=None, node_id=None, wrong_id=None, wrong_url=None,
                                                     wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_change_attributes_negative():
    status, response, res_headers = org.change_attributes(attributes=None, node_id=None, wrong_id=None, wrong_url=None,
                                                          wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_change_order_negative():
    status, response, res_headers = org.change_order(node_id_out=None, node_id_in=None, wrong_id=None, wrong_url=None,
                                                     wrong_headers=None, wrong_params=None, wrong_data=None)
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_change_hidden_attr_negative():
    status, response, res_headers = org.change_hidden_attr(hidden=None, node_id=5630, wrong_id=None, wrong_url=None,
                                                           wrong_headers=None, wrong_params=None,
                                                           wrong_data={'project_id': '3e3028cd-3849-461b-a32b-90c0d6411dbd',
                                                                'item_type': 'orgstructureM2', 'item': 'start_project',
                                                                'hidden': None})
    print(f"\nCode: {status}")
    print(f"Response: {response}")
    print(f'Response headers: {res_headers}')


def test_get_children():
    res = requests.get("https://api.cloveri.skroy.ru/api/v1/nodes/934/", headers={'Accept': 'application/json'},
                       params={
                           'project_id': project_id,
                           'item_type': item_type,
                           'item': item})
    status = res.status_code
    res_headers = res.headers
    response = ""
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(status, response, res_headers)


def test_change_attributes():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {
        'project_id': project_id,
        'item_type': item_type,
        'item': item,
        'attributes': json.dumps({'name': 'some_new_name'}, ensure_ascii=False)
    }
    res = requests.put("https://api.cloveri.skroy.ru/api/v1/node/1795/attributes/", headers=headers, json=data)
    status = res.status_code
    res_headers = res.headers
    try:
        response = res.json(),
    except json.decoder.JSONDecodeError:
        response = res.text
    print(status, response, res_headers)
