from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import JsonResponse , HttpResponseRedirect
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "welcome.html", para)

def about_us(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "about_us.html", para)

@login_required
def search_view(request):
    query = request.GET.get('q')
    if query:
        search_query = Q(name__icontains=query)
        quiz = Quiz.objects.filter(search_query)
    else:
        quiz = Quiz.objects.all()

    context = {"quiz": quiz}
    return render(request, 'search_view.html', context)

@login_required(login_url = '/login')
def quizzes(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, 'index.html', para)

@login_required(login_url = '/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz.html", {'quiz':quiz})

def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, myid):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                correct_answer = None
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                            break  # Once correct answer found, no need to check further
                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})
     
        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})
    else:
        # Handle non-AJAX or non-POST requests here
        pass




def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('/signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please <a href="/login">Login</a>.')
            return redirect('/signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('/signup')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/login')
    
    return render(request, "signup.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, 'Invalid username or password. Please register if new')
            return render(request, "login.html") 
    return render(request, "login.html")

def Logout(request):
    logout(request)
    return redirect('/')


def add_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_quiz')
    else:
        form = QuizForm()
    
    quizzes = Quiz.objects.all()
    quiz_details = [
        {
            'id': quiz.id,
            'name': quiz.name,
        }
        for quiz in quizzes
    ]
    return render(request, 'add_quiz.html', {'form': form, 'quiz_details': quiz_details})

#delete quiz
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz.delete()
    return HttpResponseRedirect(reverse('add_quiz'))


def add_question(request):
    questions = Question.objects.all().order_by('-id')
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            quiz = question.quiz  # Get the related Quiz instance
            question.save()  # Save the question
            quiz.number_of_questions = Question.objects.filter(quiz=quiz).count()
            quiz.save()
            return redirect('add_question')  
    else:
        form = QuestionForm()
    
    question_count = questions.count()

    
    context = {
        'form': form,
        'questions': questions,
        'question_count': question_count,
    }
    
    return render(request, 'add_question.html', context)



def edit_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        new_content = request.POST.get('content', '')
        if new_content:
            question.content = new_content
            question.save()
            return JsonResponse({'message': 'Question updated successfully'})
        else:
            return JsonResponse({'error': 'Empty content provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def delete_question(request, myid):
    # Retrieve the question object if it exists, otherwise return 404 error page
    question = get_object_or_404(Question, id=myid)
    
    quiz = question.quiz  # Fetch the quiz associated with the deleted question

    if request.method == "POST":
        question.delete()
        quiz.save()

        # Update number_of_questions for the associated quiz
        quiz.refresh_from_db()  # Ensure we have the latest data from the database
        quiz.number_of_questions =Question.objects.filter(quiz=quiz).count()

        # Save the quiz object after updating its number_of_questions field
        quiz.save()

        return redirect('/add_question')

    context = {
        'question': question,
        'question_count':  quiz.number_of_questions,  # Update question_count to reflect current count
    }
    return render(request, "delete_question.html", context)



def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "add_options.html", {'alert':alert})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_options.html", {'formset':formset, 'question':question})

def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "results.html", {'marks':marks})

def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/results')
    return render(request, "delete_result.html", {'marks':marks})



