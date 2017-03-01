from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        # 	user = user_qs.first()

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_("Este usuário não existe!"))

            if not user.check_password(password):
                raise forms.ValidationError(_('Senha incorreta!'))

            if not user.is_active:
                raise forms.ValidationError(_("Este usuário não esta ativo."))
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    email2 = forms.EmailField(label=_('Confirme o seu email'))
    password = forms.CharField(label=_('Escolha uma senha'),widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirme a sua senha'),widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
        labels = {
            'username': _('Usuário'),
        }
        help_texts = {
            'username': _(''),
        }



    # with clean the validations errors messages dont goes to the actual field ...
    # def clean(self, *args, **kwargs):
    # 	email = self.cleaned_data.get('email')
    # 	email2 = self.cleaned_data.get('email2')
    # 	if not email == email2:
    # 		raise forms.ValidationError("Emails must match")
    # 	email_qs = User.objects.filter(email=email)
    # 	if email_qs.exists():
    # 		raise forms.ValidationError("This Email has already been registered!")
    #
    # 	return super(UserRegisterForm, self).clean(*args, **kwargs)

    # with this the validation error goes to the actual field
    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if not email == email2:
            raise forms.ValidationError(_("Emails precisam ser iguais."))
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError(_('Este email já esta cadastrado.'))

        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password == password2:
            raise forms.ValidationError(_("Senha devem ser iguais"))
        #
        # if email_qs.exists():
        #     raise forms.ValidationError("This Email has already been registered!")

        return password
