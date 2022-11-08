from manim import *

class PolarDemo(Scene):
    def construct(self):

        def polarf(theta):
            return 2-2*np.sin(theta)

        axes = PolarPlane(radius_max=4, azimuth_step=12, radius_step=1).add_coordinates()
        table = MathTable([[r"\theta",r"r=2-2\sin\theta"],
                           [0,2],
                           [r"\pi/6",1],
                           [r"\pi/2",0],
                           [r"\pi",2],
                           [r"3\pi/2",4]]).scale(0.7)
        layout = VGroup(axes,table).arrange(RIGHT, buff=LARGE_BUFF).scale_to_fit_height(0.95*config.frame_height)

        # A helper animation that pivots a small vector initially pointing east to angle endangle,
        # which then lengthens to length rval and then fades out
        def vectorAnim(endangle,rval,color):
            rTrack = ValueTracker(0.75)
            tTrack = ValueTracker(0)
            vec = always_redraw(lambda: Arrow(start=axes.polar_to_point(0,0),
                                              end=axes.polar_to_point(rTrack.get_value(),tTrack.get_value()),
                                              color=color, stroke_width=6, buff=0))
            self.play(FadeIn(vec))
            self.play(tTrack.animate.set_value(endangle), run_time=0.5)
            self.play(rTrack.animate.set_value(rval), run_time=0.5)
            dot = Dot(axes.polar_to_point(rTrack.get_value(), tTrack.get_value()), color=color)
            self.play(FadeIn(dot))
            self.play(FadeOut(vec))


        # initial setup
        self.next_section(skip_animations=False)
        self.play(DrawBorderThenFill(axes), FadeIn(table))
        self.wait()


        # step through table values
        self.next_section(skip_animations=False)
        tvals = [0,PI/6,PI/2,PI,3*PI/2]
        colors = [BLUE, GREEN, RED, ORANGE, PURPLE]
        for i in range(5):
            row = table.get_rows()[i+1]
            color = colors[i]
            rect = SurroundingRectangle(row, color=color)
            self.play(Create(rect))
            tval = tvals[i]
            rval = polarf(tval)
            vectorAnim(tval,rval,color)
            self.play(FadeOut(rect))


        # step through [0,2*PI] continuously and trace curve
        self.next_section(skip_animations=False)
        fsize = 36  # font size for r and theta labels below
        self.play(table.animate.shift(1.5*UP))
        t = ValueTracker(0)  # keeps track of theta's value
        tTex = Tex(r"$\theta$: ",font_size=fsize,color=YELLOW).next_to(table,DOWN,buff=LARGE_BUFF).shift(0.5*LEFT)
        rTex = Tex(r"$r$: ",font_size=fsize,color=YELLOW).next_to(tTex,DOWN)
        tVal = always_redraw(lambda: DecimalNumber(t.get_value(), 2,
                                                   font_size=fsize,
                                                   color=YELLOW).next_to(tTex,RIGHT))
        rVal = always_redraw(lambda: DecimalNumber(polarf(t.get_value()), 2,
                                                   font_size=fsize,
                                                   color=YELLOW).next_to(rTex,RIGHT))
        self.play(FadeIn(tTex,rTex,tVal,rVal))

        self.next_section(skip_animations=False)
        dot = always_redraw(lambda: Dot(axes.polar_to_point(polarf(t.get_value()), t.get_value()), color=YELLOW))

        polargraph = always_redraw(lambda:
                                   ParametricFunction(lambda u: axes.polar_to_point(polarf(u),u),
                                                      t_range=[0,t.get_value(),0.005], color=YELLOW,
                                                      stroke_width=8))

        self.play(FadeIn(dot,polargraph))
        self.play(t.animate.set_value(2*PI),run_time=5)
        self.wait(3)
