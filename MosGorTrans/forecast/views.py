from django.shortcuts import render, redirect
from .forms import homeForm
from formulas import *

def index(request):
    error = ""
    if request.method == "POST":
        form = homeForm(request.POST)
        if form.is_valid():
            data = load_database()
            data.appartaments.area = data.appartaments.area+int(request.POST["apart"])
            data.living.area = data.living.area+int(request.POST["flats"])
            data.office.area = data.office.area+int(request.POST["office"])
            ndata = count_values(config=data)
            context = {
                "data":ndata,
            }
            save_database(data.dict())
            return redirect('index')
        else:
            error = "Form is an invalid"

    form = homeForm()
    data = load_database()
    ndata = count_values(config=data)
    if ndata[0][0][2] > 10:
        ndata[0][0][2] = 11
    if ndata[0][1][2] > 10:
        ndata[0][1][2] = 11
    if ndata[0][2][2] > 10:
        ndata[0][2][2] = 11
    context = {
        "form":form,
        "error": error,
        "data": ndata,
    }
    return render(request, "forecast/index.html", context)

def delete(request):
    data = load_database()
    clear_all_values(data)
    return redirect("index")