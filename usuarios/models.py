from django.db import models
from django.contrib.auth.models import User
from .validators import rfc_validador, foto_validador

class Usuario(User):
    rfc = models.CharField('R.F.C.', max_length=13, validators=[rfc_validador])
    foto = models.ImageField('Foto', upload_to='perfil', blank=True, null=True, validators=[foto_validador])

    def __str__(self):
        return self.username
    
