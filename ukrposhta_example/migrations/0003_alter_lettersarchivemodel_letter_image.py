# Generated by Django 4.2.4 on 2023-09-18 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ukrposhta_example', '0002_recipientmodel_recipientnamemodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lettersarchivemodel',
            name='letter_image',
            field=models.CharField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]