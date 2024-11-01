from django.shortcuts import render, redirect
from django.urls import reverse

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from orders.services.tasks import order_created


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
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            order_created.delay(order.id)
            request.session["order_id"] = order.id  # сохранить заказ в сеансе
            return redirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
    return render(request, "order/create.html", {"cart": cart, "form": form})
