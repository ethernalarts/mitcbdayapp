from django import forms
from django.core.exceptions import ValidationError
from staffapp.models import staffDetails


# Email domain validator
def validate_email_domain(value):
    if value.split("@")[-1].lower() != "edostate.gov.ng":
        raise ValidationError("Please provide your official email address")


# Add Staff form
class staffDetailsCreateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    first_appointment = forms.DateField(
        label="Date of First Appointment",
        required=True,
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
            raise forms.ValidationError("Please upload a JPG, PNG or GIF file only")
