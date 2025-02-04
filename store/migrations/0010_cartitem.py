# Generated by Django 5.1.5 on 2025-02-04 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart')),
                ('productVariation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.productvariation')),
            ],
            options={
                'unique_together': {('cart', 'productVariation')},
            },
        ),
    ]
