from datetime import datetime

from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, CheckboxInput
from django.core import validators

from .models import SenderModel, RecipientModel, RecipientNameModel
from .models import LettersArchiveModel


class AddLetterDateField(forms.DateInput):
    input_type = 'date'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'input-box', 'placeholder': 'Username'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'input-box', 'placeholder': 'Password'
    }))


class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control mr-sm-2 right-angle outline media-input',
        'placeholder': 'Пошук серед листів', 'aria-label': 'search'
    }))


class AddLetterForm(forms.Form):
    track_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control right-angle media-input', 'placeholder': 'Номер відстеження'}
    ))
    date_of_storage_starting = forms.DateField(widget=AddLetterDateField(attrs={
        'class': 'form-control right-angle media-input',
    }),
        initial=datetime.today())
    repeat_delivery = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input right-angle media-input'}))
    recipient_address = forms.ModelChoiceField(label='', queryset=RecipientModel.objects.all(),
                                               widget=forms.Select(attrs={
                                                   'class': 'form-control right-angle select2-entry-point-single media-input'
                                               }))
    sender_data = forms.ModelChoiceField(empty_label='Відправник',
                                         queryset=SenderModel.objects.all(),
                                         widget=forms.Select(attrs={
                                             'class': 'form-control right-angle media-input'
                                                      ' select2-entry-point-single'
                                         }))
    is_court = forms.BooleanField(label='Суд',
                                  initial=False,
                                  required=False,
                                  widget=forms.CheckboxInput(attrs={
                                      'class': 'form-check-input right-angle media-input'
                                  }))
    is_court_subpoena = forms.BooleanField(label='Повістка',
                                           initial=False, required=False,
                                           widget=forms.CheckboxInput(attrs={
                                               'class': 'form-check-input right-angle media-input'
                                           }))
    is_police_fine = forms.BooleanField(label='',
                                        initial=False,
                                        required=False,
                                        widget=forms.CheckboxInput(attrs={
                                            'class': 'form-check-input right-angle media-input'
                                        }))
    comments = forms.CharField(label='',
                               required=False,
                               widget=forms.Textarea(attrs={
                                   'class': 'form-control right-angle media-input',
                                   'placeholder': 'Супровідний коментар (у разі потреби)',
                                   'rows': 1
                               }))
    # letter_image = forms.ImageField(label='Фото', required=False,
    #                                 widget=forms.FileInput(attrs={
    #                                     'class': 'form-control-file right-angle media-input'
    #                                 }))
    letter_image = forms.CharField(label='', required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control right-',
                                       'placeholder': 'Адреса фото'
                                   }))


class AddLetterModelForm(forms.ModelForm):
    track_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control right-angle media-input', 'placeholder': 'Номер відстеження'}
    ))
    date_of_storage_starting = forms.DateField(widget=AddLetterDateField(attrs={
        'class': 'form-control right-angle media-input',
    }),
        initial=datetime.today())
    repeat_delivery = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input right-angle media-input'}))
    recipient_address = forms.ModelChoiceField(label='', queryset=RecipientModel.objects.all(),
                                               widget=forms.Select(attrs={
                                                   'class': 'form-control right-angle select2-entry-point-single media-input'
                                               }))
    sender_data = forms.ModelChoiceField(empty_label='Відправник',
                                         queryset=SenderModel.objects.all(),
                                         widget=forms.Select(attrs={
                                             'class': 'form-control right-angle media-input'
                                                      ' select2-entry-point-single'
                                         }))
    is_court = forms.BooleanField(label='Суд',
                                  initial=False,
                                  required=False,
                                  widget=forms.CheckboxInput(attrs={
                                      'class': 'form-check-input right-angle'
                                  }))
    is_court_subpoena = forms.BooleanField(label='Повістка',
                                           initial=False, required=False,
                                           widget=forms.CheckboxInput(attrs={
                                               'class': 'form-check-input right-angle media-input'
                                           }))
    is_police_fine = forms.BooleanField(label='',
                                        initial=False,
                                        required=False,
                                        widget=forms.CheckboxInput(attrs={
                                            'class': 'form-check-input right-angle media-input'
                                        }))
    comments = forms.CharField(label='',
                               required=False,
                               widget=forms.Textarea(attrs={
                                   'class': 'form-control right-angle media-input',
                                   'placeholder': 'Супровідний коментар (у разі потреби)',
                                   'rows': 1
                               }))
    # letter_image = forms.ImageField(label='Фото', required=False,
    #                                 widget=forms.FileInput(attrs={
    #                                     'class': 'form-control-file right-angle media-input'
    #                                 }))
    letter_image = forms.CharField(label='', required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control right-angle media-input',
                                       'placeholder': 'Адреса фото'
                                   }))

    class Meta:
        model = LettersArchiveModel
        fields = [
            'track_number', 'date_of_storage_starting', 'repeat_delivery',
            'recipient_address', 'sender_data', 'is_court', 'is_court_subpoena',
            'is_police_fine', 'comments', 'letter_image'
        ]


