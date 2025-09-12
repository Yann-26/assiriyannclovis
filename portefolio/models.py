from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class about_me(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    address = models.CharField(max_length=50)
    email =  models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    cv =  models.FileField(upload_to='cv/')
    cellphone =  models.CharField(max_length=50)
    description = models.TextField()

    # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"Je suis {self.name}"
    

class resume(models.Model):
  
    year = models.CharField(max_length=50)
    diplome_or_post = models.CharField(max_length=50)
    entreprise_or_school = models.CharField(max_length=50)
    short_resume = models.CharField(max_length=250)

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.diplome_or_post
    

class service(models.Model):
  
    icon = models.CharField(max_length=50)
    service_name = models.CharField(max_length=50)

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.service_name
    

class skill(models.Model):
    
    title = models.CharField(max_length=25)
    percentage = models.IntegerField()

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title
    

# ############################################################
class BlogCategory(models.Model):
    """Category model for organizing blog posts"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    # Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    """Tag model for blog post tagging"""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    # Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """Enhanced Blog model with additional fields and functionality"""

    # Basic Information
    title = models.CharField(max_length=200, help_text="Blog post title")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="URL slug (auto-generated if empty)",
    )
    subtitle = models.CharField(
        max_length=300, blank=True, null=True, help_text="Optional subtitle"
    )

    # Content
    excerpt = models.TextField(
        max_length=500, blank=True, null=True, help_text="Short description/summary"
    )
    content = models.TextField(help_text="Main blog content")

    # Media
    featured_image = models.ImageField(
        upload_to="blog/images/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text="Main blog image",
    )
    featured_image_alt = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Alt text for featured image (for SEO and accessibility)",
    )

    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        help_text="Blog post author",
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="blog_posts")

    # Publishing
    is_published = models.BooleanField(
        default=False, help_text="Publish this blog post"
    )
    publish_date = models.DateTimeField(
        default=timezone.now, help_text="When to publish this post"
    )
    date_issue = models.DateField(auto_now_add=True, help_text="Original creation date")

    # SEO Fields
    meta_title = models.CharField(
        max_length=60, blank=True, null=True, help_text="SEO meta title (60 chars max)"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        null=True,
        help_text="SEO meta description (160 chars max)",
    )
    meta_keywords = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="SEO keywords (comma separated)",
    )

    # Analytics
    view_count = models.PositiveIntegerField(default=0, help_text="Number of views")
    reading_time = models.PositiveIntegerField(
        default=0, help_text="Estimated reading time in minutes"
    )

    # Social Sharing
    allow_comments = models.BooleanField(
        default=True, help_text="Allow comments on this post"
    )
    featured = models.BooleanField(
        default=False, help_text="Feature this post on homepage"
    )

    # Standards
    status = models.BooleanField(default=True, help_text="Active/Inactive status")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-publish_date", "-date_add"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["publish_date"]),
            models.Index(fields=["is_published", "status"]),
            models.Index(fields=["featured"]),
        ]

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)

        # Ensure unique slug
        original_slug = self.slug
        counter = 1
        while Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:60]

        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]

        # Calculate reading time (average 200 words per minute)
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the absolute URL for this blog post"""
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def get_published_posts():
        """Class method to get published posts"""
        return Blog.objects.filter(
            is_published=True, status=True, publish_date__lte=timezone.now()
        )

    def get_related_posts(self, limit=3):
        """Get related posts based on tags and category"""
        related_posts = Blog.objects.filter(
            is_published=True, status=True, publish_date__lte=timezone.now()
        ).exclude(pk=self.pk)

        if self.category:
            related_posts = related_posts.filter(category=self.category)

        if self.tags.exists():
            related_posts = related_posts.filter(tags__in=self.tags.all()).distinct()

        return related_posts.order_by("-publish_date")[:limit]

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=["view_count"])

    @property
    def is_published_now(self):
        """Check if post should be visible now"""
        return self.is_published and self.status and self.publish_date <= timezone.now()

    @property
    def get_tags_list(self):
        """Get comma-separated list of tag names"""
        return ", ".join([tag.name for tag in self.tags.all()])

    def __str__(self):
        return self.title
    

# ############################################################
class testi_cards(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=50)

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title

class contact(models.Model):
  
    address = models.CharField(max_length=50, blank=True, null=True)
    contact_number =models.CharField(max_length=50, blank=True, null=True)
    mon_email = models.EmailField(blank=True, null=True)
    
    # form
    visitor_name = models.CharField(max_length=50, blank=True, null=True)
    visitor_email = models.EmailField(blank=True, null=True)
    visitor_subject = models.CharField(max_length=500, blank=True, null=True)
    visitor_message = models.TextField(blank=True, null=True)

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.visitor_subject} de {self.visitor_email}"
    
class landing(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='landing/')

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title
    

class catalog(models.Model):
    file = models.FileField(upload_to='catalog/')
    file_title = models.CharField(max_length=50)

    # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.file_title
    

class SocialLink(models.Model):
    link = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=500 , blank=True, null=True)
   
     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

class VisitorCounter(models.Model):
    total_visitors = models.IntegerField(default=0)

    def __str__(self):
        return f"Total Visitors: {self.total_visitors}"





    









