from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import TakeQuizForm, EmployeeSignUpForm, OrganizerSignUpForm, QuestionForm, BaseAnswerInlineFormSet, \
    EmployeeInterestsForm, PostForm
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from .models import TakenQuiz, Profile, Quiz, Question, Answer, Employee, User, Interest, Books, Announcement
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


def login_form(request):
    return render(request, 'landing/login.html')


def logoutView(request):
    logout(request)
    return redirect('login_form')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('owner')
            elif user.is_organizer:
                return redirect('organizer')
            elif user.is_employee:
                return redirect('employee')
            else:
                return redirect('login_form')
        else:
            messages.warning(request, "Invalid Username Or Password")
            return redirect('login_form')


class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'landing/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        messages.warning(self.request, "Check Password And Select Atleast 2 Interests")
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Employee Created Successfully")
        return redirect('login_form')


# employee dashboard
class EmployeeHomeQuizListView(ListView):
    model = Quiz
    ordering = ('name',)

    context_object_name = 'quizzes'
    template_name = 'dashboard/employee/home.html'

    def get_queryset(self):
        employee = self.user.employee
        employee_interests = employee.interests.values_list('pk', flat=True)
        taken_quizzes = employee.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(interest__in=employee_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset

class EmployeeHomeAnnouncementsListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/employee/home.html'

    def get_queryset(self):
        return Announcement.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')

@login_required(login_url='login_form')
def home_employee(self):
    employee = User.objects.filter(is_employee=True).count()
    interest = Interest.objects.all().count()
    quizzes = EmployeeHomeQuizListView.get_queryset(self)
    notices = EmployeeHomeAnnouncementsListView.get_queryset(self)
    context = {'employee': employee, 'interest': interest, 'quizzes': quizzes, 'notices': notices}
    template_name = 'dashboard/employee/home.html'

    return render(self, template_name, context)


class EmployeeInterestsView(UpdateView):
    model = Employee
    form_class = EmployeeInterestsForm
    template_name = 'dashboard/employee/interests_form.html'
    success_url = reverse_lazy('employee')

    def get_object(self):
        return self.request.user.employee

    def form_valid(self, form):
        messages.success(self.request, 'Interest Was Updated Successfully')
        return super().form_valid(form)


class EmployeeAllQuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    context_object_name = 'quizzes'
    template_name = 'dashboard/employee/quiz_list.html'

    def get_queryset(self):
        employee = self.request.user.employee
        employee_interests = employee.interests.values_list('pk', flat=True)
        taken_quizzes = employee.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(interest__in=employee_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


class EmployeeTakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'dashboard/employee/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.employee.taken_quizzes \
            .select_related('quiz', 'quiz__interest') \
            .order_by('quiz__name')
        return queryset


def start_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    employee = request.user.employee

    if employee.quizzes.filter(pk=pk).exists():
        return render(request, 'dashboard/employee/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = employee.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    question = unanswered_questions.first()

    counter = total_questions - total_unanswered_questions + 1
    progress = 100 - round(((total_unanswered_questions) / total_questions) * 100)

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                employee_answer = form.save(commit=False)
                employee_answer.student = employee
                employee_answer.save()
                if employee.get_unanswered_questions(quiz).exists():
                    return redirect('start_quiz', pk)
                else:
                    correct_answers = employee.quiz_answers.filter(answer__question__quiz=quiz,
                                                                   answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(employee=employee, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (
                            quiz.name, score))
                    else:
                        messages.success(request,
                                         'Congratulations! You completed the quiz %s with success! You scored %s points.' % (
                                             quiz.name, score))
                    return render(request, 'dashboard/employee/quiz_result.html',{
                        'quiz': quiz,
                        'score': score,
                        'employee': employee
                    })
    else:
        form = TakeQuizForm(question=question)

    
    return render(request, 'dashboard/employee/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress,
        'counter': counter,
        'total': total_questions,
    })


class EmployeeBooksListView(ListView):
    model = Books
    template_name = 'dashboard/employee/list_books.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        return Books.objects.order_by('-id')


class EmployeeAnnouncementsListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/employee/announcements.html'

    def get_queryset(self):
        return Announcement.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


def emp_profile(request):
    current_user = request.user
    user_id = current_user.id
    print(user_id)
    users = Profile.objects.filter(user_id=user_id)
    users = {'users': users}
    return render(request, 'dashboard/employee/user_profile.html', users)


def emp_create_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phonenumber = request.POST['phonenumber']
        hobby = request.POST['hobby']
        city = request.POST['city']
        country = request.POST['country']
        birth_date = request.POST['birth_date']
        avatar = request.FILES['avatar']
        current_user = request.user
        user_id = current_user.id
        # print(user_id)

        Profile.objects.filter(id=user_id).create(user_id=user_id, first_name=first_name, last_name=last_name,
                                                  phonenumber=phonenumber, hobby=hobby, city=city, country=country,
                                                  birth_date=birth_date, avatar=avatar)
        messages.success(request, 'Profile Was Created Successfully')
        return redirect('emp_profile')
    else:
        current_user = request.user
        user_id = current_user.id
        print(user_id)
        users = Profile.objects.filter(user_id=user_id)
        users = {'users': users}
        return render(request, 'dashboard/employee/create_profile.html', users)


# organizer dashboard
@login_required(login_url='login_form')
def home_organizer(request):
    employee = User.objects.filter(is_employee=True).count()
    organizer = User.objects.filter(is_organizer=True).count()
    interest = Interest.objects.all().count()
    users = User.objects.all().count()
    context = {'employee': employee, 'interest': interest, 'organizer': organizer, 'users': users}
    return render(request, 'dashboard/organizer/home.html', context)


class QuizAddView(CreateView):
    model = Quiz
    fields = ('name', 'interest')
    template_name = 'dashboard/organizer/quiz/add_quiz.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'Quiz created, Go Ahead And Add Questions')
        return redirect('update_quiz', quiz.pk)


class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'interest')
    template_name = 'dashboard/organizer/quiz/update_quiz.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('update_quiz', kwargs={'pk', self.object.pk})


def add_question(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You May Now Add Options To The Question')
            return redirect('update_question', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'dashboard/organizer/question/add_question.html', {'quiz': quiz, 'form': form})


def update_question(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormatSet = inlineformset_factory(
        Question,
        Answer,
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormatSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                formset.save()
                formset.save()
            messages.success(request, 'Question And Answers Saved Successfully')
            return redirect('update_quiz', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormatSet(instance=question)
    return render(request, 'dashboard/organizer/question/update_question.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'dashboard/organizer/question/delete_question.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The Question Was Deleted Successfully')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('update_question', kwargs={'pk': question.quiz_id})


class EditQuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    context_object_name = 'quizzes'
    template_name = 'dashboard/organizer/quiz/edit_quizlist.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('interest') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


class QuizResultsView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'dashboard/organizer/quiz/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('employee__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }

        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'dashboard/organizer/quiz/delete_quiz.html'
    success_url = reverse_lazy('edit_quizlist')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


def publish_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        interest_id = request.POST['interest_id']
        cover = request.FILES['cover']
        file = request.FILES['file']
        current_user = request.user
        user_id = current_user.id

        a = Books(title=title, cover=cover, file=file, user_id=user_id, interest_id=interest_id)
        a.save()
        messages.success = (request, 'Books Was Published Successfully')
        return redirect('allbooks')
    else:
        messages.error = (request, 'Books Was Not Published Successfully')
        return redirect('add_book')


class AllBooksList(ListView):
    model = Books
    template_name = 'dashboard/organizer/list_books.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        return Books.objects.order_by('-id')


def add_book(request):
    interests = Interest.objects.only('id', 'name')
    context = {'interests': interests}
    return render(request, 'dashboard/organizer/add_books.html', context)


def update_book(request, pk):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = request.FILES['file'].name

        fs = FileSystemStorage()
        file = fs.save(file.name, file)
        # fileurl = fs.url(file)
        file = file_name
        print(file)

        Books.objects.filter(id=pk).update(file=file)
        messages.success = (request, 'Books was updated successfully!')
        return redirect('allbooks')
    else:
        return render(request, 'dashboard/organizer/update_book.html')



class AddNoticeView(CreateView):
    form_class = PostForm
    model = Announcement
    template_name = 'dashboard/organizer/add_notice.html'
    success_url = reverse_lazy('allnotices')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class OrganizerAnnouncementsView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/organizer/announcements.html'

    def get_queryset(self):
        return Announcement.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


def org_profile(request):
    current_user = request.user
    user_id = current_user.id
    print(user_id)
    users = Profile.objects.filter(user_id=user_id)
    users = {'users': users}
    return render(request, 'dashboard/organizer/user_profile.html', users)


def org_create_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phonenumber = request.POST['phonenumber']
        hobby = request.POST['hobby']
        city = request.POST['city']
        country = request.POST['country']
        birth_date = request.POST['birth_date']
        avatar = request.FILES['avatar']
        current_user = request.user
        user_id = current_user.id
        print(user_id)

        Profile.objects.filter(id=user_id).create(user_id=user_id, first_name=first_name, last_name=last_name,
                                                  phonenumber=phonenumber, hobby=hobby, city=city, country=country,
                                                  birth_date=birth_date, avatar=avatar)
        messages.success(request, 'Profile was created successfully')
        return redirect('org_profile')
    else:
        current_user = request.user
        user_id = current_user.id
        print(user_id)
        users = Profile.objects.filter(user_id=user_id)
        users = {'users': users}
        return render(request, 'dashboard/organizer/create_profile.html', users)


# admin dashboard
@login_required(login_url='login_form')
def home_admin(request):
    employee = User.objects.filter(is_employee=True).count()
    organizer = User.objects.filter(is_organizer=True).count()
    interest = Interest.objects.all().count()
    users = User.objects.all().count()
    context = {'employee': employee, 'interest': interest, 'organizer': organizer, 'users': users}

    return render(request, 'dashboard/admin/home.html', context)


class RegisterOrganizerView(CreateView):
    model = User
    form_class = OrganizerSignUpForm
    template_name = 'dashboard/admin/reg_organizer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'organizer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Organizer Was Added Successfully')
        return redirect('reg_organizer')


class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'dashboard/admin/reg_employee.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Employee Was Added Successfully')
        return redirect('reg_employee')


def register_interest(request):
    if request.method == 'POST':
        name = request.POST['name']
        color = request.POST['color']

        a = Interest(name=name, color=color)
        a.save()
        messages.success(request, 'New Interest Was Registed Successfully')
        return redirect('reg_interest')
    else:
        return render(request, 'dashboard/admin/reg_interest.html')


class AdminQuizAddView(CreateView):
    model = Quiz
    fields = ('name', 'interest')
    template_name = 'dashboard/admin/quiz/add_quiz.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'Quiz created, Go A Head And Add Questions')
        return redirect('adm_update_quiz', quiz.pk)


class AdminQuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'interest')
    template_name = 'dashboard/admin/quiz/update_quiz.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('adm_update_quiz', kwargs={'pk', self.object.pk})


def adm_add_question(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('adm_update_question', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'dashboard/admin/question/add_question.html', {'quiz': quiz, 'form': form})


def adm_update_question(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormatSet = inlineformset_factory(
        Question,
        Answer,
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormatSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                formset.save()
                formset.save()
            messages.success(request, 'Question And Answers Saved Successfully')
            return redirect('adm_update_quiz', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormatSet(instance=question)
    return render(request, 'dashboard/admin/question/update_question.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


class AdminQuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'dashboard/admin/question/delete_question.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The Question Was Deleted Successfully')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('adm_update_question', kwargs={'pk': question.quiz_id})


class AdminEditQuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    context_object_name = 'quizzes'
    template_name = 'dashboard/admin/quiz/edit_quizlist.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('interest') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


class AdminQuizResultsView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'dashboard/admin/quiz/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('employee__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }

        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


class AdminQuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'dashboard/admin/quiz/delete_quiz.html'
    success_url = reverse_lazy('adm_edit_quizlist')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


def adm_publish_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        interest_id = request.POST['interest_id']
        cover = request.FILES['cover']
        file = request.FILES['file']
        current_user = request.user
        user_id = current_user.id

        a = Books(title=title, cover=cover, file=file, user_id=user_id, interest_id=interest_id)
        a.save()
        messages.success = (request, 'Books Was Published Successfully')
        return redirect('adm_allbooks')
    else:
        messages.error = (request, 'Books Was Not Published Successfully')
        return redirect('adm_add_book')


class AdminAllBooksList(ListView):
    model = Books
    template_name = 'dashboard/admin/list_books.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        return Books.objects.order_by('-id')


def adm_add_book(request):
    interests = Interest.objects.only('id', 'name')
    context = {'interests': interests}
    return render(request, 'dashboard/admin/add_books.html', context)


def adm_update_book(request, pk):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = request.FILES['file'].name

        fs = FileSystemStorage()
        file = fs.save(file.name, file)
        # fileurl = fs.url(file)
        file = file_name
        print(file)

        Books.objects.filter(id=pk).update(file=file)
        messages.success = (request, 'Books was updated successfully!')
        return redirect('adm_allbooks')
    else:
        return render(request, 'dashboard/admin/update_book.html')


class AdminAddNoticeView(CreateView):
    model = Announcement
    form_class = PostForm
    template_name = 'dashboard/admin/add_notice.html'
    success_url = reverse_lazy('adm_allnotices')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class AdminAnnouncementsView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/admin/announcements.html'

    def get_queryset(self):
        return Announcement.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


class AdminDeleteAnnouncementsView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/admin/list_announcements.html'
    context_object_name = 'tises'
    paginated_by = 20

    def get_queryset(self):
        return Announcement.objects.order_by('-id')


class AdminDeleteAnnouncementView(SuccessMessageMixin, DeleteView):
    model = Announcement
    template_name = 'dashboard/admin/delete_notice.html'
    success_url = reverse_lazy('adm_delete_notices')
    success_message = "Announcement Was Deleted Successfully"


class AllUsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/admin/all_users_list.html'
    context_object_name = 'users'
    paginated_by = 20

    def get_queryset(self):
        return User.objects.order_by('-id')


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'dashboard/admin/delete_user.html'
    success_url = reverse_lazy('all_users')
    success_message = "User Was Deleted Successfully"


def create_user_form(request):
    return render(request, 'dashboard/admin/add_user.html')


def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)

        a = User(first_name=first_name, last_name=last_name, username=username, password=password, email=email,
                 is_admin=True)
        a.save()
        messages.success(request, 'Admin Was Created Successfully')
        return redirect('all_users')
    else:
        messages.error(request, 'Admin Was Not Created Successfully')
        return redirect('create_user_form')


def adm_profile(request):
    current_user = request.user
    user_id = current_user.id
    users = Profile.objects.filter(user_id=user_id)
    users = {'users': users}
    return render(request, 'dashboard/admin/user_profile.html', users)


def adm_create_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birth_date = request.POST['birth_date']
        phonenumber = request.POST['phonenumber']
        city = request.POST['city']
        country = request.POST['country']
        avatar = request.FILES['avatar']
        hobby = request.POST['hobby']
        current_user = request.user
        user_id = current_user.id
        print(user_id)

        Profile.objects.filter(id=user_id).create(user_id=user_id, phonenumber=phonenumber, first_name=first_name,
                                                  last_name=last_name, hobby=hobby, birth_date=birth_date,
                                                  avatar=avatar,
                                                  city=city, country=country)
        messages.success(request, 'Your Profile Was Created Successfully')
        return redirect('auser_profile')
    else:
        current_user = request.user
        user_id = current_user.id
        users = Profile.objects.filter(user_id=user_id)
        users = {'users': users}
        return render(request, 'dashboard/admin/create_profile.html', users)
