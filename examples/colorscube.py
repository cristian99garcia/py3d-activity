#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import py3d
from utils import DemoUtils

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GLib


class ColorsCubesExample(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(100, 100)
        self.area.connect("draw", self._draw_cb)
        self.pack_start(self.area, True, True, 0)

        self.black = py3d.RGBA(0, 0, 0, 1)
        self.white = py3d.RGBA(1, 1, 1, 1)

        self.renderer = py3d.Renderer()

        self.cubes = [ ]

        for i in range(0, 10):
            for j in range(0, 10):
                for k in range(0, 10):
                    if (i == 0 or j == 0 or k == 0 or
                        i == 9 or j == 9 or k == 9):

                        cube = py3d.ShapeUtils.make_cube(0.5)
                        transform = py3d.Transform()
                        transform.translate(i - 5, j - 5, k - 5)
                        self.cubes.append({
                            "shape": cube,
                            "color": py3d.RGBA(i / 10.0, j / 10.0, k / 10.0, 0.3),
                            "trans": transform
                        })

        self.num_cubes = len(self.cubes)
        self.cur_white = False

        DemoUtils.auto_camera(self.renderer, self.area, 0, 0, -30, 0.40, -1.06, 0, lambda: GLib.idle_add(self.queue_draw))
        self.renderer.camera.focal_length = 2.5

        self.buffer_shapes()
        self.show_all()

    def buffer_shapes(self):
        for cube in self.cubes:
            self.renderer.fill_rgba = cube["color"]
            self.renderer.transform = cube["trans"]
            self.renderer.buffer_shape(cube["shape"], cube["color"])

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
