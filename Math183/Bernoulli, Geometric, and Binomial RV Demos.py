import random

from manim import *
from numpy.random import default_rng


class BNode(VGroup):
    def __init__(self, size=1, angle=60 * DEGREES, color=PURE_BLUE, trialNum=1, p=0.5,
                 showpandq=True, textoverride=False, **kwargs):
        super().__init__(color=color, **kwargs)

        # make the Bernoulli node: contains a square with arrows for success and failure
        self.p = p  # probability of success
        self.trialNum = trialNum
        self.sq = Square(side_length=size, stroke_color=color)
        self.trialText = VGroup(MathTex(r"\text{Trial}"), MathTex(str(trialNum))).arrange(DOWN)
        if textoverride:
            self.trialText = VGroup(Tex("Bernoulli"), Tex("RV")).arrange(DOWN)
        self.trialText.move_to(self.sq.get_center()).scale_to_fit_width(size * 0.7).set_color(color)

        self.svector = [-np.cos(angle) * size, -np.sin(angle) * size, 0]
        self.fvector = [np.cos(angle) * size, -np.sin(angle) * size, 0]

        base = self.sq.get_bottom()
        self.sarrow = Arrow(start=base, end=base + self.svector, buff=0, color=color, tip_shape=ArrowCircleTip,
                            stroke_width=4)
        self.slabel = Text("S", font_size=14, color=color).move_to(self.sarrow.get_tip().get_center())
        self.farrow = Arrow(start=base, end=base + self.fvector, buff=0, color=color, tip_shape=ArrowCircleTip,
                            stroke_width=4)
        self.flabel = Text("F", font_size=14, color=color).move_to(self.farrow.get_tip().get_center())

        # the main object
        super().add(self.sq, self.trialText, self.sarrow, self.slabel, self.farrow, self.flabel)

        self.plabel = VMobject()
        self.qlabel = VMobject()
        if showpandq:
            self.plabel = MathTex(r"p", font_size=18 * size, color=color).next_to(self.sarrow.get_center(), 0.5 * UL,
                                                                                  SMALL_BUFF)
            self.qlabel = MathTex(r"q", font_size=18 * size, color=color).next_to(self.farrow.get_center(), 0.5 * UR,
                                                                                  SMALL_BUFF)
            super().add(self.plabel, self.qlabel)

    # returns a set of animations that highlight the node and then color the node based on whether
    # a success or failure occurred.  This choice can be randomized or (if randomize is False) can be forced
    def getAnimations(self, total_run_time=1, randomize=True, forceLeft=True):
        top = self.sq.get_top()
        bot = self.sq.get_bottom()
        vs = self.sq.get_vertices()  # vertices of the square: 0 = upper right, 1 = upper left, etc.
        lPath = VMobject().set_points_as_corners([top, vs[1], vs[2], bot])
        rPath = VMobject().set_points_as_corners([top, vs[0], vs[3], bot])
        lDot = Dot(lPath.get_start(), color=BLACK)
        rDot = Dot(rPath.get_start(), color=BLACK)

        if randomize:
            rng = default_rng()
            goLeft = True if rng.uniform(0, 1, 1) < self.p else False
        else:
            goLeft = forceLeft

        path = self.sarrow if goLeft else self.farrow
        letter = self.slabel if goLeft else self.flabel
        prob = self.plabel if goLeft else self.qlabel
        trialColor = PURE_GREEN if goLeft else PURE_RED
        colorGroup = VGroup(path, letter, prob, self.sq)

        anims = [AnimationGroup(MoveAlongPath(lDot, lPath, run_time=total_run_time * 2 / 5),
                                MoveAlongPath(rDot, rPath, run_time=total_run_time * 2 / 5)),
                 AnimationGroup(MoveAlongPath(lDot, path, run_time=total_run_time / 5, remover=True),
                                MoveAlongPath(rDot, path, run_time=total_run_time / 5, remover=True)),
                 AnimationGroup(FadeOut(VGroup(lDot, rDot), run_time=total_run_time * 2 / 5),
                                colorGroup.animate(run_time=total_run_time * 2 / 5).set_color(trialColor))
                 ]

        return anims

    def getTrialNum(self):
        return self.trialNum


