from manim import *

class RFUsage(Scene):
    def construct(self):

        # Some global constants
        fsize = 36
        scale = 1.5
        waitrate = 1.75

        # main tex
        header = Tex(r"Find $\displaystyle\int x^3 e^x \, dx$ using a reduction formula.").to_edge(UP)
        rftext = r"\int x^{n} e^x \, dx = x^{n} e^x - {n}\int x^{{n}-1} e^x \, dx"
        rf = MathTex(rftext, font_size=fsize).to_edge(DOWN)
        # progressive formulas
        tex1 = MathTex(r"\int x^3 e^x \, dx=x^3 e^x - 3",r"\int x^2 e^x \, dx", font_size=fsize)
        tex2 = MathTex(r"\int x^3 e^x \, dx=x^3 e^x - 3\left(",r"x^2 e^x - 2\int x e^x \, dx",r"\right)", font_size=fsize)
        tex2[1].set_color(BLUE)
        tex3 = MathTex(r"\int x^3 e^x \, dx=x^3 e^x - 3x^2 e^x + 6", r"\int x e^x \, dx", font_size=fsize)
        tex4 = MathTex(r"\int x^3 e^x \, dx = x^3 e^x - 3 x^2 e^x + 6\left(", r"x e^x - \int e^x \, dx", r"\right)",
                       font_size=fsize)
        tex5 = MathTex(r"\int x^3 e^x \, dx = x^3 e^x - 3 x^2 e^x + 6x e^x - 6\int e^x \, dx",font_size=fsize)
        tex6 = MathTex(r"\int x^3 e^x \, dx = x^3 e^x - 3 x^2 e^x + 6x e^x - 6 e^x +C", font_size=fsize)
        tex4[1].set_color(GREEN)

        # a function that shows the rf for a particular value of n
        def getRF(n, color):
            start = rf.get_left()+0.5*LEFT
            arrow = CurvedArrow(start_point=start, end_point=start+1.5*UP, radius=2, stroke_width=3, color=color).flip(UP)
            arrowstr = r"Let $n=" + str(n) + r"$"
            arrowtext = Tex(arrowstr, color=color, font_size=fsize).next_to(arrow,LEFT)
            newrftext = rftext.replace("{n}",str(n))
            newrf = MathTex(newrftext, color=color, font_size=fsize).next_to(arrow.get_end(), RIGHT)

            self.play(Create(arrow),Write(arrowtext), run_time=waitrate)
            self.play(Write(newrf), run_time=waitrate)
            self.wait(waitrate)
            self.play(FadeOut(arrow,arrowtext), run_time=waitrate)
            return newrf

        # a function that shifts formulas on the screen to always keep 2 visible
        def advance(texA, texB, texC):
            self.play(FadeOut(texA, shift=scale*UP),
                      texB.animate.shift(scale*UP),
                      FadeIn(texC, shift=scale*UP),
                      run_time=waitrate
                      )
            self.wait(waitrate)

        # initial setup
        self.next_section(skip_animations=False)
        self.play(Write(header), run_time=waitrate)
        self.wait(waitrate)
        self.play(Write(rf), run_time=waitrate)
        self.wait(waitrate)

        # begin RF with n=3
        self.next_section(skip_animations=False)
        formula = getRF(3, WHITE)
        self.wait(waitrate)
        self.play(FadeIn(tex1,shift=UP),FadeOut(formula), run_time=waitrate)
        self.wait(waitrate)
        self.play(tex1[1].animate.set_color(BLUE), run_time=waitrate)
        self.wait(waitrate)

        # on to n=2
        self.next_section(skip_animations=False)
        formula = getRF(2, BLUE)
        self.wait(waitrate)
        self.play(tex1.animate.shift(scale*UP), FadeIn(tex2,shift=scale*UP), run_time=waitrate)
        self.play(FadeOut(formula), run_time=waitrate)
        self.wait(waitrate)
        advance(tex1,tex2,tex3)
        self.play(tex3[1].animate.set_color(GREEN), run_time=waitrate)
        self.wait(waitrate)

        # on to n=1
        self.next_section(skip_animations=False)
        formula = getRF(1, GREEN)
        self.wait(waitrate)
        advance(tex2,tex3,tex4)
        self.play(FadeOut(formula), run_time=waitrate)
        self.wait(3*waitrate)
        advance(tex3,tex4,tex5)
        self.wait(waitrate)
        advance(tex4,tex5,tex6)
        self.wait(waitrate)
        box = SurroundingRectangle(tex6)
        self.play(FadeOut(tex5), Create(box), run_time=waitrate)
        self.wait(5*waitrate)