from django.contrib import admin

from services.template.models import Template, TemplateSize, Dropzone


class TemplateSizeInline(admin.StackedInline):
    model = TemplateSize
    extra = 0
    max_num = 1
    can_delete = True


class DropzoneInline(admin.TabularInline):
    model = Dropzone
    extra = 0


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "location")
    search_fields = ("name", "type")
    list_filter = ("type",)

    inlines = [
        TemplateSizeInline,
        DropzoneInline,
    ]


@admin.register(TemplateSize)
class TemplateSizeAdmin(admin.ModelAdmin):
    list_display = ("id", "template", "width_photostrip", "height_photostrip")
    search_fields = ("template__name",)


@admin.register(Dropzone)
class DropzoneAdmin(admin.ModelAdmin):
    list_display = ("id", "template", "top", "left", "width", "height")
    search_fields = ("template__name",)
