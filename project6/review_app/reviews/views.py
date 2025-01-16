from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import Review, Like
from .forms import ReviewForm
from django.shortcuts import render,get_object_or_404
from.models import Review,Like

@login_required
def profile(request):

    user_reviews = Review.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'user': request.user,  
        'user_reviews': user_reviews,  
    })

def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like_count = Like.objects.filter(review=review).count()

    return render(request, 'review_detail.html', {
        'review': review,
        'like_count': like_count
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def post_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'post_review.html', {'form': form})

def review_list(request):
    category = request.GET.get('category')
    if category:
        reviews = Review.objects.filter(category=category)
    else:
        reviews = Review.objects.all()
    return render(request, 'review_list.html', {'reviews': reviews})

@login_required
def like_review(request, review_id):
    review = Review.objects.get(id=review_id)
    like, created = Like.objects.get_or_create(user=request.user, review=review)
    if not created:
        like.delete()
        return JsonResponse({'liked': False})
    return JsonResponse({'liked': True})
