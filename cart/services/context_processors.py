from cart.cart import Cart


def cart(request):
    """
    Процессор контекста для корзины
    """
    return {'cart': Cart(request)}