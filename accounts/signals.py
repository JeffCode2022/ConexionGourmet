from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('¡Perfil creado!')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()  # Si tienes lógica adicional, inclúyela aquí.
            print('¡Perfil actualizado!')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)
            print('El perfil no se había creado antes, así que se creó ahora.')

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'este usuario está siendo guardado')
