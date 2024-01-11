

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_rename_users_author_rename_userses_author_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
    ]
