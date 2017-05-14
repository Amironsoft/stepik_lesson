import unittest
from app.stepik_http_server_adv import get_theor_steps


class TestStepikServer(unittest.TestCase):
    def test_server_positive(self):
        test_id_list_positive = [24471,
                        7627,
                        24813,
                        42713]
        for lesson_id in test_id_list_positive:
            message, success_status = get_theor_steps(lesson_id)
            print(lesson_id, message, success_status)
            self.assertTrue(success_status)

    def test_server_negative(self):
        test_id_list_negative = [244711111,
                                 7627777,
                                 'some strange str',
                                 ['{', 12312321312]]
        for lesson_id in test_id_list_negative:
            message, success_status = get_theor_steps(lesson_id)
            print(lesson_id, message, success_status)
            self.assertFalse(success_status)


if __name__ == '__main__':
    unittest.main()
