from django.shortcuts import render

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem


def order_create(request):
    """
    Вью создания заказа
    """
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            return render(request, "order/created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "order/created.html", {"cart": cart, "form": form})
