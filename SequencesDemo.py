from manim import *


class SeqDemo(Scene):
    def construct(self):
        # the sequence we study:  d_q = 1/q for q = 1, 2, ...
        def d(q):
            return 1 / q

        # global definitions
        title = MathTex(r"\text{Visualizing Sequences in 1D and 2D}", font_size=48).to_edge(UP, MED_SMALL_BUFF)
        dq = MathTex(r"d_", r"q", r"= \dfrac{1}{", r"q", r"}", font_size=36).shift(2 * UP + 5 * RIGHT)
        tempo = 1  # controls the overall speed of the animation
        skip = False

        ###########
        # Section 1 - Initial setup and calculation for first few terms
        self.next_section(skip_animations=skip)
        self.play(Write(title), run_time=2 * tempo)
        self.wait(tempo)
        self.play(Write(dq), run_time=2 * tempo)
        self.wait(tempo)

        self.next_section(skip_animations=skip)
        dqcopy = dq.copy()
        terms = []  # list to hold mobjects for first four terms
        for q in range(1, 5):
            term = MathTex(r"d_", str(q), r"= \dfrac{1}{", str(q), r"}", font_size=36).shift(2 * UP + 5 * RIGHT)
            term[1].set_color(BLUE)
            term[3].set_color(BLUE)
            self.play(TransformMatchingTex(dq, term), run_time=1.5 * tempo)
            self.play(term.animate.shift(1.2 * q * DOWN),
                      FadeIn(dq),
                      run_time=1.5 * tempo)
            terms.append(term)
        self.wait(tempo)

        ###########
        # Section 2 - 1D Visualization
        self.next_section(skip_animations=skip)
        fadeGroup = VGroup()  # things to fade out at end of section
        line = NumberLine(x_range=[-0.1, 1.1, 0.2], length=8, include_numbers=True).shift(1.5 * LEFT + DOWN)
        self.play(Create(line), run_time=2 * tempo)
        self.wait(tempo)

        self.next_section(skip_animations=skip)
        maxQ = 20  # last term to display
        colors = color_gradient([BLUE, GREEN], 2 * maxQ)  # colors from BLUE to GREEN, only get halfway to GREEN
        fadeGroup.add(line)
        for q in range(1, 5):
            newdot = Dot(line.n2p(d(q)), color=colors[q - 1])
            newlabel = MathTex(r"d_", str(q), font_size=24, color=BLUE).next_to(newdot, UP, SMALL_BUFF)
            fadeGroup.add(newdot, newlabel)
            self.play(TransformFromCopy(terms[q - 1], newdot), run_time=2 * tempo)
            self.play(FadeIn(newlabel), run_time=tempo)
            self.wait(tempo)

        self.next_section(skip_animations=skip)
        for q in range(5, maxQ + 1):
            newdot = Dot(line.n2p(d(q)), color=colors[q - 1])
            fadeGroup.add(newdot)
            self.play(FadeIn(newdot), run_time=tempo * (0.1 + d(q)))
        self.wait(tempo)

        self.next_section(skip_animations=skip)
        limit = Dot(line.n2p(0), color=GREEN)
        limitLabel = VGroup(MathTex(r"\text{Terms heading}\\",
                                    r"\text{to value of 0}",
                                    font_size=24, color=GREEN)).arrange(DOWN).next_to(limit, UP, MED_SMALL_BUFF)
        self.play(FadeIn(limit, limitLabel), run_time=2 * tempo)
        self.wait(tempo)
        box = SurroundingRectangle(VGroup(line.numbers[0], limit), color=YELLOW)
        self.play(Create(box), run_time=2 * tempo)
        limTex = MathTex(r"\lim_{q \to \infty} d_q = ",
                         r"0", font_size=24).next_to(box, DOWN, MED_SMALL_BUFF)
        limTex[1].set_color(YELLOW)
        fadeGroup.add(limit, limitLabel, box, limTex)
        self.play(Write(limTex), run_time=2 * tempo)
        self.wait(4 * tempo)
        self.play(FadeOut(fadeGroup), run_time=2 * tempo)

        ###########
        # Section 3 - 2D Visualization
        self.next_section(skip_animations=skip)
        axes = Axes(x_range=[0, 15.5, 1], y_range=[-0.1, 1.1, 0.2], x_length=9, y_length=6,
                    tips=False, axis_config={"font_size": 24}).add_coordinates()
        xlabel = MathTex(r"\text{Term number}", font_size=24).next_to(axes, DOWN, MED_SMALL_BUFF)
        ylabel = MathTex(r"\text{Term value}", font_size=24).rotate(90 * DEGREES).next_to(axes, LEFT, MED_LARGE_BUFF)
        axisgroup = VGroup(axes, xlabel, ylabel).to_corner(DL, MED_SMALL_BUFF)
        self.play(Create(axes), run_time=2 * tempo)
        self.play(Write(xlabel), Write(ylabel), run_time=tempo)
        self.wait(2 * tempo)

        self.next_section(skip_animations=skip)
        colors = color_gradient([BLUE, GREEN], 17)  # colors from BLUE to GREEN, get mostly to GREEN with 15 dots
        for q in range(1, 5):
            newdot = Dot(axes.c2p(q, d(q)), color=colors[q - 1])
            newlabel = MathTex(r"(", str(q), r", d_", str(q), r")", font_size=24,
                               color=BLUE).next_to(newdot, UP, SMALL_BUFF)
            self.play(TransformFromCopy(terms[q - 1], newdot), run_time=2 * tempo)
            self.play(FadeIn(newlabel), run_time=tempo)
            self.wait(2 * tempo)

        self.next_section(skip_animations=skip)
        for q in range(5, 16):
            newdot = Dot(axes.c2p(q, d(q)), color=colors[q - 1])
            self.play(FadeIn(newdot), run_time=tempo * (0.1 + d(q)))
        self.wait(tempo)

        self.next_section(skip_animations=skip)
        limit = DashedLine(axes.c2p(0, 0), axes.c2p(16.5, 0), color=GREEN, dash_length=0.4, dashed_ratio=0.7,
                           stroke_width=8)
        limitLabel = VGroup(MathTex(r"\text{Terms heading}\\",
                                    r"\text{to value of 0}",
                                    font_size=24, color=GREEN)).move_to(axes.c2p(1.6, 0.1))
        self.play(FadeIn(limit), run_time=2 * tempo)
        self.play(Write(limitLabel))
        self.wait()

        limitTick = axes.y_axis.get_tick(0).set_color(YELLOW)
        limitVal = MathTex(r"0", font_size=24, color=YELLOW).next_to(limitTick, LEFT, SMALL_BUFF)
        box = SurroundingRectangle(VGroup(limitVal, limitTick))
        self.play(FadeIn(limitTick, limitVal), run_time=2 * tempo)
        self.wait(tempo)
        self.play(Create(box), run_time=2 * tempo)
        limTex.move_to(axes.c2p(11, 0.2))
        self.play(Write(limTex), run_time=2 * tempo)
        self.wait(5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
