"""Regression checks for intentionally replaced headers and reserved footers."""
import unittest

from manim import RoundedRectangle

from shared.narrated import NarratedScene
from shared.style import T, header
from shared.workshop import tally_text


class LayoutHeaderReplacementTests(unittest.TestCase):
    def test_hidden_header_does_not_cause_false_crowding(self):
        scene = NarratedScene()
        h = header("Q27 part a: calibration")
        ribbon = RoundedRectangle(width=12.0, height=0.75).move_to([0, 2.89, 0])
        scene.add(h, ribbon)
        self.assertTrue(any("header-crowding" in x for x in scene.layout_problems()))
        h.set_opacity(0)
        self.assertFalse(any("header-crowding" in x for x in scene.layout_problems()))

    def test_intentional_mark_tally_may_occupy_footer(self):
        scene = NarratedScene()
        scene.add(tally_text("Q27", 3, 14))
        self.assertEqual(scene.layout_problems(), [])

    def test_regular_content_still_triggers_caption_warning(self):
        scene = NarratedScene()
        scene.add(T("ordinary diagram label").move_to([0, -3.4, 0]))
        self.assertTrue(any("caption-strip" in x for x in scene.layout_problems()))

    def test_footer_can_still_trigger_off_frame_warning(self):
        scene = NarratedScene()
        footer = tally_text("Q27", 3, 14)
        footer.move_to([0, -4.4, 0])
        scene.add(footer)
        self.assertTrue(any("off-frame" in x for x in scene.layout_problems()))


if __name__ == "__main__":
    unittest.main()
