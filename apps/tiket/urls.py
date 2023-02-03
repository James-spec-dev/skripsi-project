from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from apps.tiket import views

urlpatterns = [
	path('manage/update/<int:pk>', views.TiketUpdateView.as_view(), name='update'),
	path('manage/delete/<int:pk>', views.TiketDeleteView.as_view(), name='delete'),
	path('manage/', views.TiketManageView.as_view(), name='manage'),
	path('tambahmove/<int:pk>', views.MoveStateCreateView.as_view(), name='createmove'),
	path('tambah/', views.TiketCreateView.as_view(), name='create'),
	path('detail/<str:slug>', views.TiketDetailView.as_view(), name='detail'),
	path('detailmove/<int:pk>', views.MoveStateDetailView.as_view(), name='detailmove'),
	path('tiketopen/<int:pk>', views.TiketNotDoneYet.as_view(), name='tiketopen'),
	path('tiketclosed/<int:pk>', views.TiketDone.as_view(), name='tiketclosed'),
	path('makepdf/', views.show_tiket, name='makepdf'),
	path('createpdf/', views.pdf_report, name='createpdf'),
	path('', views.TiketMoveView.as_view(), name='listmove' ),
	# path('', views.TiketListView.as_view(), name='list' ),

	#export file

	# path('listm/', views.TiketListMahasiswa.as_view(), name='listmahasiswa' ),
	# path('delete/<int:delete_id>', TiketDeleteView.as_view(), name='delete'),
	# path('update/<int:update_id>', TiketFormView.as_view(mode='update'), name='update'),
	# path('create/', TiketFormView.as_view(), name='create'),
	# path('', TiketListView.as_view(), name='list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
