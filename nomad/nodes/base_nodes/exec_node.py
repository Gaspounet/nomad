#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Base exec node to execute code
"""

# Python Core Import
import logging
from typing import Any

# Third-party Imports
from NodeGraphQt.nodes.base_node import BaseNode
from NodeGraphQt.qgraphics.node_base import NodeItem

# Nomad Imports
from nomad.pkg_info import __module_name__
from nomad.constants import PortTypeColor, NodeStatus


class ExecNode(BaseNode):
    __identifier__ = 'nomad.base'
    NODE_NAME = 'ExecNode'

    def __init__(self, qgraphics_item=None):
        super(ExecNode, self).__init__(qgraphics_item or NodeItem)
        self.add_input('in', port_type='exec', multi_input=True, display_name=False)
        self.add_output('out', port_type='exec', multi_output=True, display_name=False)
        self._command_line = 'print(\'Hello World\')'
        self._status = NodeStatus.IDLE
        self._payload = {}
        print(__module_name__, self.__class__, self.name())
        self._logger = logging.getLogger('{}.{}.{}'.format(__module_name__, self.name(), self.get_property('id')))
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.critical = self._logger.critical
        self.debug('Init')

    def add_input(self, name='input', port_type='', multi_input=False, display_name=True, locked=False,
                  painter_func=None):
        color = PortTypeColor[port_type].value
        return super().add_input(name, multi_input, display_name, color, locked, painter_func)

    def add_output(self, name='output', port_type='', multi_output=True, display_name=True, locked=False,
                   painter_func=None):
        color = PortTypeColor[str(port_type)].value
        return super().add_output(name, multi_output, display_name, color, locked, painter_func)

    def execute(self):
        """Execute the current node and previous base_nodes if not disabled or complete"""
        for port in self.get_input('in').connected_ports():
            if port.node().status == NodeStatus.IDLE:
                port.node().execute()
        if not self.status == NodeStatus.DISABLED:
            self.on_execute()

    def on_execute(self):
        self.debug('Hello World, I\'m {}'.format(self.name()))

    @property
    def status(self) -> NodeStatus:
        """Get the status of the current node"""
        return self._status

    @status.setter
    def status(self, status: NodeStatus):
        """Set the status and the color of the current node"""
        color = status.value
        self.set_color(*color)

    # Logger management

    def info(self, message):
        self._logger.info(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)

    def critical(self, message):
        self._logger.critical(message)
