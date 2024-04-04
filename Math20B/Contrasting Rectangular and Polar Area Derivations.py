from manim import *


class PADemo(Scene):
    def construct(self):

        # global constants
        skip = False
        tempo = 1.2
        self.camera.background_color = WHITE
        smallfontsize = 28
        mediumfontsize = 32
        largefontsize = 36
        labelcolor = PURE_BLUE

        def rectf(x):
            return 2 + 0.5 * np.sin(x)  # arbitrary looking function

        def polarf(theta):
            return 3 + 0.6 * np.cos(6 * theta)  # just a function that looks arbitrary

        ###########
        # section 1 - reminder of the rectangular partitioning process
        self.next_section(skip_animations=skip)
        rectaxes = Axes(x_range=[-1, 4], y_range=[-1, 3], x_length=8, y_length=6, tips=False)
        rectaxes.color = BLACK
        rectgraph = rectaxes.plot(rectf, x_range=[-0.5, 3.5, 0.01], color=PURE_RED)
        rectarea = rectaxes.get_area(rectgraph, x_range=[1, 3], color=RED)
        rectlabel = MathTex(r"y=f(x)", font_size=mediumfontsize, color=BLACK).move_to(rectaxes.c2p(3.5, 2.5))
        rectstart = MathTex(r"x=a", font_size=mediumfontsize, color=BLACK).next_to(rectaxes.c2p(1, 0), DOWN)
        rectend = MathTex(r"x=b", font_size=mediumfontsize, color=BLACK).next_to(rectaxes.c2p(3, 0), DOWN)
        numPartitions = 6
        rectpartition = rectaxes.get_riemann_rectangles(rectgraph, x_range=[1, 3], dx=(3 - 1) / numPartitions,
                                                        stroke_color=BLACK, fill_opacity=0.3,
                                                        color=[RED, BLUE], input_sample_type='right')
        rectgrp = VGroup(rectaxes, rectgraph, rectarea, rectlabel, rectstart, rectend, rectpartition)

        self.play(Succession(Create(rectaxes, run_time=2 * tempo), FadeIn(rectgraph, rectlabel, run_time=2 * tempo),
                             FadeIn(rectarea, run_time=2 * tempo), FadeIn(rectstart, rectend, run_time=2 * tempo),
                             Create(rectpartition, run_time=2 * tempo)))
        self.wait(2 * tempo)

        ###########
        # section 2 - show partition
        self.next_section(skip_animations=skip)
        segment = Line(rectaxes.c2p(2, 0), rectaxes.c2p(2.333, 0))
        brace = Brace(segment, DOWN, sharpness=4, color=labelcolor)
        deltax = MathTex(r"\Delta x", font_size=smallfontsize, color=labelcolor).next_to(brace, DOWN)
        rectlabel1 = MathTex(r"f(x_0)", font_size=smallfontsize, color=labelcolor).next_to(
            rectaxes.c2p(1, rectf(1) / 2), 0.5 * LEFT)
        rectlabel2 = MathTex(r"f(x_i)", font_size=smallfontsize, color=labelcolor).move_to(
            rectaxes.c2p(2.33, rectf(2.33) / 2))
        rectlabel3 = MathTex(r"f(x_n)", font_size=smallfontsize, color=labelcolor).next_to(
            rectaxes.c2p(3, rectf(3) / 2), 0.5 * RIGHT)
        self.play(FadeIn(brace, deltax, rectlabel1, rectlabel2, rectlabel3, run_time=2 * tempo))
        self.wait(3 * tempo)
        rlabelgrp = VGroup(brace, deltax, rectlabel1, rectlabel2, rectlabel3)
        self.play(VGroup(rectgrp, rlabelgrp).animate.to_edge(LEFT), run_time=2 * tempo)
        self.wait(2 * tempo)

        ###########
        # section 3 - show derivation
        self.next_section(skip_animations=skip)
        rderive = MathTex(r"\text{Area} &\approx \text{Sum of Rectangles}\\",
                          r"&\approx \sum_{i=1}^n f(x_i) \Delta x\\",
                          r"\text{Area} &= \lim_{n \to \infty} \sum_{i=1}^n f(x_i) \Delta x\\",
                          r" &= \boxed{\int_{x=a}^{x=b} f(x) \, dx}",
                          font_size=largefontsize, color=BLACK).next_to(rectgrp, RIGHT, buff=MED_LARGE_BUFF)
        self.play(Write(rderive[0]))
        self.wait(3 * tempo)
        self.play(Write(rderive[1]))
        self.wait(5 * tempo)
        self.play(FadeOut(rlabelgrp, run_time=2 * tempo))
        # show number of rectangles getting large
        numSlides = 25
        for n in range(7, 7 + numSlides):
            pic = rectaxes.get_riemann_rectangles(rectgraph, x_range=[1, 3], dx=(3 - 1) / n,
                                                  stroke_color=BLACK, fill_opacity=0.3,
                                                  color=[RED, BLUE], input_sample_type='right')
            self.play(Transform(rectpartition, pic), run_time=6 * tempo / numSlides)

        self.play(Write(rderive[2]))
        self.wait(3 * tempo)
        self.play(Write(rderive[3]))
        self.wait(6 * tempo)
        self.play(FadeOut(rectgrp, rderive, run_time=2 * tempo))
        self.wait(1 * tempo)

        ###########
        # section 4 - show polar area
        self.next_section(skip_animations=skip)
        polaraxes = PolarPlane(radius_max=4, radius_step=1, azimuth_step=8)
        polaraxes.x_axis.set_color(BLUE_D)
        polaraxes.y_axis.set_color(BLUE_D)
        polaraxes.add_coordinates().scale_to_fit_height(config.frame_height * 0.95)
        polaraxes.coordinate_labels.set_color(BLUE_D)
        polargraph = ParametricFunction(lambda t: polaraxes.polar_to_point(polarf(t), t), t_range=[-.5, 2, 0.01],
                                        color=PURE_GREEN)
        polarlabel = MathTex(r"r=f(\theta)", font_size=smallfontsize,
                             color=PURE_GREEN).next_to(polargraph.get_end(), 0.5 * UP + 0.5 * RIGHT)
        thetaa = 17 * DEGREES  # bounds that look arbitrary
        thetab = 73 * DEGREES

        lowerbound = Line(polaraxes.get_origin(), polaraxes.polar_to_point(polarf(thetaa), thetaa), color=PURE_GREEN)
        upperbound = Line(polaraxes.get_origin(), polaraxes.polar_to_point(polarf(thetab), thetab), color=PURE_GREEN)
        thetaalabel = MathTex(r"\theta=\alpha", font_size=smallfontsize,
                              color=PURE_GREEN).next_to(lowerbound.get_end(), RIGHT + 0.1 * UP)
        thetablabel = MathTex(r"\theta=\beta", font_size=smallfontsize,
                              color=PURE_GREEN).next_to(upperbound.get_end(), 1.6 * UP)
        self.play(Succession(FadeIn(polaraxes, run_time=2 * tempo), FadeIn(polargraph, polarlabel, run_time=2 * tempo),
                             FadeIn(lowerbound, upperbound, thetaalabel, thetablabel, run_time=2 * tempo)))

        # make polygon for area by specifying vertices
        vertices = [polaraxes.polar_to_point(0, 0)]
        for t in np.arange(thetaa, thetab, 0.01):
            vertices.append(polaraxes.polar_to_point(polarf(t), t))
        vertices.append(polaraxes.polar_to_point(0, 0))
        polararea = Polygon(*vertices, fill_color=[PURE_RED, PURE_BLUE], fill_opacity=0.3, stroke_color=BLACK)
        self.play(FadeIn(polararea, run_time=3 * tempo))
        self.wait(2 * tempo)
        polargrp = VGroup(polaraxes, polargraph, lowerbound, upperbound, polararea, thetaalabel, thetablabel,
                          polarlabel)
        self.play(polargrp.animate.scale(2).shift(3 * DOWN + 2 * LEFT),
                  run_time=2 * tempo)  # zoom in to make viz clearer
        self.wait(2 * tempo)

        ###########
        # section 5 - show polar partition
        self.next_section(skip_animations=skip)

        def getRiemannSectors(numsectors):
            thetastep = (thetab - thetaa) / numsectors
            sectors = VGroup()
            center = polaraxes.get_center()
            # use +thetastep in below line to get "right-endpoint" idea in polar
            for t in np.arange(thetaa + thetastep, thetab + thetastep, thetastep):
                pointoncurve = polaraxes.polar_to_point(polarf(t), t)
                length = np.linalg.norm(pointoncurve - center)
                sectors.add(Sector(arc_center=center, outer_radius=length,
                                   start_angle=t - thetastep, angle=thetastep, color=BLACK,
                                   fill_opacity=0.3, stroke_width=4, stroke_opacity=0.7))
            return sectors

        psectors = getRiemannSectors(6)
        polargrp.add(psectors)
        self.play(FadeIn(psectors, run_time=3 * tempo))
        self.wait(2 * tempo)
        deltatheta = MathTex(r"\Delta\theta", font_size=smallfontsize,
                             color=labelcolor).move_to(polaraxes.polar_to_point(1.25, PI / 4 - (thetaa - thetab) / 12))
        flabel1 = MathTex(r"f(\theta_0)", font_size=smallfontsize,
                          color=labelcolor).next_to(polaraxes.polar_to_point(1.5, thetaa), 0.5 * DOWN)
        flabel2 = MathTex(r"f(\theta_i)", font_size=smallfontsize,
                          color=labelcolor).next_to(polaraxes.polar_to_point(1.6, PI / 4), UP)
        flabel3 = MathTex(r"f(\theta_n)", font_size=smallfontsize,
                          color=labelcolor).next_to(polaraxes.polar_to_point(2.3, thetab), 0.5 * LEFT)
        plabelgrp = VGroup(deltatheta, flabel1, flabel2, flabel3)
        self.play(FadeIn(plabelgrp, run_time=3 * tempo))
        self.wait(2 * tempo)

        ###########
        # section 6 - show derivation
        self.next_section(skip_animations=skip)
        self.play(VGroup(polargrp, plabelgrp).animate.shift(4 * LEFT), run_time=3 * tempo)
        pderive = MathTex(r"\text{Area} &\approx \text{Sum of Sectors}\\",
                          r"&\approx \sum_{i=1}^n \dfrac12 f(\theta_i)^2 \Delta\theta\\",
                          r"\text{Area} &= \lim\limits_{n \to \infty} \dfrac12 \sum_{i=1}^n  f(\theta_i)^2 \Delta\theta\\",
                          r"&= \boxed{\dfrac12 \int_{\theta = \alpha}^{\theta = \beta} f(\theta)^2 \, d\theta}",
                          font_size=largefontsize, color=BLACK).next_to(polargrp, RIGHT, buff=MED_LARGE_BUFF).to_edge(
            DOWN)

        sector = Sector(outer_radius=2, angle=PI / 4, fill_opacity=0, stroke_width=4, stroke_color=BLACK)
        sectorrlabel = MathTex(r"r_i=f(\theta_i)", font_size=mediumfontsize, color=BLACK).next_to(sector, DOWN)
        sectortlabel = MathTex(r"\Delta\theta", font_size=mediumfontsize, color=BLACK).move_to([0.5, 0.25, 0])
        sectorformula = MathTex(r"\text{Sector area} = \dfrac12(\text{radius})^2 \cdot \text{angle}", font_size=28,
                                color=BLACK)
        sectorgrp = VGroup(VGroup(sector, sectortlabel, sectorrlabel),
                           sectorformula).arrange(DOWN).scale(0.8).move_to(pderive).to_edge(UP, buff=SMALL_BUFF)

        self.play(Write(pderive[0]))
        self.wait(3 * tempo)
        self.play(FadeIn(sectorgrp))
        self.wait(3 * tempo)
        self.play(Write(pderive[1]))
        self.wait(5 * tempo)
        self.play(FadeOut(plabelgrp, run_time=2 * tempo))
        # show number of sectors getting large
        numSlides = 30
        for n in range(7, 7 + numSlides):
            pic = getRiemannSectors(n)
            self.play(Transform(psectors, pic), run_time=6 * tempo / numSlides)

        self.play(Write(pderive[2]))
        self.wait(3 * tempo)
        self.play(Write(pderive[3]))
        self.wait(6 * tempo)
        self.play(FadeOut(polargrp, pderive, sectorgrp))
        self.wait(1 * tempo)

        ###########
        # section 7 - compare rectangular and polar approaches
        self.next_section(skip_animations=skip)
        rsummary = Tex(r"Partition the $x$ axis\\",
                       r"Rectangles created\\",
                       r"$\text{Area} = \displaystyle\int_{x=a}^{x=b} f(x) \, dx$",
                       font_size=largefontsize, color=BLACK)
        psummary = Tex(r"Partition the $\theta$ axis\\",
                       r"Sectors created\\",
                       r"Area $= \dfrac12 \displaystyle\int_{\theta=\alpha}^{\theta=\beta} f(\theta)^2 \, d\theta$",
                       font_size=largefontsize, color=BLACK)

        rectgrp.scale(0.75)
        rsumgrp = VGroup(*rsummary).arrange(DOWN, buff=MED_LARGE_BUFF)
        psumgrp = VGroup(*psummary).arrange(DOWN, buff=MED_LARGE_BUFF)
        polargrp.scale_to_fit_height(rectgrp.height)
        macrogrp = VGroup(VGroup(rectgrp, rsumgrp).arrange(DOWN, buff=LARGE_BUFF),
                          VGroup(polargrp, psumgrp).arrange(DOWN, buff=LARGE_BUFF)).arrange(RIGHT, buff=LARGE_BUFF)
        macrogrp.scale_to_fit_height(0.95 * config.frame_height)
        finalanims = [FadeIn(rectgrp, polargrp, run_time=4 * tempo),
                      *[Write(eq, run_time=4 * tempo) for eq in rsummary],
                      *[Write(eq, run_time=4 * tempo) for eq in psummary]]
        self.play(Succession(*finalanims))
        self.wait(4 * tempo)
