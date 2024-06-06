# Generated by Django 4.2.3 on 2024-05-29 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_remove_mijoz_maxsulot_remove_tavar_nom_delete_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('avtive', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['created_time'],
            },
        ),
        migrations.CreateModel(
            name='Tavar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iSHCH_mamlakat', models.CharField(max_length=100)),
                ('iSHCH_sana', models.DateField()),
                ('yaroqlilik_muddati', models.CharField(max_length=10, null=True)),
                ('soni', models.IntegerField()),
                ('narxi', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rasm', models.ImageField(blank=True, null=True, upload_to='tavar_rasmlari/')),
            ],
        ),
        migrations.CreateModel(
            name='Tavar_nomi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tavar_rasmiylashtirish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdor', models.PositiveIntegerField(default=1)),
                ('jami_summa', models.IntegerField()),
                ('kod', models.CharField(editable=False, max_length=36, unique=True)),
                ('comments', models.ManyToManyField(related_name='tavar_rasmiylashtirish_comments', to='blog.comment')),
                ('mahsulot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tavar')),
                ('mijoz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tavar',
            name='nom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.tavar_nomi'),
        ),
        migrations.CreateModel(
            name='MijozTavar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mijoz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mijoz_tavari', to=settings.AUTH_USER_MODEL)),
                ('tavar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tavar')),
            ],
        ),
        migrations.CreateModel(
            name='Mijoz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mijoz', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kassa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod', models.CharField(max_length=36, unique=True)),
                ('yuk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tavar_rasmiylashtirish')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.tavar'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]