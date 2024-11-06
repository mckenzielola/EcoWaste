from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms # import from forms.py

# Create your views here.
def register(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)

        # if submitted form is valid
        if form.is_valid():
            # save form to backend
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}, your account has been created!")

            # send user to home page using redirect
            return redirect('ecowaste-home')

    # form is not valid 
    else:
        # return back empty form, with password 
        form = forms.UserRegisterForm()
    return render(request, "users/register.html", {'form':form})