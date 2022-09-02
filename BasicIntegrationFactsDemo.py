from manim import *


class BasicFacts(Scene):
    def construct(self):
        # global
        title = Tex(r"Integration Facts Review", font_size=48).to_edge(UP, buff=SMALL_BUFF)
        facts = MathTex(
            r"&1. \int_a^b f(x) \, dx \overset{\text{def}}{=} \text{area under }f(x) \text{ from }a \text{ to }b \overset{\text{def}}{=} \lim_{n \to \infty} \sum_{i=1}^n f(x_i) \Delta x\\[0.5em]",
            r"&2. \int_a^b f(x) \, dx \text{ is a signed area}\\[0.5em]",
            r"&3. \int_a^b f(x)+g(x) \, dx = \int_a^b f(x) \, dx + \int_a^b g(x) \, dx\\[0.5em]",
            r"&4. \int_a^b C \cdot f(x) \, dx = C \int_a^b f(x) \, dx \text{  and  } \int_a^b C \, dx = C \cdot (b-a)\\[0.5em]",
            r"&5. \int_b^a f(x) \, dx = - \int_a^b f(x) \, dx", font_size=36).next_to(title, DOWN, buff=MED_LARGE_BUFF)
        tempo = 1  # controls overall speed of video
        skip = False

        # from a blank screen, lists title and facts 0 through i - 1, adds fact i, clears facts previous facts,
        # and shifts fact i to top of screen
        def transitionToFact(i):
            if i > 0:
                self.play(FadeIn(title), FadeIn(*facts[0:i]), run_time=tempo)
                self.wait(tempo)
            else:
                self.play(FadeIn(title))
            self.wait(tempo)

            self.play(FadeIn(facts[i], shift=UP), run_time=tempo)
            self.wait(2 * tempo)

            if i > 0:
                self.play(FadeOut(title), FadeOut(*facts[0:i]))
            else:
                self.play(FadeOut(title))
            self.remove(facts[i])
            self.play(facts[i].copy().animate.to_edge(UP, buff=SMALL_BUFF))
            self.wait(tempo)

        ###########
        # Section 1 - Intro and limit derivation
        self.next_section(skip_animations=skip)

        transitionToFact(0)

        # subsection - draw ticks and partition
        self.next_section(skip_animations=skip)

        def func1(x):
            return 2 + np.sin(1.2 * x)

        axes = Axes(x_range=[-1, 6], y_range=[-1, 4], x_length=8, y_length=6, tips=False,
                    x_axis_config={"include_ticks": False},
                    y_axis_config={"include_ticks": False}).to_corner(DL, buff=MED_LARGE_BUFF)
        graph = axes.plot(func1, x_range=[-0.5, 5.5], color=GREEN)
        graphlabel = MathTex("y=f(x)", color=GREEN, font_size=24)
        graphlabel.next_to(axes.c2p(5.5, func1(5.5)), UP, buff=SMALL_BUFF)
        a = 1.3
        b = 5.2
        atick = axes.x_axis.get_tick(a).set_color(RED)
        btick = axes.x_axis.get_tick(b).set_color(RED)
        alabel = MathTex("a", color=RED, font_size=24).next_to(atick, DOWN, buff=SMALL_BUFF)
        blabel = MathTex("b", color=RED, font_size=24).next_to(btick, DOWN, buff=SMALL_BUFF)
        area = axes.get_area(graph, x_range=[a, b], color=RED_B)

        self.play(Create(axes), run_time=2 * tempo)
        self.wait(tempo)
        self.play(Create(graph), run_time=2 * tempo)
        self.play(FadeIn(graphlabel), run_time=tempo)
        self.wait(tempo)
        endGroup = VGroup(atick, btick, alabel, blabel)
        self.play(FadeIn(endGroup), run_time=tempo)
        self.wait(tempo)
        self.play(FadeIn(area))
        self.wait(tempo)

        # subsection - finite partition and details
        self.next_section(skip_animations=skip)
        self.play(FadeOut(endGroup), run_time=tempo)
        self.wait(tempo)
        n = 7  # how many rectangles to start in partition
        deltax = (b - a) / n
        partxs = np.arange(start=a, stop=b + deltax, step=deltax)
        partlabels = MathTex(r"x_0", r"x_1", r"\cdots", r"x_{i-1}", r"x_i", r"\cdots", r"x_{n-1}", r"x_n",
                             color=BLUE,
                             font_size=24)
        partticks = [axes.x_axis.get_tick(val).set_color(BLUE) for val in partxs]
        partanims = [FadeIn(partticks[i], partlabels[i].next_to(partticks[i], DOWN, SMALL_BUFF)) for i in range(n + 1)]
        self.play(LaggedStart(*partanims, lag_ratio=0.6 * tempo))
        self.wait(tempo)
        deltaxbrace = Brace(VGroup(*partlabels[0:2]), direction=DOWN, sharpness=1, color=PURPLE)
        deltaxlabel = MathTex(r"\Delta x = \frac{b-a}{n}", color=PURPLE,
                              font_size=24).next_to(deltaxbrace, DOWN, buff=SMALL_BUFF)
        line = Line(axes.c2p(partxs[4], 0), axes.c2p(partxs[4], func1(partxs[4])))
        heightbrace = Brace(line, direction=RIGHT, sharpness=1, color=YELLOW, buff=SMALL_BUFF)
        heightlabel = MathTex(r"f(x_i)", color=YELLOW,
                              font_size=24).next_to(heightbrace, RIGHT, buff=SMALL_BUFF)
        self.play(FadeIn(deltaxbrace, deltaxlabel), run_time=tempo)
        self.wait(tempo)

        rects = axes.get_riemann_rectangles(graph, x_range=[a, b], dx=deltax, stroke_color=BLUE, fill_opacity=0.3,
                                            input_sample_type="right", stroke_width=4, color=BLUE_C)
        self.play(Create(rects), run_time=2 * tempo)
        self.wait(tempo)
        self.play(FadeIn(heightlabel, heightbrace), run_time=tempo)
        self.wait(tempo)

        derivation = MathTex(r"\text{Area} &\approx \text{Sum of } n \text{ Rectangles}\\[1em]",
                             r"  &\approx \sum_{i=1}^n f(x_i) \Delta x\\[1em]",
                             r"\text{Area} &= \lim_{n \to \infty} \sum_{i=1}^n f(x_i) \Delta x",
                             font_size=32).next_to(axes, RIGHT, buff=MED_LARGE_BUFF)
        derivation[1][6:11].set_color(YELLOW)
        derivation[1][11:].set_color(PURPLE)
        self.play(LaggedStart(*[FadeIn(eq) for eq in derivation[0:2]], lag_ratio=2 * tempo))
        self.wait(4 * tempo)
        self.play(FadeOut(*partticks, partlabels, deltaxbrace, deltaxlabel, heightlabel, heightbrace), run_time=tempo)
        self.wait(tempo)

        # subsection - rectangles go to infinity, finish derivation
        self.next_section(skip_animations=skip)

        numSlides = 50  # how many steps toward infinitely many rectangles to take
        for numRects in range(n + 1, n + 1 + numSlides):
            pic = axes.get_riemann_rectangles(graph, x_range=[a, b], dx=(b - a) / numRects, stroke_color=BLUE,
                                              fill_opacity=0.3, input_sample_type="right", stroke_width=4, color=BLUE_C)
            self.play(Transform(rects, pic), run_time=4 * tempo / numSlides)

        self.wait(tempo)
        self.play(FadeIn(derivation[2]), run_time=tempo)
        self.wait(3 * tempo)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2 * tempo)
        self.wait(tempo)

        ###########
        # Section 2 - Signed area explanation
        self.next_section(skip_animations=skip)

        transitionToFact(1)

        self.next_section(skip_animations=skip)

        # subsection - show new graph, draw rectangles
        def func2(x):
            return -x * (x - 3) / 4

        axes2 = Axes(x_range=[-1, 6], y_range=[-3, 1], x_length=8, y_length=5,
                     tips=False).to_corner(DL, buff=LARGE_BUFF)
        graph2 = axes2.plot(func2, x_range=[0, 5], color=WHITE)
        graphlabel2 = MathTex(r"f(x)", font_size=24, color=WHITE).next_to(axes2.c2p(5, func2(5)), RIGHT)
        area2 = axes2.get_area(graph2, x_range=[0, 5], color=WHITE)
        self.play(Create(axes2), run_time=tempo)
        self.wait(tempo)
        self.play(Create(graph2), run_time=tempo)
        self.play(FadeIn(graphlabel2), run_time=tempo)
        self.wait(tempo)
        self.play(FadeIn(area2), run_time=tempo)
        self.wait(tempo)

        rects2a = axes2.get_riemann_rectangles(graph2, x_range=[0, 3], dx=1 / 3, stroke_color=GREEN, fill_opacity=0.3,
                                               input_sample_type="right", stroke_width=4, color=GREEN_C)
        rects2b = axes2.get_riemann_rectangles(graph2, x_range=[3, 5], dx=1 / 3, stroke_color=RED, fill_opacity=0.3,
                                               input_sample_type="right", stroke_width=4, color=RED_C)

        self.play(Succession(Create(rects2a), Create(rects2b)), run_time=3 * tempo)
        self.wait(tempo)

        limitTex = MathTex(r"\lim_{n \to \infty} \sum_{i=1}^n", r"f(x_i)", r"\Delta x",
                           font_size=36).next_to(axes2.x_axis, RIGHT, buff=LARGE_BUFF)
        limitBound = SurroundingRectangle(limitTex[1], buff=0.05, color=YELLOW)
        self.play(Write(limitTex), run_time=tempo)
        self.wait(tempo)
        self.play(Create(limitBound), run_time=2 * tempo)
        self.wait(tempo)

        def showRectHeights(grp):
            for mob in grp.submobjects:
                origColor = mob.get_stroke_color()
                bound = SurroundingRectangle(mob, buff=0, color=YELLOW)

                rectbrace = Brace(bound, direction=RIGHT, sharpness=1, buff=0.1, color=YELLOW)
                rectlabel = MathTex(r"f(x_i)", font_size=24, color=YELLOW).next_to(rectbrace, buff=SMALL_BUFF)

                self.play(FadeIn(bound), FadeIn(rectbrace, rectlabel),
                          run_time=0.2 * tempo)
                limitTex[1].set_color(origColor)
                limitBound.set_color(origColor)
                self.wait(0.2 * tempo)

                self.play(FadeOut(bound), FadeOut(rectbrace, rectlabel),
                          run_time=0.2 * tempo)
                self.wait(0.2 * tempo)

        showRectHeights(rects2a)
        showRectHeights(rects2b)
        self.wait(3 * tempo)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2 * tempo)
        self.wait(tempo)

        # section 3 - additivity
        self.next_section(skip_animations=skip)

        transitionToFact(2)

        # subsection - derivation of integral's additivity property
        self.next_section(skip_animations=skip)

        addtex1 = MathTex(r"\int_a^b", r"f(x)", r"\, dx = \lim_{n \to \infty} \sum_{i=1}^n", r"f(x_i)", r"\Delta x",
                          font_size=36).to_edge(LEFT, buff=MED_LARGE_BUFF).shift(2 * UP + 2 * RIGHT)
        addtex1[1].set_color(YELLOW)
        addtex1[3].set_color(YELLOW)
        addtex2 = MathTex(r"\int_a^b", r"[f(x)+g(x)]", r"\, dx &= \lim_{n \to \infty} \sum_{i=1}^n", r"[f(x_i)+g(x_i)]",
                          r"\Delta x\\",
                          r"&= \lim_{n \to \infty} \sum_{i=1}^n \left[f(x_i) \Delta x + g(x_i) \Delta x\right]\\",
                          r"&= \lim_{n \to \infty} \left(\sum_{i=1}^n f(x_i) \Delta x + \sum_{i=1}^n g(x_i) \Delta x\right)\\",
                          r"&= \lim_{n \to \infty} \sum_{i=1}^n f(x_i) \Delta x + \lim_{n \to \infty} \sum_{i=1}^n g(x_i) \Delta x\\",
                          r"&=\int_a^b f(x) \, dx + \int_a^b g(x) \, dx",
                          font_size=36).align_to(addtex1, direction=UL)

        addtex2[1].set_color(YELLOW)
        addtex2[3].set_color(YELLOW)

        self.play(FadeIn(addtex1, shift=UP))
        self.wait(2 * tempo)
        self.play(ReplacementTransform(addtex1[0:5], addtex2[0:5]))
        self.wait(3 * tempo)
        self.play(LaggedStart(*[FadeIn(eq, shift=UP) for eq in addtex2[5:]], lag_ratio=4 * tempo))
        self.wait(2 * tempo)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2 * tempo)
        self.wait(tempo)

        # section 4 - constant facts
        self.next_section(skip_animations=skip)

        transitionToFact(3)

        # subsection - integral of a constant
        self.next_section(skip_animations=skip)

        a = 1.3
        b = 3.2
        C = 2.7

        def func3(x):
            return C  # constant function

        axes3 = Axes(x_range=[-1, 4], y_range=[-1, 4], x_length=5, y_length=5, tips=False,
                     x_axis_config={"include_ticks": False},
                     y_axis_config={"include_ticks": False}).to_edge(DOWN, buff=MED_LARGE_BUFF).shift(2 * RIGHT)
        graph3 = axes3.plot(func3, x_range=[-1, 4], color=GREEN)
        graphlabel3 = MathTex(r"y=C", font_size=24, color=GREEN).next_to(graph3, RIGHT, SMALL_BUFF)
        area3 = axes3.get_area(graph3, x_range=[a, b], color=BLUE)
        atick = axes3.x_axis.get_tick(a).set_color(RED)
        btick = axes3.x_axis.get_tick(b).set_color(RED)
        alabel = MathTex("a", color=RED, font_size=24).next_to(atick, DOWN, buff=SMALL_BUFF)
        blabel = MathTex("b", color=RED, font_size=24).next_to(btick, DOWN, buff=SMALL_BUFF)
        arrow = Arrow(start=2 * UP, end=DOWN, color=GREEN).next_to(graph3, direction=UP,
                                                                   buff=MED_SMALL_BUFF).shift(0.4 * LEFT)

        self.play(Create(axes3), run_time=tempo)
        self.wait(tempo)
        self.play(Create(arrow), FadeIn(graph3, graphlabel3))
        self.wait(tempo)
        self.play(FadeIn(atick, btick, alabel, blabel))
        self.wait(tempo)
        self.play(FadeIn(area3))
        self.wait(tempo)

        # subsection - integral of a constant text
        self.next_section(skip_animations=skip)

        consTex = MathTex(r"&\phantom{==} \int_a^b C \, dx \\[1em]",
                          r"&= \text{Area under }y=C \\&\phantom{==} \text{from }a \text{ to } b\\[1em]",
                          r"&=\text{Area of rectangle}\\[1em]",
                          r"&=(\text{Height})\cdot(\text{Width})\\[1em]",
                          r"&=C \cdot (b-a)", font_size=36).to_edge(LEFT, buff=1.5 * LARGE_BUFF).shift(0.5 * DOWN)

        self.play(LaggedStart(*[Write(eq) for eq in consTex], lag_ratio=2 * tempo))
        self.wait(3 * tempo)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2 * tempo)
        self.wait(tempo)

        # section 5 - reversed bounds
        self.next_section(skip_animations=skip)

        transitionToFact(4)

        self.next_section(skip_animations=skip)
        atHome = MathTex(
            r"\text{Try to show this at home using the }\\\lim\sum \text{ definition and focusing on }\Delta x",
            font_size=36, color=RED).center()
        self.play(Write(atHome))
        self.wait(3 * tempo)
