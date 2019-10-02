from django.contrib import admin

# Register your models here.
from django.contrib import admin
from redbosques_main.models import Institucion, DatosUsuario, Rodal, AuthUser, RedbosquesRodalF2Ident
import csv
from django.http import HttpResponse
from django.utils.html import format_html




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
    change_list_template = 'admin/redbosques/Rodal/change_list.html'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            kwargs["queryset"] = AuthUser.objects.all().order_by('username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def exportViewToCSV(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="listaDeRodales.csv"'
        test = RedbosquesRodalF2Ident.objects.all()
        writer = csv.writer(response)
        writer.writerow(["id", "nombre", "ccaa", "provincia", "municipio", "tipobosque_cod", "tipobosque_nomb",
                         "habitat_cod", "habitat_nomb", "hic_cod", "hic_nomb", "region_biograf", "spprinc_cod",
                         "spprinc_nomb", "spprinc_fcc", "spcomp_cod", "spcomp_nomb", "spcomp_fcc", "nm_val",
                         "ea_val", "ea",
                         "ce_val", "ab_val", "ab", "vv", "de_val", "de", "ev_val", "ev", "sn_val", "ae_val", "ae",
                         "mp",
                         "ms", "mm_val", "mm", "pm_val", "pm", "hm_val", "mh_val", "mh", "dn_val", "cs_val", "cs",
                         "hh_val",
                         "ha_val", "tb_val", "tb", "ua_val", "ua", "fa_val", "fa", "hr_val", "fr_val", "fr",
                         "ei_val",
                         "ei", "fg_val", "fg", "cz_val", "cz", "hb_val", "hb", "fc_val", "fc", "du_val", "du",
                         "ie_val",
                         "ar_val", "tr", "cf_val", "cd", "eb_val", "db", "cn_val", "dc", "institucion_acro",
                         "institucion_nomb", "trabajo", "rodal_ref"])

        for rodal in test:
            writer.writerow(
                [rodal.id, rodal.nombre, rodal.ccaa, rodal.provincia, rodal.municipio, rodal.tipobosque_cod,
                 rodal.tipobosque_nomb,
                 rodal.habitat_cod, rodal.habitat_nomb, rodal.hic_cod, rodal.hic_nomb, rodal.region_biograf,
                 rodal.spprinc_cod,
                 rodal.spprinc_nomb, rodal.spprinc_fcc, rodal.spcomp_cod, rodal.spcomp_nomb, rodal.spcomp_fcc,
                 rodal.nm_val, rodal.ea_val, rodal.ea,
                 rodal.ce_val, rodal.ab_val, rodal.ab, rodal.vv, rodal.de_val, rodal.de, rodal.ev_val, rodal.ev,
                 rodal.sn_val, rodal.ae_val, rodal.ae, rodal.mp,
                 rodal.ms, rodal.mm_val, rodal.mm, rodal.pm_val, rodal.pm, rodal.hm_val, rodal.mh_val, rodal.mh,
                 rodal.dn_val, rodal.cs_val, rodal.cs, rodal.hh_val,
                 rodal.ha_val, rodal.tb_val, rodal.tb, rodal.ua_val, rodal.ua, rodal.fa_val, rodal.fa, rodal.hr_val,
                 rodal.fr_val, rodal.fr, rodal.ei_val,
                 rodal.ei, rodal.fg_val, rodal.fg, rodal.cz_val, rodal.cz, rodal.hb_val, rodal.hb, rodal.fc_val,
                 rodal.fc, rodal.du_val, rodal.du, rodal.ie_val,
                 rodal.ar_val, rodal.tr, rodal.cf_val, rodal.cd, rodal.eb_val, rodal.db, rodal.cn_val, rodal.dc,
                 rodal.institucion_acro,
                 rodal.institucion_nomb, rodal.trabajo, rodal.rodal_ref])
        return response

    exportViewToCSV.short_description = "Exportar rodales"







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