from django.urls import path
from ecomm_app import views
from django.conf.urls.static import static 
from ecomm import settings
urlpatterns = [
    path('about',views.about),
    path('contact',views.contact),
    path('edit/<rid>',views.edit),
    path('addition/<x1>/<x2>',views.addition),
    path('hello',views.hello ),
    path('home',views.home),
    path('pdetail/<pid>',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.User_logout),
    path('catfilter/<cv>', views.catfilter),
    path('premove/<sid>',views.premove),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>', views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail)
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)