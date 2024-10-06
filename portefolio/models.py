from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class about_me(models.Model):
  
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    address = models.CharField(max_length=50)
    email =  models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    cv =  models.FileField(upload_to='cv/')
    cellphone =  models.CharField(max_length=50)

    # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"Je suis {about_me.name}"
    

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
    
class project(models.Model):
    project_name = models.CharField(max_length=50)
    image =models.ImageField(upload_to='projects/')
  

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.project_name
    
class blog(models.Model):
    title = models.CharField(max_length=50)
    
    date = models.DateField()
    short_description = models.TextField()
    description = HTMLField()
    image  = models.ImageField(upload_to='blog/')

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title
    
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
    whatsapp_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    discord_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    pinterest_link = models.URLField(blank=True, null=True)
    tiktok_link = models.URLField(blank=True, null=True)
    snap_link = models.URLField(blank=True, null=True)
    reddit_link = models.URLField(blank=True, null=True)
    tumblr_link = models.URLField(blank=True, null=True)
    vimeo_link = models.URLField(blank=True, null=True)
    flickr_link = models.URLField(blank=True, null=True)
    wechat_link = models.URLField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    tiktok_link = models.URLField(blank=True, null=True)
    quora_link = models.URLField(blank=True, null=True)
    nextdoor_link = models.URLField(blank=True, null=True)
    parler_link = models.URLField(blank=True, null=True)
     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Link_name(models.Model):
    link_name = models.CharField(max_length=50)
    link_url = models.ForeignKey(SocialLink, related_name='social_link',on_delete=models.SET_NULL, blank=True, null=True)

     # STANDARDS 
    status  = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"this is {self.link_name} link"



    









