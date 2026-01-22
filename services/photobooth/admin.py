from django.contrib import admin

# Register your models here.
from .models import Event, Session, File, Voucher

admin.site.register(Event)
admin.site.register(Session)
admin.site.register(File)
admin.site.register(Voucher)