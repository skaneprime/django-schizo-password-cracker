from django.db import models
from django.contrib.auth.models import User
import hashlib
from itertools import product

class HashRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_value = models.CharField(max_length=32)
    request_time = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def _hash_is_from_limited_alphabet(hash_value):
        # Allowed characters and maximum password length
        characters = 'abcdefghijklmnopqrstuvwxyz'
        max_length = 5
        # Generate all possible passwords and their MD5 hashes
        for length in range(1, max_length + 1):
            for combo in product(characters, repeat=length):
                password = ''.join(combo)
                if hashlib.md5(password.encode()).hexdigest() == hash_value:
                    return True
        return False
