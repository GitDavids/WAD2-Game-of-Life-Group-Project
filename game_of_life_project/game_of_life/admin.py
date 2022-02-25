from django.contrib import admin
from game_of_life.models import UserProfile # Category, Page,

# class PageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'url')

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('name',)}


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
