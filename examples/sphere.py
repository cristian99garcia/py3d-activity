#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import py3d
from utils import DemoUtils

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GLib


class SphereExample(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(100, 100)
        self.area.connect("draw", self._draw_cb)
        self.pack_start(self.area, True, True, 0)

        adj = Gtk.Adjustment(10, 3, 30, 1, 5)
        self.scale_x = Gtk.HScale()
        self.scale_x.set_tooltip_text("Tess X")
        self.scale_x.set_adjustment(adj)
        self.scale_x.set_digits(0)
        self.scale_x.connect("value-changed", self._value_changed_cb)
        self.pack_start(self.scale_x, False, False, 0)

        adj = Gtk.Adjustment(10, 3, 30, 1, 5)
        self.scale_y = Gtk.HScale()
        self.scale_y.set_tooltip_text("Tess Y")
        self.scale_y.set_adjustment(adj)
        self.scale_y.set_digits(0)
        self.scale_y.connect("value-changed", self._value_changed_cb)
        self.pack_start(self.scale_y, False, False, 0)

        self.renderer = py3d.Renderer()

        self.sphere = None
        self.transform = py3d.Transform()
        self.transform.translate(1, 1, 0)
        self.make_sphere()

        DemoUtils.auto_camera(self.renderer, self.area, 1, 1, -50, 0.50, 0.5, 0, self.redraw)
        self.renderer.camera.focal_length = 2.5

        self.show_all()

    def make_sphere(self):
        tess_x = int(self.scale_x.get_value())
        tess_y = int(self.scale_y.get_value())

        self.sphere = py3d.ShapeUtils.make_sphere(10, tess_x, tess_y)
        self.redraw()

    def buffer_sphere(self):
        color = py3d.RGBA(0.1, 0.8, 0.4, 1)
        self.renderer.transform = self.transform
        self.renderer.buffer_shape(self.sphere, color)

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
        self.buffer_sphere()

        self.renderer.draw_buffer()
        self.renderer.empty_buffer()

    def _value_changed_cb(self, scale):
        self.make_sphere()


if __name__ == "__main__":
    Window()
    Gtk.main()
