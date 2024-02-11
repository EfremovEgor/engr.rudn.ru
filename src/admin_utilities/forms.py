from django import forms


class UpdateStudyProfilesForm(forms.Form):
    data = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "type": "file",
            }
        ),
    )
