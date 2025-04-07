from django import forms

from django.core.exceptions import ValidationError

class getRxaui(forms.Form):
    requested_id = forms.IntegerField(help_text="Enter a valid RXAUI integer id.")

    def clean_input_id(self):
        data = self.requested_id
        
        # perform some data validation checks

        return data