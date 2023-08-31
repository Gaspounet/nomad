#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Docstring with information
"""

# Python Core Import

# Third-party Imports

# Nomad Imports
from nomad import constants
from nomad.constants import NodeStatus

if __name__ == "__main__":
    import sys
    import pprint
    # from nomad.constants import NodeStatus
    from Qt import QtWidgets
    from NodeGraphQt import NodeGraph
    from NodeGraphQt import PropertiesBinWidget
    from nomad.nodes.base_nodes.exec_node import ExecNode, disable, expand, execute

    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()
    graph.register_node(ExecNode)

    graph_widget = graph.widget
    graph_widget.show()
    graph.set_context_menu_from_file('../nomad/hotkeys/hotkeys.json')
    # graph.set_context_menu_from_file('../nomad/nodes/hotkeys.json', menu='nodes')
    nodes_menu = graph.get_context_menu('nodes')
    nodes_menu.add_command('Execute', execute, ExecNode.NODE_NAME, ExecNode)
    nodes_menu.add_command('Disable', disable, ExecNode.NODE_NAME, ExecNode)
    nodes_menu.add_command('Expand', expand, ExecNode.NODE_NAME, ExecNode)
    node_a: ExecNode = graph.create_node(ExecNode.NODE_NAME, name='node A')
    node_b: ExecNode = graph.create_node(ExecNode.NODE_NAME, name='node B')
    node_b.set_output(0, node_a.input(0))
    # node_b.add_input(name='dataIn', port_type=constants.PortType.STRING)
    # node_b.add_output(name='dataOut', port_type=constants.PortType.STRING)
    # node_b.status = NodeStatus.DISABLED
    pprint.pprint(node_b.model.custom_properties.get('status'))
    pprint.pprint(constants.NodeStatus.__getitem__('IDLE'))
    for i in node_b.widgets():
        print(i)
    pprint.pprint(node_b.model.to_dict)
    pprint.pprint(node_b.name())
    graph.auto_layout_nodes()
    graph.center_on(graph.all_nodes())
    # create properties bin widget.

    properties_bin = PropertiesBinWidget(parent=None, node_graph=graph)

    properties_bin.show()
    app.exec_()
