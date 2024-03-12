from manim import *


class USubDemo(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        title1 = Tex(r"Typical $u$-substitution", color=BLACK)
        tex1 = MathTex(r"\int_0^{\pi/2} e^{\sin x} \cos x \, dx", color=BLACK)
        tex2 = Tex(r"Let $u=\sin x$, so $du = \cos x \, dx$", color=BLACK)
        tex3 = Tex(r"UB: $u=\sin \pi/2 = 1$, LB: $u=\sin 0 = 0$", color=BLACK)
        tex4 = MathTex(r"\int_0^1 e^u \, du", color=BLACK)
        tex5 = Tex(r"$\bullet$ Both $u$ and $du$ present in integrand", color=BLACK)
        tex6 = Tex(r"$\bullet$ Collapsing only", color=BLACK)

        grp1 = VGroup(title1, tex1, tex2, tex3, tex4, tex5, tex6).arrange(DOWN, buff=1)

        line = DashedLine(6 * UP, 6 * DOWN, color=BLACK)

        title2 = Tex(r"Atypical $u$-substitution", color=BLACK)
        btex1 = MathTex(r"\int_{-1}^7 x \sqrt{2x+2} \, dx", color=BLACK)
        btex2 = Tex(r"Let $u=\sqrt{2x+2}$, so $x=\frac{1}{2}u^2-1$ and $dx = u \, du$", color=BLACK)
        btex3 = Tex(r"UB:  $u=\sqrt{2\cdot 7 +2}=4$, LB:  $u=\sqrt{2\cdot -1 + 2} = 0$", color=BLACK)
        btex4 = MathTex(r"\int_0^4 \left( \frac12 u^2-1 \right) \cdot u \cdot u \, du", color=BLACK)
        btex5 = Tex(r"$\bullet$ Only $u$ present", color=BLACK)
        btex6 = Tex(r"$\bullet$ Collapse and expansion occur", color=BLACK)

        grp2 = VGroup(title2, btex1, btex2, btex3, btex4, btex5, btex6).arrange(DOWN, buff=1)

        grp = VGroup(grp1, line, grp2).arrange(RIGHT, buff=0.75).scale(0.5).center()

        title = Title(r"Comparing Two Types of $u$-Substitution", font_size=36, color=BLACK)
        macrogrp = VGroup(title, grp).arrange(DOWN)

        ##############
        # ANIMATIONS #
        ##############
        tempo = 2

        self.next_section(skip_animations=False)

        self.play(FadeIn(title), run_time=tempo)
        self.wait(tempo)
        self.play(FadeIn(title1, title2, shift=RIGHT), Create(line), run_time=tempo)
        self.wait(2 * tempo)

        # Left column animations
        self.play(FadeIn(tex1, btex1, shift=RIGHT), run_time=tempo)
        self.wait(2 * tempo)
        self.play(FadeIn(tex2, shift=RIGHT), run_time=tempo)
        self.wait(tempo)
        self.play(tex2[0][3:9].animate.set_color(PURE_RED), tex1[0][6:10].animate.set_color(PURE_RED),
                  run_time=1.5 * tempo)
        self.play(tex2[0][12:21].animate.set_color(PURE_BLUE), tex1[0][10:16].animate.set_color(PURE_BLUE),
                  run_time=1.5 * tempo)

        self.play(FadeIn(tex3, shift=RIGHT), run_time=tempo)
        self.wait(tempo)

        self.play(FadeIn(tex4[0][0:4]), run_time=tempo)
        self.play(TransformFromCopy(tex1[0][6:10], tex4[0][4].set_color(PURE_RED)), run_time=2 * tempo)
        self.play(TransformFromCopy(tex1[0][10:16], tex4[0][5:7].set_color(PURE_BLUE)), run_time=2 * tempo)

        self.play(FadeIn(tex5, shift=RIGHT),
                  FadeIn(tex6, shift=RIGHT),
                  run_time=2 * tempo)
        self.wait(2 * tempo)

        # right column animations
        self.play(FadeIn(btex2, shift=RIGHT), run_time=tempo)
        self.wait(tempo)
        self.play(btex2[0][3:11].animate.set_color(PURE_RED), btex1[0][5:11].animate.set_color(PURE_RED),
                  run_time=1.5 * tempo)
        self.play(btex2[0][14:23].animate.set_color(PURE_GREEN), btex1[0][4].animate.set_color(PURE_GREEN),
                  run_time=1.5 * tempo)
        self.play(btex2[0][26::].animate.set_color(PURE_BLUE), btex1[0][11::].animate.set_color(PURE_BLUE),
                  run_time=1.5 * tempo)

        self.play(FadeIn(btex3, shift=RIGHT), run_time=tempo)
        self.wait(tempo)

        grp3 = VGroup(btex4[0][0:3], btex4[0][12], btex4[0][14])
        self.play(FadeIn(grp3), run_time=tempo)
        self.play(TransformFromCopy(btex1[0][5:11], btex4[0][13].set_color(PURE_RED)), run_time=2 * tempo)
        self.play(TransformFromCopy(btex1[0][4], btex4[0][3:12].set_color(PURE_GREEN)), run_time=2 * tempo)
        self.play(TransformFromCopy(btex1[0][11::], btex4[0][15::].set_color(PURE_BLUE)), run_time=2 * tempo)

        self.play(FadeIn(btex5, shift=RIGHT),
                  FadeIn(btex6, shift=RIGHT),
                  run_time=2 * tempo)
        self.wait(tempo)

        self.play(TransformFromCopy(btex1[0][5:11], btex4[0][13].copy()),
                  TransformFromCopy(btex1[0][4], btex4[0][3:12].copy()),
                  TransformFromCopy(btex1[0][11::], btex4[0][15::].copy()),
                  TransformFromCopy(tex1[0][6:10], tex4[0][4].copy()),
                  TransformFromCopy(tex1[0][10:16], tex4[0][5:7].copy()),
                  run_time=2 * tempo)

        rect1 = SurroundingRectangle(tex6, color=GOLD)
        rect2 = SurroundingRectangle(btex6, color=GOLD)
        self.play(LaggedStart(Create(rect1), Create(rect2)), run_time=2 * tempo)

        self.play(TransformFromCopy(btex1[0][5:11], btex4[0][13].copy()),
                  TransformFromCopy(btex1[0][4], btex4[0][3:12].copy()),
                  TransformFromCopy(btex1[0][11::], btex4[0][15::].copy()),
                  TransformFromCopy(tex1[0][6:10], tex4[0][4].copy()),
                  TransformFromCopy(tex1[0][10:16], tex4[0][5:7].copy()),
                  run_time=2 * tempo)

        self.play(LaggedStart(Uncreate(rect1), Uncreate(rect2)), run_time=tempo)
        self.wait(tempo)
