from django.shortcuts import redirect, get_object_or_404
from .models import (
    about_me,
    resume,
    service,
    skill,
    testi_cards,
    landing,
    catalog,
    contact,
    SocialLink,
    project,
)
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse, Http404
from blogg.models import Project, Category, Tag
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages

# Create your views here.


class index(ListView):
    model = Project
    template_name = "index.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = Project.objects.filter(status=True).prefetch_related(
            "tags", "category"
        )

        # Filter by category
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)

        # Filter by tag
        tag = self.request.GET.get("tag")
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        # Filter by project type
        project_type = self.request.GET.get("type")
        if project_type:
            queryset = queryset.filter(project_type=project_type)

        # Search
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(short_description__icontains=search)
                | Q(technologies__icontains=search)
            )

        # Ordering
        order_by = self.request.GET.get("order", "-published_date")
        if order_by in ["-published_date", "-views", "-likes", "title"]:
            queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "about": about_me.objects.all(),
                "resum": resume.objects.all(),
                "serv": service.objects.all(),
                "skil": skill.objects.all(),
                "testicard": testi_cards.objects.all(),
                "contac": get_object_or_404(contact, id=1),
                "land": landing.objects.all(),
                "catal": catalog.objects.all(),
                "proj": project.objects.all(),
                "socialinks": SocialLink.objects.all(),
                "categories": Category.objects.filter(status=True),
                "tags": Tag.objects.filter(status=True),
                "project_types": Project.PROJECT_TYPES,
                "current_category": self.request.GET.get("category"),
                "current_tag": self.request.GET.get("tag"),
                "current_type": self.request.GET.get("type"),
                "search_query": self.request.GET.get("search", ""),
                "current_order": self.request.GET.get("order", "-published_date"),
            }
        )

        return context


def download_cv(request, item_id):
    item = get_object_or_404(about_me, id=item_id)
    file_path = item.cv.path
    try:
        return FileResponse(
            open(file_path, "rb"), as_attachment=True, filename=item.cv.name
        )
    except FileNotFoundError:
        raise Http404("File not found")


def send_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        new_contact = contact.objects.create(
            visitor_name=name,
            visitor_email=email,
            visitor_subject=subject,
            visitor_message=message,
        )
        new_contact.save()
        # Envoi de email
        full_message = (
            f"Nom: {name}\nEmail: {email}\nSujet: {subject}\nMessage: {message}"
        )
        send_mail(
            subject,
            full_message,
            settings.FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        messages.success(request, "Votre message a été envoyé avec succès")
        messages.success(request, "Your message has been sent successfully !")
        return redirect("/")
