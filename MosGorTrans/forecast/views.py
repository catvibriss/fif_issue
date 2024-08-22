from django.shortcuts import render, redirect
from .forms import homeForm
from formulas import *

def index(request):
    error = ""
    if request.method == "POST":
        form = homeForm(request.POST)
        if form.is_valid():
            data = load_database()
            print(data)
            print(request.POST["apart"])
            print(request.POST["flats"])
            print(request.POST["office"])
            return redirect("index")
        else:
            error = "Form is an invalid"

    form = homeForm()
    context = {
        "form":form,
        "error": error,
    }
    return render(request, "forecast/index.html", context)