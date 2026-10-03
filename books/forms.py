from django import forms
from .models import Book,Category

class BookForm(forms.ModelForm):
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Book
        fields = ["title", "author" ,'cover','categories']
        
    
    