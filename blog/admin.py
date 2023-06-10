from django.contrib import admin
from.models import Post ,Category,AddComment
# Register your models here.

class PostAdmin(admin.ModelAdmin):  # instead of ModelAdmin
    list_display=['title','len_commnets']
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(AddComment)
