from django.shortcuts import render

# Create your views here.
def show(request):
    return render(request,'show.html')

def gmail(request):
    return render(request,'gmail.html',)

def map(request):
    return render(request,'map.html',)

