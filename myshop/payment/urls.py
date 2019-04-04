from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'payment'

urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('done/'), views.payment_done, name='done'),
    path(_('canceled/'), views.payment_canceled, name='canceled'),
    #path(r'^paypal/', include('paypal.standard.ipn.urls'),name='message'),  # 付款完成通知
    #path(r'^payment/(\d+)/$', views.payment,name='process'),
    #path(r'^done/$', views.payment_done,name='done'),
    #path(r'^canceled/$', views.payment_canceled,name='canceled'),
]