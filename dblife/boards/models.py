from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=64)
    contents = models.TextField()
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    tags = models.ManyToManyField('tag.Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'boards'
        verbose_name = '커뮤니티 게시판'
        verbose_name_plural = '커뮤니티 게시판'

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Board', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'