from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')
def terms(request):
    return render(request, 'terms.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def policy(request):
    return render(request, 'policy.html')
def faq(request):
    return render(request, 'faq.html')