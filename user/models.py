from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    
    created_at = models.DateTimeField(auto_now_add=True)
    BUYER = 'Buyer'
    SELLER = 'Seller'

    RoleChoices = (
        (BUYER, 'Buyer'),
        (SELLER, 'Seller')
    )
    role = models.CharField(max_length=7, choices=RoleChoices, default=BUYER)
    email = models.EmailField(unique=True)

    def is_buyer(self):
        return self.role == self.BUYER

    def is_seller(self):
        return self.role == self.SELLER

    def __str__(self):
        return f"{self.username} - ({self.role})" 
