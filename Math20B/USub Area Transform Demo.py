from manim import *

class usubDemo(Scene):
    def construct(self):

        # function for demo
        def func1(x):
            return np.sqrt(np.log(x))/x

        #################################
        # Set up all features to appear #
        #################################

        # main images and text
        text1 = Tex(r"Find the area under $f(x)=\frac{\sqrt{\ln x}}{x}$ from $1$ to $e^2$.", font_size=56)
        plane = NumberPlane(x_range=[-1, 9, 1], y_range=[-0.25, 1.5, 0.5], x_length=10, y_length=8, color=GREEN)
        graph = plane.plot(func1, x_range=[1,9,0.05], color=GREEN)
        label = plane.get_graph_label(graph,Tex(r"$y=\dfrac{\sqrt{\ln x}}{x}$",
                                                color=GREEN,font_size=30)).shift(LEFT*0.25+RIGHT*0.5)
        area = plane.get_area(graph, x_range=[1,np.e**2], color=GREEN, opacity=0.5)
        plot1 = VGroup(plane,graph,area,label)
        grp1 = VGroup(text1, plot1).arrange(DOWN)
        text2 = MathTex(r"\int_{1}^{e^2} \frac{\sqrt{\ln x}}{x} \,  dx", color=GREEN, font_size=36)
        text3 = Tex(r"Let $u=\ln x$, so $du=\frac{1}{x} \,dx$", font_size=28)
        arrow = Arrow(start=3*LEFT, end=3*RIGHT, stroke_width=1)
        text4 = Tex(r"LB: $u=\ln 1 = 0$\\UB:  $u=\ln e^2 = 2$", font_size=28)
        grp2 = VGroup(text3,arrow,text4).arrange(DOWN, buff=SMALL_BUFF)
        text5 = MathTex(r"\int_{0}^{2} \sqrt{u} \, du", color=RED, font_size=36)
        bottomgrp = VGroup(text2,grp2,text5).arrange(RIGHT, buff=LARGE_BUFF)
        fullgrp = VGroup(grp1,bottomgrp).arrange(DOWN, buff=MED_SMALL_BUFF).scale_to_fit_height(0.95*config.frame_height)

        # arrows for transformation
        a1 = CurvedArrow(start_point=plane.c2p(1,0),end_point=plane.c2p(0,0),
                         color = RED, tip_length=0.1)
        a2 = CurvedArrow(start_point=plane.c2p(np.e**2,0),end_point=plane.c2p(2,0),
                         color = RED, tip_length=0.1, radius=4)
        a3 = CurvedArrow(start_point=plane.c2p(np.e,0),end_point=plane.c2p(1,0),
                         color = RED, tip_length=0.1)

        # special labels
        fsf = 0.5 # font scale factor
        lab1 = Tex("$1$", color=GREEN).scale(fsf)
        lab1.next_to(plane.c2p(1,0),0.5*DL)
        lab2 = Tex("$e^2$", color=GREEN).scale(fsf)
        lab2.next_to(plane.c2p(np.e**2, 0),0.5*DOWN)

        # transformed stuff
        newlab1 = Tex("0", color=RED).scale(fsf)
        newlab1.next_to(plane.c2p(0,0),0.5*DL)
        newlab2 = Tex("2", color=RED).scale(fsf)
        newlab2.next_to(plane.c2p(2, 0),0.5*DL)
        newGraph = plane.plot(lambda x: np.sqrt(x), x_range=[0, 2, 0.05], color=RED)
        newArea = plane.get_area(newGraph, x_range=[0,2], color=RED)
        newLabel = plane.get_graph_label(newGraph,Tex(r"$y=\sqrt{u}$",
                                                      color=RED, font_size=30)).shift(0.75*LEFT+0.5*DOWN)

        xvals = [*np.arange(1,8),np.e**2]
        xpoints = VGroup()
        xlines = VGroup()
        xColor = GREEN
        for x in xvals:
            coords = plane.c2p(x,func1(x))
            xpoints.add(Dot(coords, color=xColor))
            xlines.add(plane.get_vertical_line(coords, color=xColor))

        newxvals = np.log(xvals)
        newxpoints = VGroup()
        newxlines = VGroup()
        newxColor = RED
        for x in newxvals:
            coords = plane.c2p(x,np.sqrt(x))
            newxpoints.add(Dot(coords, color=newxColor))
            newxlines.add(plane.get_vertical_line(coords, color=newxColor))

        ##############
        # Animations #
        ##############
        self.play(Write(text1))
        self.play(Create(plane))
        self.play(FadeIn(graph,label))
        self.wait()
        self.play(FadeIn(lab1,lab2,area))
        self.wait()

        self.play(Write(text2))
        self.wait()
        self.play(Create(arrow))
        self.play(Write(text3))
        self.wait()
        self.play(Write(text4))
        self.wait()
        self.play(Write(text5))
        self.wait()

        self.play(Create(a1), FadeIn(newlab1))
        self.wait()
        self.play(Create(a2), FadeIn(newlab2))
        self.wait(2)
        self.play(FadeIn(xpoints, xlines))
        self.wait()
        self.play(TransformFromCopy(xpoints, newxpoints),
                  TransformFromCopy(xlines, newxlines),
                  run_time=2)
        self.play(FadeIn(newGraph,newArea,newLabel))
        self.wait()
        # repeat for emphasis
        self.play(TransformFromCopy(xpoints, newxpoints.copy()),
                  TransformFromCopy(xlines, newxlines.copy()),
                  TransformFromCopy(label, newLabel.copy()),
                  run_time=3)
        self.wait()
