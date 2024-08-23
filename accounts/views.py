from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm


# Create your views here.
def custom_login(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Redirect to a success page
    else:
        form = CustomLoginForm()
    return render(request, "login.html", {"form": form})
