from manimlib import *
import random
import shutil

# "live"            Preview live presentation
# "render"          Render to video file
# "compile"         Compile to separate videos
MODE = "compile"

# Clicker keycodes:
# Left arrow:               65365   (Page up)
# Right arrow:              65366   (Page down)
# Play button (first):      65474   (F5)
# Play button (second):     65307   (Escape)
# Screen button:            46      (.)

pascal_mem = {(0, 0): 1}

def pascal(n, k):
    global pascal_mem

    if k < 0 or n < k:
        return 0

    if (n, k) not in pascal_mem:
        pascal_mem[(n, k)] = pascal(n - 1, k - 1) + pascal(n - 1, k)

    return pascal_mem[(n, k)]

fib_mem = {0: 0, 1: 1}

def fib(n):
    global fib_mem

    if n not in fib_mem:
        fib_mem[n] = fib(n - 2) + fib(n - 1)

    return fib_mem[n]

class PascalTrianglePresentation(Scene):
    # Structure

    def start_presentation(self):
        # Intro
        self.chapter_pascal_explanation()

        # Manhattan
        self.chapter_manhattan_scenario()

        # Fibonacci
        self.chapter_fibonacci_explanation()
        self.chapter_fibonacci_comparison()

        # Sierpinski
        self.chapter_even_odd_distribution()
        self.chapter_sierpinski_comparison()

        # Outro
        self.chapter_end_card()

    # Chapters

    def chapter_pascal_explanation(self):
        # Creation

        size = 8
        pascal_objects, pascal_group = self.create_pascal_triangle(size, with_zeros=True)
        pascal_group.shift((3.6, 2.35, 0))
        pascal_group.scale(0.8)

        squares_group = VGroup()
        for n in range(size):
            for k in range(n + 1):
                squares_group += pascal_objects[n][k][1]

        random_group = VGroup(
            Dot((-10, -10 - (size - 1), 0), radius=0, stroke_width=0),
            Dot((10, 10, 0), radius=0, stroke_width=0)
        )
        random.seed(413)
        for n in range(size):
            for k in range(n + 1):
                number = Tex(str(random.randint(1, 20)))
                number.move_to((k - n / 2, -n, 0))
                random_group += number
        random_group.shift((3.6, 2.35, 0))
        random_group.scale(0.8)

        title_text = Text("Pascal's Triangle", slant=ITALIC)
        title_text.scale(2.5)

        rule_1 = Text("Rule 1: The top of the pyramid\n        is a 1.", t2c={"[-2:-1]": ORANGE})
        rule_2 = Text("Rule 2: Every following number\n        is the sum of the two\n        numbers above it.", t2c={"following number": GREEN, "sum of the two\n        numbers above it": YELLOW})
        rules = VGroup(rule_1, rule_2)
        rules.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rules.shift((0, 0.8, 0))
        rules.to_edge(LEFT)

        rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        line_groups = []
        for stage in range(4):
            curr_line_group = VGroup(
                Dot((-10, -10 - (size - 1), 0), radius=0, stroke_width=0),
                Dot((10, 10, 0), radius=0, stroke_width=0)
            )

            if stage == 0:
                for n in range(4):
                    if n < 3:
                        curr_line_group += Line((n / 2, -n, 0), (n / 2 - 1.5, -n - 3, 0), stroke_width=4, color=BLUE)
                    curr_line_group += Line((-n / 2, -n, 0), (-n / 2 + 1, -n - 2, 0), stroke_width=4, color=BLUE)
            elif stage == 1:
                for n in range(2 * size - 1):
                    if n < size:
                        curr_line_group += Line((0.6 + n / 4, 0.4 - n / 2, 0), (-0.6 - n / 2, -0.4 - n, 0), stroke_width=4, color=rainbow_colors[n % len(rainbow_colors)])
                    else:
                        curr_line_group += Line((0.6 + n / 4, 0.4 - n / 2, 0), (-0.6 + n - 3 * size / 2, -0.4 - size, 0), stroke_width=4, color=rainbow_colors[n % len(rainbow_colors)])
            elif stage == 2:
                curr_line_group += Line((-1.75, -3.5, 0), (1.75, -3.5, 0), stroke_width=4, color=RED)
                curr_line_group += Line((1.75, -3.5, 0), (0, -7, 0), stroke_width=4, color=RED)
                curr_line_group += Line((0, -7, 0), (-1.75, -3.5, 0), stroke_width=4, color=RED)

                curr_line_group += Line((-0.75, -1.5, 0), (0.75, -1.5, 0), stroke_width=4, color=RED)
                curr_line_group += Line((0.75, -1.5, 0), (0, -3, 0), stroke_width=4, color=RED)
                curr_line_group += Line((0, -3, 0), (-0.75, -1.5, 0), stroke_width=4, color=RED)

                curr_line_group += Line((-2.75, -5.5, 0), (-1.25, -5.5, 0), stroke_width=4, color=RED)
                curr_line_group += Line((-1.25, -5.5, 0), (-2, -7, 0), stroke_width=4, color=RED)
                curr_line_group += Line((-2, -7, 0), (-2.75, -5.5, 0), stroke_width=4, color=RED)

                curr_line_group += Line((1.25, -5.5, 0), (2.75, -5.5, 0), stroke_width=4, color=RED)
                curr_line_group += Line((2.75, -5.5, 0), (2, -7, 0), stroke_width=4, color=RED)
                curr_line_group += Line((2, -7, 0), (1.25, -5.5, 0), stroke_width=4, color=RED)

            curr_line_group.shift((3.6, 2.35, 0))
            curr_line_group.scale(0.8)
            line_groups.append(curr_line_group)

        # Animation

        self.pause()

        self.play(Write(title_text), run_time=0.8)

        self.pause()

        title_text.generate_target()
        title_text.target.scale(0.6)
        title_text.target.to_edge(UP)

        self.play(MoveToTarget(title_text))

        self.pause()

        self.play(ShowCreation(squares_group), run_time=2)

        self.pause()

        self.play(Write(random_group), run_time=1)

        self.pause()

        self.play(FadeToColor(random_group, RED), run_time=0.5)
        self.pause(0.8)
        self.play(FadeOut(random_group), run_time=0.6)

        self.pause()

        pascal_objects[0][0][0].set_color(ORANGE)

        self.play(FadeIn(rule_1, UP))

        self.pause()

        self.play(Write(pascal_objects[0][0][0]))

        self.pause()

        self.play(
            FadeToColor(pascal_objects[0][0][0], WHITE),
            FadeToColor(rule_1, GREY_C),
            FadeIn(rule_2, UP)
        )

        self.pause()

        last = None

        for n in range(1, size):
            if n > 1:
                actions = [FadeIn(pascal_objects[n-1][-1][0]), FadeIn(pascal_objects[n-1][-2][0])]
                if last:
                    actions.append(FadeToColor(last, WHITE))
                    last = None
                self.play(*actions, run_time = 0.4 if n < 3 else 0.12)

            for k in range(n + 1):
                highlight_actions = []
                unhighlight_actions = []

                if last:
                    highlight_actions.append(FadeToColor(last, WHITE))

                if n == 1 and k == 0:
                    self.play(Indicate(pascal_objects[n][k][1]))

                    self.pause()

                if n == 1:
                    pascal_objects[n][k][0].set_color(GREEN)
                    last = pascal_objects[n][k][0]

                    if k == 0:
                        pascal_objects[n-1][k-1][0].set_color(YELLOW)
                        highlight_actions.append(FadeIn(pascal_objects[n-1][k-1][0]))
                        unhighlight_actions.append(FadeOut(pascal_objects[n-1][k-1][0]))
                    else:
                        highlight_actions.append(FadeToColor(pascal_objects[n-1][k-1][0], YELLOW))
                        unhighlight_actions.append(FadeToColor(pascal_objects[n-1][k-1][0], WHITE))

                    if k == n:
                        pascal_objects[n-1][k][0].set_color(YELLOW)
                        highlight_actions.append(FadeIn(pascal_objects[n-1][k][0]))
                        unhighlight_actions.append(FadeOut(pascal_objects[n-1][k][0]))
                    else:
                        highlight_actions.append(FadeToColor(pascal_objects[n-1][k][0], YELLOW))
                        unhighlight_actions.append(FadeToColor(pascal_objects[n-1][k][0], WHITE))

                    self.play(*highlight_actions, run_time=0.4)

                    self.pause()

                self.play(
                    *unhighlight_actions,
                    TransformMatchingTex(pascal_objects[n-1][k-1][0].copy(), pascal_objects[n][k][0]),
                    TransformMatchingTex(pascal_objects[n-1][k][0].copy(), pascal_objects[n][k][0]),
                    run_time = 0.4 if n < 3 else 0.12
                )

                if n == 1:
                    self.pause()

            if n > 1:
                self.play(
                    FadeOut(pascal_objects[n-1][-1][0]),
                    FadeOut(pascal_objects[n-1][-2][0]),
                    run_time = 0.4 if n < 3 else 0.12
                )

            if n == 2:
                self.pause()

        self.pause()

        for stage in range(4):
            actions = [FadeToColor(rule_2, GREY_C)] * (stage == 0)

            if stage > 0:
                actions.append(Uncreate(line_groups[stage-1]))
            if stage < 4:
                actions.append(ShowCreation(line_groups[stage]))

            for n in range(size):
                for k in range(n + 1):
                    if stage == 0:
                        color = [ORANGE, BLUE][n - k < 4 and k < 3]
                    elif stage == 1:
                        color = rainbow_colors[(n + k) % len(rainbow_colors)]
                    elif stage == 2:
                        color = [RED, GREEN][pascal(n, k) & 1]
                    else:
                        color = WHITE

                    actions.append(FadeToColor(pascal_objects[n][k][0], color))

            self.play(*actions, run_time=0.8)

            if stage < 3:
                self.pause(1)

        self.pause()

        self.end_slide("slide_up")

    def chapter_manhattan_scenario(self):
        # Creation

        manhattan_image = ImageMobject("assets/img/manhattan.png")
        manhattan_image.scale(1.5)
        home_image = ImageMobject("assets/img/home.png")
        home_image.scale(0.06)
        office_image = ImageMobject("assets/img/office.png")
        office_image.scale(0.06)

        width = 4
        height = 3
        street_width = 6
        arrow_width = 8

        block_group = Group()
        crossings, crossing_group = [], Group()
        numbers, number_group = [], Group()
        arrows, arrow_group = [], Group()
        east_arrows, south_arrows = [], []
        for iy in range(height + 1):
            crossings_row = []
            numbers_row = []
            arrows_row = []
            for ix in range(width + 1):
                if ix < width:
                    block_group += Line((ix + 0.2, -iy), (ix + 1 - 0.2, -iy), color=BLUE, stroke_width=street_width)
                if iy < height:
                    block_group += Line((ix, -iy - 0.2), (ix, -iy - 1 + 0.2), color=BLUE, stroke_width=street_width)

                crossing = Circle(radius=0.2, color=BLUE, fill_opacity=1)
                crossing.set_fill(self.background_color)
                crossing.move_to((ix, -iy, 0))
                crossing_group += crossing
                crossings_row.append(crossing)

                number = Tex(str(pascal(ix + iy, ix)))
                number.scale(0.5)
                number.move_to((ix, -iy, 0))
                number_group += number
                numbers_row.append(number)

                east = south = None
                if ix < width:
                    east = Arrow((ix, -iy), (ix + 1, -iy), stroke_width=arrow_width)
                    east.set_color(YELLOW_C)
                    east_arrows.append(east)
                    arrow_group += east
                if iy < height:
                    south = Arrow((ix, -iy), (ix, -iy - 1), stroke_width=arrow_width)
                    south.set_color(ORANGE)
                    south_arrows.append(south)
                    arrow_group += south
                arrows_row.append((east, south))
            crossings.append(crossings_row)
            numbers.append(numbers_row)
            arrows.append(arrows_row)

        for iy in range(height + 1):
            block_group += Line((-0.2 - 0.1, -iy, 0), (-0.2, -iy, 0), color=BLUE, stroke_width=street_width)
            block_group += Line((width + 0.2, -iy, 0), (width + 0.2 + 0.1, -iy, 0), color=BLUE, stroke_width=street_width)
        for ix in range(width + 1):
            block_group += Line((ix, 0.2 + 0.1, 0), (ix, 0.2, 0), color=BLUE, stroke_width=street_width)
            block_group += Line((ix, -height - 0.2, 0), (ix, -height - 0.2 - 0.1, 0), color=BLUE, stroke_width=street_width)

        home_image.move_to((-0.3, 0.3, 0))
        crossing_group += home_image
        office_image.move_to((width + 0.3, -height - 0.3, 0))
        crossing_group += office_image

        manhattan_group = Group()
        manhattan_group += block_group
        manhattan_group += crossing_group
        manhattan_group += number_group
        manhattan_group += arrow_group
        manhattan_group.scale(1.8)
        manhattan_group.move_to((0, 0, 0))

        question_text = Text("How many paths are there?", slant=ITALIC)
        question_text.scale(1.5)
        question_text.to_edge(UP)
        answer_text = Text(str(pascal(width + height, height)) + "!", slant=ITALIC)
        answer_text.scale(1.5)

        example_paths = [
            VGroup(arrows[0][0][0], arrows[0][1][0], arrows[0][2][0], arrows[0][3][0], arrows[0][4][1], arrows[1][4][1], arrows[2][4][1]),
            VGroup(arrows[0][0][1], arrows[1][0][1], arrows[2][0][1], arrows[3][0][0], arrows[3][1][0], arrows[3][2][0], arrows[3][3][0]),
            VGroup(arrows[0][0][0], arrows[0][1][1], arrows[1][1][0], arrows[1][2][0], arrows[1][3][1], arrows[2][3][0], arrows[2][4][1])
        ]

        example_descriptions = [
            Text("EEEESSS", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EEESESS", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EEESSES", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EEESSSE", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EESEESS", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EESESES", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EESSEES", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EESESSE", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("EESESES", color=YELLOW_C, t2c={"S": ORANGE}),
            Text("...")
        ]

        example_descriptions_group = VGroup(*example_descriptions)
        example_descriptions_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        example_descriptions_group.to_edge(LEFT)

        unknowns = []
        for iy in range(height + 1):
            row = []
            for ix in range(width + 1):
                row.append(Tex("?", color=GREY_C).scale(0.9))
            unknowns.append(row)

        size = width + height + 1
        pascal_objects, pascal_group = self.create_pascal_triangle(size)

        # Animation

        self.pause()

        self.play(FadeIn(manhattan_image, UP))

        self.pause()

        self.play(
            FadeIn(block_group, UP),
            FadeIn(crossing_group, UP),
            FadeOut(manhattan_image, UP)
        )

        self.pause()

        self.play(*[ShowCreation(j) for j in east_arrows], run_time=0.6)

        self.pause()

        self.play(*[ShowCreation(j) for j in south_arrows], run_time=0.6)

        self.pause()

        self.remove(arrow_group)
        self.play(
            *[Uncreate(j.copy()) for j in east_arrows],
            *[Uncreate(j.copy()) for j in south_arrows],
            run_time=0.6
        )

        arrow_group.shift((0, -0.6, 0))
        arrow_group.scale(0.85)
        number_group.shift((0, -0.6, 0))
        number_group.scale(0.85)

        street_group = Group()
        street_group += block_group
        street_group += crossing_group
        street_group.generate_target()
        street_group.target.shift((0, -0.6, 0))
        street_group.target.scale(0.85)
        self.play(MoveToTarget(street_group))
        self.play(Write(question_text), run_time=0.8)

        self.pause()

        for stage in range(len(example_paths) + 1):
            actions = []

            if stage < len(example_paths):
                actions.append(ShowCreation(example_paths[stage]))
            if stage > 0:
                actions.append(Uncreate(example_paths[stage-1]).copy())
                self.remove(arrow_group)

            self.play(*actions)

            if stage < len(example_paths):
                self.pause()

        self.play(
            question_text.animate.shift((1.1, 0, 0)),
            block_group.animate.shift((1.1, 0, 0)),
            crossing_group.animate.shift((1.1, 0, 0))
        )

        self.play(Write(example_descriptions_group))

        self.pause()

        self.play(
            FadeToColor(example_descriptions[5], "#FF0000"),
            FadeToColor(example_descriptions[8], "#FF0000"),
            run_time=0.5
        )

        self.pause()

        self.play(
            FadeOut(example_descriptions_group, LEFT),
            question_text.animate.shift((-1.1, 0, 0)),
            block_group.animate.shift((-1.1, 0, 0)),
            crossing_group.animate.shift((-1.1, 0, 0))
        )

        self.pause()

        self.bring_to_front(crossings[height-1][width])
        self.play(
            crossings[height-1][width].animate.set_stroke(ORANGE),
            ShowCreation(arrows[height-1][width][1]),
            run_time=0.8
        )

        self.pause()

        self.bring_to_front(crossings[height][width-1])
        self.play(
            crossings[height][width-1].animate.set_stroke(YELLOW_C),
            ShowCreation(arrows[height][width-1][0]),
            run_time=0.8
        )

        self.pause()

        self.play(
            FadeIn(numbers[height-1][width]),
            FadeIn(numbers[height][width-1])
        )

        self.pause()

        self.play(
            TransformMatchingTex(numbers[height-1][width].copy(), numbers[height][width]),
            TransformMatchingTex(numbers[height][width-1].copy(), numbers[height][width])
        )

        self.pause()

        for iy in range(height + 1):
            for ix in range(width + 1):
                unknowns[iy][ix].move_to(numbers[iy][ix])

        self.play(
            TransformMatchingTex(numbers[height-1][width], unknowns[height-1][width]),
            TransformMatchingTex(numbers[height][width-1], unknowns[height][width-1]),
            FadeOut(numbers[height][width]),
            run_time=0.8
        )

        self.pause()

        for i in range(width + height - 2, 0, -1):
            actions = []

            if i == width + height - 2:
                actions.extend([
                    crossings[height-1][width].animate.set_stroke(BLUE),
                    crossings[height][width-1].animate.set_stroke(BLUE),
                    FadeIn(unknowns[height][width])
                ])

            for ix in range(width + 1):
                iy = i - ix
                if iy < 0 or iy > height:
                    continue

                actions.append(FadeIn(unknowns[iy][ix]))

                if ix < width:
                    actions.append(ShowCreation(arrows[iy][ix][0]))
                if iy < height:
                    actions.append(ShowCreation(arrows[iy][ix][1]))

            self.play(*actions, run_time=0.3)

        self.pause()

        self.play(
            FadeIn(numbers[0][0]),
            ShowCreation(arrows[0][0][0]),
            ShowCreation(arrows[0][0][1]),
            run_time=0.3
        )

        self.pause()

        for i in range(1, width + height + 1):
            actions = []

            for ix in range(width + 1):
                iy = i - ix
                if iy < 0 or iy > height:
                    continue

                actions.append(FadeOut(unknowns[iy][ix]))

                if ix > 0:
                    actions.extend([
                        Uncreate(arrows[iy][ix-1][0]),
                        TransformMatchingTex(numbers[iy][ix-1].copy(), numbers[iy][ix])
                    ])
                if iy > 0:
                    actions.extend([
                        Uncreate(arrows[iy-1][ix][1]),
                        TransformMatchingTex(numbers[iy-1][ix].copy(), numbers[iy][ix])
                    ])

            self.play(*actions, run_time=0.6)

        self.pause()

        question_text.generate_target()
        question_text.target.shift((-0.9, 0, 0))
        answer_text.next_to(question_text.target, RIGHT)
        answer_text.shift((0.3, 0.05, 0))
        self.play(
            MoveToTarget(question_text),
            TransformMatchingParts(numbers[height][width].copy(), answer_text)
        )

        self.pause()

        number_group.generate_target()
        number_group.target.scale(1 / 0.85)
        number_group.target.shift((0, 0.6, 0))
        self.play(
            FadeOut(question_text, UP),
            FadeOut(answer_text, UP),
            FadeOut(block_group, DOWN),
            FadeOut(crossing_group, DOWN),
            MoveToTarget(number_group)
        )

        self.pause()

        pascal_group.move_to((0, 0, 0))
        pascal_group.scale(0.8)

        to_appear_front_group = VGroup()
        to_appear_back_group = VGroup()
        transformations = []
        for n in range(size):
            for k in range(n + 1):
                if n - k > height or k > width:
                    pascal_objects[n][k][0].set_color(GREY_D)
                    pascal_objects[n][k][1].set_color(GREY_D)
                    to_appear_back_group += pascal_objects[n][k][0]
                    to_appear_back_group += pascal_objects[n][k][1]
                else:
                    numbers[n-k][k].generate_target()
                    numbers[n-k][k].target.move_to(pascal_objects[n][k][0])
                    transformations.append(MoveToTarget(numbers[n-k][k]))
                    to_appear_front_group += pascal_objects[n][k][1]

        self.play(
            FadeIn(to_appear_back_group),
            FadeIn(to_appear_front_group),
            *transformations,
            run_time=1.2
        )

        self.pause()

        self.end_slide("slide_up")

    def chapter_fibonacci_explanation(self):
        # Creation

        title_text = Text("Fibonacci Series", slant=ITALIC)
        title_text.scale(2.5)

        size = 14

        fibonacci_objects = []
        fibonacci_group = VGroup()
        for n in range(size):
            number = Tex(str(fib(n)))
            number.move_to((n - (size - 1) / 2, 0, 0))
            fibonacci_group += number

            square = Square(stroke_width=3)
            square.move_to((n - (size - 1) / 2, 0, 0))
            square.set_width(1)
            fibonacci_group += square

            fibonacci_objects.append((number, square))
        fibonacci_group.shift((1.2, -2, 0))

        rule_1 = Text("Rule 1: The series starts with a 0 and a 1.", t2c={"0": ORANGE, "[-2:-1]": ORANGE})
        rule_2 = Text("Rule 2: Every following number is the sum of the\n        two numbers before it.", t2c={"following number": GREEN, "sum of the\n        two numbers before it": YELLOW})
        rules = VGroup(rule_1, rule_2)
        rules.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rules.shift((0, 1.2, 0))
        rules.to_edge(LEFT)

        squares_group = VGroup()
        for n in range(size):
            squares_group += fibonacci_objects[n][1]

        spiral_image = ImageMobject("assets/img/fibonacci_spiral.png")
        spiral_image.scale(1.5)
        nature_image = ImageMobject("assets/img/fibonacci_nature.png")
        nature_image.scale(1.5)
        mona_lisa_image = ImageMobject("assets/img/fibonacci_mona_lisa.png")
        mona_lisa_image.scale(2)

        # Animation

        self.pause()

        self.play(Write(title_text), run_time=0.8)

        self.pause()

        title_text.generate_target()
        title_text.target.scale(0.6)
        title_text.target.to_edge(UP)

        self.play(MoveToTarget(title_text))
        self.play(ShowCreation(squares_group))

        self.pause()

        fibonacci_objects[0][0].set_color(ORANGE)
        fibonacci_objects[1][0].set_color(ORANGE)

        self.play(FadeIn(rule_1, UP))
        self.play(Write(fibonacci_objects[0][0]), Write(fibonacci_objects[1][0]))

        self.pause()

        self.play(
            FadeToColor(fibonacci_objects[0][0], WHITE),
            FadeToColor(fibonacci_objects[1][0], WHITE),
            FadeToColor(rule_1, GREY_C),
            FadeIn(rule_2, UP)
        )

        self.pause()

        for n in range(2, size):
            if n < 4:
                fibonacci_objects[n][0].set_color(GREEN)

                self.play(
                    FadeToColor(fibonacci_objects[n-2][0], YELLOW),
                    FadeToColor(fibonacci_objects[n-1][0], YELLOW),
                    run_time=0.3
                )

                self.pause()

            self.play(
                FadeToColor(fibonacci_objects[n-2][0], WHITE),
                FadeToColor(fibonacci_objects[n-1][0], WHITE),
                TransformMatchingTex(fibonacci_objects[n-2][0].copy(), fibonacci_objects[n][0]),
                TransformMatchingTex(fibonacci_objects[n-1][0].copy(), fibonacci_objects[n][0]),
                run_time = 4 / (n + 6)
            )

            if n < 4:
                self.pause()

        self.pause()

        self.play(
            FadeToColor(rule_2, GREY_C),
            FadeIn(spiral_image, UP)
        )

        self.pause()

        self.play(
            FadeOut(spiral_image, UP),
            FadeIn(nature_image, UP)
        )

        self.pause()

        self.play(
            FadeOut(nature_image, UP),
            FadeIn(mona_lisa_image, UP)
        )

        self.pause()

        self.end_slide("fade_out")

    def chapter_fibonacci_comparison(self):
        # Creation

        size = 10
        pascal_objects, pascal_group = self.create_pascal_triangle(size, with_zeros=True)
        pascal_group.shift((0, (size - 1) / 2, 0))
        pascal_group.scale(0.7)

        number_group = VGroup()
        zeros_group = VGroup()
        for n in range(size):
            for k in range(n + 1):
                number_group += pascal_objects[n][k][0]
            zeros_group += pascal_objects[n][-2][0]
            zeros_group += pascal_objects[n][-1][0]

        rainbow_colors = [BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN]

        lines, line_group = [], VGroup()
        sums, sum_group = [], VGroup()
        for n in range(size + 1):
            if n < size:
                line = Line((0.75 + n / 4, 0.5 - n / 2, 0), (-0.75 - n / 2, -0.5 - n, 0), stroke_width=4, color=rainbow_colors[n % len(rainbow_colors)])
                line_group += line
                lines.append(line)

                sum = Tex(str(fib(n + 1)), color=rainbow_colors[n % len(rainbow_colors)])
            else:
                sum = Tex("\ldots")
            sum.scale(0.8)
            sum.move_to((n / 4 + 1.1, -n / 2 - 0.1, 0))
            sum_group += sum
            sums.append(sum)

        pair_outlines, pair_outline_group = [], VGroup()
        for n in range(size - 1):
            row = []
            for k in range(-1, n // 2 + 1):
                pair_outline = Rectangle(2, 1, color=RED, stroke_width=6)
                pair_outline.shift((0.5 - n / 2 + 3 * k / 2, k - n, 0))
                pair_outline_group += pair_outline

                row.append(pair_outline)
            pair_outlines.append(row[1:] + [row[0]])

        arrows, arrow_group = [], VGroup()
        for n in range(size - 1):
            row = []
            for k in range(n + 3):
                left = Arrow((k - n / 2 - 1, -n), (k - n / 2 - 1.5, -n - 1), stroke_width=4)
                left.set_color(rainbow_colors[(n + k - 1) % len(rainbow_colors)])
                arrow_group += left

                right = Arrow((k - n / 2 - 1, -n), (k - n / 2 - 0.5, -n - 1), stroke_width=4)
                right.set_color(rainbow_colors[(n + k - 1) % len(rainbow_colors)])
                arrow_group += right

                row.append((right, left))
            arrows.append(row)

        for group in [line_group, sum_group, pair_outline_group, arrow_group]:
            group += Dot((-15, -1, 0))
            group += Dot((15, -1, 0))
            group.shift((0, (size - 1) / 2, 0))
            group.scale(0.7)

        offset = 6

        square_equation_objects = [
            Square(0.8, color=rainbow_colors[offset % len(rainbow_colors)], stroke_width=0, fill_opacity=0.5),
            Text("+"),
            Square(0.8, color=rainbow_colors[(offset + 1) % len(rainbow_colors)], stroke_width=0, fill_opacity=0.5),
            Text("="),
            Square(0.8, color=rainbow_colors[(offset + 2) % len(rainbow_colors)], stroke_width=0, fill_opacity=0.5)
        ]
        square_equation_objects = VGroup(*square_equation_objects)
        square_equation_objects.arrange(RIGHT, buff=0.4)
        square_equation_objects.shift((3, 2, 0))

        # Animation

        self.play(FadeIn(VGroup().add(*pascal_group).remove(*zeros_group)))

        self.pause()

        highlight_actions = []
        sum_actions = []
        for n in range(size):
            for k in range(n + 1):
                if n + k < size:
                    color = rainbow_colors[(n + k) % len(rainbow_colors)]
                    sum_actions.append(TransformMatchingTex(pascal_objects[n][k][0].copy().set_color(color), sums[n + k]))
                    pascal_objects[n][k][1].set_fill(rainbow_colors[(n + k) % len(rainbow_colors)])
                else:
                    color = GREY_C
                highlight_actions.append(FadeToColor(pascal_objects[n][k][0], color))

        for n in range(size):
            pascal_objects[n][-2][0].set_color(rainbow_colors[(2 * n + 1) % len(rainbow_colors)])
            pascal_objects[n][-1][0].set_color(rainbow_colors[(n - 1) % len(rainbow_colors)])

        self.play(
            ShowCreation(line_group),
            *highlight_actions
        )

        self.pause()

        self.play(
            *sum_actions,
            FadeIn(sums[-1]),
            run_time=1.6
        )

        self.pause()

        self.play(
            FadeToColor(number_group, WHITE),
            FadeOut(VGroup(*lines[:offset], *lines[offset+2:], *sum_group)),
            FadeToColor(VGroup(lines[offset]), rainbow_colors[offset % len(rainbow_colors)]),
            FadeToColor(VGroup(lines[offset+1]), rainbow_colors[(offset + 1) % len(rainbow_colors)])
        )

        self.pause()

        highlight_actions = []
        for i in range(3):
            highlight_actions.append([])
            for n in range(size):
                if 0 <= offset - n + i <= n:
                    highlight_actions[-1].append(pascal_objects[n][offset-n+i][1].animate.set_fill(opacity=0.5))

        for i in range(2):
            self.remove(lines[offset+i])
            self.play(
                *highlight_actions[i],
                FadeOut(lines[offset+i].copy()),
                run_time=0.4
            )

            self.pause()

        zeros_to_appear = VGroup(pascal_objects[offset+1][-1][0])
        if offset & 1 == 0:
            zeros_to_appear += pascal_objects[offset // 2][-2][0]
        relevant_pair_group = VGroup(*[pair_outlines[offset][j] for j in range(-1, offset - 1)])
        self.play(
            FadeIn(zeros_to_appear),
            ShowCreation(relevant_pair_group)
        )

        self.pause()

        self.play(Uncreate(relevant_pair_group), run_time=0.4)

        to_appear_arrow_group = VGroup()
        for n in range(size):
            if 1 <= offset - n + 2 <= n + 2:
                to_appear_arrow_group += arrows[n][offset-n+2][1]
            if 0 <= offset - n + 1 <= n + 1:
                to_appear_arrow_group += arrows[n][offset-n+1][0]

        self.play(
            ShowCreation(to_appear_arrow_group),
            *highlight_actions[2]
        )

        self.pause()

        VGroup(*lines[offset:offset+3]).shift((-1.2, 0, 0))
        to_move_group = VGroup(*self.all_objects())

        self.play(
            to_move_group.animate.shift((-1.2, 0, 0)),
            FadeIn(square_equation_objects, LEFT)
        )

        self.pause()

        self.play(
            Uncreate(to_appear_arrow_group),
            FadeOut(zeros_to_appear)
        )

        self.play(ShowCreation(lines[offset+2]))

        self.pause()

        self.play(
            FadeIn(lines[offset]),
            FadeIn(lines[offset+1])
        )

        self.pause()

        self.end_slide("slide_up")

    def chapter_even_odd_distribution(self):
        # Creation

        title_text = Text("Odd and even numbers?", slant=ITALIC)
        title_text.scale(2)

        size = 5
        pascal_objects, pascal_group = self.create_pascal_triangle(size)
        pascal_group.shift((0, (size - 1) / 2 - 0.4, 0))

        odd_number_group, odd_square_group = VGroup(), VGroup()
        for n in range(size):
            for k in range(n + 1):
                pascal_objects[n][k][1].set_fill(WHITE)
                if pascal(n, k) & 1:
                    odd_number_group += pascal_objects[n][k][0]
                    odd_square_group += pascal_objects[n][k][1]

        # Animation

        self.pause()

        self.play(Write(title_text), run_time=0.8)

        self.pause()

        title_text.generate_target()
        title_text.target.scale(0.75)
        title_text.target.to_edge(UP)

        self.play(MoveToTarget(title_text))

        self.play(ShowCreation(pascal_group))

        self.pause()

        self.play(
            odd_square_group.animate.set_fill(GREY_B, opacity=1),
            FadeToColor(odd_number_group, BLACK)
        )

        self.pause()

        self.end_slide("fade_out")

    def chapter_sierpinski_comparison(self):
        # Creation

        size = 32
        height = 6

        pascal_objects, pascal_group = self.create_pascal_triangle(size, with_numbers=False, stroke_width=1)
        pascal_group.shift((0, (size - 1) / 2, 0))
        pascal_group.scale(height / size)

        to_mark = VGroup()
        for n in range(size):
            for k in range(n + 1):
                if pascal(n, k) & 1:
                    to_mark += pascal_objects[n][k]

        sierpinski_big_image = ImageMobject("assets/img/sierpinski_big.png")
        sierpinski_big_image.set_height(height)

        sierpinski_text = Text("Sierpiński Triangle")
        sierpinski_text.shift((0, -3.1, 0))

        scream_image = ImageMobject("assets/img/the_scream.png")
        scream_image.set_height(height + 1.6)

        equivalence_text = Tex("=")
        equivalence_text.scale(1.8)

        # Animation

        self.play(ShowCreation(pascal_group), run_time=2)

        self.pause()

        self.play(to_mark.animate.set_fill(WHITE, opacity=1), run_time=2)

        self.pause()

        pascal_group.generate_target()
        pascal_group.target.scale(0.25)
        pascal_group.target.shift((0, height * 0.375, 0))
        self.play(MoveToTarget(pascal_group), run_time=0.8)
        self.play(FadeIn(sierpinski_big_image))
        self.play(FadeOut(pascal_group), run_time=0.2)

        self.pause()

        self.play(
            sierpinski_big_image.animate.shift((0, 0.6, 0)),
            FadeIn(sierpinski_text, UP)
        )

        self.pause()

        self.play(FadeIn(scream_image))
        self.play(FadeOut(sierpinski_text), run_time=0.3)

        self.pause()

        scream_image.generate_target()
        scream_image.target.shift((-3.6, 0, 0))
        scream_image.target.scale(height / (height + 1.6))
        self.play(
            sierpinski_big_image.animate.shift((3.6, -0.6, 0)),
            MoveToTarget(scream_image)
        )

        self.pause()

        self.play(FadeIn(equivalence_text, UP))

        self.pause()

        self.end_slide("fade_out")

    def chapter_end_card(self):
        # Creation

        size = 13

        pascal_objects, pascal_group = self.create_pascal_triangle(size)
        pascal_group.set_color("#272727")
        pascal_group.scale(1.8)
        pascal_group.shift((0, 11.4, 0))

        title_text = Text("\"The hidden beauty of Pascal's Triangle\"\n  by Tim Huisman")

        supervisor_text = Text("Supervised by Sjaak Baars", color=GREY_B)
        supervisor_text.scale(0.8)
        manim_text = Text("Presented with Manim\n  by 3Blue1Brown", color=GREY_B)
        manim_text.scale(0.8)

        image_credits = [
            "https://commons.wikimedia.org/wiki/File:Lower_Manhattan_from_Helicopter.jpg",
            "https://www.flaticon.com/free-icons/home-button",
            "https://www.flaticon.com/free-icons/workplace",
            "https://commons.wikimedia.org/wiki/File:FibonacciSpiral.svg",
            "https://commons.wikimedia.org/wiki/File:Fibonacci_spiral.jpg",
            "https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg",
            "https://www.wikidata.org/wiki/Q18891157"
        ]

        image_credits_text = Text("Images used:\n" + "\n".join(image_credits), color=GREY_C, font_size=14)

        text_group = VGroup(
            title_text,
            supervisor_text,
            manim_text,
            image_credits_text
        )
        text_group.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        text_group.to_corner(LEFT + UP)

        # Animation

        self.play(
            FadeIn(pascal_group),
            FadeIn(text_group)
        )

        self.pause()

        self.end_slide("fade_out")

    # Utils

    def on_mouse_press(self, point, button, mods):
        if button & 1:
            self.cont = True

    def on_key_press(self, symbol, modifiers):
        self.cont = True

    def pause(self, max_time=86400):
        if MODE == "compile" and max_time > 60:
            if self.num_plays <= self.start_at_animation_number:
                self.wait(0.1)
                return

            f = open("temp", "w")
            f.write(str(self.num_plays))
            f.close()

            exit()

        if MODE == "render" and max_time > 60:
            max_time = 1

        self.cont = False
        self.wait_until(lambda: self.cont, max_time)
        self.cont = False

    def all_objects(self):
        return Group(*filter(lambda x: issubclass(type(x), Mobject), self.mobjects)).remove(self.background)

    def end_slide(self, transition=None):
        all_group = self.all_objects()

        if transition == "slide_up":
            all_group.generate_target()
            all_group.target.shift((0, 10, 0))
            self.play(MoveToTarget(all_group), run_time=0.8)
        elif transition == "fade_out":
            filter = Rectangle(15, 10, color=self.background_color, fill_opacity=0)
            self.play(filter.animate.set_fill(opacity=1))

        self.remove(all_group)

    def create_pascal_triangle(self, size, with_numbers=True, with_zeros=False, stroke_width=4):
        pascal_objects = []
        pascal_group = VGroup()

        for n in range(size):
            row = []

            for k in range(n + 1):
                square = Square(stroke_width=stroke_width)
                square.move_to((k - n / 2, -n, 0))
                square.set_width(1)
                pascal_group += square

                if with_numbers:
                    number = Tex(str(pascal(n, k)))
                    number.move_to((k - n / 2, -n, 0))
                    pascal_group += number

                    row.append((number, square))
                else:
                    row.append(square)

            if with_zeros:
                zero_left = Tex("0")
                zero_left.move_to((-1 - n / 2, -n, 0))
                pascal_group += zero_left

                zero_right = Tex("0")
                zero_right.move_to((1 + n / 2, -n, 0))
                pascal_group += zero_right

                row.extend([(zero_right,), (zero_left,)])

            pascal_objects.append(row)

        return pascal_objects, pascal_group

    def construct(self):
        self.startup()
        self.start_presentation()
        self.shutdown()

    def startup(self):
        # Creation

        self.background_color = "#171717"
        self.background = Rectangle(15, 10, color=self.background_color, fill_opacity=1)

        self.cont = False
        self.click_enabled = False

        if MODE in ["live", "compile"]:
            count_texts = [Text(str(j)) for j in range(4)]
            count_texts[0].to_corner(LEFT + DOWN)

        # Animation

        self.add(self.background)

        if MODE in ["live", "compile"]:
            for i in range(len(count_texts)):
                if i > 0:
                    count_texts[i].next_to(count_texts[i-1], RIGHT)

                self.play(FadeIn(count_texts[i], UP), run_time=0.3)

                self.pause()

            self.play(*[FadeOut(j, DOWN) for j in count_texts], run_time=0.3)

        self.end_slide()

    def shutdown(self):
        if MODE == "compile":
            f = open("temp", "w")
            f.write("-1")
            f.close()

        exit()

if __name__ == "__main__":
    if MODE == "live":
        os.system("manimgl generate.py PascalTrianglePresentation -l")
    elif MODE == "render":
        os.system("manim-render generate.py PascalTrianglePresentation -w -a --file_name pascal_triangle_presentation.mp4 --hd --frame_rate 60")
    elif MODE == "compile":
        shutil.rmtree("snippets")

        f = open("temp", "w")
        f.write("0")
        f.close()

        last = -1
        i = 1
        while True:
            f = open("temp", "r")
            start = int(f.read())
            f.close()

            if start == -1 or start == last:
                break

            print(f"Rendering section {i}...")
            os.system(f"manim-render generate.py PascalTrianglePresentation -w -a --file_name snippet_{i:03} --video_dir snippets -n {start} --hd --frame_rate 60")

            last = start
            i += 1

        os.remove("temp")
    else:
        print("ERROR: No mode was selected")