from django.shortcuts import render
from .models import GalleryImage

# Create your views here.
def home_view(request):

	images = GalleryImage.objects.all().order_by('-created_on')

	template_name = "gallery/home.html"
	context = {"images":images}

	return render(request, template_name, context)