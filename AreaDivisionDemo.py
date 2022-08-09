from manim import *

class AreaDividerViz(Scene):
    def construct(self):
        def helperfunc(t):
            xval = np.cos(b.get_value())
            if t < xval:
                return b.get_value()
            else:
                return np.arccos(t)

        b = ValueTracker(0.6)
        axes = Axes(x_range=[-1.5,1.5,1], y_range=[-1,4,1], x_length=7, y_length=8, tips=False)
        graph = axes.plot(np.arccos,x_range=[-1,1,0.01], color=GREEN)
        helpergraph = always_redraw(lambda: axes.plot(helperfunc, x_range=[-1,1,0.01], color=ORANGE))
        label = Tex(r"$y=\arccos x$", color=GREEN, font_size=28).move_to(axes.c2p(1,1.5,0))
        dot1 = Dot(axes.c2p(-1,PI,0), color=GREEN)
        dot2 = Dot(axes.c2p(1,0,0), color=GREEN)
        dot1lab = Tex(r"$(-1,\pi)$", font_size=24, color=GREEN).next_to(dot1,UP)
        dot2lab = Tex(r"$(1,0)$", font_size=24, color=GREEN).next_to(dot2, DOWN)
        line = always_redraw(lambda: DashedLine(start=axes.c2p(-1.5,b.get_value(),0),
                                                end=axes.c2p(1.5,b.get_value(),0),
                                                color=WHITE))
        area1 = always_redraw(lambda: axes.get_area(graph,x_range=[-1,np.cos(b.get_value())],
                                                    bounded_graph=helpergraph,color=RED))
        area2 = always_redraw(lambda: axes.get_area(helpergraph, x_range=[-1,1],
                                                    color=BLUE))
        toparea = always_redraw(lambda: DecimalNumber(PI-(np.sin(b.get_value())+b.get_value()),
                                                      font_size=24,color=RED).move_to(axes.c2p(1,3.5,0)))
        botarea = always_redraw(lambda: DecimalNumber(np.sin(b.get_value())+b.get_value(),
                                                      font_size=24, color=BLUE).move_to(axes.c2p(1,3,0)))
        toptext = Tex(" (Top Area)", font_size=24, color=RED).next_to(toparea,RIGHT)
        bottext = Tex(" (Bottom Area)", font_size=24, color=BLUE).next_to(botarea,RIGHT)
        linetext = always_redraw(lambda: Tex(r"$y=b$", font_size=24, color=WHITE).next_to(line,LEFT))

        self.play(Create(axes), FadeIn(graph,dot1,dot2,dot1lab,dot2lab,label))
        self.wait(1)
        self.play(Create(line), Write(linetext))
        self.wait(1)
        self.play(FadeIn(helpergraph), FadeIn(area1,area2), FadeIn(toparea,botarea,toptext,bottext))
        self.wait(2)
        self.play(b.animate.set_value(PI), run_time=2)
        self.play(b.animate.set_value(0), run_time=4)
        self.play(b.animate.set_value(0.832), run_time=2)
        self.wait(1)