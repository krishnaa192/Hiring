from django.shortcuts import render
from .forms import CandidateSignupForm, CandidateLoginForm, CandidateForm,ApplyForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
# Create your views here.

def welcome(request):
    return render(request,'welcome.html')

def home(request):

 if not request.user.is_authenticated:
        return redirect('welcome')
 else:
    user = request.user
    applied_jobs = Apply.objects.filter(profile=user.profile).values_list('job', flat=True)
    jobs = Job.objects.exclude(id__in=applied_jobs)
   
   #add logic that if user is appplied for a job then it should not be shown in the list of jobs
    profile=Candidate.objects.all()
    usr=Profile.objects.all()
    skill=Skill.objects.all()
     # Handling search logic
    query = request.GET.get('q')
    if query:
         jobs = jobs.filter(
            Q(experience__icontains=query) |
            Q(location__icontains=query) |
            Q(job_type__icontains=query)  # Search by skill name
        ).distinct()
    #handling that after applying to a job it should not be shown in the list  
    # Handling sort logic
    sort_by = request.GET.get('sort')
    if sort_by == 'experience_asc':
        jobs = jobs.order_by('experience')
    elif sort_by == 'experience_desc':
        jobs = jobs.order_by('-experience')
    elif sort_by == 'full_time':
        jobs = jobs.filter(job_type='Full Time')
    elif sort_by == 'part_time':
        jobs = jobs.filter(job_type='Part Time')
    elif sort_by == 'internship':
        jobs = jobs.filter(job_type='Internship')
    elif sort_by == 'salary_asc':
        jobs = jobs.order_by('salary')
    elif sort_by == 'salary_desc':
        jobs = jobs.order_by('-salary')
    elif sort_by == 'posted_on_asc':
        jobs = jobs.order_by('posted_on')
    elif sort_by == 'posted_on_desc':
        jobs = jobs.order_by('-posted_on')
    elif sort_by == 'Bengalore':
        jobs = jobs.filter(location='Bengalore')
    elif sort_by == 'Delhi':
        jobs = jobs.filter(location='Delhi')
    elif sort_by == 'Mumbai':
        jobs = jobs.filter(location='Mumbai')
    context = {'jobs': jobs,'profile':profile,'usr':usr,'skill':skill}
    return render(request,'hire.html',context)

def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('candidate_profile')  # Redirect to the candidate profile page after signup
    else:
        form = CandidateSignupForm()
    return render(request, 'signup.html', {'form': form})

def candidate_login(request):
    if request.method == 'POST':
        form = CandidateLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the candidate profile page after login
    else:
        form = CandidateLoginForm()
    return render(request, 'login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def candidate_profile(request):
    form = CandidateForm()
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'candidate_profile.html', context)

def job_detail(request, pk):
    job = Job.objects.get(id=pk)
    context = {'job': job}
    return render(request, 'job_detail.html', context)

def apply_job(request, pk):
    #getting logged in user
    user = request.user
    job = Job.objects.get(pk=pk)
    #getting logged in user profile of candidate
    candidate=Candidate.objects.get(pk=user.id)

    # candidate=Candidate.objects.get()
    recruiter=Recruiter.objects.get(pk=job.recruiter.comany_id)  
    profile=Profile.objects.get(pk=user.id)
    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            appli = form.save(commit=False)
            appli.job = job
            appli.save()
             # Sending email notification
            subject = 'Job Application'
            message = f'A new application has been submitted for the job "{job.title}" by {profile.name}.'
            from_email = 'krisna.upadhyayyy@gmail.com'  # Set your 'from' email address here
            recipient_list = [profile.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('verifications_job')
            
            #save the profile in databse
    else:
               
        form = ApplyForm(initial={
            'job': job.id,
            'candidate_detail': candidate.id,
            'recruiter_detail': recruiter.comany_id,
            'profile': profile.id,
        })

    context = {'job': job, 'form': form, 'candidate': candidate, 'recruiter': recruiter, 'profile': profile}
    return render(request, 'apply_form.html', context)

def verifications_job(request):
    return render(request,'job_verification.html')

def about(request):
    return render(request,'about.html')
