import numpy as np
from manim import *

class PADemo(Scene):
    def construct(self):

        # global constants
        skip = False
        smallfontsize = 20
        mediumfontsize = 28
        largefontsize = 36
        labelcolor = BLUE

        def rectf(x):
            return 2+0.5*np.sin(x)  # arbitrary looking function

        def polarf(theta):
            return 3+0.6*np.cos(6*theta)  # just a function that looks arbitrary


        ###########
        # section 1 - reminder of the rectangular partitioning process
        self.next_section(skip_animations=skip)
        rectaxes = Axes(x_range=[-1,4], y_range=[-1,3], x_length=8, y_length=6, tips=False)
        rectgraph = rectaxes.plot(rectf, x_range=[-0.5,3.5,0.01], color=GREEN)
        rectarea = rectaxes.get_area(rectgraph, x_range=[1,3], color=[RED,BLUE])
        rectlabel = MathTex(r"y=f(x)",font_size=mediumfontsize).move_to(rectaxes.c2p(3.5,2.5))
        rectstart = MathTex(r"x=a",font_size=mediumfontsize).next_to(rectaxes.c2p(1,0),DOWN)
        rectend = MathTex(r"x=b", font_size=mediumfontsize).next_to(rectaxes.c2p(3, 0), DOWN)
        numPartitions = 6
        rectpartition = rectaxes.get_riemann_rectangles(rectgraph,x_range=[1,3], dx =(3-1)/numPartitions,
                                                        stroke_color=WHITE, fill_opacity=0.3)
        rectgrp = VGroup(rectaxes,rectgraph,rectarea,rectlabel,rectstart,rectend,rectpartition)

        self.play(Succession(Create(rectaxes),FadeIn(rectgraph, rectlabel),FadeIn(rectarea),
                             FadeIn(rectstart,rectend),Create(rectpartition)))
        self.wait(2)


        ###########
        # section 2 - show partition
        self.next_section(skip_animations=skip)
        segment = Line(rectaxes.c2p(2,0),rectaxes.c2p(2.333,0))
        brace = Brace(segment,DOWN, sharpness=4, color=labelcolor)
        deltax = MathTex(r"\Delta x", font_size=smallfontsize, color=labelcolor).next_to(brace,DOWN)
        rectlabel1 = MathTex(r"f(x_0)", font_size=smallfontsize, color=labelcolor).next_to(rectaxes.c2p(1,rectf(1)/2),0.5*LEFT)
        rectlabel2 = MathTex(r"f(x_i)", font_size=smallfontsize, color=labelcolor).move_to(rectaxes.c2p(2,rectf(2)/2))
        rectlabel3 = MathTex(r"f(x_n)", font_size=smallfontsize, color=labelcolor).next_to(rectaxes.c2p(3,rectf(3)/2),0.5*RIGHT)
        self.play(FadeIn(brace,deltax,rectlabel1,rectlabel2,rectlabel3))
        self.wait(2)
        rectgrp.add(brace,deltax,rectlabel1,rectlabel2,rectlabel3)
        self.play(rectgrp.animate.to_edge(LEFT))
        self.wait(2)


        ###########
        # section 3 - show derivation
        self.next_section(skip_animations=skip)
        rderive = MathTex(r"\text{Area} &\approx \text{Sum of Rectangles}\\",
                          r"&\approx \sum_{i=1}^n f(x_i) \Delta x\\",
                          r"\text{Area} &= \lim_{n \to \infty} \sum_{i=1}^n f(x_i) \Delta x\\",
                          r" &= \boxed{\int_{x=a}^{x=b} f(x) \, dx}",
                          font_size=largefontsize).next_to(rectgrp,RIGHT,buff=MED_LARGE_BUFF)
        writeAnims = [Write(eq) for eq in rderive]
        self.play(LaggedStart(*writeAnims,lag_ratio=2))
        self.wait(4)
        self.play(FadeOut(rectgrp,rderive))
        self.wait(1)


        ###########
        # section 4 - show polar area
        self.next_section(skip_animations=skip)
        polaraxes = PolarPlane(radius_max=4, radius_step=1, azimuth_step=8)
        polaraxes.add_coordinates().scale_to_fit_height(config.frame_height*0.95)
        polargraph = ParametricFunction(lambda t: polaraxes.polar_to_point(polarf(t),t), t_range=[-.5,2,0.01],
                                        color=GREEN)
        polarlabel = MathTex(r"r=f(\theta)", font_size=smallfontsize,
                             color=GREEN).next_to(polargraph.get_end(),0.5*UP +0.5*RIGHT)
        thetaa = 17 * DEGREES  # bounds that look arbitrary
        thetab = 73 * DEGREES

        lowerbound = Line(polaraxes.get_origin(),polaraxes.polar_to_point(polarf(thetaa),thetaa), color=BLUE)
        upperbound = Line(polaraxes.get_origin(),polaraxes.polar_to_point(polarf(thetab),thetab), color=BLUE)
        thetaalabel = MathTex(r"\theta=\alpha", font_size=smallfontsize,
                              color=labelcolor).next_to(lowerbound.get_end(), RIGHT+0.1*UP)
        thetablabel = MathTex(r"\theta=\beta", font_size=smallfontsize,
                              color=labelcolor).next_to(upperbound.get_end(), 1.6*UP)
        self.play(LaggedStart(FadeIn(polaraxes), FadeIn(polargraph, polarlabel),
                             FadeIn(lowerbound,upperbound,thetaalabel,thetablabel),lag_ratio=2))

        # make polygon for area by specifying vertices
        vertices = [polaraxes.polar_to_point(0,0)]
        for t in np.arange(thetaa,thetab,0.01):
            vertices.append(polaraxes.polar_to_point(polarf(t),t))
        vertices.append(polaraxes.polar_to_point(0, 0))
        polararea = Polygon(*vertices,fill_color=[RED,BLUE], fill_opacity=0.3)
        self.play(FadeIn(polararea))
        self.wait()
        polargrp = VGroup(polaraxes,polargraph,lowerbound,upperbound,polararea,thetaalabel,thetablabel,polarlabel)
        self.play(polargrp.animate.scale(2).shift(3*DOWN+2*LEFT), run_time=2)  # zoom in to make viz clearer
        self.wait()


        ###########
        # section 5 - show polar partition
        self.next_section(skip_animations=skip)
        numsectors = 6
        thetastep = (thetab-thetaa)/numsectors
        sectors = VGroup()
        center = polaraxes.get_center()
        for t in np.arange(thetaa,thetab,thetastep):
            pointoncurve = polaraxes.polar_to_point(polarf(t),t)
            length = np.linalg.norm(pointoncurve-center)
            sectors.add(Sector(arc_center=center,outer_radius=length,
                               start_angle=t, angle=thetastep, color=WHITE,
                               fill_opacity=0.3, stroke_width=4, stroke_opacity=0.7))
        self.play(FadeIn(sectors))
        self.wait()
        deltatheta = MathTex(r"\Delta\theta", font_size=smallfontsize,
                             color=labelcolor).move_to(polaraxes.polar_to_point(1.25,PI/4-thetastep/2))
        flabel1 = MathTex(r"f(\theta_0)", font_size=smallfontsize,
                          color=labelcolor).next_to(polaraxes.polar_to_point(1.5,thetaa),0.5*DOWN)
        flabel2 = MathTex(r"f(\theta_i)", font_size=smallfontsize,
                          color=labelcolor).next_to(polaraxes.polar_to_point(1.6, PI/4),UP)
        flabel3 = MathTex(r"f(\theta_n)", font_size=smallfontsize,
                          color=labelcolor).next_to(polaraxes.polar_to_point(2.3, thetab),0.5*LEFT)
        self.play(FadeIn(deltatheta,flabel1,flabel2,flabel3))
        self.wait(2)
        polargrp.add(sectors,deltatheta,flabel1,flabel2,flabel3)


        ###########
        # section 6 - show derivation
        self.next_section(skip_animations=skip)
        self.play(polargrp.animate.shift(4*LEFT))
        pderive = MathTex(r"\text{Area} &\approx \text{Sum of Sectors}\\",
                          r"&\approx \sum_{i=1}^n \dfrac12 f(\theta_i)^2 \Delta\theta\\",
                          r"\text{Area} &= \lim\limits_{n \to \infty} \dfrac12 \sum_{i=1}^n  f(\theta_i)^2 \Delta\theta\\",
                          r"&= \boxed{\dfrac12 \int_{\theta = \alpha}^{\theta = \beta} f(\theta)^2 \, d\theta}",
                          font_size=largefontsize).next_to(polargrp,RIGHT,buff=MED_LARGE_BUFF).to_edge(DOWN)


        sector = Sector(outer_radius=2,angle=PI/4, fill_opacity=0,stroke_width=4, stroke_color=WHITE)
        sectorrlabel = MathTex(r"r_i=f(\theta_i)",font_size=mediumfontsize,color=labelcolor).next_to(sector,DOWN)
        sectortlabel = MathTex(r"\Delta\theta",font_size=mediumfontsize,color=labelcolor).move_to([0.5,0.25,0])
        sectorformula = MathTex(r"\text{Sector area} = \dfrac12(\text{radius})^2 \cdot \text{angle}", font_size=28)
        sectorgrp = VGroup(VGroup(sector,sectortlabel,sectorrlabel),
                           sectorformula).arrange(DOWN).scale(0.8).move_to(pderive).to_edge(UP,buff=SMALL_BUFF)

        self.play(Write(pderive[0]))
        self.wait()
        self.play(FadeIn(sectorgrp))
        self.wait(2)
        self.play(LaggedStart(*[Write(eq) for eq in pderive[1::]],lag_ratio=2))
        self.wait(4)
        self.play(FadeOut(polargrp,sectorgrp,pderive))
        self.wait()


        ###########
        # section 7 - compare rectangular and polar approaches
        self.next_section(skip_animations=skip)
        rsummary = Tex(r"Partition the $x$ axis\\",
                       r"Rectangles created\\",
                       r"$\text{Area} = \displaystyle\int_{x=a}^{x=b} f(x) \, dx$",
                       font_size=largefontsize)
        psummary = Tex(r"Partition the $\theta$ axis\\",
                       r"Sectors created\\",
                       r"Area $= \dfrac12 \displaystyle\int_{\theta=\alpha}^{\theta=\beta} f(\theta)^2 \, d\theta$",
                       font_size=largefontsize)

        rectgrp.scale(0.75)
        rsumgrp = VGroup(*rsummary).arrange(DOWN,buff=MED_LARGE_BUFF)
        psumgrp = VGroup(*psummary).arrange(DOWN,buff=MED_LARGE_BUFF)
        polargrp.scale_to_fit_height(rectgrp.height)
        macrogrp = VGroup(VGroup(rectgrp,rsumgrp).arrange(DOWN, buff=LARGE_BUFF),
                          VGroup(polargrp,psumgrp).arrange(DOWN, buff=LARGE_BUFF)).arrange(RIGHT,buff=LARGE_BUFF)
        macrogrp.scale_to_fit_height(0.95 * config.frame_height)
        finalanims = [FadeIn(rectgrp,polargrp), *[Write(eq) for eq in rsummary], *[Write(eq) for eq in psummary]]
        self.play(LaggedStart(*finalanims,lag_ratio=2.5))
        self.wait(4)