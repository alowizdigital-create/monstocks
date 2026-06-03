from django.shortcuts import render,redirect
from .forms import CompanyForm

# Create your views here.

def company_create(request):

    form = CompanyForm()

    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()

            return redirect("company_list")

    return render(request, "company/add.html", {
        "form": form
    })

def company_list(request):

    categories = Category.objects.filter(company=request.company)

    return render(request, "products/category_list.html", {
        "categories": categories
    })