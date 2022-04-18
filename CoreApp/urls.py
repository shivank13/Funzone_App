from django.urls import path 
from . import views
from GameApp.views import index, game

urlpatterns = [
    path('', views.login_form, name='login_form'),
    path('login_form/', views.login_form, name='login_form'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),

    # learner dashboard
    path('emp_signup/', views.EmployeeSignUpView.as_view(), name='emp_signup'),

    path('employee/', views.home_employee, name='employee'),
    path('emp_interests/', views.EmployeeInterestsView.as_view(), name='emp_interests'),
    path('emp_allquiz/', views.EmployeeAllQuizListView.as_view(), name='emp_allquiz'),
    path('emp_takenquiz/', views.EmployeeTakenQuizListView.as_view(), name='emp_takenquiz'),
    path('quiz/<int:pk>/', views.start_quiz, name='start_quiz'),
    path('emp_books/', views.EmployeeBooksListView.as_view(), name='emp_books'),
    path('emp_notice/', views.EmployeeAnnouncementsListView.as_view(), name='emp_announcements'),
    path('emp_profile/', views.emp_profile, name='emp_profile'),
    path('emp_create_profile/', views.emp_create_profile, name='emp_create_profile'),

    path('play/', index, name='index'),
    path('play/<room_code>', game, name="game"),

    # organizer dashboard
    path('organizer/', views.home_organizer, name='organizer'),

    path('add_quiz/', views.QuizAddView.as_view(), name='add_quiz'),
    path('update_quiz/<int:pk>/', views.QuizUpdateView.as_view(), name='update_quiz'),
    path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='delete_quiz'),
    path('edit_quizlist/', views.EditQuizListView.as_view(), name='edit_quizlist'),
    path('quiz/<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),

    path('add_question/<int:pk>', views.add_question, name='add_question'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/update', views.update_question, name='update_question'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(),
        name='delete_question'),

    path('add_notice/', views.AddNoticeView.as_view(), name='add_notice'),
    path('allnotices/', views.OrganizerAnnouncementsView.as_view(), name='allnotices'),
    
    path('publish_book/', views.publish_book, name='publish_book'),
    path('allbooks/', views.AllBooksList.as_view(), name='allbooks'),
    path('add_book/', views.add_book, name='add_book'),
    path('update_book/<int:pk>', views.update_book, name='update_book'),  

    path('org_profile/', views.org_profile, name='org_profile'),
    path('org_create_profile/', views.org_create_profile, name='org_create_profile'),

    # admin dashboard
    path('owner/', views.home_admin, name='owner'),
    path('reg_organizer/', views.RegisterOrganizerView.as_view(), name='reg_organizer'),
    path('reg_employee/', views.RegisterEmployeeView.as_view(), name='reg_employee'),
    path('reg_interest/', views.register_interest, name='reg_interest'),

    path('adm_add_quiz/', views.AdminQuizAddView.as_view(), name='adm_add_quiz'),
    path('adm_update_quiz/<int:pk>/', views.AdminQuizUpdateView.as_view(), name='adm_update_quiz'),
    path('adm_quiz/<int:pk>/delete/', views.AdminQuizDeleteView.as_view(), name='adm_delete_quiz'),
    path('adm_edit_quizlist/', views.AdminEditQuizListView.as_view(), name='adm_edit_quizlist'),
    path('adm_quiz/<int:pk>/results/', views.AdminQuizResultsView.as_view(), name='adm_quiz_results'),

    path('adm_add_question/<int:pk>', views.adm_add_question, name='adm_add_question'),
    path('adm_quiz/<int:quiz_pk>/question/<int:question_pk>/update', views.adm_update_question, name='adm_update_question'),
    path('adm_quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.AdminQuestionDeleteView.as_view(),
            name='adm_delete_question'),

    path('adm_publish_book/', views.adm_publish_book, name='adm_publish_book'),
    path('adm_allbooks/', views.AdminAllBooksList.as_view(), name='adm_allbooks'),
    path('adm_add_book/', views.adm_add_book, name='adm_add_book'),
    path('adm_update_book/<int:pk>', views.adm_update_book, name='adm_update_book'),  

    path('adm_add_notice/', views.AdminAddNoticeView.as_view(), name='adm_add_notice'),
    path('adm_allnotices/', views.AdminAnnouncementsView.as_view(), name='adm_allnotices'),
    path('adm_delete_notices/', views.AdminDeleteAnnouncementsView.as_view(), name='adm_delete_notices'),
    path('delete_notice/<int:pk>', views.AdminDeleteAnnouncementView.as_view(), name='adm_delete_notice'),

    path('all_users/', views.AllUsersListView.as_view(), name='all_users'),
    path('delete_user/<int:pk>', views.DeleteUserView.as_view(), name='delete_user'),
    path('create_user_form/', views.create_user_form, name='create_user_form'),
    path('create_user/', views.create_user, name='create_user'),

    path('adm_profile/', views.adm_profile, name='adm_profile'),
    path('adm_create_profile/', views.adm_create_profile, name='adm_create_profile'),
]
