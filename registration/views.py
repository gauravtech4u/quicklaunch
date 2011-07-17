"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from registration.forms import RegistrationForm
from registration.forms import ProfileEditForm
from registration.models import RegistrationProfile
from registration.models import UserProfile
from django.contrib.auth.models import User
from djangovoice.models import Feedback
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from job.models import Job

def activate(request, activation_key,
             template_name='registration/activate.html',
             extra_context=None):
    """
    Activate a ``User``'s account from an activation key, if their key
    is valid and hasn't expired.
    
    By default, use the template ``registration/activate.html``; to
    change this, pass the name of a template as the keyword argument
    ``template_name``.
    
    **Required arguments**
    
    ``activation_key``
       The activation key to validate and use for activating the
       ``User``.
    
    **Optional arguments**
       
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.
    
    ``template_name``
        A custom template to use.
    
    **Context:**
    
    ``account``
        The ``User`` object corresponding to the account, if the
        activation was successful. ``False`` if the activation was not
        successful.
    
    ``expiration_days``
        The number of days for which activation keys stay valid after
        registration.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account,
                                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=context)


def register(request, success_url=None,
             form_class=RegistrationForm, profile_callback=None,
             template_name='registration/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register an account.
    
    Following successful registration, issue a redirect; by default,
    this will be whatever URL corresponds to the named URL pattern
    ``registration_complete``, which will be
    ``/accounts/register/complete/`` if using the included URLConf. To
    change this, point that named pattern at another URL, or pass your
    preferred URL as the keyword argument ``success_url``.
    
    By default, ``registration.forms.RegistrationForm`` will be used
    as the registration form; to change this, pass a different form
    class as the ``form_class`` keyword argument. The form class you
    specify must have a method ``save`` which will create and return
    the new ``User``, and that method must accept the keyword argument
    ``profile_callback`` (see below).
    
    To enable creation of a site-specific user profile object for the
    new user, pass a function which will create the profile object as
    the keyword argument ``profile_callback``. See
    ``RegistrationManager.create_inactive_user`` in the file
    ``models.py`` for details on how to write this function.
    
    By default, use the template
    ``registration/registration_form.html``; to change this, pass the
    name of a template as the keyword argument ``template_name``.
    
    **Required arguments**
    
    None.
    
    **Optional arguments**
    
    ``form_class``
        The form class to use for registration.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.
    
    ``profile_callback``
        A function which will be used to create a site-specific
        profile instance for the new ``User``.
    
    ``success_url``
        The URL to redirect to on successful registration.
    
    ``template_name``
        A custom template to use.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            
            #form = AuthenticationForm(request.POST)
            auth_login(request,user)
            #return HttpResponseRedirect(success_url or reverse('registration_complete'))
            #return HttpResponseRedirect(success_url or reverse('registration_complete'))
            if 'next' in request.POST:
                next = request.POST['next']
            else:
                next = '/'
            return render_to_response('registration/registration_complete.html',
                              { 'next': next },
                              context_instance=RequestContext(request))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)

def edit(request):
    user_to_edit = get_object_or_404(User, username=request.user.username)
    profile = get_object_or_404(UserProfile, user = user_to_edit)     
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            edited_user = RegistrationProfile.objects.edit_profile(user_to_edit,profile,form)
            return HttpResponseRedirect('/')
            
    else:
        form = ProfileEditForm(initial={'first_name': user_to_edit.first_name,
                                        'mobile': profile.mobile,
                                        #'type': profile.type,
                                        #'category': profile.category,
                                        'location': profile.location,})
        
    question_list = Feedback.objects.filter( user = user_to_edit )    
    job_list = Job.objects.filter( author = user_to_edit )    
    current='myaccount'
    return render_to_response('registration/edit.html', locals(),
                    context_instance=RequestContext(request))
    
def detail(request,username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user = user)
    question_list = Feedback.objects.filter( user = user )    
    job_list = Job.objects.filter( author = user )    
    return render_to_response('registration/detail.html', locals(),
                    context_instance=RequestContext(request))
    
def change_setting(request):
    if request.method == 'POST':
        show_qna=request.POST.get('show_qna')
        show_searches=request.POST.get('show_searches')
        show_me=request.POST.get('show_me')
        user=UserProfile.objects.get(user=request.user.id)
        if show_qna:
            user.show_qna=show_qna
        if show_searches:
            user.show_search=show_searches
        if show_me:
            user.show_me=show_me
        user.save()
        return HttpResponseRedirect("/accounts/edit/")
    else:
            
        return render_to_response('registration/change_setting.html', locals(),
                        context_instance=RequestContext(request))
        
def get_user_profile(request,user_id=None):
    user=UserProfile.objects.get(id=user_id)
    user_to_edit = get_object_or_404(User, username=user.user.username)
    profile = get_object_or_404(UserProfile, user = user_to_edit)     
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            edited_user = RegistrationProfile.objects.edit_profile(user_to_edit,profile,form)
            return HttpResponseRedirect('/')
    else:
        form = ProfileEditForm(initial={'first_name': user_to_edit.first_name,
                                        'mobile': profile.mobile,
                                        #'type': profile.type,
                                        #'category': profile.category,
                                        'location': profile.location,})
    question_list = Feedback.objects.filter( user = user_to_edit )    
    job_list = Job.objects.filter( author = user_to_edit )    
    
    return render_to_response('registration/edit.html', locals(),
                    context_instance=RequestContext(request))
    
edit = login_required(edit)