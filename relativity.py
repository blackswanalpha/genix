from manim import *
from manim.mobject.svg.svg_mobject import SVGMobject
from manim.mobject.geometry.tips import ArrowTriangleFilledTip
from manim.mobject.three_d.three_dimensions import Surface
from manim.utils.rate_functions import ease_in_out_sine
import numpy as np

import os

# Create our own ThoughtBubble class
class ThoughtBubble(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bubbles = VGroup()
        main_bubble = Circle(radius=0.7)
        for i in range(3):
            bubble = Circle(radius=0.15 - i * 0.03)
            bubble.next_to(main_bubble, DOWN + LEFT, buff=-0.1 + i * 0.1)
            bubbles.add(bubble)
        self.add(main_bubble, bubbles)
    
    def get_bubble_center(self):
        return self[0].get_center()

class Narrator(SVGMobject):
    def __init__(self, **kwargs):
        super().__init__(file_name=os.path.join("assets", "narrator.svg"), **kwargs)
        self.scale(1.5)

class AdvancedRelativity(ThreeDScene):
    def construct(self):
        # Set up the camera for better 3D viewing
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-30 * DEGREES
        )
        
        # Configuration
        self.configure_global_settings()
        self.camera.background_color = "#1a1a1a"
        
        # Title sequence
        self.show_title()
        
        # Create and introduce narrator
        narrator = self.create_narrator()
        self.play(FadeIn(narrator))  # First bring narrator on screen
        self.introduce_narrator(narrator)

        # Core content
        self.special_relativity_chapter(narrator)
        self.general_relativity_chapter(narrator)

        # Conclusion
        self.show_conclusion()

    def configure_global_settings(self):
        self.camera.background_color = "#1a1a1a"
        config.frame_width = 16
        config.frame_height = 9
        config.pixel_width = 1920
        config.pixel_height = 1080

    def create_narrator(self):
        narrator = Narrator()
        narrator.to_edge(LEFT)
        narrator.shift(DOWN)
        return narrator

    def show_title(self):
        title = Text("Einstein's Relativity", font_size=72)
        subtitle = Text("A Modern Visualization", font_size=36)
        title.set_color_by_gradient(BLUE, GREEN)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

    def introduce_narrator(self, narrator):
        bubble = ThoughtBubble()
        bubble.scale(0.7)
        bubble.next_to(narrator, UP)
        caption = Text("Let's explore spacetime!", font_size=24)
        caption.move_to(bubble.get_bubble_center())
        
        self.play(
            Create(bubble),
            Write(caption)
        )
        self.wait(2)
        self.play(FadeOut(bubble), FadeOut(caption))

    def special_relativity_chapter(self, narrator):
        chapter_title = Text("Special Relativity", font_size=48)
        chapter_title.to_edge(UP)
        self.play(Write(chapter_title))
        
        # Interactive spacetime diagram
        diagram = self.create_spacetime_diagram()
        self.play(Create(diagram))
        
        # Time dilation interactive comparison
        earth_frame, ship_frame = self.create_reference_frames()
        self.show_time_dilation(earth_frame, ship_frame, narrator)
        
        self.play(FadeOut(diagram), FadeOut(chapter_title))
        self.play(FadeOut(earth_frame), FadeOut(ship_frame))

    def create_spacetime_diagram(self):
        # Create a simple grid
        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )
        
        # Add labels
        x_label = Text("Space", font_size=24).next_to(grid.x_axis, RIGHT)
        t_label = Text("Time", font_size=24).next_to(grid.y_axis, UP)
        
        return VGroup(grid, x_label, t_label)

    def create_reference_frames(self):
        earth_frame = Rectangle(height=2, width=1, color=BLUE)
        ship_frame = Rectangle(height=2, width=1, color=RED)
        
        earth_frame.shift(LEFT * 2)
        ship_frame.shift(RIGHT * 2)
        
        earth_label = Text("Earth", font_size=20).next_to(earth_frame, DOWN)
        ship_label = Text("Ship", font_size=20).next_to(ship_frame, DOWN)
        
        earth_frame = VGroup(earth_frame, earth_label)
        ship_frame = VGroup(ship_frame, ship_label)
        
        return earth_frame, ship_frame

    def show_time_dilation(self, earth_frame, ship_frame, narrator):
        earth_clock = Circle(radius=0.3, color=BLUE).next_to(earth_frame, UP)
        ship_clock = Circle(radius=0.3, color=RED).next_to(ship_frame, UP)
        
        self.play(Create(earth_clock), Create(ship_clock))
        
        # Show time dilation effect
        self.play(
            earth_clock.animate.scale(1.0),
            ship_clock.animate.scale(0.8),
            run_time=2
        )
        
        # Add explanation
        self.show_narration(narrator, "Time runs slower\nfor fast-moving objects!")
        
        # Cleanup
        self.play(
            FadeOut(earth_clock),
            FadeOut(ship_clock)
        )

    def create_clock(self):
        face = Circle(radius=0.5, color=WHITE)
        hand = Line(ORIGIN, UP * 0.4, color=RED)
        return VGroup(face, hand)

    def general_relativity_chapter(self, narrator):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        chapter_title = Text("General Relativity", font_size=48, color=GREEN)
        self.play(Write(chapter_title))
        self.wait(1)

        mass, warped_grid = self.create_spacetime_curvature()
        einstein_eq = MathTex(r"G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}")
        einstein_eq.to_edge(UP)

        self.play(
            Create(warped_grid),
            FadeIn(mass),
            Write(einstein_eq)
        )

        self.show_gravitational_waves(warped_grid)
        self.show_black_hole(mass, warped_grid, narrator)

        self.play(FadeOut(chapter_title), FadeOut(einstein_eq))

    def create_spacetime_curvature(self):
        grid = Surface(
            lambda u, v: np.array([
                u,
                v,
                0.5 * np.exp(-(u**2 + v**2))
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(15, 15),
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=1
        )
        
        mass = Sphere(radius=0.5)
        mass.set_color(YELLOW)
        mass.set_opacity(0.8)
        
        return mass, grid

    def show_gravitational_waves(self, grid):
        waves = VGroup(*[
            Circle(radius=0.5 + 0.5 * i, stroke_width=2)
            for i in range(5)
        ])
        waves.set_color(BLUE)

        animations = [Create(wave) for wave in waves]
        self.play(*animations, run_time=3)

    def show_black_hole(self, mass, grid, narrator):
        event_horizon = Sphere(radius=1, color=BLACK)
        event_horizon.set_opacity(0.5)
        accretion_disk = Annulus(
            inner_radius=1.5,
            outer_radius=3,
            color=BLUE
        ).rotate(PI / 4)

        self.play(
            Transform(mass, event_horizon),
            grid.animate.scale(0.8),
            Create(accretion_disk)
        )
        photons = self.create_photon_paths()
        for photon in photons:
            self.play(Create(photon), run_time=0.5)

        self.show_narration(narrator, "Black holes warp spacetime\nso severely that light\ncannot escape!")

    def create_photon_paths(self):
        paths = [
            ParametricFunction(
                lambda t: np.array([
                    1.5 * np.cos(t),
                    1.5 * np.sin(t),
                    0.5 * np.sin(2 * t)
                ]),
                t_range=[0, 2 * PI]
            ).set_color(WHITE)
            for _ in range(5)
        ]
        return VGroup(*paths)

    def show_narration(self, narrator, text):
        bubble = ThoughtBubble()
        bubble.scale(0.7).next_to(narrator, UP)
        caption = Text(text, font_size=24).move_to(bubble.get_center())
        self.play(Create(bubble), Write(caption))
        self.wait(3)
        self.play(FadeOut(bubble), FadeOut(caption))

    def show_conclusion(self):
        final_text = Text(
            "Relativity revolutionized our understanding\nof space, time, and gravity!",
            font_size=36
        )
        final_text.set_color_by_gradient(BLUE, GREEN)
        self.play(Write(final_text))
        self.wait(3)
        self.play(FadeOut(final_text))
