from manim import *

class VORDemo(ThreeDScene):
    def construct(self):

        def outerfunc(x):
            return x

        def innerfunc(x):
            return x**2

        skip = False
        axes = ThreeDAxes(x_range=[-0.5,1.5], y_range=[-3.5,1.5], z_range=[-2.5,2.5], tips=False,
                          x_length=6, y_length=7)
        outer = axes.plot_parametric_curve(lambda t: [t,outerfunc(t),0], t_range=[0,1,0.05], color=BLUE)
        inner = axes.plot_parametric_curve(lambda t: [t,innerfunc(t),0], t_range=[0,1,0.05], color=GREEN)
        x = 0.6  # x location of segment
        segment = Line(axes.c2p(x,innerfunc(x),0),axes.c2p(x,outerfunc(x),0))
        AOR = DashedLine(axes.c2p(-1,0,0),axes.c2p(2,0,0), color=RED)
        AORlabel = always_redraw(lambda: Tex(r"Axis of\\revolution", font_size=28, color=RED).next_to(AOR,0.5*LEFT))
        outerlabel = Tex(r"$y=x$",font_size=28,color=BLUE).move_to(axes.c2p(1,1.5,0))
        innerlabel = Tex(r"$y=x^2$", font_size=28, color=GREEN).move_to(axes.c2p(1, 0.5, 0))

        # set the stage
        self.next_section(skip_animations=skip)
        self.play(Succession(Create(axes),
                             FadeIn(inner,innerlabel),
                             FadeIn(outer,outerlabel),
                             Create(segment),
                             FadeIn(AOR,AORlabel)))
        self.wait(1)

        # move to 3D view
        self.next_section(skip_animations=skip)
        self.move_camera(phi=60*DEGREES, theta=-45*DEGREES, run_time=2)

        # first revolution: no trace
        self.next_section(skip_animations=skip)
        graphgrp = VGroup(outer,inner,segment)
        self.play(Rotating(graphgrp, axis=RIGHT, about_point=axes.c2p(0,0,0), angle=2*PI), run_time=3)
        self.wait(1)

        # second revolution: show washer
        self.next_section(skip_animations=skip)
        outerpath = TracedPath(segment.get_end)
        innerpath = TracedPath(segment.get_start)
        self.add(outerpath, innerpath)
        self.play(Rotating(graphgrp, axis=RIGHT, about_point=axes.c2p(0,0,0), angle=2*PI), run_time=3)
        self.play(FadeOut(outerpath,innerpath))

        #########################################################
        # helper functions for movement of washers along x axis #
        #########################################################
        # function draws a parametric circle in y/z plane to func(xval) from y = AOR aor, at x = xval, in color
        def getCircle(func, xval, color, aor):
            return ParametricFunction(lambda t: axes.c2p(xval,
                                                         (func(xval)-aor)*np.cos(t)+aor,
                                                         (func(xval)-aor)*np.sin(t)
                                                         ),
                                      t_range = [0,2*PI,0.1],
                                      color=color)

        def xMovement(aor, tempo=1):
            xval = ValueTracker(x)
            outerring = always_redraw(lambda: getCircle(outerfunc, xval.get_value(), BLUE, aor))
            innerring = always_redraw(lambda: getCircle(innerfunc, xval.get_value(), GREEN, aor))
            self.play(FadeIn(outerring, innerring))
            self.play(xval.animate.set_value(0), run_time=tempo)
            self.play(xval.animate.set_value(1), run_time=2*tempo)
            self.play(xval.animate.set_value(x), run_time=tempo)
            self.play(FadeOut(outerring, innerring))

        # End helper functions

        self.next_section(skip_animations=skip)
        xMovement(0,2)

        ################################################
        # helper functions to return and draw surfaces #
        ################################################

        def getSurface(func,opacity,color,resolution,aor):
            return Surface(lambda u,v: axes.c2p(u,(func(u)-aor)*np.cos(v)+aor,(func(u)-aor)*np.sin(v)),
                           u_range=[0,1], v_range=[0,2*PI],
                           resolution=resolution,
                           checkerboard_colors=[WHITE,color],
                           fill_opacity=opacity)

        def surfaceViz(aor):
            innersurf = getSurface(innerfunc,1,GREEN,10,aor)
            outersurf = getSurface(outerfunc,0.3,BLUE,10,aor)
            self.play(FadeIn(innersurf))
            self.wait()
            self.play(FadeIn(outersurf))
            self.wait()
            self.begin_ambient_camera_rotation(-PI/4)
            self.wait(2)
            self.stop_ambient_camera_rotation()
            self.wait()
            self.begin_ambient_camera_rotation(PI/4)
            self.wait(2)
            self.stop_ambient_camera_rotation()
            self.play(FadeOut(innersurf,outersurf))

        # End surface helper functions

        # first surface viz
        self.next_section(skip_animations=skip)
        surfaceViz(0)

        # shift AOR
        self.next_section(skip_animations=skip)
        newAOR = DashedLine(axes.c2p(-1,-1,0),axes.c2p(2,-1,0), color=RED)
        self.play(ReplacementTransform(AOR,newAOR))

        # third revolution: show larger washer
        newouterpath = TracedPath(segment.get_end)
        newinnerpath = TracedPath(segment.get_start)
        self.add(newouterpath, newinnerpath)
        self.next_section(skip_animations=skip)
        self.play(Rotating(graphgrp, axis=RIGHT, about_point=axes.c2p(0, -1, 0), angle=2*PI), run_time=3)
        self.play(FadeOut(newouterpath,newinnerpath))

        # second x movement (with larger washer)
        self.next_section(skip_animations=skip)
        xMovement(-1,2)
        self.wait(2)

        # second surface viz
        self.next_section(skip_animations=skip)
        surfaceViz(-1)