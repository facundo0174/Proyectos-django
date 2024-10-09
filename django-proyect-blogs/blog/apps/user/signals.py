from apps.user.models import usuario
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.post.models import Post
from django.contrib.contenttypes.models import ContentType
from apps.post.models import Comment
from django.contrib.auth.models import Permission,Group


@receiver(post_save,sender=usuario) #para que cuando se realiza un nuevo usuario se ejecute posteriormente esta funcion

def create_groups_and_permissions(sender,instance,created,**kwargs):
    if created and instance.is_superuser:
        try:
            post_content_type=ContentType.objects.get_for_model(Post)
            #permisos de post
            view_post_permission=Permission.objects.get(codename='view_post', content_type= post_content_type)
            add_post_permission=Permission.objects.get(codename='add_post', content_type= post_content_type)
            change_post_permission=Permission.objects.get(codename='change_post', content_type= post_content_type)
            delete_post_permission=Permission.objects.get(codename='delete_post', content_type= post_content_type)
            #permisos de comentarios
            comment_content_type=ContentType.objects.get_for_model(Comment)
            view_comment_permission=Permission.objects.get(codename='view_comment', content_type=comment_content_type)
            add_comment_permission=Permission.objects.get(codename='add_comment', content_type=comment_content_type)
            change_comment_permission=Permission.objects.get(codename='change_comment', content_type=comment_content_type)
            delete_comment_permission=Permission.objects.get(codename='delete_comment', content_type=comment_content_type)

            #creacion del grupo "registrados/usuarios"
            registered_group, created= Group.objects.get_or_create(name = 'registred')
            registered_group.permissions.add(view_post_permission,
                                            view_comment_permission,
                                            add_comment_permission,
                                            change_comment_permission,
                                            delete_comment_permission)
            #creacion del grupo "Colaboradores"
            registered_group, created= Group.objects.get_or_create(name = 'collaborators')
            registered_group.permissions.add(delete_post_permission,
                                            change_post_permission,
                                            add_post_permission,
                                            view_post_permission,
                                            view_comment_permission,
                                            add_comment_permission,
                                            change_comment_permission,
                                            delete_comment_permission)
            #creacion del grupo administrador
            registered_group, created= Group.objects.get_or_create(name = 'administrator')
            registered_group.permissions.set(Permission.objects.all())



        except ContentType.DoesNotExist:
            print(f'el tipo de contenido aun no esta definido')
        except Permission.DoesNotExist:
            print(f'el Permiso aun no esta definido')
#el proposito de esta funcion es automatizar en cierta forma el trabajo que se podria realizar logeando al apartado /admin de django