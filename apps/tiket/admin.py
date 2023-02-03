from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from apps.tiket import models

class MahasiswaInline(admin.StackedInline):
	model = models.Mahasiswa
	can_delete = False
	verbose_name_plural='mahasiswa'

class UserAdmin(BaseUserAdmin):
	inlines = (MahasiswaInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class StateMoveAdmin(admin.ModelAdmin):
	readonly_fields =[
		'date_move',
		'updated',
	]
admin.site.register(models.MoveState, StateMoveAdmin)

class MoveStateInline(admin.StackedInline):
	model = models.MoveState
	verbose_name_plural = 'status'

class TiketAdmin(admin.ModelAdmin):
	def get_readonly_fields(self, request, obj):
		current_user = request.user

		if obj != None:
			if current_user.has_perm("tiket.manage_tiket"):
				readonly_fields = [
					'mahasiswa',
					'tiket',
					'judul',
					'aduan',
					'kategori',
					'slug',
					'date',
					'updated',
					'file',
				]
				return readonly_fields

			elif current_user.has_perm("tiket.add_tiket"):
				readonly_fields = [
					# 'status',
					'tiket',
					'mahasiswa',
					'slug',
					'date',
					'updated',
				]
				return readonly_fields

			else:
				readonly_fields = [
					# 'status',
					'tiket',
					'mahasiswa',
					'slug',
					'date',
					'updated',
				]
				return readonly_fields

		else:
			readonly_fields = [
				# '	',
				'tiket',
				'mahasiswa',
				'slug',
				'date',
				'updated',
			]
			return readonly_fields

	inlines = (MoveStateInline,)
admin.site.register(models.TiketModel, TiketAdmin)

# admin.site.register(models.Tag)
admin.site.register(models.State)
admin.site.register(models.Mahasiswa)