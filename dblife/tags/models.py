from django.db import models

class Tag(models.Model):
    name =models.CharField(max_length=32, verbose_name='태그명')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'community_tag'
        verbose_name = '태그'
        verbose_name_plural = '태그'