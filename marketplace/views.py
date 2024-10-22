from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from .models import Cart
from django.http import JsonResponse
from .context_processors import get_cart_counter, get_cart_amounts


from django.db.models import Prefetch
from menu.models import FoodItem, Category
from django.contrib.auth.decorators import login_required

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

# ADD TO CART

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Verificar si el alimento existe
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                
                # Verificar si el usuario ya ha agregado ese alimento al carrito
                cart_item, created = Cart.objects.get_or_create(user=request.user, fooditem=fooditem)
                
                if not created:
                    # Si el alimento ya está en el carrito, aumentar la cantidad
                    cart_item.quantity += 1
                    cart_item.save()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Increased the cart quantity', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': cart_item.quantity, 
                         'cart_amount': get_cart_amounts(request)
                    })
                else:
                    # Si es un nuevo ítem en el carrito, establecer cantidad en 1
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Added the food to the cart', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': cart_item.quantity, 
                         'cart_amount': get_cart_amounts(request)
                    })
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})