from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "avatar.%s" % ext
    return filename


def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    org_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    about = models.TextField(null=True)
    pic = models.ImageField(null=True, blank=True,
                            upload_to='avatars/', validators=[file_size])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

