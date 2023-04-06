from django.shortcuts import get_object_or_404, render, redirect 
from courses.forms import CourseCreateForm, CourseEditForm, UploadForm
from .models import Course, Category, UploadModel, Slider
from django.core.paginator import Paginator
import random
import os
from django.contrib.auth.decorators import login_required ,user_passes_test

@login_required()
def index(request):
    kurslar = Course.objects.filter(isActive=1, isHome=1)
    kategoriler = Category.objects.all()
    sliders = Slider.objects.filter(isActive=True)

    return render(request , 'courses/index.html' , {
        'categories': kategoriler,
        'courses' : kurslar,
        'sliders': sliders
    })

def isAdmin(user):
    return user.is_superuser

@user_passes_test(isAdmin)
def create_course(request):
    if request.method == "POST":
        form = CourseCreateForm(request.POST, request.FILES)

        if form.is_valid():
            # kurs = Course(
            #     title=form.cleaned_data["title"],
            #     description=form.cleaned_data["description"],
            #     imageUrl=form.cleaned_data["imageUrl"],
            #     slug=form.cleaned_data["slug"])
            # kurs.save()
            form.save()
            return redirect("/kurslar")
    else:
        form = CourseCreateForm()
    return render(request, "courses/create-course.html", {"form":form})

def mobiluygulama(request):
    return HttpResponse('mobil uygulama listesi')

@user_passes_test(isAdmin)
@login_required()
def course_list(request):
    kurslar = Course.objects.all()
    return render(request , 'courses/course-list.html' , {
        'courses' : kurslar
    })

def course_edit(request, id):
    course = get_object_or_404(Course, pk=id)

    if request.method == "POST":
        form = CourseEditForm(request.POST, request.FILES, instance=course)
        form.save()
        return redirect("course_list")
    else:
        form = CourseEditForm(instance=course)

    return render(request, "courses/edit-course.html", { "form":form })


def course_delete(request, id):
    course = get_object_or_404(Course, pk=id)

    if request.method == "POST":
        Course.objects.get(pk=1).delete()
        return redirect("course_list")
    
    return render(request, "courses/course-delete.html", { "course":course })

def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            model = UploadModel(image=request.FILES["image"])
            model.save()
            return render(request, "courses/success.html")
    else:
        form = UploadForm()
    return render(request, "courses/upload.html",{"form":form})

def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        kurslar = Course.objects.filter(isActive=True,title__contains=q).order_by("date")
        kategoriler = Category.objects.all()
    else:
        return redirect("/kurslar")

    return render(request , 'courses/search.html' , {
        'categories': kategoriler,
        'courses': kurslar,
    })



def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    context = {
        'course': course
    }
    return render(request, 'courses/details.html', context)


def getCoursesByCategory(request , slug):
    kurslar = Course.objects.filter(category__slug=slug , isActive=True).order_by("date")
    kategoriler = Category.objects.all()

    paginator = Paginator(kurslar, 3)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    print(page_obj.paginator.count)
    print(page_obj.paginator.num_pages)

    return render(request , 'courses/list.html' , {
        'categories': kategoriler,
        'page_obj': page_obj,
        'secilikategori': slug
    })