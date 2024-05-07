from manim import *


class ITViz(Scene):
    def construct(self):
        # the functification of the sequence based on the series a_1 + a_2 + ...
        # once you define f, a_n = f(n)
        def f(x):
            return 3 / x

        self.camera.background_color = WHITE
        question = MathTex(r"\text{Visual Intuition Behind}\\",
                           r"\text{The Integral Test for Series}", color=BLACK).arrange(DOWN)
        series = MathTex(r"a_1", r"+", r"a_2", r"+", r"a_3", r"+", r"a_4", r"+", r"a_5", r"+", r"a_6", r"+",
                         r"\cdots", color=BLACK).to_edge(UP, MED_SMALL_BUFF)
        maxterm = 6
        colors = [PURE_RED, ORANGE, YELLOW, PURE_GREEN, PURE_BLUE, PURPLE]
        for i in range(0, maxterm):
            series[2 * i].set_color(colors[i])
        skip = True

        ###########
        # Section 1 - Setting the stage
        self.next_section(skip_animations=not skip)
        self.play(FadeIn(question, shift=UP), run_time=3)
        self.wait(3)
        self.play(FadeOut(question), FadeIn(series, shift=UP), run_time=3)
        self.wait(3)

        ###########
        # Section 2 - Seeing the terms as heights
        self.next_section(skip_animations=not skip)
        axes = Axes(x_range=[-0.5, 6.5, 1], y_range=[-0.5, f(1) + 0.5, 1], tips=False,
                    x_length=10, y_length=5, x_axis_config={"include_numbers": True}).to_edge(DOWN, MED_LARGE_BUFF)
        axes.set_color(BLACK)
        self.play(Create(axes))
        self.wait(2)
        tempos = [2, 1.5, 1, 0.5, 0.5, 0.5]
        for i in range(0, maxterm):
            loc = axes.c2p(i + 1, f(i + 1))
            xloc = axes.c2p(i + 1, 0)
            color = colors[i]
            tempo = tempos[i]
            dot = Dot(loc, color=color)
            segment = Line(xloc, loc, color=color)
            brace = Brace(segment, direction=LEFT, color=color)
            label = MathTex(r"a_{", str(i + 1), r"}", color=color, font_size=28).next_to(brace, LEFT, SMALL_BUFF)
            self.play(TransformFromCopy(series[2 * i], dot), run_time=tempo)
            self.play(FadeIn(brace, label), run_time=tempo)
            self.wait(tempo)
            self.play(FadeOut(brace, label), run_time=tempo)

        ###########
        # Section 3 - Seeing the series as left or right rectangles
        self.next_section(skip_animations=not skip)
        lrects = VGroup()
        llabels = VGroup()
        xunit = np.linalg.norm(axes.c2p(1, 0) - axes.c2p(0, 0))
        yunit = np.linalg.norm(axes.c2p(0, 1) - axes.c2p(0, 0))
        for i in range(0, maxterm):
            color = colors[i]
            rect = Rectangle(color=color, height=yunit * f(i + 1), width=xunit, fill_color=color,
                             fill_opacity=0.2).move_to(axes.c2p(i + 0.5, f(i + 1) / 2))
            label = MathTex(r"a_{", str(i + 1), r"}", color=color, font_size=28).move_to(rect.get_center())
            lrects.add(rect)
            llabels.add(label)

        self.play(LaggedStart(*[Create(rect) for rect in lrects], lag_ratio=3),
                  LaggedStart(*[FadeIn(label) for label in llabels], lag_ratio=3))

        dots = MathTex(r"\cdots", color=BLACK, font_size=44).move_to(axes.c2p(6.3, f(7) / 2))
        self.play(FadeIn(dots))
        self.wait(4)

        allObjects = VGroup(lrects, llabels)
        lastRectAndLabel = VGroup(lrects.submobjects.pop(), llabels.submobjects.pop())
        # shift all right
        self.play(allObjects.animate.shift(xunit * RIGHT), FadeOut(lastRectAndLabel), run_time=3)
        self.wait(4)

        ###########
        # Section 4 - Exploring the first half of statement of the Integral Test (IT)
        self.next_section(skip_animations=not skip)

        graph = axes.plot(f, x_range=[0.9, 6.5, 0.05])
        graph.set_color(BLACK)
        flabel = MathTex(r"f(x)", color=BLACK, font_size=28).next_to(axes.c2p(0.9, f(0.9)), LEFT, MED_SMALL_BUFF)
        self.play(FadeIn(graph, flabel), run_time=2)
        self.wait(4)

        area = axes.get_area(graph, x_range=[1, 6.5], color=BLACK)
        comparison = MathTex(r"\int_1^{\infty} f(x) \, dx", r"<", r"\text{series}",
                             r"\text{If divergent}", r"\Rightarrow", r"\text{divergent}", color=BLACK,
                             font_size=36).arrange_in_grid(2, 3).next_to(axes.c2p(3, 3), RIGHT)
        for i in range(0, 6): comparison[2][i].set_color(colors[i])

        anims = [FadeIn(area, comparison[0]), FadeIn(comparison[1:3]), FadeIn(comparison[3]),
                 FadeIn(comparison[4::])]

        self.play(LaggedStart(*anims, lag_ratio=5))
        self.wait(4)
        self.play(FadeOut(comparison[3::]))
        self.wait(4)

        ###########
        # Section 5 - Exploring the second half of statement of the Integral Test (IT)
        self.next_section(skip_animations=not skip)
        comparison2 = MathTex(r"\int_1^{\infty} f(x) \, dx", r"<", r"\text{series}",
                              r"\text{If convergent}", r"\not\Rightarrow", r"\text{convergent}",
                              color=BLACK, font_size=36).arrange_in_grid(2, 3).next_to(axes.c2p(3, 3), RIGHT)

        anims = [FadeIn(comparison2[3]), FadeIn(comparison2[4::])]

        self.play(LaggedStart(*anims, lag_ratio=5))
        self.wait(7)
        self.play(FadeOut(comparison[0:3], comparison2[3::]))
        self.wait(4)
        self.play(allObjects.animate.shift(xunit * LEFT), FadeIn(lastRectAndLabel), run_time=3)
        self.wait(2)

        ###########
        # Section 6 - Continue exploring the second half of statement of the Integral Test (IT)
        self.next_section(skip_animations=not skip)
        comparison3 = MathTex(r"\text{series}-a_1", r"<", r"\int_1^{\infty} f(x) \, dx",
                              r"\text{convergent}", r"\Leftarrow", r"\text{If convergent}",
                              color=BLACK, font_size=36).arrange_in_grid(2, 3).next_to(axes.c2p(3, 3), RIGHT)
        for i in range(0, 6): comparison3[0][i].set_color(colors[i])
        comparison3[0][7::].set_color(colors[0])

        anims = [FadeIn(comparison3[2]), FadeIn(comparison3[0:2]), FadeIn(comparison3[5]),
                 FadeIn(comparison3[3:5])]
        self.play(LaggedStart(*anims, lag_ratio=5))
        self.wait(7)
