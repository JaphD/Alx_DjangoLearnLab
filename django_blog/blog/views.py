from django.shortcuts import render

# Create your views here.
def blog_view(request):
    return render(request, 'blog/base.html', {})  # Renders the home.html template