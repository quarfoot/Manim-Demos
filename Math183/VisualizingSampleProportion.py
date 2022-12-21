import numpy as np
from manim import *
from numpy.random import default_rng

class phatViz(Scene):
    def construct(self):

        ##################
        # Global variables
        skip=False
        self.camera.background_color = WHITE
        p = 0.7  # the true population proportion (unknown to us)
        n = 100  # sample size (known to us)

        #################
        # MAIN ANIMATIONS

        ############
        # Intro text
        self.next_section(skip_animations=skip)
        main = Tex(r"Visualizing the Distribution of the Sample Proportion\\",
                   r"$\widehat{p} \approx N\left(p,\sqrt{\dfrac{pq}{n}}\right)$",
                   font_size=40, color=BLACK).arrange(DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeIn(main, shift=UP, run_time=2))
        self.wait(4)
        self.play(FadeOut(main))


        ###################
        # Show first sample
        self.next_section(skip_animations=skip)
        rectShift = 4*LEFT+1.5*UP
        rectWidth = 4
        rectHeight = 3
        rect = Rectangle(width=rectWidth,height=rectHeight,color=BLACK, fill_color=WHITE).shift(rectShift)
        rectText = Tex("Population ($p=0.7$)", font_size=28, color=BLACK).next_to(rect,UP, buff=SMALL_BUFF)
        rng = default_rng()

        self.play(Create(rect))
        self.wait()
        self.play(Write(rectText))
        self.wait(5)

        dots = VGroup()
        greenDots = VGroup()
        redDots = VGroup()
        dotColors = []
        dotRadius = 0.04
        a = rectWidth/2 - dotRadius   # avoid dots falling on edge of rectangle
        b = rectHeight/2 - dotRadius
        for i in range(n):
            loc = [rng.uniform(-a,a),rng.uniform(-b,b),0] + rectShift
            dot = Dot(loc,color=BLACK,radius=dotRadius)
            if rng.uniform(0,1) < p:
                color = PURE_GREEN
                greenDots += dot
            else:
                color = PURE_RED
                redDots += dot
            dotColors.append(color)
            dots += dot

        self.play(LaggedStart(*[FadeIn(dot) for dot in dots], run_time=3))
        self.wait(3)
        self.play(*[dot.animate.set_color(color) for dot, color in zip(dots,dotColors)])
        self.wait(2)


        ###################
        # Create first phat
        self.next_section(skip_animations=skip)
        sfont = 30 # font size for text when doing summary (finding phat)
        yesText = Tex(r"\underline{Yes}", color=PURE_GREEN, font_size=sfont)
        noText = Tex(r"\underline{No}", color=PURE_RED, font_size=sfont)
        summary = VGroup(yesText,noText).arrange(RIGHT, buff=LARGE_BUFF).next_to(rect, DOWN, buff=MED_LARGE_BUFF)

        self.play(FadeIn(summary, shift=UP))
        self.wait()

        numS = len(greenDots)  # number of successes
        yesCount = Integer(numS, color=PURE_GREEN, font_size=sfont).next_to(yesText,DOWN)
        noCount = Integer(n-numS, color=PURE_RED, font_size=sfont).next_to(noText,DOWN)
        self.play(TransformFromCopy(greenDots,yesCount),
                  TransformFromCopy(redDots,noCount),
                  run_time=2)
        self.wait()

        phat = r"\widehat{p} =\dfrac{"+str(numS)+r"}{100} = 0."+str(numS)
        print(phat)
        phatText = MathTex(phat,
                           color=BLACK, font_size=sfont).next_to(VGroup(yesCount,noCount),DOWN,MED_LARGE_BUFF)
        self.play(FadeIn(phatText, shift=UP))
        self.wait(3)
        self.play(phatText[0][-4:].animate.set_color(PURE_BLUE))
        self.wait()


        #####################
        # Start dot histogram
        self.next_section(skip_animations=skip)
        line = NumberLine(x_range=[p-0.12, p+0.12, 0.02],length=7,decimal_number_config={"num_decimal_places": 2},
                          include_numbers=True, color=BLACK, font_size=20).shift(RIGHT*2.8)
        line.numbers.set_color(BLACK)
        self.play(FadeIn(line, shift=UP))
        self.wait()

        histDotRadius = 0.06
        newDot = Dot(line.n2p(numS/n) + UP*histDotRadius * 2, color=PURE_BLUE, radius=histDotRadius)
        pHatList = [numS/n]
        self.play(TransformFromCopy(phatText[0][-4:],newDot))
        self.wait(4)

        self.play(FadeOut(dots,yesText,yesCount,noText,noCount,phatText), run_time=2)
        self.wait()


        #################################
        # Make next few dots of histogram
        self.next_section(skip_animations=skip)

        def phatSample(showSample = True, sampleTime = 3, dotDropTime = 1, waitTime = 1, fadeOutTime = 1):
            dots = VGroup()
            sCount = 0
            for i in range(n):
                loc = [rng.uniform(-a,a),rng.uniform(-b,b),0] + rectShift
                dot = Dot(loc,color=PURE_RED,radius=dotRadius)
                if rng.uniform(0,1) < p:
                    dot.set_color(PURE_GREEN)
                    sCount += 1
                dots += dot

            phat = sCount/n
            pHatList.append(phat)
            pHatArray = np.array(pHatList)
            howMany = sum(pHatArray == phat)
            newDot = Dot(line.n2p(phat) + howMany * UP * histDotRadius * 2, color=PURE_BLUE, radius=histDotRadius)
            if showSample:
                self.play(LaggedStart(*[FadeIn(dot) for dot in dots], run_time=sampleTime))
                self.wait(waitTime)

            self.play(FadeIn(newDot,shift=DOWN, run_time=dotDropTime))

            if showSample:
                self.play(FadeOut(dots, run_time=fadeOutTime))

        sampleTimes = [3,2,1,0.5]
        waitTimes = [1,1,0.5,0.5]
        fadeOutTimes = [1,1,0.5,0.5]
        for i in range(4):
            phatSample(True,sampleTimes[i],1,waitTimes[i],fadeOutTimes[i])
        self.wait(1)

        ##################
        # Finish histogram
        self.next_section(skip_animations=skip)

        moreDots = 200 # how many more dots to add
        anims = []

        for i in range(moreDots):
            newPHat = 0.4
            while newPHat < 0.58 or newPHat > 0.82:  # want values in picture range
                newPHat = rng.binomial(n,p)/n
            pHatList.append(newPHat)
            pHatArray = np.array(pHatList)
            howMany = sum(pHatArray == newPHat)
            newDot = Dot(line.n2p(newPHat) + howMany * UP * histDotRadius * 2, color=PURE_BLUE, radius=histDotRadius)
            anims.append(FadeIn(newDot, shift=DOWN, run_time=0.5))

        self.play(LaggedStart(*anims, run_time=10))
        self.play(FadeOut(rect, rectText))
        self.wait(2)
        self.play(*[obj.animate.shift(2.8*LEFT) for obj in self.mobjects])
        self.wait(2)

        #############################################################
        # Draw theoretical distribution and check raw data against it
        self.next_section(skip_animations=skip)
        ourMean = round(np.average(pHatArray),ndigits=3)
        ourSD = round(np.std(pHatArray), ndigits=3)

        theory = Tex(r"Theoretically: $\widehat{p} \approx N\left(p, \sqrt{\dfrac{pq}{n}}\right)$",
                     r"$\phantom{} \approx N(0.7,0.046)$", color=PURE_RED,font_size=24)
        data1 = Tex(r"Shape of our $\widehat{p}$s $\approx \phantom{}$","Normal", color=PURE_BLUE,font_size=24)
        data2 = Tex(r"Mean of our $\widehat{p}$s $\approx \phantom{}$",str(ourMean), color=PURE_BLUE,font_size=24)
        data3 = Tex(r"SD of our $\widehat{p}$s $\approx \phantom{}$", str(ourSD), color=PURE_BLUE, font_size=24)
        allText = VGroup(theory,data1,data2,data3).\
            arrange(DOWN, buff=1.8*MED_SMALL_BUFF).next_to(line,DOWN,1.8*MED_SMALL_BUFF)

        objs = [theory[0],theory[1]]
        self.play(LaggedStart(*[FadeIn(obj,shift=UP) for obj in objs], lag_ratio=6))
        self.wait(4)
        axes = Axes(x_range=[0.58,0.82,0.02], x_length=7, y_range=[0,6], y_length=2)

        mu = p
        var = p*(1-p)/n
        def ourPDF(x):
            return 1/np.sqrt(2*PI*var)*np.exp(-(x-mu)**2/(2*var))

        graph = axes.plot(ourPDF, x_range=[0.58,0.82],color=PURE_RED).shift(UP)
        self.play(FadeIn(graph))
        self.wait(3)

        objs = [data1[0],data1[1],data2[0],data2[1],data3[0],data3[1]]
        self.play(LaggedStart(*[FadeIn(obj, shift=UP) for obj in objs], lag_ratio=4))
        self.wait(5)