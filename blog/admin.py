from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from blog.models import Category, Post, Comments, DailyQuote, Carousel

class CarouselAdmin(admin.ModelAdmin):
	def image_tag(self, obj):
		return format_html(
			'<img style="width:80px; height:50px;" src="{}" />'.format(obj.image.url))
	
	image_tag.short_description = 'Image'

	list_display = ('name','image_tag','created_on')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','slug','created_on','last_modified')
	list_filter = ("name","created_on",)
	prepopulated_fields = {'slug': ('name',)}

class CommentsAdmin(admin.ModelAdmin):

	list_display = ('author','body','post','created_on')
	list_filter = ("author","created_on",)


class PostsAdmin(admin.ModelAdmin):
	def image_tag(self, obj):
		return format_html(
			'<img style="width:30px; height:30px;" src="{}" />'.format(obj.image.url))
	
	image_tag.short_description = 'Image'

	def make_published_posts(self, request, queryset):
		updated_rows = queryset.update(status=1)

		if updated_rows == 1:
			message = "1 story was"
		else:
			message = "%s stories were" % updated_rows
		self.message_user(request,"%s successfully published" %message)

	make_published_posts.short_description = "Publish the selected posts"

	def make_drafted_posts(self, request, queryset):
		updated_rows = queryset.update(status=0)

		if updated_rows == 1:
			message = "1 story was"
		else:
			message = "%s stories were" % updated_rows
		self.message_user(request,"%s successfully unpublished" %message)

	make_drafted_posts.short_description = "UnPublish the selected posts"

	

	list_display = ('title', 'image_tag','status', 'author','created_on','last_modified')
	list_filter = ("status","created_on","author",)
	search_fields = ['title', 'categories__name','author']
	prepopulated_fields = {'slug': ('title',)}
	actions = [make_published_posts, make_drafted_posts]

class DailyQuoteAdmin(admin.ModelAdmin):
	list_display = ('quote','author','created_on')


admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(DailyQuote, DailyQuoteAdmin)

admin.site.site_title='Intelligny'
admin.site.site_header="Intelligny AdminPanel"
admin.site.index_title = 'Intelligny ControlPanel'

