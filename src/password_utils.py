import secrets
import string

class PasswordGenerator:
    def __init__(self):
        self.characters = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'digits': string.digits,
            'special': '!@#$%^&*'
        }

    def generate_strong_password(self, length=12):
        if length < 12:
            raise ValueError("Password length must be at least 12 characters")
        
        # Ensure at least one of each character type
        password = [
            secrets.choice(self.characters['uppercase']),
            secrets.choice(self.characters['lowercase']),
            secrets.choice(self.characters['digits']),
            secrets.choice(self.characters['special'])
        ]
        
        # Fill remaining length
        remaining = length - 4
        all_chars = ''.join(self.characters.values())
        password += [secrets.choice(all_chars) for _ in range(remaining)]
        
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)