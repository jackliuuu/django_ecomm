from django.shortcuts import render
from django.views.generic import FormView,TemplateView
from django.core.mail import EmailMultiAlternatives
from core.models import Setting
from django.db import connection
from django.utils.translation import get_language
# Create your views here.
from .models import EPaperEmail
from .form import EPaperForm
class EPaperViews(FormView):
    template_name="epaper/epaper.html"
    form_class = EPaperForm
    success_url = '/epaper/thanks/'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not EPaperEmail.objects.filter(email=self.object.email):
            self.object.save()
            to = [self.object.email]
            self.send_email(to)
        return super().form_valid(form)
    def send_email(self,to):
        language = get_language()
        setting = Setting.objects.get(id=language)
        subject = f'您已成功訂閱 {setting.sitename} 電子報'
        text_content = f'您已成功訂閱 {setting.sitename} 電子報'
        html_content = f'<p>您已成功訂閱 {setting.sitename} 電子報</p>'
        msg = EmailMultiAlternatives(subject,text_content,None,to)
        msg.attach_alternative(html_content,"text/html")
        msg.send()
class EPaperThanksView(TemplateView):
    template_name="epaper/thanks.html"
    
    
    