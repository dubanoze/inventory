#
# inventory/projects/forms.py
#

from django import forms
#from django.utils.translation import ugettext_lazy as _

from .models import Project


#
# Project
#
class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(
            attrs={u'size': 100, u'maxlength': 256})

    class Meta:
        model = Project
        exclude = []
