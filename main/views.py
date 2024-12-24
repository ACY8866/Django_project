# main/views.py


from django.shortcuts import render,redirect
from django.contrib import messages
from .models import News, Category,Comment
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import render
from .models import Contact


def thank_you(request):
    return render(request, 'thank_you.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            contact = form.save()

            # Send Email
            subject = contact.subject
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL, contact.email]
            text_content = f"Message from {contact.name} ({contact.email}):\n\n{contact.message}"
            html_content = f"""
             <h2>New Contact Us Inquiry</h2>
            <p><strong>Name:</strong> {contact.name}</p>
            <p><strong>Email:</strong> {contact.email}</p>
            <p><strong>Subject:</strong> {contact.subject}</p>
            <p><strong>Message:</strong><br>{contact.message}</p>
            """
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except Exception as e:
                # Handle the error or log it for debugging
                print(f"Error sending email: {e}")

            return redirect('thank_you')  # Redirect to a 'thank_you' view
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})





def home(request):
    first_news=News.objects.first()
    three_news=News.objects.all()
    three_categories=Category.objects.all()
    return render(request,'home.html',{
        'first_news':first_news,
        'three_news':three_news,
        'three_categories':three_categories
    })

# All News
def all_news(request):
    all_news=News.objects.all()
    return render(request,'all-news.html',{
        'all_news':all_news
    })

# Detail Page
def detail(request,id):
    news=News.objects.get(pk=id)
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        comment=request.POST['message']
        Comment.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment
        )
        messages.success(request,'Comment submitted but in moderation mode.')
    category=Category.objects.get(id=news.category.id)
    rel_news=News.objects.filter(category=category).exclude(id=id)
    comments=Comment.objects.filter(news=news,status=True).order_by('-id')
    return render(request,'detail.html',{
        'news':news,
        'related_news':rel_news,
        'comments':comments
    })

# Fetch all category
def all_category(request):
    cats=Category.objects.all()
    return render(request,'category.html',{
        'cats':cats
    })


# Fetch all category
def category(request,id):
    category=Category.objects.get(id=id)
    news=News.objects.filter(category=category)
    return render(request,'category-news.html',{
        'all_news':news,
        'category':category
    })

