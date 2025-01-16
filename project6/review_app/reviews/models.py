from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('movie', '映画'),
    ('anime', 'アニメ'),
    ('novel', '小説'),
    ('manga', '漫画'),
    ('game', 'ゲーム'),
    ('other', 'その他'),
]

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='reviews/photos/', blank=True, null=True)
    comment = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=[(i, f'{i} Stars') for i in range(1, 6)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
