from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.db import models
import os


def artwork_file(instance, filename):
    artwork_filename = os.path.basename(instance.artwork.name)
    file_extension = os.path.splitext(artwork_filename)[1]

    return mark_safe('music/artwork/' + instance.name + '_' + instance.author + file_extension)

def music_file(instance, filename):
    music_filename = os.path.basename(instance.file.name)
    file_extension = os.path.splitext(music_filename)[1]

    return mark_safe('music/file/' + instance.name + '_' + instance.author + file_extension)

@receiver(pre_save)
def processFields(sender, instance, *args, **kwargs):
    if isinstance(instance, Music):
        instance.author = instance.author.lower()
        instance.genre = instance.genre.lower()

@receiver(post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if isinstance(instance, Music):
        if instance.artwork:
            if os.path.isfile(instance.artwork.path):
                os.remove(instance.artwork.path)

        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)

class Music(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(default='Song', max_length=250, help_text='song name')

    author = models.CharField(default='Author', max_length=100, help_text='song author')

    genre = models.CharField(
        default='breakcore', max_length=50, help_text='genre of music'
    )

    hide = models.BooleanField(default=False, help_text='hide song from listing')

    file = models.FileField(upload_to=music_file, default='unknown.mp3')

    artwork = models.FileField(upload_to=artwork_file, default='unknown.png')
    artwork_censor = models.BooleanField(default=False, help_text='make artwork blur')
    
    explicit = models.BooleanField(default=False, help_text='mark if the song has uncensored content')

    type = models.CharField(max_length=50, default='-', help_text='Song type, write like "reverb, remix, slowed"\nLeave empty for nothing')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    def ext(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def artwork_preview(self):
        return mark_safe(f"<img src='{self.artwork.url}' width='30px' height='30px' />")

    artwork_preview.short_description = 'Artwork'

class Author(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(default='author', max_length=60, help_text='author name')

    pfp = models.FileField(
        upload_to='music/author/',
        default='music/author/unknown.png',
        help_text='author profile picture',
    )

    description = models.TextField(help_text='description of author')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/author/{self.name}'


class Update(models.Model):
    id = models.AutoField(primary_key=True)

    version = models.CharField(default='Update!', max_length=120)

    text = models.TextField(help_text='text of update')
    
    hide = models.BooleanField(default=False, help_text='hide update from /updates')

    def __str__(self):
        return self.version
    
    def get_absolute_url(self):
        return f'/updates/{self.version}'