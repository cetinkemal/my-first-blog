from django import forms
from django.forms import TextInput, Textarea, SelectMultiple
from courses.models import Course

# class CourseCreateForm(forms.Form):
#     title = forms.CharField(
#         label="kurs başlığı",
#         error_messages= {"required":"kurs başlığı girmelisiniz."},
#         max_length=0, 
#         widget=forms.TextInput(attrs={"class":"form-control"}))

#     description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
#     imageUrl = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
#     slug = forms.SlugField(widget=forms.TextInput(attrs={"class":"form-control"}))

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'image', 'slug')
        labels = {
            'title':'kurs başlığı',
            'description':'açıklama'
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
        }
        error_messages = {
            "title": {
                "required": "kurs başlığı girmelisiniz.",
                "max_length": "maksimum 50 karakter girmelisiniz"
            },
            "description": {
                "required": "kurs açıklaması gereklidir."
            }
        }


class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'image', 'slug','category','isActive')
        labels = {
            'title':'kurs başlığı',
            'description':'açıklama'
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
        }
        error_messages = {
            "title": {
                "required": "kurs başlığı girmelisiniz.",
                "max_length": "maksimum 50 karakter girmelisiniz"
            },
            "description": {
                "required": "kurs açıklaması gereklidir."
            }
        }


class UploadForm(forms.Form):
    image = forms.ImageField()