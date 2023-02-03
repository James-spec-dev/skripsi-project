from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


# Create your views here.
from apps.tiket import forms
from apps.tiket import models

def show_tiket(request):
    tikets = models.TiketModel.objects.all()
    movestates = []
    for tiket in tikets:
        move = models.MoveState.objects.filter(tiket_move=tiket).order_by('-updated')
        if move.exists():
            movestates.append(move.first())
    context = {
        'tikets':movestates
    }

    return render(request, 'tiket/report.html', context)

def pdf_report(request):
    tikets = models.TiketModel.objects.all()

    template_path = 'tiket/report2.html'
    movestates = []
    for tiket in tikets:
        move = models.MoveState.objects.filter(tiket_move=tiket).order_by('-updated')
        if move.exists():
            movestates.append(move.first())
    context = {
        'tikets':movestates
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"' # kalau mau langsung download tambahkan 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class TiketUpdateView(UpdateView):
    form_class = forms.TiketForm
    model = models.TiketModel
    context_object_name = 'tiket'

    def get_template_names(self):
        test_group = Group.objects.get(name='mahasiswa')
        user_group = self.request.user.groups.all()

        if test_group in user_group:
            self.template_name = "tiket/tiket_update.html"
        else:
            self.template_name = "tiket/tiket_update_front.html"
        return super(TiketUpdateView, self).get_template_names()

class TiketDeleteView(DeleteView):
    model = models.TiketModel
    template_name = "tiket/tiket_delete_confirmation.html"
    success_url = reverse_lazy('tiket:manage')
    context_object_name = 'tiket'

class TiketManageView(ListView):
    # permission_required = ("tiket.manage_tiket")
    model = models.MoveState
    template_name = "tiket/tiket_manage.html"
    context_object_name = 'tiket_list'

    def get_context_data(self, **kwargs):
        context = super(TiketManageView, self).get_context_data(**kwargs)
        test_group = Group.objects.get(name='mahasiswa')
        user_group = self.request.user.groups.all()
        if test_group in user_group:
            tikets = models.TiketModel.objects.filter(mahasiswa=self.request.user)
        else : 
            tikets = models.TiketModel.objects.all()

        movestates = []
        for tiket in tikets:
            move = models.MoveState.objects.filter(tiket_move=tiket).order_by('-updated')
            if move.exists():
                movestates.append(move.first())
        context['status'] = movestates
        return context
        
class MoveStateCreateView(View):
    # permission_required = ("tiket.view_tiketmodel", "tiket.add_tiketmodel")
    template_name = "tiket/tiket_form_move_state.html"
    form = forms.MoveStateForm
    mode = None
    # model = models.MoveState
    context = {}

    def get(self, *args, **kwargs):
        self.context = {
            'form':self.form,
        }

        return render(self.request, self.template_name, self.context)

    move = None
    def post(self, *args, **kwargs):

        if kwargs.__contains__('update_id'):
            akun_update = models.MoveState.objects.get(id=kwargs['update_id'])
            self.form = forms.MoveStateForm(self.request.POST, instance=akun_update)
        else:
            self.form = forms.MoveStateForm(self.request.POST)
        tikets_id = models.MoveState.objects.get(id=kwargs['pk'])
        if self.form.is_valid():
            move = self.form.save(commit=False)
            move.tiket_move = tikets_id.tiket_move
            move.user_move = self.request.user
            print(move)
            move.save()

        return redirect('tiket:listmove')

class TiketCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ("tiket.view_tiketmodel", "tiket.add_tiketmodel")
    model = models.TiketModel
    form_class = forms.TiketForm
    template_name = "tiket/tiket_form.html"
    context_object_name = 'tiket'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.mahasiswa = self.request.user
        instance.tiket = get_random_string(10, 'abcdef0123456789')
        instance.save()
        States = models.State.objects.get(code_name=1)
        movestates =  models.MoveState.objects.create(tiket_move=instance, user_move=instance.mahasiswa, state_move=States)
        print(movestates)
        return super(TiketCreateView, self).form_valid(form)

class TiketMoveView(LoginRequiredMixin, ListView):
    model = models.MoveState
    context_object_name = 'tiket_list'
    template_name = None

    def get_context_data(self, **kwargs):
        context = super(TiketMoveView, self).get_context_data(**kwargs)
        test_group = Group.objects.get(name='mahasiswa')
        staf_group = Group.objects.get(name='staf')
        stafadmin_group = Group.objects.get(name='staf administrasi')
        stafnil_group = Group.objects.get(name='staf nilai')
        stafvisa_group = Group.objects.get(name='staf visa')
        user_group = self.request.user.groups.all()
        if test_group in user_group:
            tikets = models.TiketModel.objects.filter(mahasiswa=self.request.user)
            self.template_name = "tiket/tiket_move_mahasiswa.html"
        elif stafadmin_group in user_group:
            tikets = models.TiketModel.objects.filter(kategori='dokumen')
            self.template_name = "tiket/tiket_move.html"
        elif stafvisa_group in user_group:
            tikets = models.TiketModel.objects.filter(kategori='visa')
            self.template_name = "tiket/tiket_move.html"
        elif stafnil_group in user_group:
            tikets = models.TiketModel.objects.filter(kategori='nilai')
            self.template_name = "tiket/tiket_move.html"
        else :
            tikets = models.TiketModel.objects.all()
            self.template_name = "tiket/tiket_move.html"

        movestates = []
        for tiket in tikets:
            if staf_group in user_group:
                move = models.MoveState.objects.filter(tiket_move=tiket).exclude(state_move=1).order_by('-updated')
            else :
                move = models.MoveState.objects.filter(tiket_move=tiket).order_by('-updated')
            if move.exists():
                movestates.append(move.first())
        context['status'] = movestates
        return context

class TiketDetailView(DetailView):
    model = models.TiketModel
    template_name = "tiket/tiket_detail.html"
    context_object_name = 'tiket'

# confirmation finish for mahsasiswa
class MoveStateDetailView(DetailView):
    model = models.MoveState
    template_name = "tiket/tiket_detail_move_state.html"
    context_object_name = 'tiket'

class TiketNotDoneYet(View):
    model = models.MoveState
    form = forms.ConfirmationForm
    template_name = "tiket/tiket_belum_selesai.html"
    context_object_name = 'tiket'
    mode=0

    def get(self, *args, **kwargs):
        self.context = {
            'page_title':'Tambah Akun',
            'form':self.form,
        }

        return render(self.request, self.template_name, self.context)

    move = None

    def post(self, *args, **kwargs):
        self.form = forms.ConfirmationForm(self.request.POST)
        tikets_id = models.MoveState.objects.get(id=kwargs['pk'])
        if self.form.is_valid():
            move = self.form.save(commit=False)
            move.user_move = self.request.user
            move.tiket_move = tikets_id.tiket_move
            States = models.State.objects.get(code_name=2)
            move.state_move = States
            move.save()
            print(move)

        return redirect('tiket:listmove')

class TiketDone(View):
    model = models.MoveState
    form = forms.ConfirmationForm
    template_name = "tiket/tiket_sudah_selesai.html"
    context_object_name = 'tiket'
    mode=0

    def get(self, *args, **kwargs):
        self.context = {
            'page_title':'Tambah Akun',
            'form':self.form,
        }

        return render(self.request, self.template_name, self.context)

    move = None
    def post(self, *args, **kwargs):
        self.form = forms.ConfirmationForm(self.request.POST)
        tikets_id = models.MoveState.objects.get(id=kwargs['pk'])
        if self.form.is_valid():
            move = self.form.save(commit=False)
            move.user_move = self.request.user
            move.tiket_move = tikets_id.tiket_move
            States = models.State.objects.get(code_name=5)
            move.state_move = States
            print(move)
            move.save()

        return redirect('tiket:listmove')