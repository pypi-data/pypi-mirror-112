import unittest
from whikoperator import functions
from whikoperator import settings


class FuncsTest(unittest.TestCase):
    def test_get_photo_test(self):
        response = functions.return_test_photo_obj(settings.TEST_PHOTO)
        print(response)


if __name__ == '__main__':
    unittest.main()