#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Docstring with information
"""

# Python Core Import

# Third-party Imports

# Nomad Imports


if __name__ == "__main__":
    import sys
    from Qt import QtWidgets
    from NodeGraphQt import NodeGraph
    from nomad.nodes.base_nodes.exec_node import ExecNode

    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()
    graph.register_node(ExecNode)
    graph_widget = graph.widget
    graph_widget.show()
    node_a = graph.create_node('nomad.base.ExecNode', name='node A')  # -> ExecNode
    node_b = graph.create_node('nomad.base.ExecNode', name='node B')  # -> ExecNode
    node_b.set_output(0, node_a.input(0))
    node_b.add_input('data', port_type='str')
    node_a.execute()
    app.exec_()
