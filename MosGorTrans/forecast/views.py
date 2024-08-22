from django.shortcuts import render, redirect
from .forms import homeForm

def index(request):
    error = ""
    if request.method == "POST":
        form = homeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            error = "Form is an invalid"

    form = homeForm()
    context = {
        "form":form,
        "error": error,
    }
    return render(request, "forecast/index.html", context)