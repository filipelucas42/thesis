# Generated by Django 4.0.3 on 2022-05-24 17:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('arctel', '0002_remove_menuitem_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(label='Item'))), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(label='Item'))), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=None),
        ),
    ]
