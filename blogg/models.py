# models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7, default="#6366f1", help_text="Hex color code"
    )
    icon = models.CharField(
        max_length=50, blank=True, help_text="FontAwesome icon class"
    )

    # Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    color = models.CharField(
        max_length=7, default="#10b981", help_text="Hex color code"
    )

    # Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECT_TYPES = [
        ("web", "Web Application"),
        ("mobile", "Mobile App"),
        ("desktop", "Desktop Application"),
        ("api", "API/Backend"),
        ("library", "Library/Package"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("development", "In Development"),
        ("testing", "Testing"),
        ("completed", "Completed"),
        ("maintenance", "Maintenance"),
        ("archived", "Archived"),
    ]

    # Basic Information
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    short_description = models.TextField(max_length=300)
    description = HTMLField()

    # Project Details
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default="web")
    project_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="completed"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)

    # Media
    featured_image = models.ImageField(
        upload_to="projects/featured/", help_text="Main project image"
    )
    gallery = models.ManyToManyField(
        "ProjectImage", blank=True, related_name="project_gallery"
    )

    # Links and Demo
    demo_url = models.URLField(blank=True, help_text="Live demo URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    documentation_url = models.URLField(blank=True, help_text="Documentation URL")
    download_url = models.URLField(blank=True, help_text="Download URL")

    # Technical Details
    technologies = models.TextField(
        help_text="Comma-separated list of technologies used"
    )
    features = models.TextField(help_text="Key features of the project")
    challenges = models.TextField(
        blank=True, help_text="Challenges faced during development"
    )
    lessons_learned = models.TextField(
        blank=True, help_text="Lessons learned from this project"
    )

    # Project Metrics
    duration_weeks = models.PositiveIntegerField(
        blank=True, null=True, help_text="Project duration in weeks"
    )
    team_size = models.PositiveIntegerField(
        default=1, help_text="Number of team members"
    )
    client = models.CharField(
        max_length=100, blank=True, help_text="Client or company name"
    )

    # SEO and Meta
    meta_description = models.TextField(
        max_length=160, blank=True, help_text="SEO meta description"
    )
    meta_keywords = models.TextField(blank=True, help_text="SEO keywords")

    # Engagement
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_open_source = models.BooleanField(default=False)

    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    # Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date", "-date_add"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(",") if tech.strip()]

    def get_features_list(self):
        return [
            feature.strip() for feature in self.features.split("\n") if feature.strip()
        ]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    # Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "date_add"]
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


class ProjectView(models.Model):
    """Track project views for analytics"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["project", "ip_address", "session_key"]
        verbose_name = "Project View"
        verbose_name_plural = "Project Views"
