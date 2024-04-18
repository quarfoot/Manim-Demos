from manim import *


class IIT(Scene):
    def construct(self):
        # global constants
        skip = False

        # initial setup
        self.camera.background_color = WHITE
        header = Tex(r"Integration Intuition Training (30-45 Seconds Each)", font_size=48, color=BLACK).to_edge(UP)
        subheader = Tex(r"Pick the technique that seems most promising.  Begin the transformation.",
                        font_size=36, color=PURE_RED).next_to(header, DOWN, buff=MED_LARGE_BUFF)
        tech = Tex(r"\begin{enumerate} \item Straight Out (SO) \item U-Sub (A)Typical (USUB) "
                   r"\item Integration By Parts (IBP) \item Trig Identities (TI)"
                   r"\item Trig-Sub (TSUB) \item Partial Fractions (PF) \end{enumerate}",
                   font_size=30, color=BLACK).next_to(subheader, DOWN, buff=LARGE_BUFF)
        slideBox = Rectangle(width=config.frame_width / 2, height=config.frame_height / 2, color=PURE_BLUE)
        VGroup(tech, slideBox).arrange(RIGHT, buff=MED_LARGE_BUFF).next_to(subheader, DOWN, buff=LARGE_BUFF)

        #######################
        # Section 1 - The setup
        self.next_section(skip_animations=skip)

        self.play(FadeIn(header, shift=UP))
        self.wait(4)
        self.play(FadeIn(subheader, shift=UP))
        self.wait(4)
        self.play(FadeIn(tech))
        self.wait(4)
        self.play(FadeIn(slideBox))
        self.wait(2)

        # plays a slide with the problem (a string to convert to LaTeX) and the initial steps, a list of strings
        def playSlide(problem, steps, slide_time, pause_time):
            probTex = MathTex(problem, font_size=36, color=BLACK)
            stepTex = [MathTex(step, font_size=30, color=PURE_RED) for step in steps]
            stepGroup = VGroup(*stepTex).arrange(DOWN, MED_SMALL_BUFF)
            slide = VGroup(probTex, stepGroup).arrange(DOWN, MED_LARGE_BUFF)
            slide.move_to(slideBox.get_center())

            frac = ValueTracker(0.1)  # start at 10% of width of slideBox
            loc = slideBox.get_center()
            statusbar = always_redraw(lambda:
                                      Rectangle(width=slideBox.width * frac.get_value(), fill_opacity=1,
                                                fill_color=PURE_BLUE, height=0.1,
                                                color=PURE_BLUE).move_to(loc).shift(DOWN * slideBox.height / 2))

            self.play(FadeIn(probTex, shift=UP))
            self.play(FadeIn(statusbar))
            self.play(frac.animate(rate_func=linear).set_value(1), run_time=slide_time)
            self.play(LaggedStart(*[FadeIn(step, shift=UP) for step in stepTex], lag_ratio=2))
            self.wait(pause_time)
            self.play(FadeOut(slide, statusbar))

        ##########################
        # Section 2 - The problems
        self.next_section(skip_animations=skip)

        playSlide(r"\text{Find } \int \dfrac{\cos (\arctan x)}{1+x^2} \, dx",
                  [r"\text{USUB: Let } u=\arctan x, \text{ so }du = \dfrac{1}{1+x^2} \, dx"], 25, 8)

        playSlide(r"\text{Find } \int \csc x \cdot \cot x \, dx",
                  [r"\text{SO: We know } \dfrac{d}{dx} \csc x = -\csc x \cdot \cot x"], 30, 8)

        playSlide(r"\text{Find } \int x^2 \sin x \, dx",
                  [r"\text{IBP: Let } u=x^2, dv = \sin x\, dx"], 35, 8)

        playSlide(r"\text{Find } \int \dfrac{x}{\sqrt{x^2+4}} \, dx",
                  [r"\text{While TSUB is tempting } (x=2\tan \theta)",
                   r"\text{USUB is easier:  Let } u=x^2+4, \text{ so } du =2x\,dx"], 35, 8)

        playSlide(r"\text{Find } \int \sin^3 x \cdot \cos^2 x \, dx",
                  [r"\text{First TI: } \int \sin x \cdot (1-\cos^2 x) \cdot \cos^2 x \, dx ",
                   r"\text{Then USUB: } u=\cos x, \text{ so } du =-\sin x \,dx"], 40, 12)

        playSlide(r"\text{Find } \int 3^x \sin\left( 3^x \right) \, dx",
                  [r"\text{USUB: Let } u=3^x, \text{ so } du = \ln 3 \cdot 3^x \,dx"], 40, 10)

        playSlide(r"\text{Find } \int \dfrac{3^x}{4^x} \, dx",
                  [r"\text{SO: } \int \left( \dfrac34 \right)^x \,dx",
                   r"=\dfrac{1}{\ln(3/4)} \cdot \left(\dfrac34 \right)^x + C"], 40, 12)

        playSlide(r"\text{Find } \int \arcsin x \, dx",
                  [r"\text{IBP: Let } u=\arcsin x, dv = 1 \, dx"], 35, 8)

        playSlide(r"\text{Find } \int \dfrac{\sqrt{x^2-4}}{2x} \, dx",
                  [r"\text{TSUB: Let } x=2 \sec\theta, \text{ so } dx=2\sec\theta \tan\theta \, d\theta"], 35, 8)

        playSlide(r"\text{Find } \int \dfrac{\sqrt{x+1}}{x^2} \, dx",
                  [r"\text{USUB (Atypical): Let } u=\sqrt{x+1}",
                   r"\text{So }x=u^2-1 \text{ and }dx=2u \, du"], 45, 12)

        self.play(FadeOut(header, subheader, tech, slideBox), run_time=2)
        self.wait(4)
