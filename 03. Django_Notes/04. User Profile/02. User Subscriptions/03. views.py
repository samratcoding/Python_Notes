from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CreditPackage



# Purchase credit by user
@login_required(login_url='login/')
def purchase_credits(request):
    if request.method == 'GET':
        credit_packages = CreditPackage.objects.all()
        return render(request, 'user/credit/purchase_credits.html', {'credit_packages': credit_packages})

    elif request.method == 'POST':
        package_id = request.POST.get('package_id')
        credit_package = CreditPackage.objects.get(pk=package_id)
        request.user.purchase_credit(credit_package)

        return redirect('profile')
