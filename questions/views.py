from django.shortcuts import render,redirect,get_object_or_404
from .models import Question
from .forms import Questionform
from compiler.forms import CodeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from compiler.models import Submission
from .tasks import evaluate_submission

def is_admin(user):
    return user.is_superuser

def question_lists(request):
    questions=Question.objects.filter()
    return render(request,'frontend/templates/questions/question_list.html',{'questions':questions})

@login_required
@user_passes_test(is_admin)
def create_question(request):
    if request.method=='POST':
        form=Questionform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form=Questionform()

    return render(request,'frontend/templates/questions/question_form.html',{'form':form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            user = request.user  # Ensure user is authenticated
            submission=Submission.objects.create(
                user=user,
                question=question,
                verdict='Pending',
                language=language,
            )
            evaluate_submission.delay(submission.id, code, language)
        else:
            print(form.errors)
    else:
        form = CodeForm()
    return render(request, 'frontend/templates/questions/question_detail.html', {'question': question,'form': form,})

@login_required
@user_passes_test(is_admin)
def update_question(request,pk):
    question=get_object_or_404(Question,pk=pk)
    form=Questionform(request.POST or None ,instance=question)
    if form.is_valid():
        form.save()
        return redirect('question_list')
    return render(request,'frontend/templates/questions/question_form.html',{'form':form})

@login_required
@user_passes_test(is_admin)
def delete_question(request,pk):
    question=get_object_or_404(Question,pk=pk)
    if request.method=='POST':
        question.delete()
        return redirect('question_list')
    return render(request,'frontend/templates/questions/question_confirm_delete.html',{'question':question})
