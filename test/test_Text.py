import unittest
import Text


class TestTextMethods(unittest.TestCase):
    Text.base_path = "../PokerInPython/"
    Text.font_path = f"../PokerInPython/Font/Minecraft.ttf"

    def test_smoke(self):
        text = Text.Text("Test", 32, (0, 0, 0), (255, 255, 255))
        self.assertEqual(text.text_string, "Test")

    def test_can_change_text(self):
        text = Text.Text("Test", 32, (0, 0, 0), (255, 255, 255))
        self.assertEqual(text.text_string, "Test")

        text.set_text("Change")
        self.assertEqual(text.text_string, "Change")

    def test_can_move_text(self):
        text = Text.Text("Test", 32, (0, 0, 0), (255, 255, 255))
        self.assertEqual(text.text_rect.x, 0)
        self.assertEqual(text.text_rect.y, 0)

        text.move_to(100, 100)
        self.assertEqual(text.text_rect.x, 100)
        self.assertEqual(text.text_rect.y, 100)

if __name__ == '__main__':
    unittest.main()
