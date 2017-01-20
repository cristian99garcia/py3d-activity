#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import py3d
from utils import DemoUtils

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GLib


class RubiksCubeExample(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(100, 100)
        self.area.connect("draw", self._draw_cb)
        self.pack_start(self.area, True, True, 0)

        self.renderer = py3d.Renderer()
        self.transform = py3d.Transform()
        self.transform.translate(1, 1, 1)

        self.colors = [
            py3d.RGBA(0, 0, 1, 1),
            py3d.RGBA(1, 0, 0, 1),
            py3d.RGBA(1, 1, 0, 1),
            py3d.RGBA(0, 1, 0, 1),
            py3d.RGBA(1, 0.35, 0, 1),
            py3d.RGBA(1, 1, 1, 1),
        ]

        self.shapes = []
        self.cube_whd = 10

        for i in range(0, 6):
            self.make_side(i)

        DemoUtils.auto_camera(self.renderer, self.area, 1, 1, -50, 0.50, 0.5, 0, self.redraw)
        self.renderer.camera.focal_length = 2

        self.show_all()

    def make_side(self, constant):
        def make_planes(w, h, d):
            back = constant >= 3
            planes = []
            x = 1.0
            y = 0
            j = -1 if back else 1

            for i in range(1, 10):
                if w == 0:
                    plane = py3d.ShapeUtils.make_plane(
                        py3d.Point3D(x=self.cube_whd * j, y=-self.cube_whd + x * h,       z=-self.cube_whd + y * d),
                        py3d.Point3D(x=self.cube_whd * j, y=-self.cube_whd + (x - 1) * h, z=-self.cube_whd + y * d),
                        py3d.Point3D(x=self.cube_whd * j, y=-self.cube_whd + (x - 1) * h, z=-self.cube_whd + (y + 1) * d),
                        py3d.Point3D(x=self.cube_whd * j, y=-self.cube_whd + x * h,       z=-self.cube_whd + (y + 1) * d),
                    )

                    if not back:
                        plane.quads = [py3d.QuadFace(3, 2, 1, 0)]

                elif h == 0:
                    plane = py3d.ShapeUtils.make_plane(
                        py3d.Point3D(x=self.cube_whd - x * w,       y=-self.cube_whd * j, z=-self.cube_whd + y * d),
                        py3d.Point3D(x=self.cube_whd - (x - 1) * w, y=-self.cube_whd * j, z=-self.cube_whd + y * d),
                        py3d.Point3D(x=self.cube_whd - (x - 1) * w, y=-self.cube_whd * j, z=-self.cube_whd + (y + 1) * d),
                        py3d.Point3D(x=self.cube_whd - x * w,       y=-self.cube_whd * j, z=-self.cube_whd + (y + 1) * d),
                    )

                    if back:
                        plane.quads = [py3d.QuadFace(3, 2, 1, 0)]

                elif d == 0:
                    plane = py3d.ShapeUtils.make_plane(
                        py3d.Point3D(x=self.cube_whd - x * w,       y=-self.cube_whd + y * h,       z=-self.cube_whd * j),
                        py3d.Point3D(x=self.cube_whd - (x - 1) * w, y=-self.cube_whd + y * h,       z=-self.cube_whd * j),
                        py3d.Point3D(x=self.cube_whd - (x - 1) * w, y=-self.cube_whd + (y + 1) * h, z=-self.cube_whd * j),
                        py3d.Point3D(x=self.cube_whd - x * w,       y=-self.cube_whd + (y + 1) * h, z=-self.cube_whd * j),
                    )

                    if not back:
                        plane.quads = [py3d.QuadFace(3, 2, 1, 0)]

                py3d.ShapeUtils.rebuild_meta(plane)
                planes.append(plane)

                x += 1.0
                if x >= 4:
                    x = 1
                    y += 1

            return planes

        x = 1
        y = 0

        planes = []
        color = None
        c = self.cube_whd * 2.0 / 3.0

        if constant % 3 == 0:
            planes = make_planes(0, c, c)

        elif constant % 3 == 1:
            planes = make_planes(c, c, 0)

        elif constant % 3 == 2:
            planes = make_planes(c, 0, c)

        for plane in planes:
            self.shapes.append({
                "shape": plane,
                "color": self.colors[constant]
            })

    def buffer_shapes(self):
        self.renderer.transform = self.transform

        for shape in self.shapes:
            self.renderer.buffer_shape(shape["shape"], shape["color"])

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
