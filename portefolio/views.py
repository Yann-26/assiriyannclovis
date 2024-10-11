from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.http import FileResponse, Http404

# Create your views here.

def index(request):
    about = about_me.objects.all()
    resum  = resume.objects.all()
    serv = service.objects.all()
    skil = skill.objects.all()
    proj  = project.objects.all()
    blogg =  blog.objects.all()
    testicard = testi_cards.objects.all()
    contac = get_object_or_404(contact, id=1)
    land = landing.objects.all()
    catal = catalog.objects.all()
    socialinks = SocialLink.objects.all()

    datas = {
        'about' :about,
        'resum' : resum,
        'serv' : serv,
        'skil' : skil,
        'proj' : proj,
        'blogg' :  blogg,
        'testicard' : testicard,
        'contac' : contac,
        'land' : land,
        'catal' : catal,
        'socialinks' : socialinks,

     }
    return render(request, 'index.html', datas)


def singleblog(request, blog_id):
    le_blog = get_object_or_404(blog, id=blog_id)
    return render(request, 'single.html', {'le_blog':le_blog} )


def download_cv(request, item_id):
    item = get_object_or_404(about_me, id=item_id)
    file_path = item.cv.path
    try:
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=item.cv.name)
    except FileNotFoundError:
        raise Http404("File not found")


def send_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        new_contact = contact.objects.create(
            visitor_name=name,
            visitor_email=email,
            visitor_subject=subject,
            visitor_message=message
        )
        new_contact.save()
           # Envoi de email
        full_message = f"Nom: {name}\nEmail: {email}\nSujet: {subject}\nMessage: {message}"
        send_mail(
            subject,  
            full_message, 
            settings.EMAIL_HOST_USER, 
            [email], 
            fail_silently=False,
        )

        messages.success(request, 'Votre message a été envoyé avec succès')
        return redirect('/')

