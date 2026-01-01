from urllib import request
from django.shortcuts import render, get_object_or_404, redirect


from .models import Quiz, Choice, UserAnswer, Question
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.html')


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})



@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':

        UserAnswer.objects.filter(user=request.user, question__quiz=quiz).delete()

        score = 0
        total = quiz.questions.count()

        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f"question_{question.id}")
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)

                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice
                )

                if selected_choice.is_correct:
                    score += 1

        return render(request, 'result.html', {
            'quiz': quiz,
            'correct': score,
            'score': score,
            'total': total
        })

    return render(request, 'quiz_detail.html', {'quiz': quiz})






# ===== DASHBOARD VIEWS - EE RENDU ADD CHEYYANDI ===== #

@login_required
def student_dashboard(request):



    available_quizzes = Quiz.objects.filter(is_active=True)
   
    # Check profile exists
    if not hasattr(request.user, 'profile'):
        from accounts.models import Profile
        Profile.objects.create(user=request.user, is_student=True)
    
   
   
    # Get stats
    user_answers = UserAnswer.objects.filter(user=request.user)
    total_quizzes_taken = user_answers.values('question__quiz').distinct().count()
    total_questions_answered = user_answers.count()
   

    context = {
        'total_quizzes_taken': total_quizzes_taken,
        'total_questions_answered': total_questions_answered,
        'available_quizzes': available_quizzes,
    }
    
    return render(request, 'student_dashboard.html', context)


@login_required
def my_results(request):
    answers = UserAnswer.objects.filter(user=request.user).select_related('question__quiz')

    quiz_scores = {}

    for ans in answers:
        quiz = ans.question.quiz
        if quiz not in quiz_scores:
            quiz_scores[quiz] = {'total': 0, 'correct': 0}
        quiz_scores[quiz]['total'] += 1
        if ans.selected_choice.is_correct:
            quiz_scores[quiz]['correct'] += 1

    return render(request, 'my_results.html', {'quiz_scores': quiz_scores})


def leaderboard(request):
    from django.contrib.auth.models import User
    from .models import UserAnswer

    users = User.objects.all()
    leaderboard_data = []

    for user in users:
        total = UserAnswer.objects.filter(user=user, selected_choice__is_correct=True).count()
        leaderboard_data.append({
            'username': user.username,
            'score': total
        })

    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_data})




@login_required
def settings(request):
    if request.method=='POST':
        request.user.username=request.POST['username']
        request.user.email=request.POST['email']
        request.user.save()
        messages.success(request,"Profile updated!")
        return redirect('settings')
    return render(request,'settings.html')

      
       