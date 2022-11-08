from manim import *

class USubDemo(Scene):
    def construct(self):

        title1 = Tex(r"Typical $u$-substitution")
        tex1 = MathTex(r"\int_0^{\pi/2} e^{\sin x} \cos x \, dx")
        tex2 = Tex(r"Let $u=\sin x$, so $du = \cos x \, dx$")
        tex3 = Tex(r"UL: $u=\sin \pi/2 = 1$, LL: $u=\sin 0 = 0$")
        tex4 = MathTex(r"\int_0^1 e^u \, du")
        tex5 = Tex(r"$\bullet$ Both $u$ and $du$ present in integrand", color=BLUE)
        tex6 = Tex(r"$\bullet$ Collapsing only", color=BLUE)

        grp1 = VGroup(title1,tex1,tex2,tex3,tex4,tex5,tex6).arrange(DOWN, buff=1)

        line = DashedLine(6*UP, 6*DOWN)

        title2 = Tex(r"Atypical $u$-substitution")
        btex1 = MathTex(r"\int_{-1}^7 x \sqrt{2x+2} \, dx")
        btex2 = Tex(r"Let $u=\sqrt{2x+2}$, so $x=\frac{1}{2}u^2-1$ and $dx = u \, du$")
        btex3 = Tex(r"UL:  $u=\sqrt{2\cdot 7 +2}=4$, LL:  $u=\sqrt{2\cdot -1 + 2} = 0$")
        btex4 = MathTex(r"\int_0^4 \left( \frac12 u^2-1 \right) \cdot u \cdot u \, du")
        btex5 = Tex(r"$\bullet$ Only $u$ present", color=BLUE)
        btex6 = Tex(r"$\bullet$ Collapse and expansion occur", color=BLUE)

        grp2 = VGroup(title2,btex1,btex2,btex3,btex4,btex5,btex6).arrange(DOWN, buff=1)

        grp = VGroup(grp1,line,grp2).arrange(RIGHT, buff=0.75).scale(0.5).center()

        title = Title(r"Comparing Two Types of $u$-Substitution",font_size=36)
        macrogrp = VGroup(title,grp).arrange(DOWN)

        self.next_section(skip_animations=False)

        self.play(FadeIn(title))
        self.play(FadeIn(title1,title2,shift=RIGHT), Create(line))
        self.wait()

        # Left column animations
        self.play(FadeIn(tex1,btex1,shift=RIGHT))
        self.wait(2)
        self.play(FadeIn(tex2,shift=RIGHT))
        self.wait()
        self.play(tex2[0][3:9].animate.set_color(RED),tex1[0][6:10].animate.set_color(RED), run_time=1.5)
        self.play(tex2[0][12:21].animate.set_color(YELLOW), tex1[0][10:16].animate.set_color(YELLOW), run_time=1.5)

        self.play(FadeIn(tex3,shift=RIGHT))
        self.wait()

        self.play(FadeIn(tex4[0][0:4]))
        self.play(TransformFromCopy(tex1[0][6:10], tex4[0][4].set_color(RED)), run_time=2)
        self.play(TransformFromCopy(tex1[0][10:16], tex4[0][5:7].set_color(YELLOW)), run_time=2)

        self.play(FadeIn(tex5, shift=RIGHT),
                  FadeIn(tex6, shift=RIGHT),
                  run_time=2)

        # right column animations
        self.play(FadeIn(btex2, shift=RIGHT))
        self.wait()
        self.play(btex2[0][3:11].animate.set_color(RED), btex1[0][5:11].animate.set_color(RED), run_time=1.5)
        self.play(btex2[0][14:23].animate.set_color(PURE_GREEN), btex1[0][4].animate.set_color(PURE_GREEN), run_time=1.5)
        self.play(btex2[0][26::].animate.set_color(YELLOW), btex1[0][11::].animate.set_color(YELLOW), run_time=1.5)

        self.play(FadeIn(btex3, shift=RIGHT))
        self.wait()

        grp3 = VGroup(btex4[0][0:3],btex4[0][12],btex4[0][14])
        self.play(FadeIn(grp3))
        self.play(TransformFromCopy(btex1[0][5:11], btex4[0][13].set_color(RED)), run_time=2)
        self.play(TransformFromCopy(btex1[0][4], btex4[0][3:12].set_color(PURE_GREEN)), run_time=2)
        self.play(TransformFromCopy(btex1[0][11::], btex4[0][15::].set_color(YELLOW)), run_time=2)

        self.play(FadeIn(btex5, shift=RIGHT),
                  FadeIn(btex6, shift=RIGHT),
                  run_time=2)
        self.wait(1)

        self.play(TransformFromCopy(btex1[0][5:11], btex4[0][13].copy()),
                  TransformFromCopy(btex1[0][4], btex4[0][3:12].copy()),
                  TransformFromCopy(btex1[0][11::], btex4[0][15::].copy()),
                  TransformFromCopy(tex1[0][6:10], tex4[0][4].copy()),
                  TransformFromCopy(tex1[0][10:16], tex4[0][5:7].copy()),
                  run_time=2)

        rect1 = SurroundingRectangle(tex6, color=GOLD)
        rect2 = SurroundingRectangle(btex6, color=GOLD)
        self.play(LaggedStart(Create(rect1),Create(rect2)),run_time=2)

        self.play(TransformFromCopy(btex1[0][5:11], btex4[0][13].copy()),
                  TransformFromCopy(btex1[0][4], btex4[0][3:12].copy()),
                  TransformFromCopy(btex1[0][11::], btex4[0][15::].copy()),
                  TransformFromCopy(tex1[0][6:10], tex4[0][4].copy()),
                  TransformFromCopy(tex1[0][10:16], tex4[0][5:7].copy()),
                  run_time=2)

        self.play(LaggedStart(Uncreate(rect1), Uncreate(rect2)), run_time=1)
        self.wait()
