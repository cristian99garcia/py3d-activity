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

import math

import gi
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk


class Point2D:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Point3D:
    x = 0
    y = 0
    z = 0

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class AffineMatrix:

    def __init__(self, e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11):
        self.e0  = e0
        self.e1  = e1
        self.e2  = e2
        self.e3  = e3
        self.e4  = e4
        self.e5  = e5
        self.e6  = e6
        self.e7  = e7
        self.e8  = e8
        self.e9  = e9
        self.e10 = e10
        self.e11 = e11


class Transform:

    def __init__(self):
        self.m = None
        self.reset()

    def reset(self):
        self.m = Py3D.make_identity_affine()

    def rotate_x(self, theta):
        self.m = Py3D.multiply_affine(Py3D.make_rotate_affine_x(theta), self.m)

    def rotate_x_pre(self, theta):
        self.m = Py3D.multiply_affine(self.m, Py3D.make_rotate_affine_x(theta))

    def rotate_y(self, theta):
        self.m = Py3D.multiply_affine(Py3D.make_rotate_affine_y(theta), self.m)

    def rotate_y_pre(self, theta):
        self.m = Py3D.multiply_affine(self.m, Py3D.make_rotate_affine_y(theta))

    def rotate_z(self, theta):
        self.m = Py3D.multiply_affine(Py3D.make_rotate_affine_z(theta), self.m)

    def rotate_z_pre(self, theta):
        self.m = Py3D.multiply_affine(self.m, Py3D.make_rotate_affine_z(theta))

    def translate(self, dx, dy, dz):
        self.m = Py3D.multiply_affine(Py3D.make_translate_affine(dx, dy, dz), self.m)

    def translate_pre(self, dx, dy, dz):
        self.m = Py3D.multiply_affine(self.m, Py3D.make_translate_affine(dx, dy, dz))

    def scale(self, sx, sy, sz):
        self.m = Py3D.multiply_affine(Py3D.make_scale_affine(sx, sy, sz), self.m)

    def scale_pre(self, sx, sy, sz):
        self.m = Py3D.multiply_affine(self.m, Py3D.make_scale_affine(sx, sy, sz))

    def transform_point(self, p):
        return Py3D.transform_point(self.m, p)

    def mult_transform(self, t):
        self.m = Py3D.multiply_affine(self.m, t.m)

    def set_dcm(self, u, v, w):
        m = self.m
        m.e0 = u.x
        m.e4 = u.y
        m.e8 = u.z

        m.e1 = v.x
        m.e5 = v.y
        m.e9 = v.z

        m.e2 = w.x
        m.e6 = w.y
        m.e10 = w.z

    def dup(self):
        tm = Transform()
        tm.m = sup_affine(self.m)

        return tm