class AddRecipientForm(forms.Form):
    street = forms.ChoiceField(label='Вулиця', choices=RecipientModel.STREET,
                               widget=forms.Select(attrs={
                                   'class': 'form-control right-angle media-input media-input'}))
    build = forms.ChoiceField(label='№ будинку (Поле пусте по замовченню)',
                              choices=RecipientModel.BUILD,
                              widget=forms.Select(attrs={
                                  'class': 'form-control right-angle media-input media-input'}))
    build_letter = forms.ChoiceField(label='Літера будинку (Поле пусте по замовченню)',
                                     choices=RecipientModel.BUILD_LETTER,
                                     widget=forms.Select(attrs={
                                         'class': 'form-control right-angle media-input media-input'}))
    flat = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control right-angle media-input', 'placeholder': '№ квартири'
    }))


class AddRecipientModelForm(forms.ModelForm):
    build = forms.ModelChoiceField(label='',
                                   # empty_label='Номер будинку',
                                   queryset=RecipientModel.objects.all(),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control right-angle media-input'}))
    flat = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control right-angle', 'placeholder': '№ квартири'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['build'].empty_label = 'Номер будинку'

    class Meta:
        model = RecipientModel
        fields = [
            'street',
            'build',
            'build_letter',
            'flat',
        ]
        labels = {
            'street': 'Вулиця',
        }
        widgets = {
            'street': forms.Select(attrs={
                'class': 'form-control right-angle media-input'
            }),
            # 'build': forms.Select(attrs={
            #     'class': 'form-control right-angle media-input'
            # }),
            'build_letter': forms.Select(attrs={
                'class': 'form-control right-angle media-input'
            })
        }


class AddRecipientFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(AddRecipientFormSet, self).add_fields(form, index)

        form.nested = RecipientNameFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='parent-%s-%s' % (
                form.prefix,
                RecipientNameFormSet.get_default_prefix())
        )

        form.nested = LettersArchiveFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='parent-%s-%s' % (
                form.prefix,
                LettersArchiveFormSet.get_default_prefix())
        )


RecipientNameFormSet = inlineformset_factory(RecipientModel, RecipientNameModel,
                                             extra=3, fields=['name'])
LettersArchiveFormSet = inlineformset_factory(RecipientModel, LettersArchiveModel,
                                              fields=[
                                                  'track_number'
                                              ], extra=10)
SenderNameFormSet = inlineformset_factory(RecipientModel,
                                          RecipientNameModel,
                                          formset=AddRecipientFormSet,
                                          extra=3,
                                          fields=[
                                              'name'
                                          ])
SenderLetterFormSet = inlineformset_factory(RecipientModel,
                                            LettersArchiveModel,
                                            formset=AddRecipientFormSet,
                                            fields=[
                                                'track_number'
                                            ],
                                            extra=3, )


class AddSenderForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control right-angle media-input', 'placeholder': 'Наіменування відправника'
    }))


class SubscriberNameForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control right-angle media-input', 'placeholder': 'Відправник'
    }))