class BernoulliDemo(Scene):
    def construct(self):
        skip = False

        self.camera.background_color = WHITE
        title = MathTex(r"\text{The Bernoulli Random Variable}", color=BLACK, font_size=48).shift(3 * UP)

        self.next_section(skip_animations=skip)
        self.play(FadeIn(title, shift=UP, run_time=2))
        self.wait(2)

        node = BNode(size=2, textoverride=True)
        self.play(FadeIn(node, run_time=2))
        self.wait()

        self.next_section(skip_animations=skip)
        self.wait(2)
        self.play(node.animate(run_time=2).shift(3 * LEFT + 0.5 * UP).scale(0.9))
        self.wait(2)

        self.next_section(skip_animations=skip)
        keypoints = Tex(r"\checkmark \,\, Exactly \textbf{two} outcomes:\\",
                        r"Success (1), prob: $p$\\",
                        r"Failure (0), prob. $q=1-p$",
                        r"\checkmark \,\, Trials are \textbf{independent}\\",
                        r"\checkmark \,\, Examples:\\",
                        font_size=36, color=BLACK)
        pointsGroup = VGroup(*keypoints).arrange(DOWN, aligned_edge=LEFT, buff=MED_SMALL_BUFF).shift(
            2 * RIGHT + 0.5 * UP)

        # discuss 2 outcomes
        self.play(FadeIn(pointsGroup[0]))
        self.wait(2)
        self.play(FadeIn(pointsGroup[1].shift(RIGHT), shift=RIGHT))
        self.wait(8)
        self.play(FadeIn(pointsGroup[2].shift(RIGHT), shift=RIGHT))
        self.wait(10)

        # discuss independence
        self.play(FadeIn(pointsGroup[3].shift(0.5 * DOWN)))
        self.wait(8)

        self.next_section(skip_animations=skip)

        times = [4, 3, 3, 3, 3, 2, 2]
        lefts = [False, True, True, False, True, False, False]
        for left, time in zip(lefts, times):
            self.play(Succession(*node.getAnimations(total_run_time=time, randomize=False, forceLeft=left)))
            self.wait(1)
            self.play(node.animate.set_color(PURE_BLUE))
        self.wait(2)

        self.next_section(skip_animations=skip)

        # helper method to show a few examples
        def playExample(text, showReversal=False):
            text.next_to(pointsGroup, DOWN, MED_SMALL_BUFF)
            text.align_to(pointsGroup[2], LEFT)
            self.play(FadeIn(text, shift=UP))
            self.wait(2)
            name = text[0].copy()
            succ = text[2].copy()
            fail = text[4].copy()
            self.play(name.animate.next_to(node, UP, MED_SMALL_BUFF),
                      succ.animate.next_to(node.sarrow.get_end(), DOWN, MED_SMALL_BUFF),
                      fail.animate.next_to(node.farrow.get_end(), DOWN, MED_SMALL_BUFF))

            self.wait(4)
            if showReversal:
                self.play(Swap(succ, fail, run_time=2))
                self.wait(3)

            self.play(FadeOut(name, succ, fail, text, run_time=3))
            self.wait(1)

        self.play(FadeIn(pointsGroup[4].shift(DOWN)))
        self.wait(2)
        playExample(Tex("Coin flip", ": ", "Heads", ", ", "Tails", font_size=36, color=BLACK), True)
        playExample(Tex("Email", ": ", "Not Spam", ", ", "Spam", font_size=36, color=BLACK), True)
        playExample(Tex("Shot on goal", ": ", "Goal", ", ", "No goal", font_size=36, color=BLACK), False)
        self.wait(5)


