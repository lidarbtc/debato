from django.db import models

class User(models.Model):
    username = models.CharField(max_length=64)
    useremail = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'community_user'
        verbose_name = '커뮤니티 사용자'
        verbose_name_plural = '커뮤니티 사용자'