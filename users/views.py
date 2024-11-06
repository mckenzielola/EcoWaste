from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # if submitted form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}, your account has been created!")

            # send user to home page using redirect
            return redirect('ecowaste-home')

    # form is not valid 
    else:
         form = UserCreationForm()
    return render(request, "users/register.html", {'form':form})