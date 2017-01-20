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

from gettext import gettext as _
from examples_chooser import ExamplesChooser

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GtkSource

from sugar3.activity import activity
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton


class Py3DActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.make_toolbar()

        self.paned = Gtk.HPaned()
        self.set_canvas(self.paned)

        self.make_view()

        self.canvasbox = Gtk.VBox()
        self.paned.pack2(self.canvasbox, False)

        self.area = Gtk.VBox()
        self.area.set_size_request(200, 1)
        self.canvasbox.pack_start(self.area, True, True, 0)

        self.show_all()

    def make_toolbar(self):
        toolbarbox = ToolbarBox()
        self.set_toolbar_box(toolbarbox)

        button = ActivityToolbarButton(self)
        toolbarbox.toolbar.insert(button, -1)

        toolbarbox.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        button = ToolButton("open-example")
        button.set_tooltip(_("Open an example"))
        button.connect("clicked", self._load_example_cb)
        toolbarbox.toolbar.insert(button, -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbarbox.toolbar.insert(separator, -1)

        button = StopButton(self)
        toolbarbox.toolbar.insert(button, -1)

    def make_view(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(200, 1)
        self.paned.pack1(scroll, False)

        self.view = GtkSource.View()
        self.view.set_editable(False)
        self.view.set_cursor_visible(False)
        self.view.set_show_line_numbers(True)
        scroll.add(self.view)

        manager = GtkSource.LanguageManager()
        buffer = GtkSource.Buffer()
        buffer.set_language(manager.get_language("python"))
        self.view.set_buffer(buffer)

    def _load_example_cb(self, button):
        chooser = ExamplesChooser()
        chooser.set_transient_for(self)
        chooser.connect("load-example", self._load_example)
        chooser.show_all()

    def _load_example(self, chooser, example):
        with open(example.file, "r") as file:
            self.view.get_buffer().set_text(file.read())

        self.canvasbox.remove(self.area)
        del self.area

        self.area = example.canvas()
        self.area.set_size_request(200, 1)
        self.canvasbox.pack_start(self.area, True, True, 0)

        self.show_all()
