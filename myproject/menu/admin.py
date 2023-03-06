from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'parent', 'url')
    list_filter = ('menu', 'parent')

    # prepopulated_fields = {'url': ('name',)}

    def save_model(self, request, obj, form, change):
        if not obj.url:
            # определяем URL, если он не задан
            parent = obj.parent
            if parent:
                obj.url = parent.url.lower() + '/' + obj.name.lower()
            else:
                obj.url = obj.name

        obj.save()
