from django import forms  # Djangoが準備しているforms
from .models import DemoImage
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class ImageForm(forms.ModelForm):
    class Meta:
        model = DemoImage
        fields = '__all__' # 全てのカラムを使用する

# サインアップ
class SignUpForm(UserCreationForm):
    def signup(request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                new_user = authenticate(username=username, password1=password1, password2=password2)
                if new_user is not None:
                    login(request, new_user)
                    return redirect('index')
        else:
            form = SignUpForm()
            return render(request, 'herokudjangoapp/signup.html', {'form': form})

# ログインフォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # htmlの表示を変更可能にする
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'