from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='about', view=views.about, name='about'),
    path(route='contact', view=views.contact, name='contact'),
    path(route='registrationrequest', view=views.registration_request, name='registration'),
    path(route='loginrequest', view=views.login_request, name='login'),
    path(route='logoutrequest', view=views.logout_request, name='logout'),
    path(route='', view=views.get_dealerships, name='index'),
    path(route='st/<state>', view=views.get_dealerships_by_st, name='index_by_state'),
    path(route='id/<int:id>', view=views.get_dealerships_by_id, name='index_by_id'),
    path(route='review/<int:dealership>', view=views.get_dealer_review, name='review'),
    path(route='postreview', view=views.post_review, name='post_review'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)