# Generated by Django 4.2.10 on 2024-03-13 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione_gruppi', '0003_rename_via_soggiorno_gruppo_indirizzo_soggiorno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gruppo',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
