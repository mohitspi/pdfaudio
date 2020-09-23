from django.urls import path
from myapp import views 
from .views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.akbar)),
    path('login/', LoginView.as_view(), name = 'LoginView'),
    path('logout/', LogoutView.as_view(), name = 'LogoutView'),
    path('delete_audio/', views.Deleteaudio, name = 'Deleteaudio'),


    path('akbar/<int:id>/', views.akbar_detail),
    path('demo/', login_required(views.model_form_upload), name = 'demo'),


    path('pricing/', views.pricing, name = 'pricing'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('account/', views.account),
    path('membership/', views.membership),
    path('membership/<int:id>/', views.productView),
    path('checkout/', views.checkout),
    path('audio/', views.audio, name = 'audio'),
    path('convert/<int:pk>', views.convert),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
] 