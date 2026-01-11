from django.shortcuts import render, redirect
from .forms import JobApplicationForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .models import JobApplication 
from django.core.mail import send_mail 
from django.conf import settings  
from datetime import date, timedelta  
from .forms import RegisterForm
from django.contrib import messages 


def home(request):
    return render(request, 'applications/home.html')


@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()

            print("DEBUG: job saved, now sending email")   # 👈 DEBUG

            send_mail(
                subject='Job Added Successfully',
                message=f'You added a new job application for {job.company_name} - {job.job_title}.',
                from_email='test@example.com',
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            print("DEBUG: email function executed")        # 👈 DEBUG

            return redirect('job_list')
    else:
        form = JobApplicationForm()

    return render(request, 'applications/add_job.html', {'form': form})


@login_required
def job_list(request):
    jobs = JobApplication.objects.filter(user=request.user)
    return render(request, 'applications/job_list.html', {'jobs': jobs})


@login_required
def edit_job(request, job_id):
    job = JobApplication.objects.get(id=job_id, user=request.user)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm(instance=job)

    # return must be INSIDE the function
    return render(request, 'applications/edit_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = JobApplication.objects.get(id=job_id, user=request.user)
    job.delete()
    return redirect('job_list') 

@login_required
def dashboard(request):
    total = JobApplication.objects.filter(user=request.user).count()
    interviews = JobApplication.objects.filter(user=request.user, status='Interview').count()
    offers = JobApplication.objects.filter(user=request.user, status='Offer').count()
    rejected = JobApplication.objects.filter(user=request.user, status='Rejected').count()

    context = {
        'total': total,
        'interviews': interviews,
        'offers': offers,
        'rejected': rejected,
    }

    return render(request, 'applications/dashboard.html', context)

@login_required
def send_reminders(request):
    seven_days_ago = date.today() - timedelta(days=7)

    jobs = JobApplication.objects.filter(
        user=request.user,
        status='Applied',
        applied_date__lte=seven_days_ago
    )

    for job in jobs:
        send_mail(
            subject='Job Follow-up Reminder',
            message=f'Remember to follow up on your application at {job.company_name} for {job.job_title}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

    return redirect('dashboard') 

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'applications/register.html', {'form': form})