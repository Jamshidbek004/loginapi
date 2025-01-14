# Generated by Django 4.2.3 on 2024-04-30 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tavar_nomi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=500)),
            ],
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
                ('nom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.tavar_nomi')),
            ],
        ),
        migrations.CreateModel(
            name='Mijoz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soni', models.IntegerField()),
                ('maxsulot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.tavar_nomi')),
            ],
        ),
    ]
