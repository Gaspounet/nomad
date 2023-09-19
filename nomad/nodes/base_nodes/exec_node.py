#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Base exec node to execute code
"""

# Python Core Import
import logging

# Third-party Imports
from NodeGraphQt.constants import NodePropWidgetEnum
from NodeGraphQt.nodes.base_node import BaseNode
from NodeGraphQt.qgraphics.node_base import NodeItem

# Nomad Imports
from nomad.pkg_info import __module_name__
from nomad.constants import PortType, NodeStatus


class ExecNode(BaseNode):
    __identifier__ = f'{__module_name__}.base'
    NODE_NAME = f'{__identifier__}.ExecNode'

    def __init__(self, qgraphics_item=None):
        super(ExecNode, self).__init__(qgraphics_item or NodeItem)
        self.add_input(name='in', port_type=PortType.EXEC, multi_input=True, display_name=False, )
        self.add_output(name='out', port_type=PortType.EXEC, multi_output=True, display_name=False)
        self.create_property('status', NodeStatus.IDLE.name, widget_type=NodePropWidgetEnum.QLABEL.value, tab='Properties')
        self.create_property('payload', {})
        self.create_property(
            'script',
            'self.info("Hello World")',
            widget_type=NodePropWidgetEnum.QTEXT_EDIT.value,
            tab='Properties',
            widget_tooltip='Code that will run when Executing the node'
        )
        self._logger = logging.getLogger(f'{self.name()}.{self.id}')
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.critical = self._logger.critical

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

    def execute(self):
        """Execute the current node and previous base_nodes if not disabled or complete"""
        self.pre_execute()
        if not self.disabled():
            self.status = NodeStatus.WORKING
            try:
                self.on_execute()
            except:
                self.status = NodeStatus.ERROR
                raise
            else:
                self.post_execute()

    def pre_execute(self):
        for port in self.get_input('in').connected_ports():
            if port.node().status == NodeStatus.IDLE:
                port.node().execute()

    def on_execute(self):
        script: str = self.get_property('script')
        exec(script)

    def post_execute(self):
        self.status = NodeStatus.COMPLETE

    @property
    def status(self) -> NodeStatus:
        """Get the status of the current node"""
        return NodeStatus.__getitem__(self.get_property('status'))

    @status.setter
    def status(self, status: NodeStatus):
        """Set the status and the color of the current node"""
        if status == NodeStatus.DISABLED and not self.disabled():
            self.set_disabled(True)
        elif status != NodeStatus.DISABLED and self.disabled():
            self.set_disabled(False)
        else:
            self.set_property('status', status.name)
            self.set_color(*status.color)


def execute(graph, node):
    node.execute()


def disable(graph, node):
    if node.disabled():
        node.set_disabled(False)
    else:
        node.set_disabled(True)


def expand(graph, node):
    node.expand()
