import re
from pathlib import Path

class PasswordValidator:
    def __init__(self):
        self.common_passwords = set()
        self._load_common_passwords()
    
    def _load_common_passwords(self):
        try:
            with open(Path(__file__).parent / 'common_passwords.txt', 'r') as f:
                self.common_passwords = set(f.read().splitlines())
        except FileNotFoundError:
            print("Warning: Common passwords file not found")

    def _check_common_patterns(self, password):
        patterns = [
            r'(.)\1{2,}',  # Repeated characters
            r'12345|54321',  # Number sequences
            r'qwerty|asdfgh|zxcvbn',  # Keyboard patterns
            r'password|admin|letmein'  # Common weak passwords
        ]
        return any(re.search(pattern, password.lower()) for pattern in patterns)

    def evaluate_password(self, password):
        score = 0
        feedback = []
        strength = {'score': 0, 'strength': '', 'suggestions': []}

        # Initial checks
        if password in self.common_passwords:
            strength['suggestions'].append("❌ This password is too common")
            return {**strength, 'strength': 'Very Weak'}

        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
            feedback.append("🔍 Consider making password longer (12+ characters)")
        else:
            feedback.append("❌ Password must be at least 8 characters")

        # Character diversity
        checks = {
            'uppercase': r'[A-Z]',
            'lowercase': r'[a-z]',
            'digit': r'\d',
            'special': r'[!@#$%^&*]'
        }

        for name, pattern in checks.items():
            if re.search(pattern, password):
                score += 1
            else:
                feedback.append(
                    f"❌ Missing {name} character" if name != 'special' 
                    else "❌ Missing special character (!@#$%^&*)"
                )

        # Deductions for bad patterns
        if self._check_common_patterns(password):
            score = max(0, score - 2)
            feedback.append("❌ Contains common patterns or sequences")

        # Determine strength
        if score >= 7:
            strength['strength'] = 'Strong'
        elif 4 <= score < 7:
            strength['strength'] = 'Moderate'
        else:
            strength['strength'] = 'Weak'

        strength['score'] = min(10, max(0, score))  # Clamp score 0-10
        strength['suggestions'] = feedback
        
        return strength