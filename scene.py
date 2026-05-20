import numpy as np
from manim import *


class BaseRegion(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=0, theta=-90 * DEGREES
        )  # convert 3d to a 2d view

        # -- Title card ---
        title_main = Text("AP CALCULUS AB - Mr Malchoff", weight=BOLD).scale(0.55)
        title_sub = Text(
            "Solid of Revolution by the Washer Method", slant=ITALIC
        ).scale(0.45)
        title_byline = Text("Ruikai Peng | May 2026").scale(0.35)

        title_card = VGroup(title_main, title_sub, title_byline).arrange(
            DOWN, buff=0.35
        )
        self.add_fixed_in_frame_mobjects(title_card)

        self.play(FadeIn(title_card), run_time=1.0)
        self.wait(2)
        self.play(FadeOut(title_card), run_time=1.0)

        # starting with axes
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            z_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=5,
            z_length=5,
        )
        axes_labels = axes.get_axis_labels(
            x_label="x", y_label="y", z_label="z"
        )  # labeling these axes

        f_graph = axes.plot(lambda x: np.sqrt(x), x_range=[0, 1], color=BLUE)
        f_label = MathTex(r"f(x)=\sqrt{x}", color=BLUE).scale(0.6)
        f_label.move_to(axes.c2p(0.85, 1.05))

        g_graph = axes.plot(lambda x: x**2, x_range=[0, 1], color=GREY)
        g_label = MathTex(r"g(x)=x^2", color=GREY).scale(0.6)
        g_label.move_to(axes.c2p(1.15, 0.45))

        region = axes.get_area(
            f_graph, x_range=(0, 1), bounded_graph=g_graph, color=ORANGE, opacity=0.5
        )
        r_label = MathTex("R", color=WHITE).scale(0.8)
        r_label.move_to(axes.c2p(0.5, 0.45))

        # title = MathTex(
        #    r"R: \text{ bounded by } f(x)=\sqrt{x},\ g(x)=x^2"
        # ).scale(0.7).to_edge(UP, buff=0.5)
        # self.add_fixed_in_frame_mobjects(title)

        # self.play(Write(title))
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(f_graph), Write(f_label))
        self.play(Create(g_graph), Write(g_label))
        self.play(Create(region), Write(r_label))

        # Rubric: derive [0, 1] interval rigorously from intersections.
        intersect_dots = VGroup(
            Dot(axes.c2p(0, 0), color=YELLOW, radius=0.07),
            Dot(axes.c2p(1, 1), color=YELLOW, radius=0.07),
        )
        intersect_eq = (
            MathTex(
                r"f(x)=g(x):\ \sqrt{x}=x^2 \ \Rightarrow\ x=0,\,1",
                color=YELLOW,
            )
            .scale(0.5)
            .to_edge(UP, buff=0.4)
        )
        self.add_fixed_in_frame_mobjects(intersect_eq)
        self.play(Create(intersect_dots), Write(intersect_eq), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(intersect_eq), run_time=0.6)
        # dots remain as bound markers on the x-axis interval

        title = MathTex(r"\text{area of } R").scale(0.7)
        title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # ---

        what_is_x = ValueTracker(0.5)  # a container to track x
        cur = lambda: what_is_x.get_value()  # when t, x?
        upper = lambda: np.sqrt(cur())  # when t, upper?
        lower = lambda: cur() ** 2  # when t, lower?

        # always_redraw, use the lambda to regenerate
        # a new MObject every frame, that replace old line (scan)
        dy = always_redraw(
            lambda: Line(
                axes.c2p(cur(), lower()),  # start
                axes.c2p(cur(), upper()),  # end
                color=RED,
            )
        )

        upper_where = always_redraw(
            lambda: Dot(axes.c2p(cur(), upper()), color=YELLOW, radius=0.07)
        )
        lower_where = always_redraw(
            lambda: Dot(axes.c2p(cur(), lower()), color=YELLOW, radius=0.07)
        )

        x_to_lower_dashed = always_redraw(
            lambda: DashedLine(
                axes.c2p(cur(), 0),  # start
                axes.c2p(cur(), lower()),  # end
                color=RED,
            )
        )

        x_where = always_redraw(
            lambda: Dot(
                axes.c2p(cur(), 0),
                color=RED,
            )
        )

        x_what = DecimalNumber(0.5, num_decimal_places=3).scale(0.5)
        x_what_label = VGroup(
            MathTex(r"x = ").scale(0.5),
            x_what,
        ).arrange(RIGHT, buff=0.02)

        x_what.add_updater(lambda m: m.set_value(cur()))
        x_what_label.add_updater(
            lambda m: m.next_to(axes.c2p(cur(), 0), DOWN, buff=0.25)
        )

        def show(label, color, fn):
            label = MathTex(label, color=color).scale(0.55)
            num = DecimalNumber(fn(), num_decimal_places=3, color=color).scale(0.55)
            row = VGroup(label, num).arrange(RIGHT, buff=0.15)

            def update_row(m):
                num.set_value(fn())

            row.add_updater(update_row)
            return row

        f_show = show(r"f(x) = ", BLUE, upper)
        g_show = show(r"g(x) = ", GREY, lower)
        dy_show = show(r"f(x)-g(x)=", GREEN, lambda: upper() - lower())

        info = VGroup(f_show, g_show, dy_show).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        )
        info.to_edge(RIGHT, buff=0.5)

        self.play(
            Create(dy),
            FadeIn(upper_where),
            FadeIn(lower_where),
            FadeIn(x_to_lower_dashed),
            FadeIn(x_what_label),
        )

        self.add_fixed_in_frame_mobjects(info)
        self.play(FadeIn(info))

        self.play(what_is_x.animate.set_value(0.9), run_time=2, rate_func=smooth)
        self.play(what_is_x.animate.set_value(0.2), run_time=2, rate_func=smooth)

        self.remove(info)

        # Rubric: name axis of revolution + justify washer method choice.
        # Fade the cross-section caption since we're leaving 2D scan mode.
        self.play(FadeOut(title))
        self.move_camera(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            run_time=2,
        )
        method_caption = (
            MathTex(
                r"\text{Revolve } R \text{ about the } x\text{-axis};\ "
                r"\text{outer } R(x)=f(x),\ \text{inner } r(x)=g(x) "
                r"\Rightarrow \text{washer method}",
                color=YELLOW,
            )
            .scale(0.42)
            .to_edge(UP, buff=0.4)
        )
        self.add_fixed_in_frame_mobjects(method_caption)
        self.play(Write(method_caption), run_time=1.4)
        self.wait(0.3)

        # ---
        # we're revolving dy against x
        # we need to know:
        # u: the angle dy is [0, 2pi]
        # v: the distance to x (r)

        what_is_theta = ValueTracker(0.001)  # tracks the angle we've revolved
        washer = always_redraw(
            lambda: Surface(
                lambda u, v: axes.c2p(
                    cur(),  # x
                    v * np.cos(u),  # y
                    v * np.sin(u),  # z
                ),
                u_range=(0, what_is_theta.get_value()),  # from 0 to 2*pi
                v_range=(lower(), upper()),  # from inner to radius
                resolution=(30, 8),  # 2pi to 30 pieces, inner to outer radius 8 pieces
                fill_opacity=0.8,
                checkerboard_colors=[RED, ORANGE],
                stroke_width=0.5,
                stroke_color=BLUE_A,
            )
        )
        self.add(washer)

        self.play(
            what_is_theta.animate.set_value(2 * np.pi),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(1)

        self.play(what_is_x.animate.set_value(0.7), run_time=2, rate_func=smooth)
        self.play(what_is_x.animate.set_value(0.4), run_time=1.7, rate_func=smooth)

        self.play(
            FadeOut(washer),
            FadeOut(dy),
            FadeOut(upper_where),
            FadeOut(lower_where),
            FadeOut(x_to_lower_dashed),
            FadeOut(x_where),
            FadeOut(x_what_label),
        )

        formula = (
            MathTex(
                r"V \approx \sum_{i=1}^{",
                r"n",
                r"} \pi \left[ f(x_i)^2 - g(x_i)^2 \right] \Delta x",
            )
            .scale(0.6)
            .to_edge(DOWN, buff=0.5)
        )
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(1)

        def right_riemann(given_x, dx):
            x_k = given_x + dx
            r_outer = np.sqrt(x_k)
            r_inner = x_k**2

            style = dict(
                resolution=(20, 4),
                fill_opacity=0.75,
                stroke_width=0.4,
                stroke_color=BLUE_A,
            )

            outer = Surface(
                lambda u, v: axes.c2p(v, r_outer * np.cos(u), r_outer * np.sin(u)),
                u_range=(0, 2 * np.pi),
                v_range=(given_x, x_k),
                **style,  # pyright: ignore[reportArgumentType]
            )

            inner = Surface(
                lambda u, v: axes.c2p(v, r_inner * np.cos(u), r_inner * np.sin(u)),
                u_range=(0, 2 * np.pi),
                v_range=(given_x, x_k),
                **style,  # pyright: ignore[reportArgumentType]
            )

            right_face = Surface(
                lambda u, v: axes.c2p(x_k, v * np.cos(u), v * np.sin(u)),
                u_range=(0, 2 * np.pi),
                v_range=(r_inner, r_outer),
                **style,  # pyright: ignore[reportArgumentType]
            )

            return VGroup(outer, inner, right_face)

        n_tracker = ValueTracker(2)

        # cache the original n-glyph geometry so the overlay matches its
        # scriptstyle size (a superscript on \sum is much smaller than 0.6x)
        formula[1].set_opacity(0)

        # n label: only rebuild when int(n) actually crosses a new integer.
        # without this, MathTex gets recompiled every frame -- huge slowdown.
        last_n_label = [-1]

        def make_n_label(m):
            cur = int(n_tracker.get_value())
            if cur == last_n_label[0]:
                return
            last_n_label[0] = cur
            new = (
                MathTex(str(cur), color=YELLOW)
                .match_height(formula[1])
                .move_to(formula[1])
            )
            m.become(new)

        n_label = (
            MathTex("2", color=YELLOW).match_height(formula[1]).move_to(formula[1])
        )
        n_label.add_updater(make_n_label)
        self.add_fixed_in_frame_mobjects(n_label)

        # washers: same caching trick. only rebuild the VGroup when int(n) changes,
        # not every frame. cuts ~180 rebuilds down to ~23.
        last_n_washers = [-1]
        dynamic_washers = VGroup()

        def update_washers(m):
            cur = max(1, int(n_tracker.get_value()))
            if cur == last_n_washers[0]:
                return
            last_n_washers[0] = cur
            dx = 1.0 / cur
            m.become(VGroup(*[right_riemann(i * dx, dx) for i in range(cur)]))

        dynamic_washers.add_updater(update_washers)
        self.add(dynamic_washers)

        # 90° azimuthal (theta) change -- quarter turn instead of full orbit.
        # shorter run_time too: fewer frames -> faster render overall.
        self.move_camera(
            theta=-45 * DEGREES + PI / 2,
            run_time=3.5,
            added_anims=[n_tracker.animate.set_value(25)],  # pyright: ignore[reportArgumentType]
        )
        self.wait(1)

        # --- Step 6: morph ONE formula through the derivation --
        # Each transition is paired with a synced 3D update so the symbolic
        # change and the geometric change land together.

        # 6.0: freeze knob-driven updaters, fade the knob overlays, and revert
        # the camera to the original phi=70°, theta=-45° view from before the
        # Riemann knob beat -- the derivation reads better against that
        # canonical solid-of-revolution viewpoint.
        dynamic_washers.clear_updaters()
        n_label.clear_updaters()
        self.play(FadeOut(n_label), FadeOut(title), FadeOut(method_caption))
        self.move_camera(theta=-45 * DEGREES, run_time=1.5)

        # `current` always points at whatever MathTex is on screen right now.
        # Each step builds the next MathTex at the SAME bottom-edge slot and
        # Transforms current -> next. The formula stays parked at the bottom;
        # only its content morphs through the derivation.
        current = formula

        def morph_to(new_tex, *companions, run_time=1.6):
            """Transform the bottom-anchored formula into a new expression.
            New MathTex is built at the same scale + DOWN edge anchor as the
            original `formula` so the morph happens in place at the bottom.
            `companions` play in sync (3D updates) so symbolic and geometric
            changes are bound."""
            new = MathTex(new_tex).scale(0.6).to_edge(DOWN, buff=0.5)
            # Don't add `new` to the scene -- Transform only needs it as a
            # target shape. Adding would leave an invisible duplicate behind.
            self.play(
                Transform(current, new),
                *companions,
                run_time=run_time,
            )
            # Transform replaces current's submobjects with copies of new's.
            # The camera's fixed_in_frame list is identity-based and only knew
            # about the ORIGINAL submobject objects, so the freshly-copied ones
            # would otherwise render as 3D world-space mobjects on the XY plane.
            # Re-register so each post-morph submobject is treated as 2D HUD.
            self.add_fixed_in_frame_mobjects(current)

        # -- L1 -> L2: Σ becomes ∫, washers morph into smooth solid --
        # build the smooth solid of revolution for the companion animation
        smooth_outer = Surface(
            lambda u, v: axes.c2p(u, np.sqrt(u) * np.cos(v), np.sqrt(u) * np.sin(v)),
            u_range=(0.001, 1),
            v_range=(0, TAU),
            resolution=(14, 18),
            fill_opacity=0.55,
            checkerboard_colors=[RED, ORANGE],
            stroke_width=0.3,
            stroke_color=BLUE_A,
        )
        smooth_inner = Surface(
            lambda u, v: axes.c2p(u, (u**2) * np.cos(v), (u**2) * np.sin(v)),
            u_range=(0.001, 1),
            v_range=(0, TAU),
            resolution=(14, 18),
            fill_opacity=0.55,
            checkerboard_colors=[GREY_D, GREY_E],
            stroke_width=0.3,
            stroke_color=BLUE_A,
        )
        smooth_solid = VGroup(smooth_outer, smooth_inner)

        # Rubric: name the general washer formula at the Σ -> ∫ transition.
        gen_washer = (
            MathTex(
                r"\text{Washer: } V = \int_a^b \pi\left(R(x)^2 - r(x)^2\right) dx",
                color=BLUE_C,
            )
            .scale(0.45)
            .to_edge(UP, buff=0.4)
        )
        self.add_fixed_in_frame_mobjects(gen_washer)

        # --- L1 -> L2: Σ becomes ∫. Crossfade washers -> smooth solid, then
        # highlight the whole solid: that VGroup IS the "integration region"
        # the new ∫ symbol is measuring.
        # (ReplacementTransform would hang on 240->2 submobject alignment.)
        morph_to(
            r"V = \int_0^1 \pi \left[ f(x)^2 - g(x)^2 \right] dx",
            FadeOut(dynamic_washers),
            FadeIn(smooth_solid),
            FadeIn(gen_washer, shift=DOWN * 0.15),
            run_time=2.0,
        )
        self.play(Indicate(smooth_solid, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.wait(0.5)
        self.play(FadeOut(gen_washer), run_time=0.5)
        self.wait(0.2)

        # --- L2 -> L3: substitute f, g; pulse the bounding curves so the
        # viewer connects "f" and "g" in the formula to actual blue/grey curves.
        morph_to(
            r"V = \int_0^1 \pi \left[ (\sqrt{x})^2 - (x^2)^2 \right] dx",
            Indicate(f_graph, color=BLUE, scale_factor=1.1),
            Indicate(g_graph, color=GREY, scale_factor=1.1),
        )
        self.wait(0.3)

        # --- L3 -> L4: simplify squares + factor π out (pure algebra) ---
        morph_to(r"V = \pi \int_0^1 (x - x^4) \, dx")
        self.wait(0.3)

        # --- L4 -> L5: antiderivative (pure symbolic; no 3D companion) ---
        morph_to(r"V = \pi \left[ \frac{x^2}{2} - \frac{x^5}{5} \right]_0^1")
        self.wait(0.3)

        # --- evaluation beat: show F(1) - F(0) explicitly before L6 ---
        # This is the "plug in the bounds" moment. We surface two HUD lines
        # above the formula so the algebra of L5 -> L6 reads as substitution,
        # not magic. They fade out before the next morph.
        eval_at_1 = MathTex(
            r"F(1) = \tfrac{1^2}{2} - \tfrac{1^5}{5} = \tfrac{3}{10}",
            color=YELLOW,
        ).scale(0.55)
        eval_at_0 = MathTex(r"F(0) = 0 - 0 = 0", color=YELLOW).scale(0.55)
        eval_group = VGroup(eval_at_1, eval_at_0).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )
        eval_group.to_edge(LEFT, buff=0.6).shift(DOWN * 1.5)
        self.add_fixed_in_frame_mobjects(eval_group)
        self.play(FadeIn(eval_group, shift=UP * 0.2), run_time=0.9)
        self.wait(0.9)

        # --- L5 -> L6: evaluate at bounds (the F(1) - F(0) result) ---
        morph_to(r"V = \pi \left( \frac{1}{2} - \frac{1}{5} \right)")
        self.play(FadeOut(eval_group), run_time=0.6)
        self.wait(0.3)

        # --- L6 -> L7: arithmetic to closed form ---
        morph_to(r"V = \pi \cdot \frac{3}{10} = \frac{3\pi}{10}")
        self.wait(0.5)

        # --- Step 7: final reveal ---
        viz3d = VGroup(
            axes,
            axes_labels,
            f_graph,
            g_graph,
            f_label,
            g_label,
            region,
            r_label,
            smooth_solid,
        )

        final = (
            MathTex(r"V = \frac{3\pi}{10} \approx 0.9425", color=YELLOW)
            .scale(1.4)
            .move_to(ORIGIN)
        )
        box = SurroundingRectangle(final, color=YELLOW, buff=0.3)
        self.add_fixed_in_frame_mobjects(final, box)

        self.play(
            FadeOut(viz3d),
            current.animate.set_opacity(0.3),
            Write(final),
            Create(box),
            run_time=2,
        )
        self.wait(2.5)
