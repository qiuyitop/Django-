import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # 获得交易token
        nonce = request.POST.get('payment_method_nonce', None)
        # 使用交易token和附加信息，创建并提交交易信息
        result = braintree.Transaction.sale(
            {
                'amount': '{:2f}'.format(order.get_total_cost()),
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True,
                }
            }
        )
        if result.is_success:
            # 标记订单状态为已支付
            order.paid = True
            # 保存交易ID
            order.braintree_id = result.transaction.id
            order.save()
            # 创建带有PDF发票的邮件
            subject = 'My Shop - Invoice no. {}'.format(order.id)
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

            # 生成PDF文件
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

            # 附加PDF文件作为邮件附件
            email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')

            # 发送邮件
            email.send()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        # 生成临时token交给页面上的JS程序
        client_token = braintree.ClientToken.generate()
        return render(request,'payment/process.html',{'order': order,'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')
def payment_canceled(request):
    return render(request, 'payment/canceled.html')