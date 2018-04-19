from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import Users 
import bcrypt

# Create your views here.
def index(request):
    return render(request,'login_app/login.html')

def validation(request):
    errors = Users.objects.basic_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        passW= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        check=Users.objects.all()
        for item in check:
            if item.email_address==request.POST['email']:
                messages.add_message(request, messages.ERROR, "User Already exists.. Please login")
                print item.email_address
                print "User Already Exists"
                return redirect('/')
            
        use=Users.objects.create(first_name=request.POST['fName'],last_name=request.POST["lName"],email_address=request.POST['email'],password= passW)
        if use.id:
            return redirect('/sendtosuccess')
        else:
            messages.add_message(request, messages.ERROR, "Could not add new user.. Try again")

def success(request):
    use=Users.objects.get(id=request.session['user_id'])
    context={
        'fname':use.first_name,
        'lname':use.last_name,
    }
    return render(request,"login_app/success.html",context)   

def login(request):
    val=Users.objects.filter(email_address = request.POST['lemail'] )
    print val
    log=Users.objects.all()
    for item in log:
        if item.email_address==request.POST['lemail'] and bcrypt.checkpw(request.POST['lpassword'].encode(), item.password.encode()):
            request.session['user_id']=item.id
            return redirect('/sendtosuccess') 
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong..check your id & password")
            return redirect('/')
    
    