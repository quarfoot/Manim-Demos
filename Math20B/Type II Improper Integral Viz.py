from manim import *


class ImproperIntegral2(Scene):
    def construct(self):
        # general variables
        skip = False
        texsize = 36
        ticklabelsize = 24

        def func1(t):
            return 1 / np.tan(t)

        ###########
        # Section 1 - Draw the initial area, see Type II improper integral

        # new objects
        self.camera.background_color = WHITE
        axes = Axes(x_range=[-.3, 3.6, PI / 2], y_range=[-18, 7, 5], y_length=8, tips=False)
        axes.set_color(BLACK)
        pi2label = MathTex(r"\frac{\pi}2", color=BLACK, font_size=ticklabelsize).next_to(axes.c2p(PI / 2, 0), DOWN)
        pilabel = MathTex(r"\pi", color=BLACK, font_size=ticklabelsize).next_to(axes.c2p(PI, 0), DR)
        graph = axes.plot(func1, x_range=[-.3, 3.6, 0.01], discontinuities=[0, PI], dt=0.05, color=PURE_BLUE)
        asymp1 = DashedLine(axes.c2p(0, -20), axes.c2p(0, 10), color=BLACK, stroke_width=8, dash_length=0.3,
                            dashed_ratio=0.7)
        asymp2 = DashedLine(axes.c2p(PI, -20), axes.c2p(PI, 10), color=BLACK, stroke_width=8, dash_length=0.3,
                            dashed_ratio=0.7)
        area = axes.get_area(graph, x_range=[PI / 2, PI - 0.01], color=PURE_RED)
        label = MathTex(r"y=\cot x", color=PURE_BLUE, font_size=28).next_to(axes.c2p(PI / 4, func1(PI / 4)), UP)
        improper = MathTex(r"\text{Goal:  Find }", r"\int_{\pi/2}^{\pi} \cot x \, dx", color=BLACK,
                           font_size=texsize).move_to(axes.c2p(1.55, -10))

        # animations
        self.next_section(skip_animations=skip)
        self.play(
            LaggedStart(
                *[Create(axes), FadeIn(graph, label, asymp1, asymp2, pi2label, pilabel), FadeIn(area), Write(improper)],
                lag_ratio=4))
        self.wait(3)

        ###########
        # Section 2 - Showing the proper integral and limit process

        # new features
        t = ValueTracker(2.3)  # start at a random-looking spot
        tdot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), 0), color=PURE_RED))
        tarea = always_redraw(lambda: axes.get_area(graph, x_range=[PI / 2, t.get_value()], color=PURE_RED))
        tlabel = always_redraw(
            lambda: MathTex(r"t", color=PURE_RED, font_size=28).next_to(axes.c2p(t.get_value(), 0), UP))
        proper = MathTex(r"=\lim_{t \to \pi^-}", r"\int_{\pi/2}^{t} \cot x \, dx", color=BLACK,
                         font_size=texsize).next_to(improper, DOWN).shift(0.3 * RIGHT)

        # animations
        self.next_section(skip_animations=skip)
        self.play(LaggedStart(*[FadeOut(area), FadeIn(tarea, tdot, tlabel), FadeIn(proper[1])], lag_ratio=4))
        self.play(t.animate.set_value(PI - 0.01), run_time=4)
        self.remove(tdot, tlabel)
        self.wait(2)
        self.play(FadeIn(proper[0]))
        self.wait(4)
