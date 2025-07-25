from django.shortcuts import render,redirect,get_object_or_404
from .models import Question
from .forms import Questionform
from compiler.forms import CodeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from compiler.models import Submission
from .tasks import evaluate_submission
from django.core.exceptions import PermissionDenied
import os
import subprocess
import uuid
import shutil

# Function to check if the user is an admin
def is_admin(user):
    return user.is_superuser


def question_lists(request):
    questions=Question.objects.filter()
    return render(request,'frontend/templates/questions/question_list.html',{'questions':questions})

@login_required
@user_passes_test(is_admin)
def create_question(request):
    # if not request.user.is_superuser:
    #     raise PermissionDenied
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
            action=request.POST.get('action')  # Get the action from the form submission
            if(action=='run'):
                user_input = form.cleaned_data.get('input')  # Get custom input if provided
                folder = f"/tmp/{uuid.uuid4()}"
                os.makedirs(folder, exist_ok=True)
                output=run_and_output(code, user_input, language,folder)  # Call the function to run the code
                shutil.rmtree(folder)  # Clean up the temporary folder
                return render(request, 'frontend/templates/questions/question_detail.html', {'question': question, 'form': form, 'output': output})
            
            else:
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
    # if not request.user.is_superuser:
    #     raise PermissionDenied
    question=get_object_or_404(Question,pk=pk)
    form=Questionform(request.POST or None ,instance=question)
    if form.is_valid():
        form.save()
        return redirect('question_list')
    else :
        print(form.errors)
    return render(request,'frontend/templates/questions/question_form.html',{'form':form})

@login_required
@user_passes_test(is_admin)
def delete_question(request,pk):
    # if not request.user.is_superuser:
    #     raise PermissionDenied
    question=get_object_or_404(Question,pk=pk)
    if request.method=='POST':
        question.delete()
        return redirect('question_list')
    return render(request,'frontend/templates/questions/question_confirm_delete.html',{'question':question})

def run_and_output(code, input_str, language, folder):
    output = ''
    try:
        os.makedirs(folder, exist_ok=True)

        if language == 'cpp':
            source_file = os.path.join(folder, 'main.cpp')
            exe_file = os.path.join(folder, 'main')

            with open(source_file, 'w') as f:
                f.write(code)
                f.flush()

            compile_process = subprocess.run(
                ['g++', source_file, '-o', exe_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if compile_process.returncode != 0:
                return compile_process.stderr

            run_process = subprocess.run(
                [exe_file],
                input=input_str,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1,
                text=True
            )
            output = run_process.stdout or run_process.stderr

        elif language == 'python':
            source_file = os.path.join(folder, 'main.py')

            with open(source_file, 'w') as f:
                f.write(code)
                f.flush()

            run_process = subprocess.run(
                ['python3', source_file],
                input=input_str,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1,
                text=True
            )
            output = run_process.stdout or run_process.stderr

        elif language == 'java':
            source_file = os.path.join(folder, 'Main.java')

            with open(source_file, 'w') as f:
                f.write(code)
                f.flush()

            compile_process = subprocess.run(
                ['javac', source_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if compile_process.returncode != 0:
                return compile_process.stderr

            run_process = subprocess.run(
                ['java', 'Main'],
                input=input_str,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1,
                text=True,
                cwd=folder
            )
            output = run_process.stdout or run_process.stderr

        else:
            output = "Choose The Language"

    except subprocess.TimeoutExpired:
        output = "Time Limit Exceeded"
    except Exception as e:
        output = str(e)

    return output
