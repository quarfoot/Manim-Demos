from manim import *


class HistViz(Scene):
    def construct(self):

        # a datum (value) needs to be placed in an appropriate bin; bins is a list of cut points
        # returns the value of the midpoint of the correct bin
        # e.g., if value = 4.2 and bins = [4,8,12,16], then we return 6 = (4+8)/2
        def getBinMidpoint(value, bins):
            for index, cut in enumerate(bins):
                if cut > value:
                    if index > 0:
                        return (bins[index] + bins[index - 1]) / 2
                    else:
                        raise Exception("value is below binning structure")

            raise Exception("value is above binning structure")

        # counts how many data points in dataSet fall into the same bin as value would
        # in general, dataSet will be the values before value in a larger data set
        def countHowMany(value, dataSet, bins):
            lower = 0
            upper = 0
            for i, cut in enumerate(bins):
                if cut > value:
                    upper = cut
                    lower = bins[i - 1]
                    break

            count = 0
            for datum in dataSet:
                if lower <= datum < upper:
                    count += 1

            return count

        def animateBinStrategy(costTex, hist, bins, timings, vals, fade=True):
            # draw ticks on axis to show bins
            binning = VGroup()
            for x in bins:
                newtick = hist.get_tick(x)
                newlabel = MathTex(str(x), font_size=18, color=PURE_BLUE).next_to(newtick, DOWN, SMALL_BUFF)
                binning.add(newtick, newlabel)
                self.play(FadeIn(newtick, newlabel), run_time=0.5)

            self.wait(1)
            brace = Brace(binning, DOWN, color=PURE_RED)
            braceText = MathTex(r"\text{Binning Strategy}", font_size=20, color=PURE_RED).next_to(brace, DOWN, SMALL_BUFF)
            self.play(FadeIn(brace, braceText))
            self.wait(3)
            self.play(FadeOut(brace, braceText))

            rect = SurroundingRectangle(costTex, color=PURE_RED)
            self.play(Create(rect), run_time=2)
            unit = hist.get_unit_size()
            binwidth = (bins[1] - bins[0]) * unit
            sq = Rectangle(width=binwidth, height=unit, color=PURE_RED, fill_color=PURE_RED, fill_opacity=0.3)

            i = 0
            sqGroup = VGroup()
            for (val, t) in zip(vals, timings):
                value = val.get_value()
                loc = hist.n2p(getBinMidpoint(value, bins))  # where to put the new datum
                numInBin = countHowMany(value, costs[:i], bins)
                newSq = sq.copy().next_to(loc, UP, buff=unit * numInBin)
                newrect = SurroundingRectangle(val, color=PURE_RED)
                self.play(Transform(rect, newrect), run_time=t)
                self.wait(t)
                valcopy = val.copy()
                self.add(valcopy)
                self.play(valcopy.animate.next_to(loc, DOWN).set_color(PURE_RED), run_time=t)
                self.wait(t)
                self.play(Transform(valcopy, newSq), run_time=t)
                self.wait(t)
                sqGroup += valcopy
                i += 1

            self.wait(2)
            fauxorigin = hist.n2p(5.7)
            yaxis = NumberLine(x_range=[0, 5, 1], color=PURE_BLUE, include_tip=False, unit_size=unit,
                               label_direction=0.5 * UL, rotation=90 * DEGREES, include_numbers=True,
                               font_size=18).move_to(fauxorigin, aligned_edge=DOWN)
            yaxis.numbers.set_color(PURE_BLUE)
            ylabel = MathTex(r"\text{Counts}", font_size=20, color=PURE_BLUE).rotate(angle=90 * DEGREES).next_to(yaxis, LEFT)
            self.play(FadeIn(yaxis, ylabel))
            self.wait(2)
            if fade:
                self.play(FadeOut(sqGroup, rect))
                self.play(FadeOut(binning))

        # global variables
        self.camera.background_color=WHITE
        costs = [6.50, 8.25, 6.34, 7.29, 12.31, 11.39, 14.23, 12.65, 12.21, 7.53, 14.21, 9.32, 10.53]
        costTex = MathTex(r"\underline{\text{Recent Chipotle Bills}}", font_size=24, color=BLACK)
        vals = [DecimalNumber(x, color=GRAY_E, font_size=24, stroke_color=BLACK, stroke_opacity=0) for x in costs]
        costsGroup = VGroup(costTex, *vals).arrange(DOWN).to_edge(LEFT, buff=MED_LARGE_BUFF)

        intro = MathTex(r"\text{Visualizing Numeric Data:  The Histogram", color=BLACK, font_size=48).shift(UP)
        hist = NumberLine(x_range=[5.5, 15.5, 1], length=10, color=PURE_BLUE,
                          include_tip=False, include_ticks=False).to_edge(RIGHT, buff=LARGE_BUFF).shift(2 * DOWN)
        histlabel = MathTex(r"\text{cost}", font_size=20, color=PURE_BLUE).next_to(hist, RIGHT)

        skip = False
        self.next_section(skip_animations=skip)
        self.play(FadeIn(intro, shift=UP))
        self.wait(3)
        self.play(FadeOut(intro))
        self.play(LaggedStart(*[FadeIn(obj) for obj in costsGroup], lag_ratio=0.2))
        self.wait()
        self.play(FadeIn(hist, histlabel))
        self.wait(3)

        self.next_section(skip_animations=skip)
        bins = range(6, 16)
        timings = [2, 2, 1, 1, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        animateBinStrategy(costTex, hist, bins, timings, vals, True)
        self.wait()

        self.next_section(skip_animations=skip)
        bins = [6, 9, 12, 15]
        timings = [0.25] * 13
        animateBinStrategy(costTex, hist, bins, timings, vals, False)
        self.wait()
