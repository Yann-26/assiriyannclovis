from django.contrib import admin
from .models import (
    about_me,
    resume,
    service,
    skill,
    Blog,
    testi_cards,
    landing,
    catalog,
    contact,
    SocialLink,
    BlogCategory,
    BlogTag,
)

# Register your models here.
admin.site.register(about_me)
admin.site.register(resume)
admin.site.register(service)
admin.site.register(skill)
admin.site.register(Blog)
admin.site.register(BlogTag)
admin.site.register(BlogCategory)
admin.site.register(contact)
admin.site.register(landing)
admin.site.register(catalog)
admin.site.register(SocialLink)
admin.site.register(testi_cards)
