from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_otpverification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OTPVerification',
        ),
    ]
