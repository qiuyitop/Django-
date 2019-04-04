from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """
    当一个订单创建完成后发送邮件通知给用户
    """

    order = Order.objects.get(id=order_id)
    subject = 'Order {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                                               order_id)
    mail_sent = send_mail(subject, message, 'lee0709@vip.sina.com', [order.email])
    print(mail_sent, type(mail_sent))
    return mail_sent