from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
# class Tag(models.Model):
# 	id 			= models.AutoField(primary_key=True)
# 	tag_name  	= models.CharField(max_length=255)
# 	keterangan	= models.CharField(max_length=255)

# 	def __str__(self):
# 		return "{},{}".format(self.id, self.tag_name)

class State(models.Model):
	id 				= models.AutoField(primary_key=True)
	state_name  	= models.CharField(max_length=255)
	keterangan  	= models.CharField(max_length=255)
	code_name  		= models.CharField(max_length=255)

	def __str__(self):
		return "{},{}".format(self.id, self.state_name)

class Mahasiswa(models.Model):
	id = models.AutoField(primary_key=True)
	user 		= models.OneToOneField(User, on_delete=models.CASCADE)
	nim 		= models.CharField(max_length=12, null=True, blank=True)
	# nama 		= models.CharField(max_length=50)
	JURUSAN = [
		('Informatika', 'Informatika'),
    ('Ilmu Komunikasi', 'Ilmu Komunikasi'),
    ('Tekanik', 'Tekanik'),
    ('Psikologi', 'Psikologi'),
	]
	jurusan 	= models.CharField(max_length=100, choices=JURUSAN, null=True, blank=True)
	no_hp		= models.CharField(max_length=12, null=True, blank=True)
	foto 		= models.ImageField(default='profile.jpg', upload_to='upload/foto/', null=True, blank=True)

	def __str__(self):
		return "{}, {}".format(self.id, self.nim)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Mahasiswa.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.mahasiswa.save()

class TiketModel(models.Model):
	id 			= models.AutoField(primary_key=True)
	mahasiswa  	= models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	tiket 		= models.CharField(max_length=10)
	judul 		= models.CharField(max_length=100)
	aduan  		= models.TextField()
	KATEGORI_LIST = [
		('visa', 'Visa'),
		('dokumen', 'dokumen'),
		('nilai', 'nilai'),
	]
	kategori  	= models.CharField(max_length=15, choices=KATEGORI_LIST)
	date  		= models.DateTimeField(auto_now_add=True)
	updated  	= models.DateTimeField(auto_now=True)
	file 		= models.FileField(null=True, upload_to='upload/', blank=True)
	# STATUS = [
	# 	('pending', 'pending'),
	# 	('open', 'open'),
	# 	('process', 'process'),
	# 	('finish', 'finish'),
	# 	('closed', 'closed'),
	# ]
	# status 		= models.CharField(max_length=10, null=True, choices=STATUS, default="pending")
	slug  	 	= models.SlugField(blank=True, editable=False)

	class Meta:
		permissions = (
			('manage_tiket', 'Can Manage Tiket'),
			('close_tiket', 'Can Closed Tiket'),
		)

	def save(self):
		# self.tiket = get_random_string(10, 'abcdef0123456789')
		self.slug = slugify(self.tiket)
		super().save()

	def get_absolute_url(self):
		url_slug = {'slug':self.slug}
		return reverse('tiket:detail', kwargs=url_slug)

	def __str__(self):
		return "{},{}".format(self.id, self.tiket)

class MoveState(models.Model):
	id 				= models.AutoField(primary_key=True)
	tiket_move		= models.ForeignKey(TiketModel, null=True, on_delete=models.CASCADE)
	user_move		= models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
	state_move		= models.ForeignKey(State, null=True, on_delete=models.CASCADE)
	# tag_move		= models.ForeignKey(Tag, null=True, on_delete=models.CASCADE)
	comment 		= models.TextField(null=True)
	date_move		= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)
	# slug  	 		= models.SlugField(blank=True, editable=False)

	# def save(self):
	# 	# self.tiket = get_random_string(10, 'abcdef0123456789')
	# 	self.slug = slugify(self.id)
	# 	super().save()

	def get_absolute_url(self):
		url_slug = {'id':self.id}
		return reverse('tiket:detailmove', kwargs=url_slug,)

	def __str__(self):
		return "{},{}".format(self.id, self.tiket_move)