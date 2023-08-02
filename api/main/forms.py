
from django import forms

class CSVForm(forms.Form):
    upload_limit = 2 * 1024 * 1024
    upload_limit_text = naturalsize(upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    csv = forms.FileField(required=True, label="File to Upload <= "+upload_limit_text)
    upload_field_name = "csv"

    # Data currently exists as request.FILES["csv"]

    # Validate the size of the file
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("csv")
        if file is None:
            return
        if len(file) > self.upload_limit:
            self.add_error("csv", "File must be < "+self.upload_limit_text+" bytes")