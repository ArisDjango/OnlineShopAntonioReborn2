from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint
import functools

from django.conf import settings
from django.views.generic import DetailView

# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import CONTENT_TYPE_PNG, WeasyTemplateResponse

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # order = form.save() #waktu penambahan coupon
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                'orders/order/create.html',
                {'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                'admin/orders/order/detail.html',
                {'order': order})

# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html',
#                             {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response,
#                                             stylesheets=[weasyprint.CSS(
#                                                 settings.STATIC_ROOT + 'css/pdf.css')])
#     return response
# Create your views here.


#---- pdf -----------------------------
# class MyModelView(DetailView):
#     # vanilla Django DetailView
#     model = MyModel
#     template_name = 'pdf.html'45

# class CustomWeasyTemplateResponse(WeasyTemplateResponse):
#     # customized response class to change the default URL fetcher
#     def get_url_fetcher(self):
#         # disable host and certificate check
#         context = ssl.create_default_context()
#         context.check_hostname = False
#         context.verify_mode = ssl.CERT_NONE
#         return functools.partial(django_url_fetcher, ssl_context=context)

# class MyModelPrintView(WeasyTemplateResponseMixin, MyModelView):
#     # output of MyModelView rendered as PDF with hardcoded CSS
#     pdf_stylesheets = [
#         settings.STATIC_ROOT + 'css/pdf.css',
#     ]
#     # show pdf in-line (default: True, show download dialog)
#     pdf_attachment = False
#     # custom response class to configure url-fetcher
#     response_class = CustomWeasyTemplateResponse

# class MyModelDownloadView(WeasyTemplateResponseMixin, MyModelView):
#     # suggested filename (is required for attachment/download!)
#     pdf_filename = 'foo.pdf'

# class MyModelImageView(WeasyTemplateResponseMixin, MyModelView):
#     # generate a PNG image instead
#     content_type = CONTENT_TYPE_PNG

#     # dynamically generate filename
#     def get_pdf_filename(self):
#         return 'foo-{at}.pdf'.format(
#             at=timezone.now().strftime('%Y%m%d-%H%M'),
#         )