class RGBA:

    def __init__(self, r=0, g=0, b=0, a=1):
        self.set_rgba(r, g, b, a)

    def set_rgba(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def set_rgb(self, r, g, b):
        self.set_rgba(r, g, b, 1)

    def invert(self):
        self.r = 1 - self.r
        self.g = 1 - self.g
        self.b = 1 - self.b

    def dup(self):
        return RGBA(self.r, self.g, self.b, self.a)


class QuadFace:

    def __init__(self, i0, i1, i2, i3):
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3

        self.centroid = None
        self.normal1 = None
        self.normal2 = None

    def is_triangle(self):
        return self.i3 == None

    def set_quad(self, i0, i1, i2, i3):
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3

    def set_triangle(self, i0, i1, i2):
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2
        self.i3 = None


class Shape:

    def __init__(self):
        self.vertices = []
        self.quads = []


class Curve:

    def __init__(self, ep, c0, c1):
        self.ep = ep    # End point.
        self.c0 = c0    # Control point.
        self.c1 = c1    # Control point.

    def is_quadratic(self):
        return (self.c1 == None)

    def set_quadratic(self, ep, c0):
        self.ep = ep
        self.c0 = c0
        self.c1 = None

    def set_cubic(self, ep, c0, c1):
        self.ep = ep
        self.c0 = c0
        self.c1 = c1


class Path:

    def __init__(self):
        self.points = []
        self.curves = []
        self.starting_point = None


class Camera:

    def __init__(self):
        self.transform = Transform()
        self.focal_length = 1


class TextureInfo:

    def __init__(self):
        self.image = None
        self.u0 = None
        self.v0 = None
        self.u1 = None
        self.v1 = None
        self.u2 = None
        self.v2 = None
        self.u3 = None
        self.v3 = None


class Renderer:

    def __init__(self):
        self.perform_z_sorting = True
        self.draw_overdraw = True
        self.draw_backfaces = False

        self.texture = None
        self.fill_rgba = RGBA(1, 0, 0, 1)

        self.stroke_rgba = None

        self.normal1_rgba = None
        self.normal2_rgba = None

        self.context = None
        self.camera = Camera()
        self.transform = Transform()

        self.transform_stack = []
        self.quad_callback = None

        self.width = 0
        self.height = 0
        self.scale = 0
        self.xoff = 0

        self.buffered_quads = None
        self.empty_buffer()

    def append_transform(self):
        self.transform_stack.append(self.transform.dup())

    def pop_transform(self):
        self.transform = self.transform_stack.pop()

    def empty_buffer(self):
        self.buffered_quads = []

    def project_point_to_canvas(self, p):
        if hasattr(p, "z"):
            v = self.camera.focal_length / -p.z

        else:
            v = 0

        scale = self.scale
        return Point2D(x=p.x * v * scale + self.xoff, y=p.y * v * -scale + scale)

    def project_points_to_canvas(self, ps):
        out = []
        for p in ps:
            out.append(self.project_point_to_canvas(p))

        return out

    def project_quad_face_to_canvas_ip(self, qf):
        qf.i0 = self.project_point_to_canvas(qf.i0)
        qf.i1 = self.project_point_to_canvas(qf.i1)
        qf.i2 = self.project_point_to_canvas(qf.i2)
        if not qf.is_triangle():
            qf.i3 = self.project_point_to_canvas(qf.i3)

        return qf

    def buffer_shape(self, shape, color=None):
        draw_backfaces = self.draw_backfaces
        quad_callback = self.quad_callback

        t = Py3D.multiply_affine(self.camera.transform.m, self.transform.m)
        tn = Py3D.trans_adjoint(t)

        world_vertices = Py3D.transform_points(t, shape.vertices)
        quads = shape.quads

        for j in range(0, len(shape.quads)):
            qf = quads[j]

            if quad_callback is not None and quad_callback(qf, j, shape):
                continue

            centroid = Py3D.transform_point(t, qf.centroid)

            if centroid.z >= -1:
                continue

            n1 = Py3D.unit_vector_3d(Py3D.transform_point(tn, qf.normal1))
            n2 = Py3D.transform_point(tn, qf.normal2)

            if not draw_backfaces and Py3D.dot_product_3d(centroid, n1) > 0 and Py3D.dot_product_3d(centroid, n2) > 0:
                continue

            intensity = Py3D.dot_product_3d(Py3D.g_z_axis_vector, n1)
            if intensity < 0:
                intensity = 0

            world_qf = None

            if qf.is_triangle():
                world_qf = QuadFace(
                    world_vertices[qf.i0],
                    world_vertices[qf.i1],
                    world_vertices[qf.i2],
                    None
                )

            else:
                world_qf = QuadFace(
                    world_vertices[qf.i0],
                    world_vertices[qf.i1],
                    world_vertices[qf.i2],
                    world_vertices[qf.i3]
                )

            world_qf.centroid = centroid
            world_qf.normal1 = n1
            world_qf.normal2 = n2

            fill_rgba = self.fill_rgba if color is None else color

            obj = {
                "qf": world_qf,
                "intensity": intensity,
                "draw_overdraw": self.draw_overdraw,
                "texture": self.texture,
                "fill_rgba": fill_rgba,
                "stroke_rgba": self.stroke_rgba,
                "normal1_rgba": self.normal1_rgba,
                "normal2_rgba": self.normal2_rgba
            }

            self.buffered_quads.append(obj)

    def draw_background(self):
        if self.context is not None:
            self.context.rectangle(0, 0, self.width, self.height)
            self.context.fill()

    def draw_buffer(self):
        context = self.context

        all_quads = self.buffered_quads
        num_quads = len(all_quads)

        if self.perform_z_sorting:
            all_quads.sort(Py3D.z_sorter)

        for obj in all_quads:
            qf = obj["qf"]

            self.project_quad_face_to_canvas_ip(qf)

            is_triangle = qf.is_triangle()

            if obj["draw_overdraw"]:
                Py3D.push_points_2s_ip(qf.i0, qf.i1)
                Py3D.push_points_2s_ip(qf.i1, qf.i2)
                if is_triangle:
                    Py3D.push_points_2s_ip(qf.i2, qf.i0)

                else:
                    Py3D.push_points_2s_ip(qf.i2, qf.i3)
                    Py3D.push_points_2s_ip(qf.i3, qf.i0)

            context.new_path()
            context.move_to(qf.i0.x, qf.i0.y)
            context.line_to(qf.i1.x, qf.i1.y)
            context.line_to(qf.i2.x, qf.i2.y)
            if not is_triangle:
                context.line_to(qf.i3.x, qf.i3.y)

            frgba = obj["fill_rgba"]
            if frgba != None:
                iy = obj["intensity"] 
                context.set_source_rgba(frgba.r * iy, frgba.g * iy, frgba.b * iy, frgba.a)
                context.fill()

            texture = obj["texture"]
            if texture != None:
                draw_canvas_textured_triangle(context, texture.image,
                    qf.i0.x, qf.i0.y, qf.i1.x, qf.i1.y, qf.i2.x, qf.i2.y,
                    texture.u0, texture.v0, texture.u1, texture.v1,
                    texture.u2, texture.v2)
                if not is_triangle:
                    draw_canvas_textured_triangle(context, texture.image,
                        qf.i0.x, qf.i0.y, qf.i2.x, qf.i2.y, qf.i3.x, qf.i3.y,
                        texture.u0, texture.v0, texture.u2, texture.v2,
                        texture.u3, texture.v3)

            srgba = obj["stroke_rgba"]
            if srgba != None:
                context.close_path()
                context.set_source_rgba(srgba.r, srgba.g, srgba.b, srgba.a)
                context.stroke()

            n1r = obj["normal1_rgba"]
            n2r = obj["normal2_rgba"]
            if n1r != None:
                context.set_source_rgba(n1r.r, n1r.g, n1r.b, n1r.a)
                screen_centroid = self.project_point_to_canvas(qf.centroid)
                screen_point = self.project_point_to_canvas(add_points_3d(qf.centroid, Py3D.unit_vector_3d(qf.normal1)))
                context.new_path()
                context.move_to(screen_centroid.x, screen_centroid.y)
                context.line_to(screen_point.x, screen_point.y)
                context.stroke()

            if n2r != None:
                context.set_source_rgba(n2r.r, n2r.g, n2r.b, n2r.a)
                screen_centroid = self.project_point_to_canvas(qf.centroid)
                screen_point = self.project_point_to_canvas(add_points_3d(qf.centroid, Py3D.unit_vector_3d(qf.normal2)))
                context.new_path()
                context.move_to(screen_centroid.x, screen_centroid.y)
                context.line_to(screen_point.x, screen_point.y)
                context.stroke()

        return num_quads

    def draw_path(self, path, opts):
        context = self.context
        opts = opts or { }
        t = Py3D.multiply_affine(self.camera.transform.m, self.transform.m)
        screen_points = self.project_points_to_canvas(transform_points(t, path.points))

        start_point = self.project_point_to_canvas(transform_point(t, Point3D())) if path.starting_point == None else screen_points[path.starting_point]
        context.new_path()
        context.move_to(start_point.x, start_point.y)

        for curve in path.curves:
            if curve.is_quadratic():
                c0 = screen_points[curve.c0]
                ep = screen_points[curve.ep]
                context.curve_to(start_point.x, start_point.y, c0.x, c0.y, ep.x, ep.y)

            else:
                c0 = screen_points[curve.c0]
                c1 = screen_points[curve.c1]
                ep = screen_points[curve.ep]
                context.curve_to(start_point.x, start_point.y, c0.x, c0.y, ep.x, ep.y)

        if opts.fill:
            context.fill()
        
        else:
            context.stroke()


class Py3D:

    @classmethod
    def cross_product(self, a, b):
        # a1b2 - a2b1, a2b0 - a0b2, a0b1 - a1b0
        return Point3D(
            x=a.y * b.z - a.z * b.y,
            y=a.z * b.x - a.x * b.z,
            z=a.x * b.y - a.y * b.x
        )

    @classmethod
    def dot_product_2d(self, a, b):
        return a.x * b.x + a.y * b.y

    @classmethod
    def dot_product_3d(self, a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    # a - b
    @classmethod
    def sub_points_2d(self, a, b):
        return Point2D(x=a.x - b.x, y=a.y - b.y)

    @classmethod
    def sub_points_3d(self, a, b):
        return Point3D(x=a.x - b.x, y=a.y - b.y, z=a.z - b.z)

    # c = a - b
    @classmethod
    def sub_points_2d_ip(self, c, a, b):
        c.x = a.x - b.x
        c.y = a.y - b.y
        return c

    @classmethod
    def sub_points_3d_ip(self, c, a, b):
        c.x = a.x - b.x
        c.y = a.y - b.y
        c.z = a.z - b.z
        return c

    # a + b
    @classmethod
    def add_points_2d(self, a, b):
        return Point2D(x=a.x + b.x, y=a.y + b.y)

    @classmethod
    def add_points_3d(self, a, b):
        return Point3D(x=a.x + b.x, y=a.y + b.y, z=a.z + b.z)

    # c = a + b
    @classmethod
    def add_points_2d_ip(self, c, a, b):
        c.x = a.x + b.x
        c.y = a.y + b.y
        return c

    @classmethod
    def add_points_3d_ip(self, c, a, b):
        c.x = a.x + b.x
        c.y = a.y + b.y
        c.z = a.z + b.z
        return c

    # a * s
    @classmethod
    def mul_point_2d(self, a, s):
        return Point2D(x=a.x * s, y=a.y * s)

    @classmethod
    def mul_point_3d(self, a, s):
        return Point3D(x=a.x * s, y=a.y * s, z=a.z * s)

    # |a|
    @classmethod
    def vec_mag_2d(self, a):
        ax = a.x; ay = a.y
        return math.sqrt(ax * ax + ay * ay)

    @classmethod
    def vec_mag_3d(self, a):
        ax = a.x; ay = a.y; az = a.z
        return math.sqrt(ax * ax + ay * ay + az * az)

    # a / |a|
    @classmethod
    def unit_vector_2d(self, a):
        return Py3D.mul_point_2d(a, 1 / Py3D.vec_mag_2d(a))

    @classmethod
    def unit_vector_3d(self, a):
        return Py3D.mul_point_3d(a, 1 / Py3D.vec_mag_3d(a))

    @classmethod
    def linear_interpolate(self, a, b, d):
        return (b - a) * d + a

    @classmethod
    def linear_interpolate_points_3d(self, a, b, d):
        return Point3D(
            x=(b.x - a.x) * d + a.x,
            y=(b.y - a.y) * d + a.y,
            z=(b.z - a.z) * d + a.z
        )

    @classmethod
    def multiply_affine(self, a, b):
        a0 = a.e0; a1 = a.e1; a2 = a.e2; a3 = a.e3; a4 = a.e4; a5 = a.e5
        a6 = a.e6; a7 = a.e7; a8 = a.e8; a9 = a.e9; a10 = a.e10; a11 = a.e11
        b0 = b.e0; b1 = b.e1; b2 = b.e2; b3 = b.e3; b4 = b.e4; b5 = b.e5
        b6 = b.e6; b7 = b.e7; b8 = b.e8; b9 = b.e9; b10 = b.e10; b11 = b.e11

        return AffineMatrix(
            a0 * b0 + a1 * b4 + a2 * b8,
            a0 * b1 + a1 * b5 + a2 * b9,
            a0 * b2 + a1 * b6 + a2 * b10,
            a0 * b3 + a1 * b7 + a2 * b11 + a3,
            a4 * b0 + a5 * b4 + a6 * b8,
            a4 * b1 + a5 * b5 + a6 * b9,
            a4 * b2 + a5 * b6 + a6 * b10,
            a4 * b3 + a5 * b7 + a6 * b11 + a7,
            a8 * b0 + a9 * b4 + a10 * b8,
            a8 * b1 + a9 * b5 + a10 * b9,
            a8 * b2 + a9 * b6 + a10 * b10,
            a8 * b3 + a9 * b7 + a10 * b11 + a11
        )

    @classmethod
    def make_identity_affine(self):
        return AffineMatrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0
        )

    @classmethod
    def make_rotate_affine_x(self, theta):
        s = math.sin(theta)
        c = math.cos(theta)
        return AffineMatrix(
            1, 0,  0, 0,
            0, c, -s, 0,
            0, s,  c, 0
        )

    @classmethod
    def make_rotate_affine_y(self, theta):
        s = math.sin(theta)
        c = math.cos(theta)
        return AffineMatrix(
             c, 0, s, 0,
             0, 1, 0, 0,
            -s, 0, c, 0
        )

    @classmethod
    def make_rotate_affine_z(self, theta):
        s = math.sin(theta)
        c = math.cos(theta)
        return AffineMatrix(
            c, -s, 0, 0,
            s,  c, 0, 0,
            0,  0, 1, 0
        )

    @classmethod
    def make_translate_affine(self, dx, dy, dz):
        return AffineMatrix(
            1, 0, 0, dx,
            0, 1, 0, dy,
            0, 0, 1, dz
        )

    @classmethod
    def make_scale_affine(self, sx, sy, sz):
        return AffineMatrix(
             sx, 0,  0, 0,
             0, sy,  0, 0,
             0,  0, sz, 0
        )

    # Return a copy of the affine matrix |m|.
    @classmethod
    def sup_affine(self, m):
        return AffineMatrix(
            m.e0, m.e1, m.e2, m.e3,
            m.e4, m.e5, m.e6, m.e7,
            m.e8, m.e9, m.e10, m.e11
        )

    @classmethod
    def trans_adjoint(self, a):
        a0 = a.e0; a1 = a.e1; a2 = a.e2; a4 = a.e4; a5 = a.e5
        a6 = a.e6; a8 = a.e8; a9 = a.e9; a10 = a.e10
        return AffineMatrix(
            a10 * a5 - a6 * a9,
            a6 * a8 - a4 * a10,
            a4 * a9 - a8 * a5,
            0,
            a2 * a9 - a10 * a1,
            a10 * a0 - a2 * a8,
            a8 * a1 - a0 * a9,
            0,
            a6 * a1 - a2 * a5,
            a4 * a2 - a6 * a0,
            a0 * a5 - a4 * a1,
            0
        )

    @classmethod
    def transform_point(self, t, p):
        return Point3D(
            x=t.e0 * p.x + t.e1 * p.y + t.e2  * p.z + t.e3,
            y=t.e4 * p.x + t.e5 * p.y + t.e6  * p.z + t.e7,
            z=t.e8 * p.x + t.e9 * p.y + t.e10 * p.z + t.e11
        )

    @classmethod
    def transform_points(self, t, ps):
        out = []
        for p in ps:
            out.append(Py3D.transform_point(t, p))

        return out

    @classmethod
    def average_points(self, ps):
        avg = Point3D(x=0, y=0, z=0)
        for p in ps:
            avg.x += p.x
            avg.y += p.y
            avg.z += p.z

        f = 1 / len(ps)

        avg.x *= f
        avg.y *= f
        avg.z *= f

        return avg

    @classmethod
    def push_points_2s_ip(self, a, b):
        vec = Py3D.unit_vector_2d(Py3D.sub_points_2d(b, a))
        Py3D.add_points_2d_ip(b, b, vec)
        Py3D.sub_points_2d_ip(a, a, vec)

    @classmethod
    def draw_canvas_textured_triangle(self, context, im, x0, y0, x1, y1, x2, y2, sx0, sy0, sx1, sy1, sx2, sy2):
        context.save()

        # Clip the output to the on-screen triangle boundaries.
        context.new_path()
        context.move_to(x0, y0)
        context.line_to(x1, y1)
        context.line_to(x2, y2)
        context.close_path()
        context.clip()

        denom = \
                sx0 * (sy2 - sy1) - \
                sx1 * sy2 + \
                sx2 * sy1 + \
                (sx1 - sx2) * sy0

        m11 = - (
                sy0 * (x2 - x1) - \
                sy1 * x2 + \
                sy2 * x1 + \
                (sy1 - sy2) * x0) / denom
        m12 = (
                sy1 * y2 + \
                sy0 * (y1 - y2) - \
                sy2 * y1 + \
                (sy2 - sy1) * y0) / denom
        m21 = (
                sx0 * (x2 - x1) - \
                sx1 * x2 + \
                sx2 * x1 + \
                (sx1 - sx2) * x0) / denom
        m22 = - (
                sx1 * y2 + \
                sx0 * (y1 - y2) - \
                sx2 * y1 + \
                (sx2 - sx1) * y0) / denom
        dx = (
                sx0 * (sy2 * x1 - sy1 * x2) + \
                sy0 * (sx1 * x2 - sx2 * x1) + \
                (sx2 * sy1 - sx1 * sy2) * x0) / denom
        dy = (
                sx0 * (sy2 * y1 - sy1 * y2) + \
                sy0 * (sx1 * y2 - sx2 * y1) + \
                (sx2 * sy1 - sx1 * sy2) * y0) / denom

        context.transform(m11, m12, m21, m22, dx, dy)

        Gdk.cairo_set_source_pixbuf(context, im, 0, 0)
        context.paint()
        context.restore()

    g_z_axis_vector = Point3D(z=1)

    @classmethod
    def z_sorter(self, x, y):
        return int(x["qf"].centroid.z - y["qf"].centroid.z)


class ShapeUtils:

    k2PI = math.pi * 2

    @classmethod
    def average_points2(self, a, b):
        return Point3D(
            x=(a.x + b.x) * 0.5,
            y=(a.y + b.y) * 0.5,
            z=(a.z + b.z) * 0.5
        )

    @classmethod
    def rebuild_meta(self, shape):
        quads = shape.quads
        vertices = shape.vertices

        for qf in quads:
            centroid = None
            n1 = n2 = None

            vert0 = vertices[qf.i0]
            vert1 = vertices[qf.i1]
            vert2 = vertices[qf.i2]
            vec01 = Py3D.sub_points_3d(vert1, vert0)
            vec02 = Py3D.sub_points_3d(vert2, vert0)
            n1 = Py3D.cross_product(vec01, vec02)

            if qf.is_triangle():
                n2 = n1
                centroid = Py3D.average_points([vert0, vert1, vert2])

            else:
                vert3 = vertices[qf.i3]
                vec03 = Py3D.sub_points_3d(vert3, vert0)
                n2 = Py3D.cross_product(vec02, vec03)
                centroid = Py3D.average_points([vert0, vert1, vert2, vert3])

            qf.centroid = centroid
            qf.normal1 = n1
            qf.normal2 = n2

        return shape

    @classmethod
    def triangulate(self, shape):
        for qf in shape.quads:
            if qf.is_triangle():
                continue

            newtri = QuadFace(qf.i0, qf.i2, qf.i3, None)
            qf.i3 = None
            shape.quads.append(newtri)

        ShapeUtils.rebuild_meta(shape)
        return shape

    @classmethod
    def for_each_face(self, shape, func):
        for i in range(0, len(shape.quads)):
            if func(shape.quads[i], i, shape):
                break

        return shape

    @classmethod
    def for_each_vertex(self, shape, func):
        for i in range(0, len(shape.vertices)):
            if func(shape.vertices[i], i, shape):
                break

        return shape

    @classmethod
    def make_plane(self, p1, p2, p3, p4):
        s = Shape()
        s.vertices = [p1, p2, p3, p4]
        s.quads = [QuadFace(0, 1, 2, 3)]
        ShapeUtils.rebuild_meta(s)
        return s

    @classmethod
    def make_box(self, w, h, d):
        s = Shape()
        s.vertices = [
            Point3D(x= w, y= h, z=-d),    # 0
            Point3D(x= w, y= h, z= d),    # 1
            Point3D(x= w, y=-h, z= d),    # 2
            Point3D(x= w, y=-h, z=-d),    # 3
            Point3D(x=-w, y= h, z=-d),    # 4
            Point3D(x=-w, y= h, z= d),    # 5
            Point3D(x=-w, y=-h, z= d),    # 6
            Point3D(x=-w, y=-h, z=-d)     # 7
        ]

        #   4 --- 0
        #  /|    /|         +y
        # 5 --- 1 |            |__ +x
        # | 7---|-3           /
        # |/    |/         +z
        # 6 --- 2

        s.quads = [
            QuadFace(0, 1, 2, 3),    # Right side
            QuadFace(1, 5, 6, 2),    # Front side
            QuadFace(5, 4, 7, 6),    # Left side
            QuadFace(4, 0, 3, 7),    # Back side
            QuadFace(0, 4, 5, 1),    # Top side
            QuadFace(2, 6, 7, 3)     # Bottom side
        ]

        ShapeUtils.rebuild_meta(s)

        return s

    @classmethod
    def make_cube(self, whd):
        return ShapeUtils.make_box(whd, whd, whd)

    @classmethod
    def make_box_with_hole(self, w, h, d, hw, hh):
        s = Shape()
        s.vertices = [
            Point3D(x= w, y= h, z=-d),    # 0
            Point3D(x= w, y= h, z= d),    # 1
            Point3D(x= w, y=-h, z= d),    # 2
            Point3D(x= w, y=-h, z=-d),    # 3
            Point3D(x=-w, y= h, z=-d),    # 4
            Point3D(x=-w, y= h, z= d),    # 5
            Point3D(x=-w, y=-h, z= d),    # 6
            Point3D(x=-w, y=-h, z=-d),    # 7

            # The front points ...
            Point3D(x=hw, y=  h, z=d),    # 8
            Point3D(x= w, y= hh, z=d),    # 9
            Point3D(x=hw, y= hh, z=d),    # 10
            Point3D(x=hw, y= -h, z=d),    # 11
            Point3D(x= w, y=-hh, z=d),    # 12
            Point3D(x=hw, y=-hh, z=d),    # 13

            Point3D(x=-hw, y=  h, z=d),    # 14
            Point3D(x= -w, y= hh, z=d),    # 15
            Point3D(x=-hw, y= hh, z=d),    # 16
            Point3D(x=-hw, y= -h, z=d),    # 17
            Point3D(x= -w, y=-hh, z=d),    # 18
            Point3D(x=-hw, y=-hh, z=d),    # 19

            # The back points ...
            Point3D(x=hw, y=  h, z=-d),    # 20
            Point3D(x= w, y= hh, z=-d),    # 21
            Point3D(x=hw, y= hh, z=-d),    # 22
            Point3D(x=hw, y= -h, z=-d),    # 23
            Point3D(x= w, y=-hh, z=-d),    # 24
            Point3D(x=hw, y=-hh, z=-d),    # 25

            Point3D(x=-hw, y=  h, z=-d),    # 26
            Point3D(x=-w,  y= hh, z=-d),    # 27
            Point3D(x=-hw, y= hh, z=-d),    # 28
            Point3D(x=-hw, y= -h, z=-d),    # 29
            Point3D(x=-w,  y=-hh, z=-d),    # 30
            Point3D(x=-hw, y=-hh, z=-d)     # 31
        ]

        #                        Front               Back (looking from front)
        #    4 -   - 0           05  14  08  01      04  26  20  00
        #   /|      /|
        #  5 -   - 1 |           15  16--10  09      27  28--22  21
        #  | 7 -   |-3               |////|              |////|
        #  |/      |/            18  19--13  12      30  31--25  24
        #  6 -   - 2
        #                        06  17  11  02      07  29  23  03

        s.quads = [
            # Front side
            QuadFace( 1,  8, 10,  9),
            QuadFace( 8, 14, 16, 10),
            QuadFace(14,  5, 15, 16),
            QuadFace(16, 15, 18, 19),
            QuadFace(19, 18,  6, 17),
            QuadFace(13, 19, 17, 11),
            QuadFace(12, 13, 11,  2),
            QuadFace( 9, 10, 13, 12),
            # Back side
            QuadFace( 4, 26, 28, 27),
            QuadFace(26, 20, 22, 28),
            QuadFace(20,  0, 21, 22),
            QuadFace(22, 21, 24, 25),
            QuadFace(25, 24,  3, 23),
            QuadFace(31, 25, 23, 29),
            QuadFace(30, 31, 29,  7),
            QuadFace(27, 28, 31, 30),
            # The hole
            QuadFace(10, 16, 28, 22),
            QuadFace(19, 31, 28, 16),
            QuadFace(13, 25, 31, 19),
            QuadFace(10, 22, 25, 13),
            # Bottom side
            QuadFace( 6,  7, 29, 17),
            QuadFace(17, 29, 23, 11),
            QuadFace(11, 23,  3,  2),
            # Right side
            QuadFace( 1,  9, 21,  0),
            QuadFace( 9, 12, 24, 21),
            QuadFace(12,  2,  3, 24),
            # Left side
            QuadFace( 5,  4, 27, 15),
            QuadFace(15, 27, 30, 18),
            QuadFace(18, 30,  7,  6),
            # Top side
            QuadFace(14, 26,  4,  5),
            QuadFace( 8, 20, 26, 14),
            QuadFace( 1,  0, 20,  8)
        ]

        ShapeUtils.rebuild_meta(s)
        return s

    @classmethod
    def make_spherical_shape(self, f, tess_x, tess_y):
        vertices = []
        quads = []

        theta_step = math.pi / (tess_y + 1)
        phi_step = (ShapeUtils.k2PI) / tess_x

        theta = theta_step
        for i in range(0, tess_y):
            for j in range(0, tess_x):
                vertices.append(f(theta, phi_step * j))

            theta += theta_step

        for i in range(0, tess_y - 1):
            stride = i * tess_x
            for j in range(0, tess_x):
                n = (j + 1) % tess_x
                quads.append(QuadFace(
                    stride + j,
                    stride + tess_x + j,
                    stride + tess_x + n,
                    stride + n
                ))

        last_row = len(vertices) - tess_x
        top_p_i = len(vertices)
        bot_p_i = top_p_i + 1
        vertices.append(f(0, 0))
        vertices.append(f(math.pi, 0))

        for i in range(0, tess_x):
            quads.append(QuadFace(
                top_p_i,
                i,
                ((i + 1) % tess_x),
                None
            ))

            quads.append(QuadFace(
                bot_p_i,
                last_row + ((i + 2) % tess_x),
                last_row + ((i + 1) % tess_x),
                None
            ))

        s = Shape()
        s.vertices = vertices
        s.quads = quads
        ShapeUtils.rebuild_meta(s)
        return s

    @classmethod
    def make_octahedron(self, wdh):
        s = Shape()
        s.vertices = [
            Point3D(x=-wdh, y= 0,   z= 0  ),    # 0
            Point3D(x= 0,   y= 0,   z= wdh),    # 1
            Point3D(x= wdh, y= 0,   z= 0  ),    # 2
            Point3D(x= 0,   y= 0,   z=-wdh),    # 3
            Point3D(x= 0,   y= wdh, z= 0  ),    # 4
            Point3D(x= 0,   y=-wdh, z= 0  )     # 5
        ]

        quads = [None] * 8
        for i in range(0, 4):
            i2 = (i + 1) & 3
            quads[i * 2]     = QuadFace(4, i, i2, None)
            quads[i * 2 + 1] = QuadFace(i, 5, i2, None)

        s.quads = quads
        ShapeUtils.rebuild_meta(s)
        return s

    @classmethod
    def make_sphere(self, r, tess_x, tess_y):
        def make_point(theta, phi):
            return Point3D(
                x=r * math.sin(theta) * math.sin(phi),
                y=r * math.cos(theta),
                z=r * math.sin(theta) * math.cos(phi)
            )

        return ShapeUtils.make_spherical_shape(make_point, tess_x, tess_y)

    @classmethod
    def average_smooth(self, shape, m):
        if m is None:
            m = 1

        vertices = shape.vertices
        psl = len(vertices)
        new_ps = [None] * psl

        connections = [None] * psl
        for i in range(0, psl):
            connections[i] = []

        for i in range(0, len(shape.quads)):
            qf = shape.quads[i]
            connections[qf.i0].append(i)
            connections[qf.i1].append(i)
            connections[qf.i2].append(i)
            if not qf.is_triangle():
                connections[qf.i3].append(i)

        for i in range(0, len(vertices)):
            cs = connections[i]
            avg = Point3D(x=0, y=0, z=0)

            for j in range(0, len(cs)):
                quad = shape.quads[cs[j]]
                p1 = vertices[quad.i0]
                p2 = vertices[quad.i1]
                p3 = vertices[quad.i2]
                p4 = vertices[quad.i3]
                avg.x += (p1.x + p2.x + p3.x + p4.x) / 4
                avg.y += (p1.y + p2.y + p3.y + p4.y) / 4
                avg.z += (p1.z + p2.z + p3.z + p4.z) / 4

            f = 1 / len(cs)
            avg.x *= f
            avg.y *= f
            avg.z *= f

            new_ps[i] = linear_interpolate_points_3d(vertices[i], avg, m)

        shape.vertices = new_ps
        ShapeUtils.rebuild_meta(shape)
        return shape

    @classmethod
    def array_map(self, arr, func):
        out = [None] * len(arr)
        for i in range(0, len(arr)):
            out[i] = func(arr[i], i, arr)

        return out

    @classmethod
    def linear_subdivide(self, shape):
        share_points = { }

        for quad in shape.quads:
            i0 = quad.i0
            i1 = quad.i1
            i2 = quad.i2
            i3 = quad.i3

            p0 = shape.vertices[i0]
            p1 = shape.vertices[i1]
            p2 = shape.vertices[i2]
            p3 = shape.vertices[i3]

            #  p0   p1      p0  n0  p1
            #           ->  n3  n4  n1
            #  p3   p2      p3  n2  p2

            ni = [
                [i0, i1].sort(),
                [i1, i2].sort(),
                [i2, i3].sort(),
                [i3, i0].sort(),
                [i0, i1, i2, i3].sort()
            ]

            for j in range(0, len(ni)):
                ps = ni[j]
                key = ps.join("-")
                centroid_index = share_points[key]
                if centroid_index is None:
                    centroid_index = len(shape.vertices)
                    s = shape
                    shape.vertices.append(Py3D.average_points(array_map(ps, lambda x: s.vertices[x])))
                    share_points[key] = centroid_index

                ni[j] = centroid_index

            q0 = QuadFace(   i0, ni[0], ni[4], ni[3])
            q1 = QuadFace(ni[0],    i1, ni[1], ni[4])
            q2 = QuadFace(ni[4], ni[1],    i2, ni[2])
            q3 = QuadFace(ni[3], ni[4], ni[2],    i3)

            shape.quads[i] = q0
            shape.quads.append(q1)
            shape.quads.append(q2)
            shape.quads.append(q3)

        ShapeUtils.rebuild_meta(shape)
        return shape

    @classmethod
    def linear_subdivide_tri(self, shape):
        num_tris = len(shape.quads)
        share_points = { }

        for i in range(0, num_tris):
            tri = shape.quads[i]

            i0 = tri.i0
            i1 = tri.i1
            i2 = tri.i2

            p0 = shape.vertices[i0]
            p1 = shape.vertices[i1]
            p2 = shape.vertices[i2]

            #     p0                 p0
            #              ->      n0  n2
            # p1      p2         p1  n1  p2

            ni = [
                [i0, i1].sort(),
                [i1, i2].sort(),
                [i2, i0].sort(),
            ]

            for j in range(0, len(ni)):
                ps = ni[j]
                key = ps.join("-")
                centroid_index = share_points[key]
                if centroid_index is None:
                    centroid_index = len(shape.vertices)
                    s = shape
                    shape.vertices.append(Py3D.average_points(array_map(ps, lambda x: s.vertices[x])))
                    share_points[key] = centroid_index

                ni[j] = centroid_index

            q0 = QuadFace(   i0, ni[0], ni[2], None)
            q1 = QuadFace(ni[0],    i1, ni[1], None)
            q2 = QuadFace(ni[2], ni[1],    i2, None)
            q3 = QuadFace(ni[0], ni[1], ni[2], None)

            shape.quads[i] = q0
            shape.quads.append(q1)
            shape.quads.append(q2)
            shape.quads.append(q3)

        ShapeUtils.rebuild_meta(shape)
        return shape

    @classmethod
    def explode_faces(self, shape):
        quads = shape.quads
        num_quads = len(quads)
        verts = shape.vertices
        new_verts = []
        for q in quads:
            pos = len(new_verts)
            new_verts.append(Point3D(x=verts[q.i0].x, y=verts[q.i0].y, z=verts[q.i0].z))
            new_verts.append(Point3D(x=verts[q.i1].x, y=verts[q.i1].y, z=verts[q.i1].z))
            new_verts.append(Point3D(x=verts[q.i2].x, y=verts[q.i2].y, z=verts[q.i2].z))
            q.i0 = pos
            q.i1 = pos + 1
            q.i2 = pos + 2
            if not q.is_triangle():
                new_verts.append(Point3D(x=verts[q.i3].x, y=verts[q.i3].y, z=verts[q.i3].z))
                q.i3 = pos + 3

        shape.vertices = new_verts
        return shape


class Extruder:

    def __init__(self):
        self.distance = 1.0
        self.count = 1
        self.selector = None
        self.select_all()

        self.scale =  Point3D(x=1, y=1, z=1)
        self.rotate = Point3D()

    def select_all(self):
        self.selector = lambda shape, vertex_index: True

    def selectCustom(self, select_func):
        self.selector = select_func

    def distance(self):
        return self.distance

    def set_distance(self, d):
        self.distance = d

    def set_count(self, c):
        self.count = c

    def extrude(self, shape):
        distance = self.distance()
        count = self.count

        rx = self.rotate.x
        ry = self.rotate.y
        rz = self.rotate.z
        sx = self.scale.x
        sy = self.scale.y
        sz = self.scale.z

        vertices = shape.vertices
        quads = shape.quads

        faces = []
        for i in range(0, len(quads)):
            if self.selector(shape, i):
                faces.append(i)

        for i in range(0, len(faces)):
            face_index = faces[i]
            qf = quads[face_index]
            original_cent = qf.centroid
            surface_normal = Py3D.unit_vector_3d(add_points_3d(qf.normal1, qf.normal2))
            is_triangle = qf.is_triangle()
            inner_normal0 = Py3D.sub_points_3d(vertices[qf.i0], original_cent)
            inner_normal1 = Py3D.sub_points_3d(vertices[qf.i1], original_cent)
            inner_normal2 = Py3D.sub_points_3d(vertices[qf.i2], original_cent)
            if not is_triangle:
                inner_normal3 = Py3D.sub_points_3d(vertices[qf.i3], original_cent)

            for z in range(0, count):
                m = (z + 1) / count

                t = Transform()
                t.rotate_x(rx * m)
                t.rotate_y(ry * m)
                t.rotate_z(rz * m)

                new_cent = add_points_3d(original_cent,mul_point_3d(t.transform_point(surface_normal), m * distance))
                t.scale_pre(linear_interpolate(1, sx, m),
                           linear_interpolate(1, sy, m),
                           linear_interpolate(1, sz, m))

                index_before = len(vertices)

                vertices.append(add_points_3d(new_cent, t.transform_point(inner_normal0)))
                vertices.append(add_points_3d(new_cent, t.transform_point(inner_normal1)))
                vertices.append(add_points_3d(new_cent, t.transform_point(inner_normal2)))
                if not is_triangle:
                    vertices.append(add_points_3d(new_cent, t.transform_point(inner_normal3)))

                quads.append(
                    QuadFace(qf.i1,
                             index_before + 1,
                             index_before,
                             qf.i0))

                quads.append(
                    QuadFace(qf.i2,
                             index_before + 2,
                             index_before + 1,
                             qf.i1))

                if is_triangle:
                    quads.append(QuadFace(
                            qf.i0,
                            index_before,
                            index_before + 2,
                            qf.i2))

                else:
                    quads.append(
                        QuadFace(qf.i3,
                                 index_before + 3,
                                 index_before + 2,
                                 qf.i2))

                    quads.append(
                        QuadFace(qf.i0,
                                 index_before,
                                 index_before + 3,
                                 qf.i3))

                qf.i0 = index_before
                qf.i1 = index_before + 1
                qf.i2 = index_before + 2
                if not is_triangle:
                    qf.i3 = index_before + 3

        ShapeUtils.rebuild_meta(shape)
