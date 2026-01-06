import re
from django.core.exceptions import ValidationError

class PasswordComplexityValidator:
    def validate(self, password, user=None):
        if not password:
            return
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        if not re.match(pattern, password):
            raise ValidationError(
                "Password must be at least 8 characters and include a capital letter, a number, a symbol, and lowercase letters."
            )

    def get_help_text(self):
        return "Password must be 8+ characters, include uppercase, lowercase, number, and symbol."
