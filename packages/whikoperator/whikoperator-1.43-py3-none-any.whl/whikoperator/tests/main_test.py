import unittest
from whikoperator.main import Wpicoperator
from whikoperator import functions
from whikoperator import settings


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_test_photo_test(self):
        result_must = functions.return_test_photo_obj(settings.TEST_PHOTO)
        self.cam = Wpicoperator('192.168.100.100', 'login', 'pass', test_mode=True)
        result = self.cam.make_pic()
        self.assertEqual(result_must, result)


if __name__ == '__main__':
    unittest.main()
