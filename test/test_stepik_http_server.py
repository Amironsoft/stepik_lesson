import unittest
from app.stepik_http_server_adv import get_theor_steps


class TestStepikServer(unittest.TestCase):
    def test_server(self):
        test_id_list = [24471,
                        7627,
                        24813,
                        42713]
        for lesson_id in test_id_list:
            message, success_status = get_theor_steps(lesson_id)
            print(lesson_id, message, success_status)
            self.assertTrue(success_status)

if __name__ == '__main__':
    unittest.main()
