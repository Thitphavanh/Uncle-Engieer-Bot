# Generated by Django 5.0.6 on 2024-12-22 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('message', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='discord_images/')),
                ('purchasing_cost', models.IntegerField(blank=True, default=0, null=True)),
                ('express', models.CharField(blank=True, max_length=50, null=True)),
                ('express_price', models.IntegerField(default=0)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=50)),
            ],
        ),
    ]
