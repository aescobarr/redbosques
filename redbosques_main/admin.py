from django.contrib import admin

# Register your models here.
from django.contrib import admin
from redbosques_main.models import Institucion, DatosUsuario, Rodal, AuthUser
import csv
from django.http import HttpResponse


class DatosUsuarioAdmin(admin.ModelAdmin):
    fields = ('user', 'institucion', 'admin_institucion')
    list_display = ('user', 'user_first_name', 'user_last_name', 'institucion', 'admin_institucion')
    search_fields = ['user__first_name', 'user__last_name', 'user__email' ]


class InstitucionAdmin(admin.ModelAdmin):
    fields = ('nombre', 'acronimo',)
    search_fields = ['nombre', ]


class RodalAdmin(admin.ModelAdmin):
    fields = ('datosrestringidos', 'metodo_cod', 'nombre', 'comautonom_cod', 'provincia_cod', 'municipio', 'propietario', 'fecha', 'equipo', 'lpeht_cod', 'hic_cod', 'regbio_cod', 'espprinc_cod', 'espcomp_cod', 'espprincip_h0', 'espcomp_h0', 'numesparb', 'areabasal', 'volmadvivo', 'numestratos', 'numclasdiam', 'abundpiesexcep', 'volmmpie', 'volmmsuelo', 'volmmprop', 'nummicrohab', 'numfasessil', 'valpropbosc56', 'valagropasant', 'valforestant', 'valforestrec', 'valespinvas', 'valfragment', 'valcaza', 'valherbiv', 'valfrecuent', 'valdurabusos', 'otroespflora', 'otrohics', 'otroinfo', 'notes', 'dateadded', 'volmmtotal', 'usuario', 'rodalref', 'fotoglobo', 'espprinc_fcc', 'espcomp_fcc', 'municipio1',)
    list_display = ('nombre', 'usuario', 'municipio1',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            kwargs["queryset"] = AuthUser.objects.all().order_by('username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    '''def export_users_csv(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

        users = Rodal.objects.all()
        for user in users:
            writer.writerow(user)

        return response'''


admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(DatosUsuario, DatosUsuarioAdmin)
admin.site.register(Rodal, RodalAdmin)