#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import py3d
from utils import DemoUtils

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GLib


class RGBAExample(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(100, 100)
        self.area.connect("draw", self._draw_cb)
        self.pack_start(self.area, True, True, 0)

        self.scales = {}

        for value in ["red", "green", "blue", "alpha"]:
            adj = Gtk.Adjustment(1.0, 0.0, 1.0, 0.01, 0.01)
            scale = Gtk.HScale()
            scale.set_digits(3)
            scale.set_adjustment(adj)
            scale.set_tooltip_text(value)
            scale.connect("value-changed", self._value_change_cb)
            self.pack_start(scale, False, False, 0)

            self.scales[value] = scale

        self.renderer = py3d.Renderer()

        self.cube = py3d.ShapeUtils.make_cube(10)
        self.transform = py3d.Transform()
        self.transform.translate(1, 1, 1)

        DemoUtils.auto_camera(self.renderer, self.area, 1, 1, -50, 0.50, 0.5, 0, self.redraw)
        self.renderer.camera.focal_length = 2

        self.show_all()

    def buffer_shapes(self):
        color = py3d.RGBA(
            self.scales["red"].get_value(),
            self.scales["green"].get_value(),
            self.scales["blue"].get_value(),
            self.scales["alpha"].get_value())

        self.renderer.transform = self.transform
        self.renderer.buffer_shape(self.cube, color)

    def redraw(self):
        GLib.idle_add(self.queue_draw)

    def _draw_cb(self, widget, context):
        self.renderer.context = context

        allocation = self.area.get_allocation()
        self.renderer.width = allocation.width
        self.renderer.height = allocation.height
        self.renderer.scale = self.renderer.height / 2
        self.renderer.xoff = self.renderer.width / 2

        self.renderer.draw_background()
        self.buffer_shapes()

        self.renderer.draw_buffer()
        self.renderer.empty_buffer()

    def _value_change_cb(self, scale):
        self.redraw()