class GeometricDemo(Scene):
    def construct(self):
        skip = False
        self.camera.background_color = WHITE
        title = MathTex(r"\text{The Geometric Random Variable}", color=BLACK, font_size=48).shift(3 * UP)
        description = MathTex(r"\text{Counts the number of Bernoulli trials needed to get a success}",
                              color=BLACK, font_size=36).next_to(title, DOWN, LARGE_BUFF)
        self.next_section(skip_animations=skip)
        self.play(FadeIn(title, shift=UP, run_time=2))
        self.wait(2)
        self.play(FadeIn(description, shift=UP, run_time=2))
        self.wait(4)

        xvals = [3, 1, 7, 5]
        times = [2, 1.5, 1, 0.5]
        psandqs = [True, True, False, False]

        for x, time, show in zip(xvals, times, psandqs):
            # make all the nodes
            nodes = VGroup(*[BNode(trialNum=i, showpandq=show) for i in np.arange(1, x + 1)])
            nodes.arrange(RIGHT, buff=MED_LARGE_BUFF).next_to(description, DOWN, 1.25 * LARGE_BUFF)

            for node in nodes:
                self.play(FadeIn(node, run_time=time))
                self.wait(time / 4)
                goLeft = True if node.getTrialNum() == x else False  # all failures until last trial
                self.play(Succession(*node.getAnimations(total_run_time=time, randomize=False, forceLeft=goLeft)))

            brace = Brace(nodes, color=BLACK)
            braceText = MathTex(r"X=", str(x), font_size=36, color=BLACK).next_to(brace, DOWN, buff=SMALL_BUFF)
            self.play(FadeIn(brace, braceText))
            self.wait(3)
            self.play(FadeOut(nodes, brace, braceText))
            self.remove(nodes)


class BinomialDemo(Scene):
    def construct(self):
        def BinomialHelper(nval=6, successes=[3, 3, 6]):
            nodes = [BNode(trialNum=i) for i in range(1, nval + 1)]
            bnodes = VGroup(*nodes).arrange(RIGHT, MED_LARGE_BUFF).shift(0.5 * DOWN)
            self.play(LaggedStart(*[FadeIn(node) for node in bnodes], lag_ratio=0.5))
            self.wait(2)

            nBrace = Brace(bnodes, UP, color=PURE_BLUE)
            nBraceLabel = MathTex(r"n=", str(nval), color=PURE_BLUE, font_size=30).next_to(nBrace, UP)
            self.play(FadeIn(nBrace, nBraceLabel))
            self.wait(1)

            # use same n for several different iterations to see different results can occur
            # the number of successes on a given iteration is determined by the successes vector
            # but the placement of these successes are random (see shuffling of Trues and Falses below)
            for successCount in successes:
                checkGroup = VGroup()
                numSuccesses = 0
                whichOnes = [True] * successCount + [False] * (nval - successCount)
                random.shuffle(whichOnes)

                for node, goLeft in zip(bnodes, whichOnes):
                    self.play(Succession(*node.getAnimations(randomize=False, forceLeft=goLeft)))
                    if goLeft:
                        checkGroup += MathTex(r"\checkmark", color=PURE_GREEN).next_to(node, DOWN, MED_SMALL_BUFF)
                        numSuccesses += 1

                self.wait()
                self.play(FadeIn(checkGroup))
                self.wait()
                summary = MathTex(r"X=", numSuccesses, color=BLACK, font_size=36).next_to(bnodes, DOWN, MED_LARGE_BUFF)
                self.play(Transform(checkGroup, summary))
                self.wait(1)
                self.play(FadeOut(checkGroup, summary), bnodes.animate.set_color(PURE_BLUE))
                self.wait()

        skip = False
        self.camera.background_color = WHITE
        title = MathTex(r"\text{The Binomial Random Variable}", color=BLACK, font_size=48).shift(3 * UP)
        description = MathTex(r"\text{Counts the number of successes in }n \text{ (fixed, known) Bernoulli trials}",
                              color=BLACK, font_size=36).next_to(title, DOWN, MED_LARGE_BUFF)
        self.next_section(skip_animations=skip)
        self.play(FadeIn(title, shift=UP, run_time=2))
        self.wait(2)
        self.play(FadeIn(description, shift=UP, run_time=2))
        self.wait(4)

        self.next_section(skip_animations=skip)
        BinomialHelper()
