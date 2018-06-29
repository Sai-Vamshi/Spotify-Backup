"""from django import forms
from django.contrib.auth.models import User

REGION_CHOICES = [
    ('us-east-2', 'US East (Ohio)'),
        ('us-east-1', 'US East (N. Virginia)'),
        ('us-west-1', 'US West (N. California)'),
        ('us-west-2', 'US West (Oregon)'),
        ('ca-central-1','Canada (Central)'),
        ('ap-south-1','Asia Pacific (Mumbai)'),
        ('ap-northeast-2','Asia Pacific (Seoul)'),
        ('ap-southeast-1','Asia Pacific (Singapore)'),
        ('ap-southeast-2','Asia Pacific (Sydney)'),
        ('ap-northeast-1','Asia Pacific (Tokyo)'),
        ('eu-central-1','EU (Frankfurt)'),
        ('sa-east-1','South America (Sao Paulo)'),
    ]
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    region = forms.CharField(label='Please choose your aws region',
                             widget=forms.Select(choices=REGION_CHOICES))

    class Meta:
        model = User
        fields = ['username', 'email', 'password','region']"""
