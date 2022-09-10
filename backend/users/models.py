from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q
from django.db.models.constraints import CheckConstraint, UniqueConstraint

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            CheckConstraint(check=~Q(user=F('author')),
                            name='could_not_follow_itself'),
            UniqueConstraint(fields=['user', 'author'], name='unique_follow'),
        ]
