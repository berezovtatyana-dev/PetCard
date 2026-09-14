from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

class Pet(models.Model):
    owner = models.ForeignKey(User, 
                              on_delete=models.CASCADE,
                              related_name='pets',
                              verbose_name='Владелец')
    name = models.CharField(max_length=100,
                            verbose_name='Кличка')
    breed = models.CharField(max_length=100,
                             verbose_name='Порода')
    slug = models.SlugField(max_length=200, unique=True,
                            db_index=True, 
                            verbose_name='ЧПУ-ссылка')
    bio = models.TextField(verbose_name='Особенности  ухода, рацион, противопоказания')
    is_public = models.BooleanField(default=True,
                                    verbose_name='Публичный доступ')
    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'
        ordering = ['name']

    def __str__(self):
        return f'{self.breed} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f'{self.breed}-{self.name}')
            slug = base_slug
            counter = 1
            while Pet.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug  
        super().save(*args, **kwargs)

    def get_absolute_url(self):  
        return reverse('pets:pet_detail', 
                       kwargs={'slug':self.slug})
    
# Create your models here.
