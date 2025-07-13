from django import forms

class CodeForm(forms.Form):#using choice for language
    LANGUAGE_CHOICES = [
        ('cpp', 'C++'),
        ('python', 'Python'),
        ('java', 'Java'),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    code = forms.CharField(widget=forms.Textarea(attrs={'rows': 12, 'cols': 70}))#code writting area