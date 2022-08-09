import math

import numpy as np
from manim import *

class CrossDemo(ThreeDScene):
    def construct(self):

        colors = color_gradient([BLUE, GREEN], 100)

        axes = ThreeDAxes(x_range=[-1,3,1], y_range=[-3,11,5], z_range=[-1,9,5]).add_coordinates()
        graph = axes.plot_parametric_curve(lambda t: np.array([t,np.exp(t),0]), t_range = [0,2,0.05])

        xlab = axes.get_x_axis_label("x")
        ylab = axes.get_y_axis_label("y")
        grp1 = VGroup(axes,graph)

        tracker = ValueTracker(1)
        segment = always_redraw(lambda: Line(axes.c2p(tracker.get_value(), 0, 0),
                                             axes.c2p(tracker.get_value(), np.exp(tracker.get_value()),0),
                                             color = colors[int(tracker.get_value()/2*99)]))

        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES)
        self.add(grp1, xlab, ylab, segment)
        self.wait()

        self.move_camera(phi=60*DEGREES, theta = -45*DEGREES, run_time=2)
        self.move_camera(zoom=0.75)
        self.wait()

        self.play(tracker.animate.set_value(0))

        #sides of square: (t,0,0) - (t,0,e^t) - (t,e^t,e^t), (t,e^t,0)
        sq1 = always_redraw(lambda: Line(axes.c2p(tracker.get_value(), 0, 0),
                                         axes.c2p(tracker.get_value(), 0, np.exp(tracker.get_value())),
                                         color = colors[int(tracker.get_value()/2*99)]))
        sq2 = always_redraw(lambda: Line(axes.c2p(tracker.get_value(), 0, np.exp(tracker.get_value())),
                                         axes.c2p(tracker.get_value(), np.exp(tracker.get_value()), np.exp(tracker.get_value())),
                                         color = colors[int(tracker.get_value()/2*99)]))
        sq3 = always_redraw(lambda: Line(axes.c2p(tracker.get_value(), np.exp(tracker.get_value()), np.exp(tracker.get_value())),
                                         axes.c2p(tracker.get_value(), np.exp(tracker.get_value()), 0),
                                         color = colors[int(tracker.get_value()/2*99)]))

        sides = VGroup(sq1,sq2,sq3)
        self.play(FadeIn(sides))
        self.play(tracker.animate.set_value(2), run_time = 2)
        self.wait()

        self.play(tracker.animate.set_value(1.5))

        label = axes.get_graph_label(graph, label=MathTex(r"y=e^x"))
        lab1 = always_redraw(lambda: MathTex(r"x").move_to(axes.c2p(tracker.get_value(), 0, 0)).shift(DOWN))
        lab2 = always_redraw(lambda: MathTex(r"e^x").move_to(axes.c2p(tracker.get_value(),np.exp(tracker.get_value())/2,0)).shift(RIGHT))
        self.play(FadeIn(label,lab1,lab2))
        self.wait()
        self.play(tracker.animate.set_value(0))
        self.play(FadeOut(lab1, lab2))

        delta = 0.005
        top = VGroup()
        face1 = VGroup()
        face2 = VGroup()
        for i in np.arange(0,2+delta,delta):
            start = axes.c2p(i, 0, np.exp(i))
            end = axes.c2p(i, np.exp(i), np.exp(i))
            base1 = axes.c2p(i, 0, 0)
            base2 = axes.c2p(i, np.exp(i), 0)
            color = colors[int(i / 2 * 99)]
            top.add(Line(start,end,color=color))
            face1.add(Line(base1,start,color=color))
            face2.add(Line(end,base2,color=color))

        topanim = []
        for line in top:
            topanim.append(FadeIn(line))

        face1anim = []
        for line in face1:
            face1anim.append(FadeIn(line))

        face2anim = []
        for line in face2:
            face2anim.append(FadeIn(line))


        self.play(LaggedStart(*topanim), run_time = 3)

        self.begin_ambient_camera_rotation(rate = PI/12)
        self.wait()
        self.play(tracker.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(tracker.animate.set_value(0), run_time = 3)
        self.play(LaggedStart(*face1anim, *face2anim), run_time=3)

        edge1 = axes.plot_parametric_curve(lambda t: np.array([t,np.exp(t),np.exp(t)]), t_range = [0,2,0.05])
        edge2 = axes.plot_parametric_curve(lambda t: np.array([t,0,np.exp(t)]), t_range = [0,2,0.05])
        self.play(FadeIn(edge1,edge2))
        self.wait(5)