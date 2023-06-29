from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from buildingmaterials.models import Product
from .models import Cart, CartItem, Order, OrderItem
from userManagement.models import Profile

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Получаем товар, который нужно добавить в корзину
        product = get_object_or_404(Product, id=product_id)

        # Получаем корзину пользователя
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Проверяем, есть ли уже такой товар в корзине
        cart_item = cart.cart_items.filter(product=product).first()

        if cart_item:
            # Если товар уже есть в корзине, увеличиваем его количество на 1
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Если товара нет в корзине, создаем новый элемент корзины
            cart_item = CartItem.objects.create(cart=cart, product=product)

        return redirect('cart')  # Перенаправляем пользователя на страницу корзины
    else:
        return redirect('home')




@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Создание заказа
        order = Order.objects.create(user=request.user, total_price=cart.get_total_price(), address=profile.city + ', ' + profile.street + ', ' + profile.house_number)

        cart_items = cart.cart_items.all()

        for item in cart_items:
            quantity = request.POST.get(f'quantity-{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()

            # Создание элемента заказа
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Очистка корзины
        cart.cart_items.all().delete()

        return redirect('order_success', order_id=order.id)

    else:
        context = {
            'cart': cart
        }
        return render(request, 'cart.html', context)



@login_required
def update_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == 'POST':
        cart_items = cart.cart_items.all()

        for item in cart_items:
            quantity = request.POST.get(f'quantity-{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()

            if f'delete-{item.id}' in request.POST:
                item.delete()
                return redirect('update_cart')

        return redirect('cart')

    else:
        context = {
            'cart': cart
        }
        return render(request, 'cart_edit.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    context = {
        'order': order
    }

    return render(request, 'order_successfully.html', context)