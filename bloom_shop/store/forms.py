from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, CustomOrder, Review

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=80, label="Full Name")

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(5, 0, -1)]),
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your experience..."})
        }

class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = ["customer_name", "phone", "email", "product_type", "preferred_color",
                  "preferred_size", "quantity", "design_description", "special_instructions", "reference_image"]
        widgets = {
            "design_description": forms.Textarea(attrs={"rows": 4}),
            "special_instructions": forms.Textarea(attrs={"rows": 3}),
        }
