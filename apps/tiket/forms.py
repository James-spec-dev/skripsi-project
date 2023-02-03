from django import forms
from django.contrib.auth.models import User

from .models import TiketModel, Mahasiswa, MoveState, State

class MoveStateForm(forms.ModelForm):
	# tiket_move = forms.ModelChoiceField(queryset=TiketModel.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
	state_move = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
	comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'form-control'}))
	# tiket_move = ModelChoiceField(queryset=TiketModel.objects.all())
	class Meta:
		model = MoveState
		fields = ['state_move', 'comment']

class ConfirmationForm(forms.ModelForm):
	# tiket_move = forms.ModelChoiceField(queryset=TiketModel.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
	# state_move = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
	comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'form-control'}))
	# tiket_move = ModelChoiceField(queryset=TiketModel.objects.all())
	class Meta:
		model = MoveState
		fields = ['comment']

	# tiket_move = forms.ChoiceField(choices=tiket_move, widget=forms.Select(attrs={"class": "form-control"}))

class UpdateUserForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ['username' ,'first_name', 'last_name', 'email']


JURUSAN = [
	('Informatika', 'Informatika'),
	('Ilmu Komunikasi', 'Ilmu Komunikasi'),
	('Tekanik', 'Tekanik'),
	('Psikologi', 'Psikologi'),
]
class MahasiswaForm(forms.ModelForm):
	class Meta:
		model = Mahasiswa
		fields = [
			'nim',
			# 'nama',
			'jurusan',
			'no_hp',
			'foto',
		]
		nim = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
		jurusan = forms.ChoiceField(choices=JURUSAN, widget=forms.Select(attrs={'class':'form-control'}))
		no_hp = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
		foto = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))

KATEGORI_LIST = [
		('visa', 'Visa'),
		('dokumen', 'dokumen'),
		('nilai', 'nilai'),
	]

# STATUS = [
# 		('pending', 'pending'),
# 		('open', 'open'),
# 		('process', 'process'),
# 		('finish', 'finish'),
# 		('closed', 'closed'),
# 	]
class TiketForm(forms.ModelForm):
	# def __init__(self, *args, **kwargs):
	# 	self.request = kwargs.pop('request', None)
	# 	return super().__init__(*args, **kwargs)

	# def save(self, request):
	# 	tiket = super().save(commit=False)
	# 	if tiket.mahasiswa is None:
	# 		tiket.mahasiswa = request.user
	# 	tiket.save()
	# 	return tiket

	class Meta :
		model = TiketModel
		fields = [
			# 'tiket',
			'judul',
			'aduan',
			'kategori',
			'file',
			# 'status',
		]

	judul = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder": "Silakan Masukkan Aduan Anda",
                "class": "form-control"}))
	aduan = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'form-control'}))
	kategori = forms.ChoiceField(choices=KATEGORI_LIST ,widget=forms.Select(attrs={'class':'form-control'}))
	# status = forms.ChoiceField(choices=STATUS ,widget=forms.Select(attrs={'class':'form-control'}))
	file = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control-file'}))