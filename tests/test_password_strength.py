import unittest
from src.password_strength import PasswordValidator

class TestPasswordStrength(unittest.TestCase):
    def setUp(self):
        self.validator = PasswordValidator()

    def test_strong_password(self):
        pwd = "SecurePass123!"
        result = self.validator.evaluate_password(pwd)
        self.assertEqual(result['strength'], 'Strong')

    def test_weak_password(self):
        pwd = "weak"
        result = self.validator.evaluate_password(pwd)
        self.assertIn('Weak', result['strength'])

    def test_common_password(self):
        pwd = "password123"
        result = self.validator.evaluate_password(pwd)
        self.assertIn('Very Weak', result['strength'])

    def test_pattern_detection(self):
        pwd = "aaaabbbb1234"
        result = self.validator.evaluate_password(pwd)
        self.assertIn('common patterns', result['suggestions'][0])

if __name__ == '__main__':
    unittest.main()