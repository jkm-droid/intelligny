from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from random import shuffle

from .forms import CommentsForm
from .models import Post, Category, Comments, DailyQuote

# Create your views here.
def all_posts_view(request):
	#get all the posts in the order they were created
    posts = Post.objects.filter(status=1).order_by('-created_on')

    #get all the categories
    categories = Category.objects.all().order_by('-created_on')

    #pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')

    #get the latest quote
    quote = DailyQuote.objects.all().order_by('-created_on')[:1]

    first_three = Post.objects.filter(status=1).order_by('-id')[4:8]
    last_three = Post.objects.filter(status=1).order_by('id')[:4]

    try:
    	posts = paginator.page(page)
    except PageNotAnInteger:
    	posts = paginator.page(1)
    except EmptyPage:
    	posts = paginator.page(paginator.num_pages)

    template_name = "blog/posts/all_posts.html"
    context = {
    			"posts":posts,
    			"categories":categories, 
    			"quotes":quote,
    			"last":last_three,
    			"first":first_three
    			}
    
    return render(request, template_name, context)

def single_post_view(request, post_slug):
	#get a specific post and its details
	#raise an error if no post is found
	try:
		post = Post.objects.get(slug=post_slug)
	except:
		raise Http404

	#get the comment form from forms.py
	form = CommentsForm()
	if request.method == "POST":
		form = CommentsForm(request.POST)

		#get all the data if the form is correctly filled
		if form.is_valid():
			comment = Comments(
					author = form.cleaned_data['author'],
					body = form.cleaned_data['body'],
					post = post
				)
			#save the form data
			comment.save()
			messages.info(request, "Comment sent successfully")
			form = CommentsForm()
			
	#get all the comments related to the post from db
	comments = Comments.objects.filter(post=post).order_by('-created_on')

	#get all the categories
	categories = Category.objects.all().order_by('-created_on')

	#getting two of the latest posts 
	latest_posts = Post.objects.filter(status=1)[:2]
	latest_list = list(latest_posts)
	shuffle(latest_list)
	
	template_name = "blog/posts/single_post.html"
	context = {"post_details":post,
				"comments":comments,
				"form":form,
				"latest_posts":latest_list,
				"categories": categories}

	#display all the post_details and comments to the html template
	return render(request, template_name, context)

def category_view(request, category):
	#get the category mapped with post
	category = Category.objects.get(slug=category)

	#get the posts mapped with the category
	posts = Post.objects.filter(
		categories__name__contains=category,status=1).order_by('-created_on')

	#get all the categories
	categories = Category.objects.all().order_by('-created_on')

	template_name = "blog/category/category.html"
	context = {"category":category, 
				"posts":posts,
				"categories":categories
				}
	#display the contents to the user
	return render(request, template_name, context)


def search_posts_view(request):

	if request.method == 'GET':
		query = request.GET.get('q').capitalize()
		if query == '':
			messages.info(request, 
				"You cannot search for an empty string.Kindly type something and click the search button")
			return redirect('/blog')
		else:
			results = Post.objects.filter(
								Q(title__icontains=query)|
								Q(title__iexact=query)
						).distinct().order_by('created_on')

			context = {"search_term":query,
						"posts":results}
			template_name = "blog/search.html"

			return render(request, template_name, context)
	else:
		return redirect('blog/home')
		

def about_view(request):

	template_name = "blog/about.html"

	return render(request, template_name)

