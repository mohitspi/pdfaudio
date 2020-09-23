from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import *
import os
from audio import settings

from gtts import gTTS
from googletrans import Translator, constants
from pprint import pprint
from .models import *
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from django.forms import ModelForm
from django.http import HttpResponse
from io import BytesIO
from gtts import gTTS
from googletrans import Translator, constants
from pprint import pprint
from gtts import gTTS
from pdf2docx import parse
from googletrans import Translator, constants
from pprint import pprint
import docxpy
from django.views.generic import ListView
import json
from django.views.decorators.csrf import csrf_exempt
# from paytm import Checksum
# Create your views here.
from django.http import HttpResponse

from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect

MERCHANT_KEY = '7CTfiIgd1jT9Rjfd'

import PyPDF2









# login view


class LoginView(View):
    def get(self,request):
        try:
            if request.user.is_authenticated:
                return redirect('/')
            return render(request, 'account/login.html', locals())
        except Exception as e:
            print(e)
            messages.error(request,'Something went wrong,Please try again later or contact us')
            return render(request, 'account/login.html', locals())

    def post(self, request):
        try:
            if request.user.is_authenticated:
                return redirect('/')

            email = self.request.POST.get('email').strip()
            password = self.request.POST.get('password')
            check_email = User.objects.filter(username = email).count()
            if check_email > 0:
                user_obj = User.objects.get(username = email)
                # check_activeness = UserProfileInfo.objects.get(user = user_obj)
                if user_obj.is_active == 1:
                    username = User.objects.get(username = email)
                    user = authenticate(username = email, password = password)
                    if user is not None:
                        login(request, user)
                        return redirect('/demo/')
                    else :
                        messages.error(request,'Incorrect password, please try again')
                        return render(request, 'account/login.html',locals())
                else:
                    messages.error(request,'Sorry, Your account is temporarily disabled,Please contact our support team')
                    return render(request, 'account/login.html',locals())
            else:
                messages.error(request,'No user account registered with provided information. Please check your details and try again')
                return render(request, 'account/login.html',locals())
        except Exception as e:
            print("\n" * 3)
            print(e)
            print("\n" * 3)
            messages.error(request,'Something Went Wrong,Please try again later')
            return render(request, 'account/login.html',locals())

class LogoutView(View):

    '''demonstarte docstring for confirm that this function is used for logout an user'''

    def get(self,request):
        try:
            logout(request)
            messages.success(request,'Your Account has been Logged Out')

            return render(request, 'account/login.html',locals())
        except:
            pass







def model_form_upload(request):
    try:
        if request.method == 'POST':
            document = request.FILES.get('document')
            language = request.POST.get('language')


            user = request.user.id
            if document and language:
                current_obj = Document.objects.create(document = document,language = language, user = User.objects.get(id = int(user)))
                pdfFileObj = open('media/{}'.format(current_obj.document.name), 'rb')





                translator = Translator()
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                mytext = ""

                for pageNum in range(pdfReader.numPages):
                    page_obj = pdfReader.getPage(pageNum)
                    mytext += page_obj.extractText()
                    print("ffff",mytext)

                pdfFileObj.close()
                print("ddd",mytext)


                # pageObj = pdfReader.getPage(0)
                # String_text = pageObj.extractText()
                name = str(current_obj.document.name)[:-4]+".txt"
                with open(name, "w", encoding="utf-8") as f:
                    f.write(mytext)
                data_file = open(name , 'r', encoding="utf-8")
                data = data_file.read().encode().decode('utf-8')
                translation = translator.translate(data, dest=current_obj.language, encoding="utf-8")



                print("\n" * 3)

                print("hereeeeeeeeeeeeeeeeeeee")

                print("\n" * 3)






                print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
                my = {translation.text}
                audio = gTTS(text=str(my), lang="hi")
                mp3_fp = BytesIO()
                audio.write_to_fp(mp3_fp)

                current_obj.audio.save(str(current_obj.document)[:-4]+".mp3", mp3_fp)


                # pdf_Reader = PyPDF2.PdfFileReader(pdf_file,strict=False)
                # mytext = ""

                # for pageNum in range(pdf_Reader.numPages):
                #     page_obj = pdf_Reader.getPage(pageNum)
                #     mytext += page_obj.extractText()
                # pdf_file.close()


                # audio = gTTS(text=mytext, lang=current_obj.language)

                # mp3_fp = BytesIO()
                # audio.write_to_fp(mp3_fp)
                # current_obj.audio.save(str(current_obj.document)[:-4]+".mp3", mp3_fp)

        user = request.user.id
        document = Document.objects.filter(user = User.objects.get(id = int(user))).order_by('-id')
        new_doc  = []
        for one in document:
            if one.audio:
                new_doc.append(one)
                break
        if new_doc:
            document = new_doc[0]
        return render(request, 'demo.html', locals())
    except Exception as e:
        error_message = 'Something Went wrong with Your Pdf Please check it'
        print(e)
        messages.error(request,'Something Went Wrong,Please try again later')
        return render(request, 'demo.html', locals())




































