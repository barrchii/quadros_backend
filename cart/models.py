from django.db import models
from django.conf import settings


class Print(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    medium_price = models.IntegerField(default=80)
    medium_framed_price = models.IntegerField(default=110)
    large_price = models.IntegerField(default=120)
    large_framed_price = models.IntegerField(default=150)

    class Meta:
        db_table = 'prints'

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    print_item = models.ForeignKey(Print, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=[('medium', 'Medium'), ('large', 'Large')])
    frame = models.CharField(max_length=10, choices=[('none', 'None'), ('black', 'Black'), ('wood', 'Wood')])
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return f'{self.print_item.name} - {self.size} - {self.frame}'