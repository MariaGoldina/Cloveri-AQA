from .methods import *


status_root1, root1, _ = org.create_root(attributes={})
id_root1 = root1[0]['id']
path_root1 = root1[0]['path']
order_root1 = root1[0]['inner_order']

status_root2, root2, _ = org.create_root(attributes={})
id_root2 = root2[0]['id']
path_root2 = root2[0]['path']
order_root2 = root2[0]['inner_order']

status_child2lvl, child2lvl, _ = org.create_child(attributes={}, node_id=id_root1)
id_child2lvl = child2lvl[0]['id']
path_child2lvl = child2lvl[0]['path']
order_child2lvl = child2lvl[0]['inner_order']

status_sec_child2lvl, sec_child2lvl, _ = org.create_child(attributes={}, node_id=id_root1)
id_sec_child2lvl = sec_child2lvl[0]['id']
path_sec_child2lvl = sec_child2lvl[0]['path']
order_sec_child2lvl = sec_child2lvl[0]['inner_order']

status_child3lvl, child3lvl, _ = org.create_child(attributes={}, node_id=id_child2lvl)
id_child3lvl = child3lvl[0]['id']
path_child3lvl = child3lvl[0]['path']
order_child3lvl = child3lvl[0]['inner_order']

status_sec_child3lvl, sec_child3lvl, _ = org.create_child(attributes={}, node_id=id_child2lvl)
id_sec_child3lvl = sec_child3lvl[0]['id']
path_sec_child3lvl = sec_child3lvl[0]['path']
order_sec_child3lvl = sec_child3lvl[0]['inner_order']

status_child4lvl, child4lvl, _ = org.create_child(attributes={}, node_id=id_child3lvl)
id_child4lvl = child4lvl[0]['id']
path_child4lvl = child4lvl[0]['path']
order_child4lvl = child4lvl[0]['inner_order']

status_sec_child4lvl, sec_child4lvl, _ = org.create_child(attributes={}, node_id=id_child3lvl)
id_sec_child4lvl = sec_child4lvl[0]['id']
path_sec_child4lvl = sec_child4lvl[0]['path']
order_sec_child4lvl = sec_child4lvl[0]['inner_order']

status_third_child4lvl, third_child4lvl, _ = org.create_child(attributes={}, node_id=id_child3lvl)
id_third_child4lvl = third_child4lvl[0]['id']
path_third_child4lvl = third_child4lvl[0]['path']
order_third_child4lvl = third_child4lvl[0]['inner_order']

status_fourth_child4lvl, fourth_child4lvl, _ = org.create_child(attributes={}, node_id=id_child3lvl)
id_fourth_child4lvl = fourth_child4lvl[0]['id']
path_fourth_child4lvl = fourth_child4lvl[0]['path']
order_fourth_child4lvl = fourth_child4lvl[0]['inner_order']

status_child4lvl_for_sec_child3lvl, child4lvl_for_sec_child3lvl, _ = org.create_child(attributes={},
                                                                                      node_id=id_sec_child3lvl)
id_child4lvl_for_sec_child3lvl = child4lvl_for_sec_child3lvl[0]['id']
path_child4lvl_for_sec_child3lvl = child4lvl_for_sec_child3lvl[0]['path']
order_child4lvl_for_sec_child3lvl = child4lvl_for_sec_child3lvl[0]['inner_order']

# status_root3, root3, _ = org.create_root(attributes=None, wrong_data={'project_id': other_project_id,
#                                                                       'item_type': other_item_type,
#                                                                       'item': other_item, 'attributes': {}})
# id_root3 = root3[0]['id']
# path_root3 = root3[0]['path']
# order_root3 = root3[0]['inner_order']


status_get, response_get, _ = org.get_tree()
nodes_list = []
nodes1lvl = []
nodes2lvl = []
nodes3lvl = []
nodes4lvl = []
nodes5lvl = []
for i in response_get[0]:
    nodes_list.append(i)
for x in nodes_list:
    if x['level_node'] == 1:
        nodes1lvl.append(x)
    elif x['level_node'] == 2:
        nodes2lvl.append(x)
    elif x['level_node'] == 3:
        nodes3lvl.append(x)
    elif x['level_node'] == 4:
        nodes4lvl.append(x)
    elif x['level_node'] == 5:
        nodes5lvl.append(x)
amount_nodes1lvl = len(nodes1lvl)
amount_nodes2lvl = len(nodes2lvl)
amount_nodes3lvl = len(nodes3lvl)
amount_nodes4lvl = len(nodes4lvl)
amount_nodes5lvl = len(nodes5lvl)


print(root1, root2, child2lvl, sec_child2lvl, child3lvl, sec_child3lvl, child4lvl, sec_child4lvl, third_child4lvl,
      fourth_child4lvl, child4lvl_for_sec_child3lvl)
print(order_root1, order_root2, order_child2lvl, order_sec_child2lvl, order_child3lvl, order_sec_child3lvl,
      order_child4lvl, order_sec_child4lvl, order_third_child4lvl, order_fourth_child4lvl,
      order_child4lvl_for_sec_child3lvl)
