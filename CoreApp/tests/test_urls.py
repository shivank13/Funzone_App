from django.test import SimpleTestCase
from django.urls import reverse, resolve
from CoreApp.views import *
from GameApp.views import *


class TestUrls(SimpleTestCase):
    def test_login_form_url_is_resolved(self):
        url = reverse('login_form')
        self.assertEquals(resolve(url).func, login_form)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutView)

    def test_emp_signup_url_is_resolved(self):
        url = reverse('emp_signup')
        self.assertEquals(resolve(url).func.view_class, EmployeeSignUpView)

    def test_employee_url_is_resolved(self):
        url = reverse('employee')
        self.assertEquals(resolve(url).func, home_employee)

    def test_emp_interests_url_is_resolved(self):
        url = reverse('emp_interests')
        self.assertEquals(resolve(url).func.view_class, EmployeeInterestsView)

    def test_emp_allquiz_url_is_resolved(self):
        url = reverse('emp_allquiz')
        self.assertEquals(resolve(url).func.view_class, EmployeeAllQuizListView)

    def test_emp_takenquiz_url_is_resolved(self):
        url = reverse('emp_takenquiz')
        self.assertEquals(resolve(url).func.view_class, EmployeeTakenQuizListView)

    def test_start_quiz_is_resolved(self):
        url = reverse('start_quiz', args=['1'])
        self.assertEquals(resolve(url).func, start_quiz)

    def test_emp_books_url_is_resolved(self):
        url = reverse('emp_books')
        self.assertEquals(resolve(url).func.view_class, EmployeeBooksListView)

    def test_emp_notice_url_is_resolved(self):
        url = reverse('emp_announcements')
        self.assertEquals(resolve(url).func.view_class, EmployeeAnnouncementsListView)

    def test_emp_profile_url_is_resolved(self):
        url = reverse('emp_profile')
        self.assertEquals(resolve(url).func, emp_profile)

    def test_emp_create_profile_url_is_resolved(self):
        url = reverse('emp_create_profile')
        self.assertEquals(resolve(url).func, emp_create_profile)

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_game_url_is_resolved(self):
        url = reverse('game', args=['1'])
        self.assertEquals(resolve(url).func, game)

    def test_ogranizer_url_is_resolved(self):
        url = reverse('organizer')
        self.assertEquals(resolve(url).func, home_organizer)

    def test_add_quiz_url_is_resolved(self):
        url = reverse('add_quiz')
        self.assertEquals(resolve(url).func.view_class, QuizAddView)

    def test_update_quiz_url_is_resolved(self):
        url = reverse('update_quiz', args=['1'])
        self.assertEquals(resolve(url).func.view_class, QuizUpdateView)

    def test_delete_quiz_url_is_resolved(self):
        url = reverse('delete_quiz', args=['1'])
        self.assertEquals(resolve(url).func.view_class, QuizDeleteView)

    def test_edit_quizlist_url_is_resolved(self):
        url = reverse('edit_quizlist')
        self.assertEquals(resolve(url).func.view_class, EditQuizListView)

    def test_quiz_results_url_is_resolved(self):
        url = reverse('quiz_results', args=['1'])
        self.assertEquals(resolve(url).func.view_class, QuizResultsView)

    def test_add_question_url_is_resolved(self):
        url = reverse('add_question', args=['1'])
        self.assertEquals(resolve(url).func, add_question)

    def test_update_queston_url_is_resolved(self):
        url = reverse('update_question', args=['1', '1'])
        self.assertEquals(resolve(url).func, update_question)

    def test_delete_question_url_is_resolved(self):
        url = reverse('delete_question', args=['1', '1'])
        self.assertEquals(resolve(url).func.view_class, QuestionDeleteView)

    def test_add_notice_url_is_resolved(self):
        url = reverse('add_notice')
        self.assertEquals(resolve(url).func.view_class, AddNoticeView)

    def test_allnotices_url_is_resolved(self):
        url = reverse('allnotices')
        self.assertEquals(resolve(url).func.view_class, OrganizerAnnouncementsView)

    def test_publish_book_url_is_resolved(self):
        url = reverse('publish_book')
        self.assertEquals(resolve(url).func, publish_book)

    def test_allbooks_url_is_resolved(self):
        url = reverse('allbooks')
        self.assertEquals(resolve(url).func.view_class, AllBooksList)

    def test_add_book_url_is_resolved(self):
        url = reverse('add_book')
        self.assertEquals(resolve(url).func, add_book)

    def test_update_book_url_is_resolved(self):
        url = reverse('update_book', args=['1'])
        self.assertEquals(resolve(url).func, update_book)

    def test_org_profile_url_is_resolved(self):
        url = reverse('org_profile')
        self.assertEquals(resolve(url).func, org_profile)

    def test_org_create_profile_url_is_resolved(self):
        url = reverse('org_create_profile')
        self.assertEquals(resolve(url).func, org_create_profile)

    def test_owner_url_is_resolved(self):
        url = reverse('owner')
        self.assertEquals(resolve(url).func, home_admin)

    def test_reg_employee_url_is_resolved(self):
        url = reverse('reg_employee')
        self.assertEquals(resolve(url).func.view_class, RegisterEmployeeView)

    def test_reg_organizer_url_is_resolved(self):
        url = reverse('reg_organizer')
        self.assertEquals(resolve(url).func.view_class, RegisterOrganizerView)

    def test_reg_interest_url_is_resolved(self):
        url = reverse('reg_interest')
        self.assertEquals(resolve(url).func, register_interest)

    def test_adm_add_quiz_url_is_resolved(self):
        url = reverse('adm_add_quiz')
        self.assertEquals(resolve(url).func.view_class, AdminQuizAddView)

    def test_adm_update_quiz_url_is_resolved(self):
        url = reverse('adm_update_quiz', args=['1'])
        self.assertEquals(resolve(url).func.view_class, AdminQuizUpdateView)

    def test_adm_delete_quiz_url_is_resolved(self):
        url = reverse('adm_delete_quiz', args=['1'])
        self.assertEquals(resolve(url).func.view_class, AdminQuizDeleteView)

    def test_adm_edit_quizlist_url_is_resolved(self):
        url = reverse('adm_edit_quizlist')
        self.assertEquals(resolve(url).func.view_class, AdminEditQuizListView)

    def test_adm_quiz_results_url_is_resolved(self):
        url = reverse('adm_quiz_results', args=['1'])
        self.assertEquals(resolve(url).func.view_class, AdminQuizResultsView)

    def test_adm_add_question_url_is_resolved(self):
        url = reverse('adm_add_question', args=['1'])
        self.assertEquals(resolve(url).func, adm_add_question)

    def test_adm_update_question_url_is_resolved(self):
        url = reverse('adm_update_question', args=['1', '1'])
        self.assertEquals(resolve(url).func, adm_update_question)

    def test_adm_delete_question_url_is_resolved(self):
        url = reverse('adm_delete_question', args=['1', '1'])
        self.assertEquals(resolve(url).func.view_class, AdminQuestionDeleteView)

    def test_adm_publish_book_url_is_resolved(self):
        url = reverse('adm_publish_book')
        self.assertEquals(resolve(url).func, adm_publish_book)

    def test_adm_allbooks_url_is_resolved(self):
        url = reverse('adm_allbooks')
        self.assertEquals(resolve(url).func.view_class, AdminAllBooksList)

    def test_adm_add_book_url_is_resolved(self):
        url = reverse('adm_add_book')
        self.assertEquals(resolve(url).func, adm_add_book)

    def test_adm_update_book_url_is_resolved(self):
        url = reverse('adm_update_book', args=['1'])
        self.assertEquals(resolve(url).func, adm_update_book)

    def test_adm_add_notice_url_is_resolved(self):
        url = reverse('adm_add_notice')
        self.assertEquals(resolve(url).func.view_class, AdminAddNoticeView)

    def test_amd_allnotices_url_is_resolved(self):
        url = reverse('adm_allnotices')
        self.assertEquals(resolve(url).func.view_class, AdminAnnouncementsView)

    def test_adm_delete_notices_url_is_resolved(self):
        url = reverse('adm_delete_notices')
        self.assertEquals(resolve(url).func.view_class, AdminDeleteAnnouncementsView)

    def test_adm_delete_notice_url_is_resolved(self):
        url = reverse('adm_delete_notice', args=['1'])
        self.assertEquals(resolve(url).func.view_class, AdminDeleteAnnouncementView)

    def test_all_users_url_is_resolved(self):
        url = reverse('all_users')
        self.assertEquals(resolve(url).func.view_class, AllUsersListView)

    def test_delete_user_url_is_resolved(self):
        url = reverse('delete_user', args=['1'])
        self.assertEquals(resolve(url).func.view_class, DeleteUserView)

    def test_create_user_form_url_is_resolved(self):
        url = reverse('create_user_form')
        self.assertEquals(resolve(url).func, create_user_form)

    def test_create_user_url_is_resolved(self):
        url = reverse('create_user')
        self.assertEquals(resolve(url).func, create_user)

    def test_adm_profile_url_is_resolved(self):
        url = reverse('adm_profile')
        self.assertEquals(resolve(url).func, adm_profile)

    def test_adm_create_profile_url_is_resolved(self):
        url = reverse('adm_create_profile')
        self.assertEquals(resolve(url).func, adm_create_profile)