def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def audio(request):
    audio = Document.objects.all()
    context = {'audio': audio}
    return render(request, 'audio.html', context)

def convert(request, pk):
        document = get_object_or_404(Document, pk=pk)
        print(document.document)
        translator = Translator()
        parse(f"D:\\audio\\audio\\static\\"+str(document.document), f"D:\\audio\\audio\\static\\"+str(document.document)[:-4]+".docx", start=0)
        print("PDF --> DOCX")
        # extract text
        text = docxpy.process(f"D:\\audio\\audio\\static\\"+str(document.document)[:-4]+".docx")
        print("DOCX --> TXT")
        print(text)
        print("Translating...")
        translator = Translator()
        translation = translator.translate(text, dest="hi")
        print("English --> Hindi")
        print(translation.text)
        
        context = {'document': document}
        return render(request, 'audio_detail.html', context)





























def akbar(request):
	akbar = Document.objects.all()
	context = {'akbar': akbar}
	return render(request, 'akbar.html', context)

def akbar_detail(request, id):
    akbar = Document.objects.filter(id=id)
    for name in akbar:
        names = name
    module_dir = os.path.dirname(__file__)
    print(akbar[0])
    translator = Translator()
    pdfFileObj = open(f"D:\\audio\\audio\\static\\documents\\"+str(names), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    print(pdfReader.numPages)
    pageObj = pdfReader.getPage(0)
    String_text = pageObj.extractText()
    name = str(names)+".txt"
    with open(name, "w", encoding="utf-8") as f:
        f.write(String_text)
    pdfFileObj.close()
    data_file = open(name , 'r', encoding="utf-8")
    data = data_file.read().encode().decode('utf-8')
    translation = translator.translate(data, dest="hi", encoding="utf-8")
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    my = {translation.text}
    final_file = gTTS(text=str(my), lang="hi")
    final_file.save("12.mp3")
    print('success')
    # closing the pdf file object
    
    context = {'akbar': akbar}
    return render(request, 'akbar_detail.html', context)


# def results(request):
      
#     file_path = os.path.join(module_dir, 'data.txt')   #full path to text.
          
    
#     context = {'rooms': data}
#     return render(request, 'javascript/results.html',context)D:\\audio\\audio\\static\\documents

def demo(request):
    return render(request, 'demo.html')

def pricing(request):
    return render(request, 'pricing.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')

        contact = Contact(name=name, email=email, phone=phone, desc=desc, cr_date=datetime.today())
        
        contact.save()
        messages.success(request, 'Your message has been sent.')
    #     send_mail(
    # 'new contact',
    # name+email+phone+desc,
    # 'nabeelahmddd@gmail.com',
    # ['nabeelahmed0111@gmail.com'],
    # fail_silently=False,
    # )
    return render(request, "contact.html",)


def account(request):
    audio = Document.objects.filter(user=request.user)
    context = {'audio': audio}
    return render(request, 'account.html', context)

def membership(request):
    membership = Membership.objects.all()
    context = {'membership': membership}
    return render(request, 'membership.html', context)
def productView(request, id):

    # Fetch the product using the id
    product = Membership.objects.filter(id=id)
    return render(request, 'membership_detail.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = json.loads(request.body)
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        
        order = Orders(items_json=items_json, name=name, email=email,  amount=amount)
        order.save()
        
        thank = True
        id = '250'
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'vfzmXD86965868321353',
                'ORDER_ID': '250',
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})
