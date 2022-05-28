from django.contrib import admin
import arctel.models as models


class NewAdmin(admin.ModelAdmin):
    list_display = ("title", "date")

    class Meta:
        ordering = ("-date",)


class DirectoryAdmin(admin.ModelAdmin):
    list_display = ("identifier",)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "directory")


class FormationOffer(admin.ModelAdmin):
    list_display = ("id", "title", )


class WagtailPage(admin.ModelAdmin):
    list_display = ("id", )


admin.site.register(models.New, NewAdmin)
admin.site.register(models.Directory, DirectoryAdmin)
admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.FormationOffer, FormationOffer)
admin.site.register(models.Page, WagtailPage)
