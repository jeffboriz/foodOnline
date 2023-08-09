from django.shortcuts import render,HttpResponse,redirect
from.forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm


# Create your views here.

def registerUser(request):
    if request.method =='POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)
            #user.role = User.CUSTOMER
            #user.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request,'You account has been registered successfully!')
            print("user is created")
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
       form=UserForm()
    context ={
           'form': form,
    }
    return render(request,'accounts/registerUser.html',context)





def registerVendor(request):
    if request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            Vendor =v_form.save(commit=False)
            Vendor.user = user
            user_profile=UserProfile.objects.get(user=user)
            Vendor.user_profile = user_profile
            Vendor.save()
            messages.success(request,'You account has been registered successfully! please wait for the approval')
            return redirect('registerVendor')
        else:
            print("invalid error")
            print(form.errors)
    else:
        form = UserForm()
        v_form=VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html',context)



