from manim import *
from numpy.random import default_rng
from numpy import *


class CRVDemo(Scene):
    def construct(self):
        skip=False
        self.camera.background_color = WHITE

        title = Tex(r"Thinking About a CRV $X$, Data Generation, $E(X)$, and $SD(X)$", color=BLACK,
                    font_size=40)
        self.next_section(skip_animations=skip)
        self.play(FadeIn(title, shift=UP))
        self.wait(3)
        self.play(FadeOut(title))
        self.wait()


        self.next_section(skip_animations=skip)
        minX = -0.5
        maxX = 2.1
        axes = Axes(x_range=[minX,maxX], y_range=[-0.1, 1.1, 1], x_length=6, y_length=6, tips = False,
                    x_axis_config={"color":BLACK, "include_numbers": False, "include_ticks": False},
                    y_axis_config={"numbers_to_include":[0,1],"color":BLACK, "include_numbers": True})
        axes.get_y_axis().numbers.set_color(BLACK)
        tick = axes.get_x_axis().get_tick(PI/2)
        ticklabel = MathTex(r"\dfrac{\pi}2", font_size=24, color=BLACK).next_to(tick,DOWN,SMALL_BUFF)
        pdfGraph1 = axes.plot(lambda x: 0, x_range=[minX, 0], color=PURE_RED)
        pdfGraph2 = axes.plot(np.cos, x_range=[0,PI/2], color=PURE_RED)
        pdfGraph3 = axes.plot(lambda x: 0, x_range=[PI/2, maxX], color=PURE_RED)
        pdfGroup = VGroup(axes,tick,ticklabel,pdfGraph1,pdfGraph2,pdfGraph3).shift(3*LEFT)

        self.play(Create(axes))
        self.play(FadeIn(tick,ticklabel))
        self.play(FadeIn(pdfGraph1,pdfGraph2,pdfGraph3))

        self.next_section(skip_animations=skip)
        area = axes.get_area(pdfGraph2, x_range=[0,PI/2], color=[PURE_BLUE,PURE_GREEN])
        self.play(Create(area), run_time=2)
        self.wait(4)
        self.play(FadeOut(area), run_time=2)
        self.wait(1)

        xvals = [0.3, 1.2, 0.8]
        yvals = [0.7, 0.3, 0.6]
        for xval, yval in zip(xvals,yvals):
            dot = Dot(axes.c2p(xval,yval),color=PURE_BLUE)
            self.play(FadeIn(dot))
            self.wait(1)
            self.play(dot.animate(run_time=2).move_to(axes.c2p(xval,0)))
            self.wait(1)
            RVValue = MathTex(r"X=",str(xval),font_size=28,color=PURE_BLUE).next_to(dot,DOWN,SMALL_BUFF)
            self.play(FadeIn(RVValue,shift=UP))
            self.wait(2)
            self.play(FadeOut(dot,RVValue))

        self.next_section(skip_animations=skip)
        xval1 = 0.3
        xval2 = 1.1

        arrow1 = DoubleArrow(start=axes.c2p(xval1,0),end=axes.c2p(xval1,np.cos(xval1)),color=PURE_GREEN,
                             buff=0, stroke_width=2, tip_length=0.2)
        arrow2 = DoubleArrow(start=axes.c2p(xval2, 0), end=axes.c2p(xval2, np.cos(xval2)), color=PURE_GREEN,
                             buff=0, stroke_width=2, tip_length=0.2)

        likely1 = Tex(r"$X=\,$",str(xval1),r" is \textbf{relatively} more likely than ...", font_size=24,
                      color=PURE_GREEN).next_to(arrow1.get_end(),RIGHT,MED_SMALL_BUFF)
        likely2 = Tex("... ",r"$X=\,$",str(xval2), font_size=24,
                      color=PURE_GREEN).next_to(arrow2.get_end(),RIGHT,MED_SMALL_BUFF)

        xval1label = MathTex(r"X=", str(xval1), font_size=24, color=PURE_BLUE).next_to(arrow1.get_start(), DOWN, SMALL_BUFF)
        xval2label = MathTex(r"X=", str(xval2), font_size=24, color=PURE_BLUE).next_to(arrow2.get_start(), DOWN, SMALL_BUFF)
        self.play(FadeIn(arrow1, xval1label))
        self.wait(1)
        self.play(FadeIn(arrow2, xval2label))
        self.wait(1)
        self.play(FadeIn(likely1))
        self.wait(2)
        self.play(FadeIn(likely2))
        self.wait(2)

        ystep = 0.02
        xval1dots = [Dot(axes.c2p(xval1,y),color=PURE_BLUE) for y in np.arange(ystep,np.cos(xval1)-ystep,ystep)]
        xval2dots = [Dot(axes.c2p(xval2, y), color=PURE_BLUE) for y in np.arange(ystep, np.cos(xval2)-ystep, ystep)]
        self.play(LaggedStart(*[FadeIn(dot) for dot in xval1dots],lag_ratio=0.1))
        self.wait()
        self.play(LaggedStart(*[FadeIn(dot) for dot in xval2dots], lag_ratio=0.1))
        self.wait()

        self.next_section(skip_animations=skip)
        self.play(LaggedStart(*[dot.animate.move_to(axes.c2p(xval1,0)) for dot in xval1dots], lag_ratio=0.1))
        self.play(LaggedStart(*[dot.animate.move_to(axes.c2p(xval2, 0)) for dot in xval2dots], lag_ratio=0.1))
        self.wait(4)

        self.next_section(skip_animations=skip)
        self.play(FadeOut(*xval1dots,*xval2dots,xval1label,xval2label,arrow1,arrow2,likely1,likely2))
        self.wait(2)
        fadeinanims = []
        dropdownanims = []
        numdots = 100
        timeperanim = 6/numdots
        dotList = VGroup()
        rng = default_rng()
        xvals = []
        for i in range(numdots):
            xval = arcsin(rng.uniform(0,1))  # find x using F^{-1}(unif on [0,1]) per generation theory
            xvals.append(xval)
            yval = rng.uniform(0,np.cos(xval))  # pick a random yval
            newDot = Dot(axes.c2p(xval,yval),color=PURE_BLUE)
            dotList += newDot
            fadeinanims.append(FadeIn(newDot,run_time=3*timeperanim))
            dropdownanims.append(newDot.animate(run_time=3*timeperanim).move_to(axes.c2p(xval,0)))

        self.play(LaggedStart(*fadeinanims, lag_ratio=timeperanim, run_time=4))
        self.play(LaggedStart(*dropdownanims, lag_ratio=timeperanim, run_time=4))
        self.wait(2)

        xbar = mean(xvals)
        sd = std(xvals)
        meanDot = Dot(axes.c2p(xbar,0),color=PURE_GREEN).shift(0.25*DOWN)
        self.play(TransformFromCopy(dotList,meanDot))
        self.wait(2)

        sdArrow = DoubleArrow(start=axes.c2p(xbar-sd,0), end=axes.c2p(xbar+sd,0), tip_length=0.1,
                              color=PURE_GREEN).move_to(meanDot.get_center())
        self.play(GrowFromCenter(sdArrow),run_time=2)
        self.wait(2)


        empMean = Tex("Empirical Mean (",str(numdots)," dots): ",str(round(xbar,3)),font_size=28,color=PURE_GREEN)
        theoryMean = Tex(r"Theoretical Mean ($\infty$ dots): $\dfrac{\pi}2-1 \approx 0.571$",font_size=28,color=BLACK)
        summary = VGroup(empMean,theoryMean).arrange(DOWN, aligned_edge=LEFT).shift(3.5*RIGHT+UP)
        self.play(FadeIn(summary))
        self.wait(6)

        empSD = Tex("Empirical SD (",str(numdots)," dots): ",str(round(sd,3)),font_size=28,color=PURE_GREEN)
        theorySD = Tex(r"Theoretical SD ($\infty$ dots): $\sqrt{\pi-3} \approx 0.376$", font_size=28, color=BLACK)
        summary2 = VGroup(empSD, theorySD).arrange(DOWN, aligned_edge=LEFT).next_to(summary,DOWN,buff=LARGE_BUFF,aligned_edge=LEFT)
        self.play(FadeIn(summary2))
        self.wait(5)
