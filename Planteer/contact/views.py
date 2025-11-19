from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

def contact_page(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    return render(request, 'contact/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact/success.html')

def contact_messages(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/messages.html', {'messages': messages})
