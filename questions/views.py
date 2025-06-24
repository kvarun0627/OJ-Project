from django.shortcuts import render,redirect,get_object_or_404
from .models import Question
from .forms import Questionform

def question_lists(request):
    questions=Question.objects.filter()
    return render(request,'questions/question_list.html',{'questions':questions})

def create_question(request):
    if request.method=='POST':
        form=Questionform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form=Questionform()

    return render(request,'questions/question_form.html',{'form':form})

def question_detail(request,pk):
    question=get_object_or_404(Question,pk=pk)
    return render(request,'questions/question_detail.html',{'question':question})

def update_question(request,pk):
    question=get_object_or_404(Question,pk=pk)
    form=Questionform(request.POST or None ,instance=question)
    if form.is_valid():
        form.save()
        return redirect('question_list')
    return render(request,'questions/question_form.html',{'form':form})

def delete_question(request,pk):
    question=get_object_or_404(Question,pk=pk)
    if request.method=='POST':
        question.delete()
        return redirect('question_list')
    return render(request,'questions/question_confirm_delete.html',{'question':question})
