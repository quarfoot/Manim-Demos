from manim import *


class ImproperIntegral(Scene):
    def construct(self):
        # general variables
        skip = False
        texsize = 36

        def func1(x):
            return 1 / (x ** 2)

        # general setup
        self.camera.background_color = WHITE
        axes = Axes(x_range=[0, 8.5, 1], y_range=[-.2, 1.5, 1], y_length=8, tips=False).add_coordinates()
        axes.set_color(BLACK)
        graph = axes.plot(func1, x_range=[0.3, 8.5, 0.05], color=PURE_BLUE)
        area = axes.get_area(graph, x_range=[1, 8.5], color=PURE_RED)
        t = ValueTracker(2.7)  # start at a random-looking spot
        label = MathTex(r"y=\frac{1}{x^2}", color=PURE_BLUE, font_size=28).next_to(axes.c2p(7, func1(7)), UP)
        improper = MathTex(r"\text{Goal:  Find }", r"\int_{1}^{\infty} \frac{1}{x^2} \, dx", color=BLACK,
                           font_size=texsize).to_edge(UP, buff=2)
        tdot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), 0), color=PURE_RED))
        tarea = always_redraw(lambda: axes.get_area(graph, x_range=[1, t.get_value()], color=PURE_RED))
        tlabel = always_redraw(
            lambda: MathTex(r"t", color=PURE_RED, font_size=28).next_to(axes.c2p(t.get_value(), 0), DOWN))
        proper = MathTex(r"=\lim_{t \to \infty}", r"\int_1^t \frac{1}{x^2} \, dx", color=BLACK,
                         font_size=texsize).next_to(improper, RIGHT)

        self.next_section(skip_animations=skip)
        self.play(LaggedStart(*[Create(axes), FadeIn(graph, label), FadeIn(area), Write(improper)], lag_ratio=2))
        self.wait(3)

        self.next_section(skip_animations=skip)
        self.play(LaggedStart(*[FadeOut(area), FadeIn(tarea, tdot, tlabel), FadeIn(proper[1])], lag_ratio=2))
        self.play(t.animate.set_value(8.5), run_time=5)
        self.remove(tlabel, tdot)
        self.play(FadeIn(proper[0]))
        self.wait()

        self.next_section(skip_animations=skip)
        brace1 = BraceLabel(improper[1], r"\text{Improper Integral}", DOWN, font_size=24)
        brace1.set_color(BLACK)
        brace2 = BraceLabel(proper[1], r"\text{Proper Integral}", DOWN, font_size=24)
        brace2.set_color(BLACK)
        self.play(FadeIn(brace1, brace2))
        self.wait(4)
