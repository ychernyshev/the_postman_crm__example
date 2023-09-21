from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView

from .models import RecipientModel, LettersArchiveModel, SenderModel
from .forms import SearchForm, AddLetterForm, AddLetterModelForm, SenderNameFormSet, \
    AddSenderForm, AddRecipientModelForm, AddRecipientFormSet, AddRecipientForm


def recipient_add(request, recipient_id=None):
    # recipient = get_object_or_404(RecipientModel, id=recipient_id)

    if request.method == 'POST':
        recipient_form = AddRecipientForm(request.POST)
        if recipient_form.is_valid():
            build = recipient_form.cleaned_data['build']
            build_letter = recipient_form.cleaned_data['build_letter']
            flat = recipient_form.cleaned_data['flat']

            if RecipientModel.objects.filter(build=build).exists() and \
                    RecipientModel.objects.filter(build_letter=build_letter).exists() and \
                    RecipientModel.objects.filter(flat=flat).exists():
                messages.warning(request, 'Такого отримувача вже було збережено раніше')
            else:
                RecipientModel.objects.create(**recipient_form.cleaned_data)
    else:
        recipient_form = AddRecipientForm()

    # recipient_formset = SenderNameFormSet(request.POST)
    # if recipient_formset.is_valid():
    #     recipient_formset.save()
    #     messages.info(request, 'Отримувача було збережено')
    #     return HttpResponseRedirect(reverse('ukrposhta_example:letter_add'))
    # else:
    #     recipient_formset = SenderNameFormSet()

    context = {
        'title': 'Додати отримувача',
        # 'recipient_formset': recipient_formset,
        'recipient_form': recipient_form,
    }

    return render(request, 'ukrposhta_example/recipient_add.html', context=context)


def recipient_list(request):
    recipients = RecipientModel.objects.all()
    recipients_paginator = Paginator(recipients, 20)
    recipients_number = request.GET.get('page')
    recipients_numbers = recipients_paginator.get_page(recipients_number)

    context = {
        'title': 'Список отримувачів',
        'recipients_numbers': recipients_numbers,
    }

    return render(request, 'ukrposhta_example/recipient_list.html', context=context)


def sender_add(request):
    last_sender = SenderModel.objects.last()

    if request.method == 'POST':
        form = AddSenderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if SenderModel.objects.filter(name=name).exists():
                messages.warning(request, 'Відправника вже було додано раніше')
            else:
                SenderModel.objects.create(**form.cleaned_data)
                messages.info(request, 'Відправника було збережено')
                return HttpResponseRedirect(reverse('ukrposhta_example:letter_add'))
    else:
        form = AddSenderForm()

    context = {
        'title': 'Додати відправника',
        'last_sender': last_sender,
        'form': form,
    }

    return render(request, 'ukrposhta_example/sender_add.html', context=context)


def sender_list(request):
    sender = SenderModel.objects.all()
    sender_paginator = Paginator(sender, 20)
    sender_number = request.GET.get('page')
    sender_numbers = sender_paginator.get_page(sender_number)

    context = {
        'title': 'Додати відправника',
        'sender_numbers': sender_numbers,
    }

    return render(request, 'ukrposhta_example/sender_list.html', context=context)


def search_results(request):
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            letter = LettersArchiveModel.objects.filter(
                Q(track_number__icontains=query) |
                Q(date_of_storage_starting__icontains=query)
            )

            context = {
                'query': query,
                'letter': letter,
            }

        return render(request, 'ukrposhta_example/search/search_results.html', context=context)


def archive(request):
    letters = LettersArchiveModel.objects.all()
    subscriber = RecipientModel.objects.all()

    context = {
        'title': 'Всі листи у Базі Даних',
        'letters': letters,
        'subscriber': subscriber,
    }

    return render(request, 'ukrposhta_example/archive.html', context=context)


def letter_add(request):
    letters = RecipientModel.objects.all()[:1]

    if request.method == 'POST':
        form = AddLetterForm(request.POST)
        if form.is_valid():
            date_of_storage_starting = form.cleaned_data['date_of_storage_starting']
            track_number = form.cleaned_data['track_number']
            recipient_address = form.cleaned_data['recipient_address']
            repeat_delivery = form.cleaned_data['repeat_delivery']
            is_court = form.cleaned_data['is_court']
            is_court_subpoena = form.cleaned_data['is_court_subpoena']
            is_police_fine = form.cleaned_data['is_police_fine']
            if LettersArchiveModel.objects.filter(track_number=track_number).exists():
                messages.warning(request, 'Лист із таким номером відстеження вже було додано раніше')
            else:
                LettersArchiveModel.objects.create(**form.cleaned_data)
                messages.success(request, f'Лист додано. №{track_number} |'
                                          f' Дата початку збереження: {date_of_storage_starting}.'
                                          f' Отримувач: {recipient_address}/'
                                          f' | Повторне: {repeat_delivery}/'
                                          f' Суд: {is_court}/'
                                          f'Повістка: {is_court_subpoena}, '
                                          f'Штраф: {is_police_fine},'
                                 )
                return HttpResponseRedirect(reverse('ukrposhta_example:letter_add'))
    else:
        form = AddLetterForm()

    context = {
        'title': 'Postman | Новий лист',
        'letters': letters,
        'last_letter': LettersArchiveModel.objects.last(),
        'form': form,
    }

    return render(request, 'ukrposhta_example/letter_add.html', context=context)


def letter_details(request, slug=None):
    letter_number = LettersArchiveModel.objects.get(slug=slug)
    letter_details = LettersArchiveModel.objects.filter(slug=slug)

    context = {
        'title': 'Деталі листа',
        'letter_number': letter_number,
        'letter_details': letter_details,
    }

    return render(request, 'ukrposhta_example/details.html', context=context)


class UpdateLetterInfo(SuccessMessageMixin, UpdateView):
    model = LettersArchiveModel
    template_name = 'ukrposhta_example/update_info.html'
    form_class = AddLetterModelForm
    success_message = 'Дані листа оновлено'
