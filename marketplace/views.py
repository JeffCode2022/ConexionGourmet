from django.shortcuts import render
from vendor.models import Vendor

from django.db.models import Prefetch
from menu.models import FoodItem, Category
# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
<<<<<<< HEAD
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)
    context = {
        'vendor': vendor
=======
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



    context = {
        'vendor': vendor,
        'categories': categories,

>>>>>>> fe413a6aaa238a57ad8be59d3961e22c6685ebe1
    }
    return render(request, 'marketplace/vendor_detail.html', context)