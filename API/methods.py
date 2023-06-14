import requests
import json
from settings import *


class OrgstructureTree():
    def __init__(self):
        pass

    def create_root(self, attributes: dict, wrong_url=None, wrong_headers=None, wrong_data=None, wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_url is None:
            url = url_node
        else:
            url = wrong_url

        if wrong_data is None:
            data = {
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'attributes': json.dumps(attributes, ensure_ascii=False)
                }
        else:
            data = wrong_data

        res = requests.post(url, headers=headers, json=data, params=wrong_params)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def create_child(self, attributes: dict, node_id: int, wrong_id=None, wrong_url=None, wrong_headers=None, wrong_data=None,
                     wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_url is None:
            url = url_node + f'{node_id}/'
        else:
            url = wrong_url

        if wrong_id is None:
            pass
        else:
            node_id = wrong_id

        if wrong_data is None:
            data = {
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'attributes': json.dumps(attributes, ensure_ascii=False)
                }
        else:
            data = wrong_data

        res = requests.post(url, headers=headers, json=data, params=wrong_params)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def get_node(self, node_id: int, wrong_id=None, wrong_url=None, wrong_headers=None, wrong_data=None,
                 wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_id is None:
            pass
        else:
            node_id = wrong_id

        if wrong_url is None:
            url = url_node + f'{node_id}/'
        else:
            url = wrong_url

        if wrong_params is None:
            params = {
            'project_id': project_id,
            'item_type': item_type,
            'item': item
            }
        else:
            params = wrong_params

        res = requests.get(url, headers=headers, params=params, json=wrong_data)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def get_tree(self, wrong_url=None, wrong_headers=None, wrong_data=None, wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_url is None:
            url = url_nodes
        else:
            url = wrong_url

        if wrong_params is None:
            params = {
            'project_id': project_id,
            'item_type': item_type,
            'item': item
            }
        else:
            params = wrong_params

        res = requests.get(url, headers=headers, params=params, json=wrong_data)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def get_descendants(self, node_id: int, wrong_id=None, wrong_url=None, wrong_headers=None, wrong_data=None, wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_id is None:
            pass
        else:
            node_id = wrong_id

        if wrong_url is None:
            url = url_nodes + f'{node_id}/'
        else:
            url = wrong_url

        if wrong_params is None:
            params = {
            'project_id': project_id,
            'item_type': item_type,
            'item': item
            }
        else:
            params = wrong_params

        res = requests.get(url, headers=headers, params=params, json=wrong_data)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def change_attributes(self, attributes: dict, node_id: int, wrong_id=None, wrong_url=None, wrong_headers=None, wrong_data=None, wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_id is None:
            pass
        else:
            node_id = wrong_id

        if wrong_url is None:
            url = url_node+f'{node_id}/attributes/'
        else:
            url = wrong_url

        if wrong_data is None:
            data = {
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'attributes': json.dumps(attributes, ensure_ascii=False)
                }
        else:
            data = wrong_data

        res = requests.patch(url, headers=headers, json=data, params=wrong_params)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def change_hidden_attr(self, hidden: bool, node_id: int, wrong_id=None, wrong_url=None, wrong_headers=None, wrong_data=None, wrong_params=None, ):
        if wrong_headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_id is None:
            pass
        else:
            node_id = wrong_id

        if wrong_url is None:
            url = url_node + f'{node_id}/hidden/'
        else:
            url = wrong_url

        if wrong_data is None:
            data = {
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'hidden': hidden
                }
        else:
            data = wrong_data

        res = requests.patch(url, headers=headers, json=data, params=wrong_params)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def change_order(self, node_id_out: int, node_id_in: int, wrong_id=None, wrong_url=None, wrong_headers=None,
                     wrong_data=None, wrong_params=None, ):
        if wrong_id is None:
            pass
        else:
            node_id_out = wrong_id

        if wrong_headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_url is None:
            url = url_node + f'{node_id_out}/'+'order/'
        else:
            url = wrong_url

        if wrong_data is None:
            data = {
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'destination_node_id': node_id_in
                }
        else:
            data = wrong_data

        res = requests.patch(url, headers=headers, json=data, params=wrong_params)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers

    def change_parent(self, node_id_out: int, node_id_in: int, wrong_id=None, wrong_url=None, wrong_headers=None,
                      wrong_data=None, wrong_params=None, ):
        if wrong_id is None:
            pass
        else:
            node_id_out = wrong_id

        if wrong_headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        else:
            headers = wrong_headers

        if wrong_url is None:
            url = url_node + f'{node_id_out}/'+'parent/'
        else:
            url = wrong_url

        if wrong_data is None:
            data = {
                'project_id': project_id,
                'item_type': item_type,
                'item': item,
                'new_parent_id': node_id_in
                }
        else:
            data = wrong_data

        res = requests.patch(url, headers=headers, json=data, params=wrong_params)
        status = res.status_code
        res_headers = res.headers
        response = ""
        try:
            response = res.json(),
        except json.decoder.JSONDecodeError:
            response = res.text
        return status, response, res_headers


org = OrgstructureTree()
