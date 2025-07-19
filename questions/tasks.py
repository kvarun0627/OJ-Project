import os
import uuid
import subprocess
from celery import shared_task
from compiler.models import Submission, TestCaseResult
import shutil

@shared_task
def evaluate_submission(submission_id, code, language):
    try:
        submission = Submission.objects.get(id=submission_id)
        question = submission.question
        user = submission.user
        testcases = question.testcases  # Assumes testcases is a list of dicts with 'input' and 'expected_output'

        folder = f"/tmp/{uuid.uuid4()}"
        os.makedirs(folder, exist_ok=True)

        final_verdict = 'Accepted'

        for case in testcases:
            input_data = case['input']
            expected_output = case['expected_output'].strip()

            user_output = run_and_output(code, input_data, language, folder).strip()

            testcase_verdict = 'Accepted' if user_output == expected_output else 'Not Accepted'

            if testcase_verdict == 'Not Accepted':
                final_verdict = 'Not Accepted'

            TestCaseResult.objects.create(
                question=question,
                user=user,
                submission=submission,
                input_data=input_data,
                user_output=user_output,
                expected_output=expected_output,
                code=code,
                verdict=testcase_verdict,
            )

        submission.verdict = final_verdict
        submission.save()
        shutil.rmtree(folder) #to remove the temporary folder

    except Exception as e:
        submission = Submission.objects.get(id=submission_id)
        submission.verdict = 'Error'
        submission.save()
        print(f"Error in evaluation: {e}")


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
                timeout=2,
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
                timeout=2,
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
                timeout=2,
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
