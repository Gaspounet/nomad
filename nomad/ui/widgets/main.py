#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Docstring with information
"""

# Python Core Import
import json
import importlib
import os
import sys

# Third-party Imports
from Qt.QtCore import Qt
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QDockWidget
from Qt.QtWidgets import QGridLayout
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QMenuBar
from Qt.QtWidgets import QWidget
from NodeGraphQt import NodeGraph
from NodeGraphQt import PropertiesBinWidget

# Nomad Imports
from nomad.nodes.base_nodes.exec_node import ExecNode


class Nomad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nomad')

        self.node_graph = NodeGraph(parent=self)
        self.node_graph.register_node(ExecNode)
        self.node_graph.set_context_menu_from_file('E:/WORK/CODING/packages/nomad/nomad/hotkeys/hotkeys.json')
        self.node_graph.set_context_menu_from_file('E:/WORK/CODING/packages/nomad/nomad/nodes/hotkeys.json', menu='nodes')
        self.setCentralWidget(self.node_graph.widget)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()


    def createActions(self):
        pass

    def createMenus(self):
        menu_bar = QMenuBar(parent=self)
        menus = []
        for action in self.node_graph.get_context_menu('graph').qmenu.actions():
            if action.menu():
                if action.menu() not in menus:
                    menus.append(action.menu())
        for menu in menus:
            print(menu.columnCount())
            menu_bar.addMenu(menu)
        self.setMenuBar(menu_bar)


    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage('Ready', 2000)

    def createDockWindows(self):
        property_widget_dock = QDockWidget()
        property_widget_dock.setFeatures(QDockWidget.DockWidgetMovable)
        property_widget_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        property_widget = PropertiesBinWidget(parent=property_widget_dock, node_graph=self.node_graph)
        property_widget_dock.setWidget(property_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, property_widget_dock)


class NomadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QGridLayout()
        node_graph_dock = QDockWidget()
        node_graph_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        property_widget_dock = QDockWidget()
        property_widget = PropertiesBinWidget(node_graph=node_graph)
        property_widget_dock.setWidget(property_widget)

        layout.addWidget(node_graph_dock, 0, 0)
        layout.addWidget(property_widget_dock, 0, 1)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    nomad = Nomad()
    nomad.show()
    app.exec_()
