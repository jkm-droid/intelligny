from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import GalleryImage


class GalleryAdmin(admin.ModelAdmin):
	def image_tag(self, obj):
		return format_html(
			'<img style="width:60px; height:40px;" src="{}" />'.format(obj.image.url))

		image_tag.short_description = 'GalleryImage'

	list_display = ('title','image_tag','author','created_on','last_modified')
	list_filter = ("author","created_on",)


admin.site.register(GalleryImage,GalleryAdmin)