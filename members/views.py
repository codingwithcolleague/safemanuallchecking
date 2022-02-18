from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_text
from .token import generate_token
# Create your views here.


def memberLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        print("usernameeeee" , username)
    return render(request,"members/login.html")




def memberRegi(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        print(username,email,password)
        res = User.objects.create_user(username=username,email=email,password=password)
        res.save()
        htmly = get_template('members/email.html')
        d = { 'username': username }
        subj = "Thanks for Registration"
        html_content = htmly.render(d)
        # send_mail(
        #     subj,
        #     html_content,
        #     '331rahul@gmail.com',
        #     [email]
        # )
        msg = EmailMultiAlternatives(subj, html_content, '331rahul@gmail.com', [email])
        msg.attach_alternative(html_content, "text/html")
        # msg.send()

        current_site = get_current_site(request)
        email_Subject = "Confirm your email @CFG - Django Login !!"
        message2 = render_to_string("members/email_confirmation.html",{
            'name' : "Rahul",
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(res.pk)),
            'token' : generate_token.make_token(res)
        })
        emailsend = EmailMessage(
            email_Subject,
            message2,
            '331rahul@gmail.com',
            [email]
        )
        emailsend.fail_silently = True
        emailsend.send()
        

    return render(request,"members/regi.html")


def activate(request,uid64,token):
    uid = force_text(urlsafe_base64_decode(uid64))
    myuser = User.objects.get(pk=uid)
    if myuser is not None and generate_token.check_token(myuser,token):
        return HttpResponse("Activate")
    return HttpResponse("Hello")