from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
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

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
