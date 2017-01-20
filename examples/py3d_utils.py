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

from py3d import Path
from py3d import Point3D
from py3d import Curve


class Utils:

    @classmethod
    def make_line(self, p0, p1):
        path = Path()
        path.points = [
            Point3D(x=p0.x, y=p0.y, z=p0.z),
            Point3D(x=p1.x, y=p1.y, z=p1.z)
        ]

        path.curves = [Curve(1, 1, 1)]
        path.starting_point = 0
        return path

    @classmethod
    def make_circle(self):
        kKappa = 0.66666666666

        path = Path()
        path.points = [
            Point3D(x=0, y=kKappa,  z=0),
            Point3D(x=1, y=kKappa,  z=0),
            Point3D(x=1, y=0,       z=0),
            Point3D(x=1, y=-kKappa, z=0),
            Point3D(x=0, y=-kKappa, z=0),
            Point3D(x=0, y=0,       z=0)
        ]
        path.curves = [
            Pre3d.Curve(2, 0, 1),
            Pre3d.Curve(5, 3, 4)
        ]
        return path

    @classmethod
    def make_spiral(self, count):
        kKappa = 0.66666666666

        points = [ ]
        curves = [ ]

        z = 0
        p = 0
        for i in range(0, count):
            points.append(Point3D(x=0, y=kKappa,  z=z))
            z -= 0.05
            points.append(Point3D(x=1, y=kKappa,  z=z))
            points.append(Point3D(x=1, y=0,       z=z))
            points.append(Point3D(x=1, y=-kKappa, z=z))
            z -= 0.05
            points.append(Point3D(x=0, y=-kKappa, z=z))
            points.append(Point3D(x=0, y=0,       z=z))
            curves.append(Pre3d.Curve(p + 2, p + 0, p + 1))
            curves.append(Pre3d.Curve(p + 5, p + 3, p + 4))
            p += 6

        path = Path()
        path.points = points
        path.curves = curves
        return path

    @classmethod
    def fit_quadratic_to_points(self, p0, p1, p2):
        return Point3D(
                x=p1.x + p1.x - 0.5 * (p0.x + p2.x),
                y=p1.y + p1.y - 0.5 * (p0.y + p2.y),
                z=p1.z + p1.z - 0.5 * (p0.z + p2.z)
        )
