from django.shortcuts import render, redirect
import json
from django.contrib import messages
from .models import Crime_Reports, Fir
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout



# User Login and Authentication

def login(request):
    if request.user.is_authenticated:
        return redirect('/index')
    
    else:
        if request.method == 'POST':
            email = request.POST['user_email']
            password = request.POST['user_pass']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request,"User login Successful!!!")
                
                return redirect('/index')
            
            else:
                messages.error(request, "Username or Password is Wrong!!! Try Again.")
                return redirect('/login')


    return render(request, 'login.html')

def register(request):

    if request.user.is_authenticated:
        return redirect('/index')
    
    else:
        if request.method == 'POST':
            fname = request.POST['user_fname']
            lname = request.POST['user_lname']
            email = request.POST['user_email']
            password = request.POST['user_pass']
            Cpassword = request.POST['user_Cpass']
            

            # Check if email already exists or not
            # Here I am using try except block because of .exists() method is not working, showing Database error
            # The following method throws a database error while it dont get results. It is only while using Mongodb

            try:
                User.objects.get(username =email)
                messages.error(request, "Email Already Exists!!! Try Again.")
                return redirect('/register')
            except:
                if password != Cpassword:
                    messages.error(request, "Password and Confirm Password did not match!!")
                    return redirect('/register')
                else:
                    user = User.objects.create_user(username=email, email=email,password=password)
                    user.first_name = fname
                    user.last_name = lname
                    user.save()
                    messages.success(request, "Account Created Successfully!!!")
                    return redirect('/index')
    
    return render(request, 'register.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "Logout Succsessfully!!!")
    return redirect('/index')








def index(request):
    return render(request, 'index.html')





def reports(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            my_reports = Crime_Reports.objects.all()
            reports_json = json.dumps(list(Crime_Reports.objects.all().values()))

            context = {
                'reports' : my_reports, 
                'reports_json' : reports_json
            }
            return render(request, 'reports.html', context)
    if request.method == "POST":
        title= request.POST.get('title')
        name= request.POST.get('name')
        description= request.POST.get('description')
        location= request.POST.get('location')
        mobile= request.POST.get('mobile')
        victim= request.POST.get('victim')
        crime_date= request.POST.get('crime_date')
        # print(title,name,description,location,mobile,victim,crime_date)
        
        new_report = Crime_Reports(title = title, name = name, description = description, location= location, mobile = mobile, victim = victim, crime_date = crime_date )

        new_report.save()
        return redirect('/reports')


        


    



def fir(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
           firs = Fir.objects.all()
           firs_json = json.dumps(list(Fir.objects.all().values()))
           context = {
                'firs' : firs,
                'firs_json' : firs_json
            }
           
           return render(request, 'fir.html', context)   
    if request.method == "POST":
        name = request.POST['name']
        title = request.POST['title']
        location = request.POST['location']
        mobile = request.POST['mobile']
        image = request.FILES["image"]
        
        newFir = Fir(name=name,title=title,location=location,mobile=mobile,image=image)
        newFir.save()

        return redirect('/fir')





def status(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            my_reports = Crime_Reports.objects.all()
            context = {
                'reports' : my_reports, 
            }
            return render(request, 'status.html', context)    

    if request.method == "POST":
        title= request.POST.get('title')
        name= request.POST.get('name')
        description= request.POST.get('description')
        location= request.POST.get('location')
        mobile= request.POST.get('mobile')
        victim= request.POST.get('victim')
        crime_date= request.POST.get('crime_date')
        report_date= request.POST.get('report_date')



        report_id = request.POST.get("id")
        withdraw = request.POST.get("withdraw", default="withdraw")
        pending = request.POST.get("pending", default="pending")
        completed = request.POST.get("completed", default="completed")

        # print(report_id, withdraw, pending, completed )


        if not withdraw:
            print("withdraw")
            update_color = Crime_Reports(id = report_id, title = title, name = name, description = description, location= location, mobile = mobile, victim = victim, crime_date = crime_date, report_date = report_date, status = "red" )
            update_color.save()

        elif not pending:
            print("pending")
            update_color = Crime_Reports(id = report_id, title = title, name = name, description = description, location= location, mobile = mobile, victim = victim, crime_date = crime_date, report_date = report_date, status = "blue" )
            update_color.save()

        elif not completed:
            print("completed")
            update_color = Crime_Reports(id = report_id, title = title, name = name, description = description, location= location, mobile = mobile, victim = victim, crime_date = crime_date, report_date = report_date, status = "green" )
            update_color.save()
        
        return redirect('/status')


    
