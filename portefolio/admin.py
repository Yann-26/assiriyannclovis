from django.contrib import admin
from .models import (
    about_me,
    resume,
    service,
    skill,
    project,
    testi_cards,
    landing,
    catalog,
    contact,
    SocialLink,
)

# Register your models here.
admin.site.register(about_me)
admin.site.register(resume)
admin.site.register(service)
admin.site.register(skill)
admin.site.register(project)
admin.site.register(testi_cards)
admin.site.register(contact)
admin.site.register(landing)
admin.site.register(catalog)
admin.site.register(SocialLink)
