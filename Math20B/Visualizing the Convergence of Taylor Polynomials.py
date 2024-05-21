import math

from manim import *


class TaylorDemo(Scene):
    def construct(self):
        # the function to create Taylor polys to approximate
        def f(x):
            return np.exp(x)

        a = 0  # center of Taylor polys

        # the Taylor polynomial of degree k for f(x) centered at a
        # f^(i)(a) needs to be hard-coded based on f(x) above (here: 1 for all k)
        def T(k, a, x):
            return sum([1 * (x - a) ** i / math.factorial(i) for i in range(0, k + 1)])

        self.camera.background_color = WHITE
        # degrees of the polynomials to show
        degrees = [0, 1, 2, 3, 4, 5, 6, 8, 20]
        # how long to run animation showing T_k(x), want to change speed for different k
        degreeTimes = [8, 8, 6, 8, 8, 6, 4, 8, 8]

        # hardcode first few for prime signs and transition to recursive notation
        polyLabels = [r"T_0(x) = f(a)\\ \text{best constant approximation}",
                      r"T_1(x) = f(a)+f'(a)(x-a)\\ \text{best linear approximation}",
                      r"T_2(x) = f(a)+f'(a)(x-a)+\dfrac{f''(a)}{2!}(x-a)^2\\ \text{best quadratic approximation}",
                      r"T_3(x) = T_2(x)+\dfrac{f'''(a)}{3!}(x-a)^3\\ \text{best cubic approximation}"]
        for k in degrees[4::]:
            polyLabels.append(r"T_{" + str(k) + r"}(x)= T_{" + str(k - 1) + r"}(x) + \dfrac{f^{(" + str(k) +
                              r")}(a) (x-a)^{" + str(k) + r"}}{" + str(k) + r"!}")
        tColor = PURE_RED  # color for all Taylor polynomial stuff
        fColor = PURE_BLUE  # color for original function and point of tangency

        xmin = -3
        xmax = 1.5
        ymin = -1
        ymax = 5
        axes = Axes(x_range=[xmin, xmax, 1], y_range=[ymin, ymax, 1], tips=False).add_coordinates()
        axes.set_color(BLACK)
        fgraph = axes.plot(f, x_range=[xmin, xmax, 0.01], color=fColor)
        flabel = MathTex(r"f(x)", color=fColor, font_size=30).next_to(axes.c2p(1, f(1)), UP, MED_LARGE_BUFF)
        POT = Dot(axes.c2p(a, f(a)), color=fColor)  # point of tangency
        atick = axes.x_axis.get_tick(a).set_color(fColor)
        atick.stroke_width = 8
        alabel = MathTex(r"a", font_size=30, color=fColor).next_to(atick, DR, SMALL_BUFF)

        # Taylor's formula
        taylor = MathTex(r"f(x) &= \sum_{i=0}^\infty \dfrac{f^{(i)}(a)}{i!}(x-a)^i\\",
                         r" &= \lim_{n \to \infty} \sum_{i=0}^n \dfrac{f^{(i)}(a)}{i!}(x-a)^i\\",
                         r" &= \lim_{n \to \infty} T_n(x)",
                         font_size=32).to_corner(UL, LARGE_BUFF)
        taylor.set_color(BLACK)
        taylor[0][0:4].set_color(fColor)
        taylor[2][-5::].set_color(tColor)

        tgraphs = [axes.plot(lambda x: T(deg, a, x), x_range=[xmin, xmax], color=tColor) for deg in degrees]
        tlabels = [MathTex(lab, font_size=24, color=tColor).move_to(axes.c2p(-1.2, 1.8)) for lab in polyLabels]

        skip = True

        ###########
        # Section 1 - Set up graph of f(x), write Taylor formula out
        self.next_section(skip_animations=not skip)
        self.play(Create(axes))
        self.play(FadeIn(fgraph, flabel, POT, atick, alabel))
        self.wait(4)
        self.play(LaggedStart(*[Write(eq) for eq in taylor], lag_ratio=4))
        self.wait(4)

        ###########
        # Section 2 - Loop through Taylor polynomials slowly for discussion
        self.next_section(skip_animations=not skip)
        for i in range(0, len(degrees)):
            tgraph = tgraphs[i]
            tlabel = tlabels[i]
            time = degreeTimes[i]
            self.play(FadeIn(tgraph, tlabel))
            self.wait(time)
            self.play(FadeOut(tgraph, tlabel))
        self.wait(2)

        ###########
        # Section 3 - Loop through Taylor polynomials quickly to reinforce convergence
        self.next_section(skip_animations=not skip)
        shortLabels = [MathTex(r"T_{" + str(deg) + r"}(x)", font_size=26,
                               color=tColor).next_to(axes.c2p(0, 1), DR, SMALL_BUFF) for deg in degrees]

        self.play(FadeIn(tgraphs[0], shortLabels[0]))
        for i in range(1, len(degrees)):
            self.play(ReplacementTransform(tgraphs[i - 1], tgraphs[i]),
                      ReplacementTransform(shortLabels[i - 1], shortLabels[i]), run_time=2)
