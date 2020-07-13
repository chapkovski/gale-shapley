from django import forms
from .models import Player, Pref, Constants
from django.forms import BaseInlineFormSet, ValidationError, inlineformset_factory
from django.core.validators import MaxValueValidator, MinValueValidator


class PrefForm(forms.ModelForm):
    position = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(attrs={'required': True}))

    class Meta:
        model = Pref
        fields = ['position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        maxval = self.instance.owner.prefs.all().count()
        self.fields['position'].validators += [MaxValueValidator(maxval)]
        self.fields['position'].widget.attrs['max'] = maxval


class PrefFormset(BaseInlineFormSet):
    non_field_errors = None

    def clean(self):
        super().clean()
        if any(self.errors):
            self.non_field_errors = 'Please check your answers'
            return
        positions = [form.cleaned_data['position'] for form in self.forms]
        num_others = self.instance.prefs.all().count()
        vals = list(range(1, num_others + 1))

        if sorted(positions) != vals:
            self.non_field_errors = f"You need to rank all participants from 1 to {num_others}"
            raise ValidationError(self.non_field_errors)


PFormset = inlineformset_factory(Player,
                                 Pref,
                                 formset=PrefFormset,
                                 form=PrefForm,
                                 extra=0,
                                 can_delete=False,
                                 fk_name='owner',
                                 fields=['position']
                                 )
