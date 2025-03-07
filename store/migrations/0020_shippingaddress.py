# Generated by Django 5.1.5 on 2025-02-06 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(max_length=250)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.createprofile')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order')),
            ],
        ),
    ]
