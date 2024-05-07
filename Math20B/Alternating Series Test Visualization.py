import math

from manim import *


class ASTDemo(Scene):
    def construct(self):
        # our alternative series is a_n = sum_{n=1}^\infty (-1)^{n+1} b_n, where b_n is defined below
        # we require b_n > 0 and b_n be decreasing to 0
        def b(n):
            return 1 / n

        self.camera.background_color = WHITE
        # global variables
        axis = NumberLine(x_range=[-0.1, 1.1, 2], length=10, numbers_to_include=[0]).shift(DOWN)
        axis.set_color(BLACK)
        intro = MathTex(r"\text{How does the Alternating Series Test work?", font_size=48, color=BLACK)
        series = MathTex(r"s =", r"b_1", r"-b_2", r"+b_3", r"-b_4", r"+b_5", r"-b_6", r"+\cdots",
                         r" = \displaystyle\sum_{n=1}^\infty (-1)^{n+1} b_n",
                         color=BLACK, font_size=36).to_edge(UP, MED_SMALL_BUFF)

        s = ValueTracker(0)  # keeps track of the partial sums so far
        sumLine = always_redraw(lambda: DashedLine(axis.n2p(s.get_value()) + 2 * DOWN,
                                                   axis.n2p(s.get_value()) + 3 * UP,
                                                   color=PURE_RED))
        sumText = always_redraw(lambda: MathTex(r"\text{sum so far}",
                                                color=PURE_RED, font_size=20).next_to(sumLine, DOWN, SMALL_BUFF))
        skip = True

        ############### ANIMATIONS ################

        #############
        ### Section 1 - Initial setup
        self.next_section(skip_animations=not skip)
        self.play(FadeIn(intro, shift=UP, run_time=2))
        self.wait(2)
        self.play(FadeOut(intro))
        self.play(FadeIn(series, shift=UP), Create(axis), run_time=2)
        self.wait(4)

        #############
        ### Section 2 - Visualizing sum of first 6 terms
        self.next_section(skip_animations=not skip)
        self.play(FadeIn(sumLine, sumText, run_time=2))
        self.wait(2)
        sum = 0  # an accumulator variable for the partial sums
        # consider partial sums for first 6 terms
        termHighlight = SurroundingRectangle(series[1], color=PURE_RED)  # a bound around terms added so far
        rectangleLabel = MathTex(r"s_1", font_size=24, color=PURE_RED).next_to(termHighlight, UP, SMALL_BUFF)
        arrowStart = axis.n2p(0)
        for n in range(1, 7):
            # term updating
            term = b(n)
            sum += (-1) ** (n + 1) * term

            # axis updating
            newtick = axis.get_tick(sum)
            newlabel = MathTex(r"s_{" + str(n) + "}", color=PURE_BLUE, font_size=24).next_to(newtick, DOWN, SMALL_BUFF)

            # arrow updating
            arrowEnd = axis.n2p(sum)
            newarrow = CurvedArrow(arrowStart, arrowEnd, color=PURE_BLUE)
            arrowlabel = MathTex(series.tex_strings[n], color=PURE_BLUE,
                                 font_size=24).next_to(newarrow, DOWN if n % 2 == 1 else UP, SMALL_BUFF)
            arrowGroup = VGroup(newarrow, arrowlabel)
            arrowStart = arrowEnd

            # new term highlighting
            newRectangle = SurroundingRectangle(series[1:(n + 1)], color=PURE_RED)
            newRectangleLabel = newlabel.copy().next_to(newRectangle, UP, SMALL_BUFF).set_color(PURE_RED)

            # animations
            if n == 1:
                self.play(FadeIn(termHighlight, rectangleLabel))
            else:
                self.play(Transform(termHighlight, newRectangle),
                          Transform(rectangleLabel, newRectangleLabel))
            self.wait(1)
            self.play(FadeIn(arrowGroup))
            self.wait(1)
            self.play(s.animate(run_time=2).set_value(sum))
            self.wait(1)
            self.play(FadeIn(newtick, newlabel), FadeOut(arrowGroup))
            self.wait(2)

        #############
        ### Section 3 - Animating sum of terms beyond first six
        self.next_section(skip_animations=not skip)
        alltermsRect = SurroundingRectangle(series[1:8], color=PURE_RED)
        alltermsLabel = MathTex(r"s", color=PURE_RED, font_size=24).next_to(alltermsRect, UP, SMALL_BUFF)
        self.play(Transform(termHighlight, alltermsRect),
                  Transform(rectangleLabel, alltermsLabel),
                  run_time=2)
        self.wait(1)

        nVals = [7, 8, 9, 10, 15, 20, 31, 42, 63, 100, 201, 402, 999]  # don't show all values of n, just key ones
        times = [2, 1.5, 1.5, 1.5, 1, 1, 1, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25]  # speed things up as we get deeper
        timesIndex = 0
        for n in nVals:
            # indexing no longer consecutive, so must explicitly create partial sum
            sum = math.fsum([(-1) ** (i + 1) * b(i) for i in range(1, n + 1)])

            self.play(s.animate(run_time=times[timesIndex]).set_value(sum))
            timesIndex += 1
        self.wait(2)

        sTick = axis.get_tick(sum).set_color(PURE_RED)
        sLabel = MathTex(r"s", color=PURE_RED, font_size=24).next_to(sTick, DOWN, SMALL_BUFF)
        self.play(FadeIn(sTick, sLabel))
        self.wait(1)
        self.play(FadeOut(sumLine, sumText))
        self.wait(5)
