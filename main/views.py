from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Juan Maxwell Tanaya',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)
