import os
import uuid
import subprocess
from django.shortcuts import render,redirect,get_object_or_404
from .models import Question
from .forms import Questionform
from compiler.forms import CodeForm
from compiler.models import Submission
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser

def question_lists(request):
    questions=Question.objects.filter()
    return render(request,'questions/question_list.html',{'questions':questions})

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

    return render(request,'questions/question_form.html',{'form':form})

def question_detail(request,pk):
    question=get_object_or_404(Question,pk=pk)
    output = ''
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_input = form.cleaned_data['user_input']
            language = form.cleaned_data['language']

            folder = f"/tmp/{uuid.uuid4()}"
            os.makedirs(folder)

            try:
                if language == 'cpp':
                    source_file = os.path.join(folder, 'main.cpp')
                    exe_file = os.path.join(folder, 'main.out')
                    with open(source_file, 'w') as f:
                        f.write(code)
                    compile = subprocess.run(['g++', source_file, '-o', exe_file],
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if compile.returncode!=0:
                        output = compile.stderr
                    else:
                        run = subprocess.run([exe_file],
                                             input=user_input,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             timeout=2,
                                             text=True)
                        output = run.stdout or run.stderr

                elif language == 'python':
                    source_file = os.path.join(folder, 'main.py')
                    with open(source_file, 'w') as f:
                        f.write(code)
                    run = subprocess.run(['python3', source_file],
                                         input=user_input,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         timeout=2,
                                         text=True)
                    output = run.stdout or run.stderr

                elif language == 'java':
                    source_file = os.path.join(folder, 'Main.java')
                    with open(source_file, 'w') as f:
                        f.write(code)
                    compile = subprocess.run(['javac', source_file],
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if compile.returncode != 0:
                        output = compile.stderr
                    else:
                        run = subprocess.run(['java', '-cp', folder, 'Main'],
                                             input=user_input,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             timeout=2,
                                             text=True)
                        output = run.stdout or run.stderr

                else:
                    output = "Choose The Language"

            except subprocess.TimeoutExpired:
                output = "Time Limit Exceeded"
            except Exception as e:
                output = str(e)

            # Save to database
            Submission.objects.create(
                language=language,
                code=code,
                user_input=user_input,
                output=output
            )

    else:
        form = CodeForm()

    return render(request, 'questions/question_detail.html', {'question': question, 'form': form, 'output': output})

@login_required
@user_passes_test(is_admin)
def update_question(request,pk):
    question=get_object_or_404(Question,pk=pk)
    form=Questionform(request.POST or None ,instance=question)
    if form.is_valid():
        form.save()
        return redirect('question_list')
    return render(request,'questions/question_form.html',{'form':form})

@login_required
@user_passes_test(is_admin)
def delete_question(request,pk):
    question=get_object_or_404(Question,pk=pk)
    if request.method=='POST':
        question.delete()
        return redirect('question_list')
    return render(request,'questions/question_confirm_delete.html',{'question':question})
