from manim import *


class AccumDemo(Scene):
    def construct(self):

        def f(x):
            return 2 - x

        # g(x) = int_1^x f(t) dt = int_1^x (2-t) dt = 2x-x^2/2-3/2
        def g(x):
            return 2 * x - (x ** 2) / 2 - 3 / 2

        # global variables
        labelsize = 28
        labelcolor = YELLOW
        faxes = Axes(x_range=[-0.5, 3.5, 1], y_range=[-1.5, 2.5, 1], x_length=config.frame_width / 2,
                     y_length=config.frame_height / 3, axis_config={"font_size": 24},
                     tips=False).add_coordinates().to_corner(UL, buff=LARGE_BUFF)
        fgraph = faxes.plot(f, x_range=[0, 3.5])
        fxlabel = faxes.get_x_axis_label(MathTex(r"t", font_size=labelsize, color=labelcolor), direction=RIGHT)
        fylabel = faxes.get_y_axis_label(MathTex(r"y=2-t", font_size=labelsize, color=labelcolor), direction=UP)
        fgrp = VGroup(faxes, fgraph, fxlabel, fylabel)

        gaxes = Axes(x_range=[-0.5, 3.5, 1], y_range=[-1.5, 2.5, 1], x_length=config.frame_width / 2,
                     y_length=config.frame_height / 3, axis_config={"font_size": 24},
                     tips=False).add_coordinates().to_corner(DL, buff=LARGE_BUFF)

        gxlabel = gaxes.get_x_axis_label(MathTex(r"x", font_size=labelsize, color=labelcolor), direction=RIGHT)
        gylabel = gaxes.get_y_axis_label(MathTex(r"g(x)", font_size=labelsize, color=labelcolor),
                                         direction=UP)
        ggrp = VGroup(gaxes, gxlabel, gylabel)

        xpos = ValueTracker(0.5)  # location of vertical line showing place for our focus
        xline = always_redraw(lambda: DashedLine(start=gaxes.c2p(xpos.get_value(), -1.5),
                                                 end=faxes.c2p(xpos.get_value(), 2),
                                                 color=BLUE))
        title = VGroup(*MathTex(r"\text{Understanding the Area}\\",
                                r"\text{Accumulator Function}\\",
                                r"g(x) = \int_1^x 2-t \, dt",
                                font_size=30)).arrange(DOWN).to_corner(UR, buff=LARGE_BUFF)
        skip = False

        # gets the area under f(x) on faxes from a=1 to b=xval, uses green for positive areas, red for negative
        # area might involve both colors, so return type is a VGroup of area mobjects
        def getArea(xval=2.0):
            if xval < 1:
                return faxes.get_area(fgraph, x_range=[xval, 1], color=RED)
            elif 1 <= xval and xval <= 2:
                return faxes.get_area(fgraph, x_range=[1, xval], color=GREEN)
            else:
                area1 = faxes.get_area(fgraph, x_range=[1, 2], color=GREEN)
                area2 = faxes.get_area(fgraph, x_range=[2, xval], color=RED)
                return VGroup(area1, area2)

        # key set of animations to show how x values on g(x) get linked to areas; these areas become the
        # height of g(x)
        def xValueDemo(xval, tempo=2):
            self.play(xpos.animate.set_value(xval), run_time=tempo)
            self.wait(tempo / 2)
            gtex = MathTex(r"g(", str(xval), r")=\int^{", str(xval), r"}_1 2-t \, dt",
                           font_size=36).next_to(gxlabel, RIGHT, MED_LARGE_BUFF)
            gtex[1].set_color(BLUE)
            gtex[3].set_color(BLUE)
            self.play(FadeIn(gtex), run_time=tempo)
            self.wait(tempo / 2)
            area = getArea(xval)
            self.play(FadeIn(area), run_time=tempo)
            self.wait(tempo / 2)
            areaVal = g(xval)
            areaColor = WHITE
            if areaVal > 0:
                areaColor = GREEN
            elif areaVal < 0:
                areaColor = RED
            gtex2 = MathTex(r"=", str(areaVal), font_size=36, color=areaColor).next_to(gtex, RIGHT, MED_SMALL_BUFF)
            self.play(FadeIn(gtex2), run_time=tempo)
            self.wait(tempo / 2)

            newDot = Dot(gaxes.c2p(xval, g(xval)), color=areaColor)
            newSegment = Line(gaxes.c2p(xval, 0), gaxes.c2p(xval, g(xval)), color=areaColor)
            gbrace = Brace(newSegment, direction=LEFT, buff=0, color=areaColor)
            bracelabel = MathTex(r"g(", str(xval), r")", font_size=18, color=areaColor).next_to(gbrace, LEFT,
                                                                                                SMALL_BUFF)
            self.play(FadeIn(gbrace, bracelabel), run_time=tempo)
            self.wait(tempo / 2)
            self.play(Transform(area, VGroup(newDot, newSegment)), run_time=tempo)
            self.wait(tempo / 2)
            self.play(FadeOut(newSegment, gbrace, bracelabel, area, gtex, gtex2),
                      FadeIn(Dot(gaxes.c2p(xval, g(xval)), color=WHITE)),
                      run_time=tempo)
            self.wait(tempo / 2)

        # introduce title and graphs
        self.next_section(skip_animations=skip)
        self.play(LaggedStart(FadeIn(title), FadeIn(ggrp), FadeIn(fgrp, xline), lag_ratio=4))
        self.wait(3)

        # show calculation of g(x) at several different x values (2, 2.5, 3, etc.) at increasing speeds (2.5, 2, etc.)
        self.next_section(skip_animations=skip)
        xValueDemo(2, 2.5)
        xValueDemo(2.5, 2)
        xValueDemo(3, 1.5)
        xValueDemo(1.5, 1)
        xValueDemo(1, 0.5)
        xValueDemo(0.5, 0.5)
        self.wait(2)

        # trace out the full g(x) curve and linked areas
        self.next_section(skip_animations=skip)
        self.play(xpos.animate.set_value(0), run_time=2)
        self.wait(2)

        movingArea = always_redraw(lambda: getArea(xpos.get_value()))
        movingDot = always_redraw(lambda: Dot(gaxes.c2p(xpos.get_value(), g(xpos.get_value()))))
        gGraph = always_redraw(lambda: gaxes.plot(g, x_range=[0, xpos.get_value()]))
        self.play(FadeIn(movingArea, movingDot, gGraph), run_time=2)
        self.play(xpos.animate.set_value(3.5), rate_func=rate_functions.linear, run_time=7)
        self.play(gylabel.animate.next_to(movingDot, RIGHT, SMALL_BUFF).set_color(WHITE), run_time=2)
        self.add(gaxes.plot(g, x_range=[0, 3.5]))  # make g graph permanent
        self.play(FadeOut(movingArea, movingDot, gGraph))
        self.wait(1)

        # draws the tangent line to g(x) at xval, lists the slope as a number above the line (using labeldirection),
        # plots a point with height equal to that slope
        def drawTangentAtXVal(xval, tempo=2, labeldirection=UP):
            self.play(xpos.animate.set_value(xval), run_time=tempo)
            self.wait(tempo / 2)
            gprime = f(xval)
            tanpoint = gaxes.c2p(xval, g(xval))
            tangent = Line(gaxes.c2p(xpos.get_value() - 0.5, g(xpos.get_value()) - 0.5 * f(xpos.get_value())),
                           gaxes.c2p(xpos.get_value() + 0.5, g(xpos.get_value()) + 0.5 * f(xpos.get_value())),
                           color=RED)
            self.play(FadeIn(tangent), run_time=tempo)
            self.wait(tempo / 2)
            tanlabel = MathTex(r"\text{slope} =" + str(gprime), font_size=24,
                               color=RED).next_to(tanpoint, labeldirection, SMALL_BUFF)
            self.play(FadeIn(tanlabel), run_time=tempo)
            self.wait(tempo)

            derivpoint = Dot(gaxes.c2p(xval, gprime), color=RED)
            self.play(Transform(tanlabel, derivpoint), FadeOut(tangent), run_time=tempo)
            self.wait(tempo)

        # draw some points on g'(x)
        self.next_section(skip_animations=skip)

        title2 = VGroup(*MathTex(r"\text{Drawing the graph of }g'(x)\\",
                                 r"\text{i.e., Finding } \dfrac{d}{dx} \int_1^x 2-t \, dt\\",
                                 font_size=30, color=RED)).arrange(DOWN).next_to(title, DOWN, LARGE_BUFF)
        self.play(FadeIn(title2), run_time=2)
        self.wait()

        drawTangentAtXVal(2, 2.5, UP)
        drawTangentAtXVal(3, 2, UR)
        drawTangentAtXVal(1, 1.5, UL)
        drawTangentAtXVal(0, 1, 1.5 * LEFT)

        # now show full g'(x) curve
        self.next_section(skip_animations=skip)
        tangency = always_redraw(lambda: Dot(gaxes.c2p(xpos.get_value(), g(xpos.get_value()))))
        tanLine = always_redraw(lambda: Line(gaxes.c2p(xpos.get_value() - 0.5,
                                                       g(xpos.get_value()) - 0.5 * f(xpos.get_value())),
                                             gaxes.c2p(xpos.get_value() + 0.5,
                                                       g(xpos.get_value()) + 0.5 * f(xpos.get_value())),
                                             color=RED))
        dotOnDeriv = always_redraw(lambda: Dot(gaxes.c2p(xpos.get_value(), f(xpos.get_value())), color=RED))
        gPrimeGraph = always_redraw(lambda: gaxes.plot(f, x_range=[0, xpos.get_value()], color=RED))
        self.play(FadeIn(tangency, tanLine, dotOnDeriv, gPrimeGraph), run_time=2)
        self.wait()
        self.play(xpos.animate.set_value(3.5), rate_func=rate_functions.linear, run_time=7)
        gPrimeLabel = MathTex(r"g'(x)", color=RED, font_size=labelsize).next_to(dotOnDeriv, RIGHT, SMALL_BUFF)
        self.play(FadeIn(gPrimeLabel), FadeOut(dotOnDeriv, xpos, tanLine, tangency))
        self.wait()

        # connect g'(x) to f(x)
        self.next_section(skip_animations=skip)
        observe = VGroup(*MathTex(r"\text{Notice: }g'(x) = f(x)\\",
                                  r"\text{i.e., } \dfrac{d}{dx} \int_1^x 2-t \, dt = 2-x",
                                  font_size=30)).arrange(DOWN).next_to(title2, DOWN, LARGE_BUFF)
        self.play(FadeIn(observe))
        self.wait(4)
