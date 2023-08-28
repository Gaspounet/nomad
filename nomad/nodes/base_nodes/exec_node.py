#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Base exec node to execute code
"""

# Python Core Import
import logging
from typing import Any

import NodeGraphQt
# Third-party Imports
from PySide2.QtCore import Slot
from NodeGraphQt.nodes.base_node import BaseNode
from NodeGraphQt.nodes.group_node import GroupNode
from NodeGraphQt.qgraphics.node_base import NodeItem

# Nomad Imports
from nomad.pkg_info import __module_name__
from nomad.constants import PortType, NodeStatus


class ExecNode(BaseNode):
    __identifier__ = 'nomad.base'
    NODE_NAME = 'nomad.base.ExecNode'

    def __init__(self, qgraphics_item=None):
        super(ExecNode, self).__init__(qgraphics_item or NodeItem)
        self.add_input(name='in', port_type=PortType.EXEC, multi_input=True, display_name=False, )
        self.add_output(name='out', port_type=PortType.EXEC, multi_output=True, display_name=False)
        self._command_line = 'print(\'Hello World\')'
        self._status = NodeStatus.IDLE
        self.model.add_property('status', NodeStatus.IDLE)
        self._payload = {}
        print(__module_name__, self.__class__, self.name())
        self._logger = logging.getLogger('{}.{}.{}'.format(__module_name__, self.name(), self.get_property('id')))
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.critical = self._logger.critical
        self.debug('Init')

    def add_input(self, name='input', port_type=None, multi_input=False, display_name=True, locked=False,
                  painter_func=None):
        """
        Add input :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the input port.
            port_type (constants.PortType): type of port being created
            multi_input (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        if not isinstance(port_type, PortType):
            raise TypeError('port_type argument needs to be of type constants.PortType')
        return super().add_input(name, multi_input, display_name, port_type.color, locked, painter_func)

    def add_output(self, name='output', port_type=None, multi_output=True, display_name=True, locked=False,
                   painter_func=None):
        """
        Add output :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the input port.
            port_type (constants.PortType): type of port being created
            multi_output (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        if not isinstance(port_type, PortType):
            raise TypeError('port_type argument needs to be of type constants.PortType')
        return super().add_output(name, multi_output, display_name, port_type.color, locked, painter_func)

    @Slot(NodeGraphQt.NodeGraph, NodeGraphQt.BaseNode)
    def execute(self, node):
        """Execute the current node and previous base_nodes if not disabled or complete"""
        self.pre_execute()
        if not self.disabled():
            self.status = NodeStatus.WORKING
            self.on_execute()
            self.post_execute()

    def pre_execute(self):
        for port in self.get_input('in').connected_ports():
            if port.node().status == NodeStatus.IDLE:
                ExecNode.execute(self, port.node())

    def on_execute(self):
        self.debug('Hello World, I\'m {}'.format(self.name()))

    def post_execute(self):
        self.status = NodeStatus.COMPLETE

    @property
    def status(self) -> NodeStatus:
        """Get the status of the current node"""
        return self._status

    @status.setter
    def status(self, status: NodeStatus):
        """Set the status and the color of the current node"""
        if status == NodeStatus.DISABLED and not self.disabled():
            self.set_disabled(True)
        elif status != NodeStatus.DISABLED and self.disabled():
            self.set_disabled(False)
        else:
            self._status = status
            self.set_property('status', status)
            self.set_color(*status.color)

    # Logger management

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)


def execute(graph, node):
    node.execute(node)


def disable(graph, node):
    if node.disabled():
        node.set_disabled(False)
    else:
        node.set_disabled(True)


def expand(graph, node):
    node.expand()
