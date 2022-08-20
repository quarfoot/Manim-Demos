from manim import *


class ComplexNums(Scene):
    def construct(self):
        # Global constants
        skip = False
        medium = 24  # medium-sized font
        large = 36  # large-sized font

        ###########
        # section 1 - create plane, highlight vertical axis
        self.next_section(skip_animations=skip)

        # setup
        cplane = ComplexPlane(x_length=9, y_length=7).add_coordinates()
        rect = SurroundingRectangle(cplane.coordinate_labels[-8::])

        # animations
        self.play(DrawBorderThenFill(cplane))
        self.wait(1)
        self.play(Create(rect))
        self.wait(2)
        self.play(Uncreate(rect))
        self.wait(2)

        ###########
        # section 2 - explore relationship of z and its conjugate
        self.next_section(skip_animations=skip)

        # setup
        conjcolor = YELLOW
        dot = Dot(cplane.n2p(5 + 2j), color=conjcolor)
        lab = MathTex(r"z=5+2i", font_size=medium, color=conjcolor).next_to(dot, UR, buff=SMALL_BUFF)
        dot2 = Dot(cplane.n2p(5 - 2j), color=conjcolor)
        lab2 = MathTex(r"\overline{z}=5-2i", font_size=medium, color=conjcolor).next_to(dot2, DR, buff=SMALL_BUFF)
        arrow = CurvedArrow(start_point=dot.get_center(), end_point=dot2.get_top(),
                            color=conjcolor, radius=4)
        arrowtext = Tex(r"Conjugation reflects\\across the $x$ axis.",
                        font_size=medium, color=conjcolor).move_to(cplane.n2p(2.4 + 1.5j))

        # animations
        self.play(FadeIn(dot, lab))
        self.wait(2)
        self.play(TransformFromCopy(dot, dot2), run_time=2)
        self.play(FadeIn(lab2))
        self.wait(1)
        self.play(FadeIn(arrow, arrowtext))
        self.wait(4)
        self.play(FadeOut(dot2, lab2, arrow, arrowtext))
        self.wait(2)

        ###########
        # section 3 - explore relationship of z and its negative
        self.next_section(skip_animations=skip)

        # setup
        negativecolor = GREEN
        dot3 = Dot(cplane.n2p(-5 - 2j), color=negativecolor)
        lab3 = MathTex(r"-z=-5-2i", font_size=medium, color=negativecolor).next_to(dot3, DL, buff=SMALL_BUFF)
        arrow2 = Arrow(start=dot.get_center(), end=dot3.get_center(), color=negativecolor, buff=0)
        arrowtext2 = Tex(r"Negation reflects\\across the origin.",
                         font_size=medium, color=negativecolor).move_to(cplane.n2p(-2 + 0.5j))

        # animations
        self.play(TransformFromCopy(dot, dot3), run_time=2)
        self.play(FadeIn(lab3))
        self.wait(1)
        self.play(FadeIn(arrow2, arrowtext2))
        self.wait(4)
        self.play(FadeOut(dot, lab, dot3, lab3, arrow2, arrowtext2))
        self.wait(2)

        ###########
        # section 4 - begin four representations with specific point, to be continued on slides
        self.next_section(skip_animations=skip)
        self.play(cplane.animate.shift(5 * LEFT), run_time=2)

        # setup and animations interwoven as needed
        repcolor = RED
        dot4 = Dot(cplane.n2p(3 + 3j), color=repcolor)
        lab4 = MathTex(r"z=3+3i", font_size=medium, color=repcolor).next_to(dot4, UR, buff=SMALL_BUFF)
        self.play(FadeIn(dot4, lab4))

        divider = Line(3 * LEFT, 3 * RIGHT, color=repcolor)
        tex = MathTex(r"\text{Rectangular complex: }z=3+3i",
                      r"\text{Rectangular point: }(3,3)",
                      r"\text{Polar point: }(3\sqrt{2},45^\circ)",
                      r"\text{Polar complex: ?}", color=repcolor, font_size=large)
        grp = VGroup(tex[0], tex[1], divider, tex[2], tex[3]).arrange(DOWN, LARGE_BUFF).next_to(cplane)
        self.play(FadeIn(divider), Write(tex[0]))
        self.play(Write(tex[1]))
        self.wait(3)

        line = DashedLine(cplane.n2p(0 + 0j), cplane.n2p(3 + 3j), color=repcolor)
        line2 = DashedLine(cplane.n2p(3 + 0j), cplane.n2p(3 + 3j), color=repcolor)
        theta = MathTex(r"45^\circ", font_size=medium, color=repcolor).move_to(cplane.n2p(0.65 + 0.25j))
        hypo = MathTex(r"3\sqrt{2}", font_size=medium, color=repcolor).next_to(cplane.n2p(1.5 + 1.8j), UP)
        self.play(FadeIn(line, line2))
        self.wait()
        self.play(FadeIn(theta, hypo))
        self.wait()
        self.play(Write(tex[2]))
        self.wait()
        self.play(Write(tex[3]))
        self.wait(4)