#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017, Cristian García <cristian99garcia@gmail.com>
#
# This library is free software you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import gi
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk
from gi.repository import GObject


camera_state = {
    "rotate_x": 0,
    "rotate_y": 0,
    "rotate_z": 0,
    "x": 0,
    "y": 0,
    "z": 0
}


class DemoUtils:

    @classmethod
    def clamp(self, a, b, c):
        return min(b, max(a, c))

    @classmethod
    def register_mouse_events(self, area, listener):
        state = {
            "first_event": True,
            "is_clicking": False,
            "last_x": 0,
            "last_y": 0
        }

        def rel_xy(event):
            return {"x": event.x, "y": event.y}

        def mousedown(area, event):
            rel = rel_xy(event)
            state["is_clicking"] = True
            state["last_x"] = rel["x"]
            state["last_y"] = rel["y"]

        def mouseup(area, event):
            state["is_clicking"] = False

        def mouseout(area, event):
            state["is_clicking"] = False

        def mousemove(area, event):
            rel = rel_xy(event)
            delta_x = state["last_x"] - rel["x"]
            delta_y = state["last_y"] - rel["y"]
            state["last_x"] = rel["x"]
            state["last_y"] = rel["y"]

            if state["first_event"]:
                state["first_event"] = False

            else:
                info = {
                    "is_clicking": state["is_clicking"],
                    "canvas_x": state["last_x"],
                    "canvas_y": state["last_y"],
                    "delta_x": delta_x,
                    "delta_y": delta_y,
                    "shift": event.state == Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.BUTTON1_MASK,
                    "ctrl": event.state == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.BUTTON1_MASK
                }

                listener(info)

        area.connect("button-press-event", mousedown)
        area.connect("button-release-event", mouseup)
        area.connect("motion-notify-event", mousemove)

    @classmethod
    def register_mouse_whell_events(self, canvas, listener):
        def handler(e):
            listener(-e.detail if e.detail else e.wheelDelta / 40)
            e.stopPropagation()
            e.preventDefault()
            return False

        """
        # Register on both mousewheel and DOMMouseScroll.    Hopefully a browser
        # only fires on one and not both.
        canvas.addEventListener('DOMMouseScroll', handler, False)
        canvas.addEventListener('mousewheel', handler, False)
        """

    @classmethod
    def set_camera(self, renderer, state):
        ct = renderer.camera.transform
        ct.reset()
        ct.rotate_z(state["rotate_z"])
        ct.rotate_y(state["rotate_y"])
        ct.rotate_x(state["rotate_x"])
        ct.translate(state["x"], state["y"], state["z"])

    @classmethod
    def auto_camera(self, renderer, area, ix, iy, iz, tx, ty, tz, redraw, opts=None):
        area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        area.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        area.add_events(Gdk.EventMask.POINTER_MOTION_MASK)

        global camera_state
        camera_state = {
            "rotate_x": tx,
            "rotate_y": ty,
            "rotate_z": tz,
            "x": ix,
            "y": iy,
            "z": iz
        }

        self.set_camera(renderer, camera_state)

        opts = opts if opts is not None else { }
        cur_pending = None

        def handle_camera_mouse(info):
            if not info["is_clicking"]:
                return

            if info["ctrl"]:
                renderer.camera.focal_length = DemoUtils.clamp(0.05, 10, renderer.camera.focal_length + (info["delta_y"] * 0.01))

            elif info["shift"]:
                camera_state["z"] += info["delta_y"] * 0.01
                if opts.get("zAxisLimit", None) is not None and camera_state["z"] > opts["zAxisLimit"]:
                    camera_state["z"] = opts["zAxisLimit"]

            #elif info["ctrl"]:
            #    camera_state["x"] -= info["delta_x"] * 0.01
            #    camera_state["y"] -= info.delta_y * 0.01
            else:
                camera_state["rotate_y"] -= info["delta_x"] * 0.01
                camera_state["rotate_x"] -= info["delta_y"] * 0.01
                self.set_camera(renderer, camera_state)

            redraw()

        DemoUtils.register_mouse_events(area, handle_camera_mouse)

        if opts.get("panZOnMouseWheel", False):
            """
            wheel_scale = opts.panZOnMouseWheelScale != undefined ?
                                                    opts.panZOnMouseWheelScale : 30
            register_mouse_whell_events(renderer.canvas, function(delta_y) {
                # Create a fake info to act as if shift + drag happened.
                fake_info = {
                    is_clicking: True,
                    canvas_x: None,
                    canvas_y: None,
                    delta_x: 0,
                    delta_y: delta_y * wheel_scale,
                    shift: True,
                    ctrl: False
                }
                handle_camera_mouse(fake_info)
            })
            """

class Ticker:

    def __init__(self, fps, callback):
        self.interval_ms = 1000 / fps
        self.callback = callback
        self.t = 0
        self.step = 1
        self.interval_handle = None

    def is_running(self):
        return self.interval_handle != None

    def start(self, fps, callback):
        if self.is_running():
            return

        def function():
            self.callback(self.t)
            self.t += self.step

        self.interval_handle = self.set_interval(function, self.interval_ms)

    def stop(self):
        if not self.is_running():
            return

        self.clear_interval(self.interval_handle)
        self.interval_handle = None

    def set_t(self, t):
        self.t = t

    def set_step(self, step):
        self.step = step

    def reverse_step_direction(self):
        self.step = -self.step
