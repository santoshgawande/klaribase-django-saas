from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("member", "Member"),
        ("owner", "Tenant Owner"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="member",
        help_text="Role assigned to the user (owner/admin/member)",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
