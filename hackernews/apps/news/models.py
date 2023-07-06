from django.db import models


class HackerNewsItem(models.Model):

    by = models.CharField(max_length=255, blank=True, null=True)
    descendants = models.IntegerField(blank=True, null=True)
    item_id = models.IntegerField(unique=True,blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    item_type = models.CharField(max_length=255, blank=True, null=True)
    in_house = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class HackerNewsComment(models.Model):

    by = models.CharField(max_length=255, blank=True, null=True)
    item_id = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    news_item = models.ForeignKey(HackerNewsItem, null=True, blank=True, related_name='comments', to_field='item_id', on_delete=models.CASCADE)


    def __str__(self):
        parent_str = str(self.parent.id) if self.parent else "None"
        return f"{parent_str} - {self.item_id}"


