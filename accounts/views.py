from django.shortcuts import render, redirect
from django.http import HttpResponse
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor

# Create your views here.

# restict the vendor from accessing the registerUser page

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

#restict the customer from accessing the registerVendor page
def check_role_customer(user):      
    if user.role == 2: 
        return True
    else:
        raise PermissionDenied


## registerUser
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request , 'Ya has iniciado sesión')
        return redirect('dashboard')
    
    elif request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST) 
        if form.is_valid():
            #creando el usuariuo utilizando el metodo save
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password) 
            # user.rol = User.CUSTOMER
            # user.save() # Save the user to the database

            #creando el usuario utilizando el metodo create_user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()

            # send verification email
            email_subject = 'Verifica tu cuenta de cliente'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, email_subject, email_template)


            messages.success( request, 'El usuario se ha creado con éxito')
            print('El usuario se ha creado con éxito')
            return redirect('registerUser')
        else:
            print('Formulario invalido!, ')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html',context) # Add this line 
## registerVendor
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request , 'Ya has iniciado sesión')
        return redirect('vendDashboard')
    
    elif request.method == 'POST':
        #store the form data in a variable
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # send verification email
            email_subject = 'Verifica tu cuenta de restaurante'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, email_subject, email_template)
            
            messages.success( request, 'El usuario se ha creado con éxito, aun falta la validación del restaurante')
        else:
            print('Formulario invalido!, ')
            print(form.errors)
            print(v_form.errors)

    else:
        form =  UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context) # Add this line
## activate

def activate(request, uidb64, token):
    # activar la cuenta del usuario
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '¡Cuenta activada con éxito!')
        return redirect('myAccount')
    else:
        messages.error(request, 'El enlace de activación es inválido')
        return redirect('myAccount')
## login

def login(request):
    if request.user.is_authenticated:
        messages.warning(request , 'Ya has iniciado sesión')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)


        if user is not None:
            auth.login(request, user)
            messages.success(request, '¡Has iniciado sesión con éxito!')
            return redirect('myAccount')
        else:
            messages.error(request, '¡Credenciales incorrectas, inténtalo de nuevo!')
            return redirect('login')
    return render(request, 'accounts/login.html') # Add this line


def logout(request):
    auth.logout(request)
    messages.info(request, '¡Has cerrado sesión con éxito!')
    return redirect('login') # Add this line


## myAccount
@login_required(login_url='login')

def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html') # Add this line

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendDashboard(request):
    return render(request, 'accounts/vendDashboard.html') # Add this line


# Forgot password

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            mail_subject = 'Restablecer tu contraseña'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)


            messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña')
            return redirect('login')
        else:
            messages.error(request, '¡No existe una cuenta con este correo electrónico!')
            return redirect('forgot_password')
         
    return render(request, 'accounts/forgot_password.html') # Add this line


# Reset password Validate
def reset_password_validate(request, uidb64, token):
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Por favor, restablece tu contraseña')
        return redirect('reset_password')
    
    else:
        messages.error(request, 'Este enlace ha caducado')
        return redirect('myAccount')

## reset_password
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, '¡Contraseña restablecida con éxito!')
            return redirect('login')
        else:
            messages.error(request, '¡Las contraseñas no coinciden!')
            return redirect('reset_password')


    return render(request, 'accounts/reset_password.html') # Add this line
