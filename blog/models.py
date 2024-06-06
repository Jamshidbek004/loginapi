
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Tavar_nomi(models.Model):
    nom = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.nom}"


    def clean(self):
        super(Tavar_nomi, self).clean()
        if self.pk is not None:  # Eger obyekt o'zgarish qilinayotgan obyekt bo'lsa
            return
        if Tavar_nomi.objects.filter(nom=self.nom).exists():
            raise ValidationError({'nom': 'Bu maxsulot qo\'shilgan})'})

class Tavar(models.Model):
    objects = None
    nom = models.ForeignKey(Tavar_nomi, on_delete=models.SET_NULL, null=True, blank=True)
    iSHCH_mamlakat = models.CharField(max_length=100)
    iSHCH_sana = models.DateField()
    yaroqlilik_muddati = models.CharField(max_length=10, null=True)
    soni = models.IntegerField()
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    rasm = models.ImageField(upload_to='tavar_rasmlari/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom}, {self.soni}, {self.narxi}"

    def clean(self):
        super(Tavar, self).clean()
        if self.pk is not None:  # Eger obyekt o'zgarish qilinayotgan obyekt bo'lsa
            return  # Obyekt tahrirlashga ruxsat bering
        if Tavar.objects.filter(nom=self.nom).exists():
            raise ValidationError({'nom': 'Bu maxsulot qo\'shilgan'})
class Mijoz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mijoz', null=True, blank=True)

    def __str__(self):
        return str(self.user)

class MijozTavar(models.Model):
    mijoz = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mijoz_tavari')
    tavar = models.ForeignKey(Tavar, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.mijoz} - {self.tavar} "

class Comment(models.Model):
    objects = None
    products = models.ForeignKey(Tavar,
                            on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    avtive = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']
    def __str__(self):
        return f"Comment - {self.body} by {self.user}"




class Tavar_rasmiylashtirish(models.Model):
    mijoz = models.ForeignKey(User, on_delete=models.CASCADE)
    mahsulot = models.ForeignKey('Tavar', on_delete=models.CASCADE)
    miqdor = models.PositiveIntegerField(default=1)
    jami_summa = models.IntegerField()
    comments = models.ManyToManyField('Comment', related_name='tavar_rasmiylashtirish_comments')
    kod = models.CharField(max_length=36, unique=True,
                           editable=False)  # 36 xonali unique kod, tahrirlanishi mumkin emas

    def save(self, *args, **kwargs):
        if not self.kod:  # Eger kod yo'qligini tekshirish
            self.kod = self.generate_unique_code()  # Kodni yaratish
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            kod = str(uuid.uuid4())[:8]  # 8 xonalik unikal kod yaratish
            if not Tavar_rasmiylashtirish.objects.filter(kod=kod).exists():  # Kod takrorlanmaganligini tekshirish
                return kod

    def __str__(self):
        return f"{self.mijoz.username}'s {self.mahsulot.nom}"


class Kassa(models.Model):
    kod = models.CharField(max_length=36, unique=True)
    yuk = models.ForeignKey(Tavar_rasmiylashtirish, on_delete=models.CASCADE)

    def __str__(self):
        return f"Kassa {self.kod}"

    @classmethod
    def kiritish(cls, kod):
        try:
            yuk = Tavar_rasmiylashtirish.objects.get(kod=kod)
            kassa, _ = cls.objects.get_or_create(kod=kod, yuk=yuk)
            kassa.save()
            return kassa
        except Tavar_rasmiylashtirish.DoesNotExist:
            raise ValidationError("Berilgan kodga mos keladigan Tavar_rasmiylashtirish topilmadi.")