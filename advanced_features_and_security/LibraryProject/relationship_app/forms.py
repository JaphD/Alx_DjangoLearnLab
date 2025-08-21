from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    author_name = forms.CharField(
        label="Author name",
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter author name"
        })
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "publication_year",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "publication_year": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "placeholder": "YYYY"
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if editing, populate the text field with existing name
        if self.instance and self.instance.pk:
            self.fields['author_name'].initial = self.instance.author.name




