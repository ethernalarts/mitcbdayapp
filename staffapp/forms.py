from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from staffapp.models import staffDetails


# Email domain validator
def validate_email_domain(value):
    if value.split("@")[-1].lower() != "edostate.gov.ng":
        raise ValidationError("Please provide your official email address")


# Add Staff form
class staffDetailsCreateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"})
    )
    first_appointment = forms.DateField(
        label="Date of First Appointment",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    official_email = forms.EmailField(validators=[validate_email_domain])

    class Meta:
        model = staffDetails
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "phone_number",
            "official_email",
            "cadre",
            "first_appointment",
            "department",
            "grade_level",
            "step",
            "staff_image",
            "date_of_birth",
        ]

    # validate image format
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("staff_image"):
            raise forms.ValidationError("Please upload a JPG, or PNG file only")


# Update Staff form
class staffDetailsUpdateForm(forms.ModelForm):
    staff_image = forms.ImageField(
        label="Change Profile Picture", widget=forms.FileInput, required=False)
    official_email = forms.EmailField(validators=[validate_email_domain])

    # delete_image = forms.BooleanField()

    class Meta:
        model = staffDetails
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "phone_number",
            "official_email",
            "cadre",
            "first_appointment",
            "department",
            "grade_level",
            "step",
            "staff_image",
            "date_of_birth",
        ]

        # validate image format

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("staff_image"):
            raise forms.ValidationError("Please upload a JPG, PNG or GIF file only")
