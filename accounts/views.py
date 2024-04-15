from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout 
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from car_rental import settings
from .models import Profile, ProfileImage
from accounts.models import *
from cars.models import *
from accounts.emails import send_password_reset_email
from django.contrib.auth.decorators import login_required
import razorpay

# registration logic
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    return render(request ,'accounts/register.html')


# login logic
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.path_info)
        user = user_obj[0]
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        if user.profile.is_email_verified:
            # User is already verified, proceed with login
            user_obj = authenticate(username=email, password=password)
            if user_obj:
                login(request, user_obj)
                return HttpResponseRedirect('/')
            messages.warning(request, "Invalid Credentials")
            return HttpResponseRedirect(request.path_info)
        else:
            # User email is not verified, initiate activation
            email_token = str(uuid.uuid4())
            profile = Profile.objects.create(user=user, email_token=email_token)
            send_account_activation_email(email, email_token)
            messages.warning(request, 'Please verify your email before logging in. Activation email sent.')
            return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')
   
# email activation logic
def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email Is Verified, Please Login')
        return redirect('/')
    except Profile.DoesNotExist:
        print(f'Invalid Email Token: {email_token}')
        return HttpResponse('Invalid Email Token')

# logout logic
@login_required
def logging_out(request):
    logout(request)
    return redirect('/')

# password reset
def reset_password(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.get(forget_password_token = token)
        context = {'user_id':profile_obj.user.id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.warning(request, 'No user id found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if new_password != confirm_password:
                messages.warning(request, 'Confirm Password Does not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')
    except Exception as e:
        print(e)
    return render(request, 'accounts/reset_password.html',context)

# forgot password and send mail logic
def forgot_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email=email).first():
                messages.error(request, 'User Not Found')
                return redirect('/forgot-password')
            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_password_reset_email(user_obj,token)
            messages.warning(request, 'Reset Password Link has been sent to your email')
            return redirect('forgot-password')
    except Exception as e:
        print(e)
    return render(request, 'accounts/forgot_password.html')

@login_required
def user_profile(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.filter(user=request.user).first()
        
        # Retrieve first name and last name from the user object
        first_name = request.user.first_name
        last_name = request.user.last_name
        
        # Handle image upload
        if request.method == 'POST' and 'profile-image' in request.FILES:
            image_file = request.FILES['profile-image']
            
            # Delete previous profile image
            ProfileImage.objects.filter(profile=user_profile).delete()
            
            # Save new profile image
            profile_image = ProfileImage(profile=user_profile)
            profile_image.image.save(image_file.name, image_file)
            profile_image.save()
        
        profile_images = ProfileImage.objects.filter(profile=user_profile)
        
        context = {
            'user_profile': user_profile,
            'profile_images': profile_images,
            'first_name': first_name,
            'last_name': last_name,
        }
        return render(request, 'accounts/user_profile.html', context)
    else:
        return redirect('login')


@login_required
def payment_page(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    discount = 0
    final_price = car.price
    applied_coupon = None 
    
    try:
        cart_obj = Cart.objects.get(is_paid=False, user=request.user)
    except Cart.DoesNotExist:
        cart_obj = Cart.objects.create(user=request.user)
    coupon = None
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if coupon.is_expired:
                messages.error(request, 'Coupon is expired.')
            elif hasattr(request.user, 'profile') and car.price >= coupon.minimum_amount:
                discount = coupon.discount_price
                final_price -= discount
                applied_coupon = coupon.coupon_code  
                messages.success(request, f'Coupon applied successfully. Discount: ₹{discount}')
            else:
                messages.error(request, f'Coupon applicable on minimum purchase of ₹{coupon.minimum_amount}.')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
            
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create({'amount': final_price * 100, 'currency': 'INR', 'payment_capture': 1})
    cart_obj.razor_pay_order_id = payment['id']
    if coupon: 
        cart_obj.coupon = coupon  
    cart_obj.save()

    print(payment)

    context = {
        'cart': cart_obj,
        'car': car,
        'discount': discount,
        'final_price': final_price,
        'applied_coupon': applied_coupon,  # Add applied_coupon to context
        'payment': payment,
    }
    return render(request, 'accounts/payment.html', context)

def remove_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    return JsonResponse({'success': True})

def success(request):
    order_id = request.GET.get('razorpay_order_id')
    try:
        cart = Cart.objects.get(razor_pay_order_id=order_id)
        cart.is_paid = True
        cart.save()
        return render(request, 'accounts/success.html')
    except ObjectDoesNotExist:
        return HttpResponse('Cart with the specified razor_pay_order_id does not exist.', status=404)
    

def test(request):
    try:
        # context = {'cars':Car.objects.all()}
        return render(request, 'accounts/test.html')
    except Exception as e:
        print(e)