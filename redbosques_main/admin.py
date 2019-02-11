from django.contrib import admin

# Register your models here.
from django.contrib import admin
from redbosques_main.models import Institucion, DatosUsuario


class DatosUsuarioAdmin(admin.ModelAdmin):
    fields = ('user', 'institucion', 'admin_institucion')
    list_display = ('user', 'user_first_name', 'user_last_name', 'institucion', 'admin_institucion')
    search_fields = ['user__first_name', 'user__last_name', 'user__email' ]


class InstitucionAdmin(admin.ModelAdmin):
    fields = ('nombre', 'acronimo',)
    search_fields = ['nombre', ]


admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(DatosUsuario, DatosUsuarioAdmin)