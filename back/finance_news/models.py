from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(unique=True)
    published_date = models.DateTimeField(null=True, blank=True)
    press = models.CharField(max_length=100, null=True, blank=True)
    crawled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date', '-crawled_at']

    def __str__(self):
        return self.title