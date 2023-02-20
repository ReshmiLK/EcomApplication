from store.models import Carts

def cart_count(request):
    if request.user.is_authenticated:
        cnt=Carts.objects.filter(user=request.user,status="in-cart").count()
    else:
        cnt=0


    return {"count":cnt}






