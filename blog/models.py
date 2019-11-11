from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    last_modified = models.DateField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

  
    def get_absolute_url(self):
        return f"/blog/category/{self.slug}"


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Post(models.Model):
    title   = models.CharField(max_length=70, unique=True)
    slug    = models.SlugField(unique=True)
    image   = models.ImageField(upload_to='images/', blank=True)
    author  = models.CharField(max_length=70, blank=False)
    created_on      = models.DateField(auto_now=False, auto_now_add=True)
    last_modified   = models.DateField(auto_now=True, auto_now_add=False)
    categories      = models.ManyToManyField("Category", related_name="posts")
    body    = RichTextUploadingField()
    status          = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def body_html( self ):
        return markdown_to_html( self.body, self.images.all() )

class Comments(models.Model):
    author = models.CharField(max_length=50)
    body   = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Comments"

class DailyQuote(models.Model):
    author = models.CharField(max_length=70)
    quote = models.TextField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

class Carousel(models.Model):
    image = models.ImageField(upload_to='wallpapers/', blank=True)
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Carousel"

    def body_html( self ):
        return markdown_to_html( self.body, self.images.all() )