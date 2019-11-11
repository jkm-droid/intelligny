from django.db import models

# Create your models here.
class GalleryImage(models.Model):
	image = models.ImageField(upload_to="gallery/")
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

	class Meta:
		ordering = ['-created_on']

	def __unicode__(self):
		return self.title