from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Submission,TestCaseResult
from questions.models import Question
@login_required
def question_submissions(request, pk):
    question = get_object_or_404(Question, id=pk)
    user = request.user

    submissions = Submission.objects.filter(user=user, question=question).order_by('-created_at')

    return render(request, 'frontend/templates/submissions/question_submissions.html', {
        'submissions': submissions,
    })

@login_required
def testcase_results(request, pk, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, question_id=pk, user=request.user)
    testcases = TestCaseResult.objects.filter(submission=submission)

    return render(request, 'frontend/templates/submissions/testcase_results.html', {'submissions': submission,
        'testcases': testcases,
    })
