from django.contrib import admin
from home.models import Contact
from home.models import Post,BlogComment


# Register your models here.
admin.site.register(Contact)
# admin.site.register(Post)
admin.site.register((BlogComment))


 #tint Editor import
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)





# catageri
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'description', 'url', 'add_date')
    search_fields = ('title',)