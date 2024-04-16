from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_password_reset_email(email,token):    
    subject = 'Reset Your Password'
    email_from = settings.EMAIL_HOST_USER
    message = f'''<p>Hi,</p>
<p>Click here to reset your password: <a href="http://127.0.0.1:8000/accounts/reset-password/{token}/">Reset Password</a></p>'''
    send_mail(subject, message, email_from, [email], html_message=message)
    return True

def send_payment_confirmation_email(user_email, amount_paid, car_details, order_id):
    subject = 'Payment Successful'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    message = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}

            .receipt-container {{
                max-width: 500px;
                margin: 0 auto;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }}

            .receipt-header {{
                text-align: center;
                margin-bottom: 20px;
            }}

            .receipt-title {{
                font-size: 24px;
                color: #333;
                margin-bottom: 5px;
            }}

            .receipt-text {{
                font-size: 16px;
                color: #555;
                margin-bottom: 10px;
            }}

            .receipt-amount {{
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }}

            .receipt-details {{
                font-size: 18px;
                color: #333;
            }}

            .receipt-id {{
                font-size: 18px;
                color: #555;
            }}

            .receipt-footer {{
                font-size: 14px;
                color: #777;
                text-align: right;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="receipt-container">
            <div class="receipt-header">
                <h1 class="receipt-title">Payment Receipt</h1>
            </div>
            <div class="receipt-body">
                <p class="receipt-text">Dear User,</p>
                <p class="receipt-text">Thank you for renting a vehicle with us!</p>
                <p class="receipt-text">Your payment of <span class="receipt-amount">₹{amount_paid}</span> for the rental of <span class="receipt-details">{car_details}</span> has been successfully processed.</p>
                <p class="receipt-text">Your order ID is: <span class="receipt-id">{order_id}</span>.</p>
                <p class="receipt-text">We hope you enjoy your ride!</p>
            </div>
            <div class="receipt-footer">
                <p class="receipt-text">Best regards,<br>The ROAD ROVER</p>
            </div>
        </div>
    </body>
    </html>
    """

    send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=message)