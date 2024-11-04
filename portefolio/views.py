from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.http import FileResponse, Http404

# Create your views here.

def index(request):
     # Vérifiez si c'est la première visite de l'utilisateur
    if not request.session.get('is_returning_visitor'):
        # L'utilisateur est nouveau, donc on incrémente le compteur
        counter, created = VisitorCounter.objects.get_or_create(id=1)
        counter.total_visitors += 1
        counter.save()

        # Marquer l'utilisateur comme "déjà venu"
        request.session['is_returning_visitor'] = True

        # Récupérer le rang de l'utilisateur
        visitor_rank = counter.total_visitors
    else:
        # Récupérer le rang actuel pour les visiteurs déjà comptés
        visitor_rank = VisitorCounter.objects.get(id=1).total_visitors

    about = about_me.objects.all()
    resum  = resume.objects.all()
    serv = service.objects.all()
    skil = skill.objects.all()
    proj  = project.objects.all()
    blogg =  blog.objects.filter(status=True)
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
        'visitor_rank': visitor_rank,

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
            settings.FROM_EMAIL, 
            [settings.EMAIL_HOST_USER], 
            fail_silently=False,
        )

        messages.success(request, 'Votre message a été envoyé avec succès')
        messages.success(request, 'Your message has been sent successfully !')
        return redirect('/')
