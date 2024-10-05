from django.contrib import admin
from apps.post.models import Post,PostImage,Comment,Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','category','creation_date','modification_date','allowed_comments')
    search_fields = ('title','author__username','creation_date','content')
    prepopulated_fields = {'slug':('title',)}
    list_filter = ('author','creation_date','allowed_comments')
    ordering = ('-creation_date',)

class CommentAdmin(admin.ModelAdmin):
    list_display=('content','author','post','creation_date')
    search_fields=('content','autor__username','author__id','post__title','id')
    list_filter=('creation_date','author')
    ordering=('-creation_date',)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name',)
    search_fields=('category_name','id')
    list_filter=('creation_date','category_name')
    ordering=('-creation_date',)


def activate_images(modeladmin,request,queryset):
    updated=queryset.update(active=True)
    modeladmin.message_user(request,f'#{updated} imagenes fueron activadas con exito')

activate_images.short_description="activar imagenes seleccionadas"

def deactivate_images(modeladmin,request,queryset):
    updated=queryset.update(active=False)
    modeladmin.message_user(request,f'#{updated} imagenes fueron desactivadas con exito')

deactivate_images.short_description="desactivar imagenes seleccionadas"


class PostImageAdmin(admin.ModelAdmin):
    list_display=('post','image','active')
    search_fields=('post__title','post__id','image','id')
    list_filter=('active',)
    ordering=('-creation_date',)
    actions=[activate_images,deactivate_images]


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(PostImage, PostImageAdmin)



