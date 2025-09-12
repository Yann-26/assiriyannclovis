# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import DetailView
from django.db.models import Q, F
from .models import Project, ProjectView



class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(status=True).prefetch_related(
            "images", "tags", "category"
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Track project view
        self.track_project_view(obj)

        # Increment view count
        Project.objects.filter(pk=obj.pk).update(views=F("views") + 1)

        return obj

    def track_project_view(self, project):
        """Track project views for analytics"""
        try:
            ip_address = self.get_client_ip()
            user_agent = self.request.META.get("HTTP_USER_AGENT", "")
            referrer = self.request.META.get("HTTP_REFERER", "")
            session_key = self.request.session.session_key or ""

            ProjectView.objects.get_or_create(
                project=project,
                ip_address=ip_address,
                session_key=session_key,
                defaults={
                    "user_agent": user_agent,
                    "referrer": referrer,
                },
            )
        except Exception as e:
            # Log error but don't break the view
            print(f"Error tracking project view: {e}")

    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Related projects
        related_projects = (
            Project.objects.filter(status=True)
            .exclude(pk=project.pk)
            .filter(Q(category=project.category) | Q(tags__in=project.tags.all()))
            .distinct()[:3]
        )

        context.update(
            {
                "related_projects": related_projects,
                "project_images": project.images.filter(status=True).order_by("order"),
                "meta_title": f"{project.title} - Project Details",
                "meta_description": project.meta_description
                or project.short_description,
                "meta_keywords": project.meta_keywords,
                "og_image": project.featured_image.url
                if project.featured_image
                else None,
            }
        )

        return context


def project_detail(request, slug):
    """Function-based view alternative"""
    project = get_object_or_404(
        Project.objects.prefetch_related("images", "tags", "category"),
        slug=slug,
        status=True,
    )

    # Track view
    track_project_view(request, project)

    # Increment view count
    Project.objects.filter(pk=project.pk).update(views=F("views") + 1)

    # Get related projects
    related_projects = (
        Project.objects.filter(status=True)
        .exclude(pk=project.pk)
        .filter(Q(category=project.category) | Q(tags__in=project.tags.all()))
        .distinct()[:3]
    )

    context = {
        "project": project,
        "related_projects": related_projects,
        "project_images": project.images.filter(status=True).order_by("order"),
        "meta_title": f"{project.title} - Project Details",
        "meta_description": project.meta_description or project.short_description,
        "meta_keywords": project.meta_keywords,
        "og_image": project.featured_image.url if project.featured_image else None,
    }

    return render(request, "project_detail.html", context)


def track_project_view(request, project):
    """Track project views for analytics"""
    try:
        # Get client IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT", "")
        referrer = request.META.get("HTTP_REFERER", "")
        session_key = request.session.session_key or ""

        ProjectView.objects.get_or_create(
            project=project,
            ip_address=ip_address,
            session_key=session_key,
            defaults={
                "user_agent": user_agent,
                "referrer": referrer,
            },
        )
    except Exception as e:
        print(f"Error tracking project view: {e}")


def ajax_project_like(request, slug):
    """AJAX view to handle project likes"""
    if request.method == "POST":
        project = get_object_or_404(Project, slug=slug, status=True)

        # Simple like system (in production, you might want to track user likes)
        Project.objects.filter(pk=project.pk).update(likes=F("likes") + 1)
        project.refresh_from_db()

        return JsonResponse(
            {"status": "success", "likes": project.likes, "message": "Project liked!"}
        )

    return JsonResponse({"status": "error", "message": "Invalid request"})


def project_demo_proxy(request, slug):
    """
    Proxy view for project demos to handle CORS issues
    This is optional - use only if you need to proxy external demos
    """
    project = get_object_or_404(Project, slug=slug, status=True)

    if not project.demo_url:
        return JsonResponse({"error": "No demo URL available"}, status=404)

    # You can add logic here to proxy the demo URL
    # For security reasons, this is just a placeholder

    return JsonResponse(
        {
            "demo_url": project.demo_url,
            "title": project.title,
            "instructions": "Demo available at the provided URL",
        }
    )


