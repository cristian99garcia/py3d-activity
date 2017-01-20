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

import os
from gettext import gettext as _

from examples.colorscube import ColorsCubesExample
from examples.rgba import RGBAExample
from examples.rubikscube import RubiksCubeExample
from examples.sphere import SphereExample

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton


class Example:

    def __init__(self, canvas, name, image, file):
        self.canvas = canvas
        self.name = name
        self.image = os.path.join(os.path.dirname(__file__), "screenshots", image)
        self.file = os.path.join(os.path.dirname(__file__), "examples", file)


class ExamplesChooser(Gtk.Dialog):

    __gsignals__ = {
        "load-example": (GObject.SIGNAL_RUN_LAST, None, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        Gtk.Dialog.__init__(self, flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)

        self.examples = []

        x, y = (Gdk.Screen.width() / 1.5, Gdk.Screen.height() / 1.5)
        self.set_size_request(x, y)

        self.make_toolbar()
        self.make_scroll()

        self.set_decorated(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)
        self.set_modal(True)

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#F3EEEE"))
        self.load_examples()
        self.show_all()

    def _destroy(self, widget):
        self.destroy()

    def make_toolbar(self):
        toolbox = ToolbarBox()
        self.vbox.pack_start(toolbox, False, False, 0)

        toolbar = toolbox.toolbar
        toolbox.set_size_request(-1, 35)

        item = Gtk.ToolItem()
        toolbar.insert(item, -1)

        label = Gtk.Label(_("Choose an example to open"))
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        item.add(label)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar.insert(separator, -1)

        close = ToolButton("entry-cancel")
        close.connect("clicked", self._destroy)
        toolbar.insert(close, -1)

    def make_scroll(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vbox.pack_start(scroll, True, True, 5)

        self.model = Gtk.ListStore(GdkPixbuf.Pixbuf, str, GObject.TYPE_PYOBJECT)

        view = Gtk.IconView()
        view.set_selection_mode(Gtk.SelectionMode.SINGLE)
        view.set_pixbuf_column(0)
        view.set_text_column(1)
        view.set_model(self.model)
        view.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse("gray"))
        view.connect("selection-changed", self._selection_changed_cb)
        scroll.add(view)

    def load_examples(self):
        canvas = [ColorsCubesExample, RGBAExample, RubiksCubeExample, SphereExample]
        images = ["colors_cube.png", "rgba.png", "rubiks_cube.png", "sphere.png"]
        names = [_("Colors Cube"), _("RGBA"), _("Rubiks Cube"), _("Sphere")]
        files = ["colorscube.py", "rgba.py", "rubikscube.py", "sphere.py"]

        for i in range(0, len(canvas)):
            example = Example(canvas[i], names[i], images[i], files[i])
            self.examples.append(example)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(example.image, 100, 100)
            self.model.append([pixbuf, example.name, example])

    def _selection_changed_cb(self, view):
        items = view.get_selected_items()
        if items != []:
            item = items[0]
            iter = self.model.get_iter(item)
            path = self.model.get(iter, 2)
            self.emit("load-example", path[0])

            self.destroy()
