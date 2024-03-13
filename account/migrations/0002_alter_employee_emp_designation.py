# Generated by Django 5.0.3 on 2024-03-11 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_designation',
            field=models.CharField(choices=[('Product Manager', 'Product Manager'), ('Jr. PHP Laravel Developer', 'Jr. PHP Laravel Developer'), ('Jr. HR Executive', 'Jr. HR Executive'), ('Python Developer', 'Python Developer'), ('Tech Lead', 'Tech Lead'), ('Content Writer', 'Content Writer'), ('Intern', 'Intern'), ('SEO Executive', 'SEO Executive'), ('Sr. Developer', 'Sr. Developer'), ('Project Manager', 'Project Manager'), ('Jr. Web Designer', 'Jr. Web Designer'), ('Web Designer', 'Web Designer'), ('Quality Engineer Lead', 'Quality Engineer Lead'), ('Jr.React Native Developer', 'Jr.React Native Developer'), ('Sr. HR Executive', 'Sr. HR Executive'), ('Sr. SEO Executive', '\tSr. SEO Executive'), ('Admin', 'Admin'), ('UI/UX Designer', 'UI/UX Designer'), ('Lead Generation Executive', 'Lead Generation Executive'), ('COO', 'COO'), ('Trainee', 'Trainee'), ('Quality Engineer', 'Quality Engineer'), ('CEO', 'CEO'), ('Jr. PHP Laravel Developer\t', 'Jr. PHP Laravel Developer')], help_text='Employee Designation', max_length=70),
        ),
    ]
