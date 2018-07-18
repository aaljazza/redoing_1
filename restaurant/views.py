ifrom django.shortcuts import render, redirect
from .models import Restaurant, Item, Like
from .forms import RestaurantForm, SignupForm, SigninForm, ItemForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.

def list(request):
	restaurants = Restaurant.objects.all()
	query = request.GET.get('q')
	if query:
		restaurants = restaurants.filter(
			Q(name__contains=query)|
			Q(description__contains=query)
			).distinct()
	context = {
	"restaurants": restaurants,
	"query":query
	}
	return render(request, "list.html", context)

def detail(request, restaurant_id):
	restaurant = Restaurant.objects.get(id=restaurant_id)
	items = Item.objects.filter(restaurant=restaurant)

	liked=False
	if request.user.is_authenticated:
		if Like.objects.filter(restaurant=restaurant, user=request.user).exists():
			liked=False
		else:
			liked=True

	post_like_count=restaurant.like_set.all().count()

	context = {
	"restaurant": restaurant,
	"items":items,
	"post_like_count":post_like_count,
	"liked":liked,
	}
	return render(request, "detail.html", context)

def restaurant_create(request):
	form = RestaurantForm
	if not request.user.is_authenticated:
		return redirect('signin')

	if request.method == "POST":
		form = RestaurantForm(request.POST, request.FILES)
		if form.is_valid():
			restaurant = form.save(commit=False)
			restaurant.owner = request.user
			restaurant.save()
			return redirect('list')

	context = {
	"form":form
	}
	return render(request, "create.html", context)

def restaurant_update(request, restaurant_id):
	restaurant = Restaurant.objects.get(id=restaurant_id)
	form = RestaurantForm(instance=restaurant)

	if not request.user.is_staff and not request.user == restaurant.owner:
		return redirect('no-access')
	if request.method == "POST":
		form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
		if form.is_valid():
			form.save()
			return redirect('list')

	context = {
	"restaurant":restaurant,
	"form":form
	}
	return render(request, "update.html", context)

def restaurant_delete(request, restaurant_id):
	if request.user.is_staff:
		Restaurant.objects.get(id=restaurant_id).delete()
		return redirect('list')
	return redirect('no-access')


def signup(request):
	form = SignupForm()
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			login(request, user)
			return redirect("list")

	context = {
	"form":form
	}
	return render(request, "signup.html", context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect('list')

def item_create(request, restaurant_id):
    form = ItemForm()
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if not request.user.is_staff and not request.user == restaurant.owner:
    	return redirect('no-access')
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            return redirect('detail', restaurant_id)
    context = {
        "form":form,
        "restaurant": restaurant,
    }
    return render(request, 'create_item.html', context)

def no_access(request):
	return render(request, 'no_access.html')


def ajax_like(request, restaurant_id):
	restaurant = Restaurant.objects.get(id=restaurant_id)
	new_like, created = Like.objects.get_or_create(restaurant=restaurant, user=request.user)

	if created:
		action = "like"
	else:
		action = "unlike"
		new_like.delete()

	post_like_count = restaurant.like_set.all().count()

	response = {
		"action":action,
		"post_like_count":post_like_count,
	}
	return JsonResponse(response, safe=False)