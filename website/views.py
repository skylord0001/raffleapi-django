from django.shortcuts import render, redirect

def home(request):
    description = 'Revolutionize your raffle experience with LuckyTreeRaffle: The top-notch Nigerian online draw platform that offers players a chance to win big through auto-randomized selection of the luckiest winner.'
    return render(request, 'home.html', {"description": description})
def terms(request):
    description = 'Welcome to Lucky Tree Raffle ("we," "us," or "our"). These Terms and Conditions ("Terms") govern your participation in our raffle activities and the use of our website. By accessing or using our website and participating in our raffles, you agree to be bound by these Terms. If you do not agree to these Terms, please refrain from using our website and participating in our raffles.'
    return render(request, 'terms.html', {"description": description})
def policy(request):
    description = 'This Privacy Policy ("Policy") describes how Lucky Tree Raffle ("we," "us," or "our") collects, uses, discloses, and protects the personal information you provide to us when you access our website and participate in our raffles. By using our website and participating in our raffles, you consent to the collection, use, and disclosure of your personal information as described in this Policy. If you do not agree with this Policy, please refrain from using our website and participating in our raffles.'
    return render(request, 'policy.html', {"description": description})
def faq(request):
    description = "Frequently Asked Questions (FAQ) for Lucky Tree Raffle."
    return render(request, 'faq.html', {"description": description})
    
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')