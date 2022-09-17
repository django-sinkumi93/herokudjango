import torch
from django.shortcuts import render, redirect
from model import predict
from PIL import Image

from .forms import ImageForm
from .models import DemoImage

from .forms import LoginForm, SignUpForm
import numpy as np
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# ユーザー認証
from django.contrib.auth.models import User

# 犬猫判別
@login_required
def index(request):
    if request.method == 'POST':    # Formの入力があった時
        form = ImageForm(request.POST, request.FILES)    # 入力データを取得する
        if form.is_valid():    # Formの記載の検証を行う
            form.save()    # 問題なければ、入力データを保存
            data = DemoImage.objects.get(id=DemoImage.objects.latest('id').id)
            image_name = data.image
            image_url = f'media/{image_name}'  # 画像のパスを生成
            # 推論パート
            image = Image.open(image_url).convert('RGB')
            x = predict.transform(image)
            x = x.unsqueeze(0)
            device = torch.device('cpu')
            # モデルのインスタンス化
            net = predict.Net().to(device).eval()
            # パラメータの読み込み
            net.load_state_dict(
                torch.load(
                    'model/dogcat_params.pt',  # パラメータを指定
                     map_location=device))
            # 推論、予測値の計算
            with torch.no_grad():
                y = net(x)
            # 正解ラベルを抽出
            y_arg = y.argmax()
            # tensor => numpy 型に変換
            y_arg = y_arg.detach().numpy()
            # ラベルの設定
            if y_arg == 1:
                y_label = '犬'
            else:
                y_label = '猫'
            return render(request, 'herokudjangoapp/result.html',
                          {'y_label': y_label, 'image_url': image_url})
            # 信頼度(確率で表す)
            y = net(x)
            y_proba = torch.max(y)
            y_proba = y_proba * 100
            y_proba = float(y_proba)
            return render(request, 'herokudjangoapp/result.html',
                          {'y_proba': y_proba, 'image_url': image_url})
    else:
        form = ImageForm()
        return render(request, 'herokudjangoapp/index.html',
                      {'form': form})

# ログインページ
class Login(LoginView):
    form_class = LoginForm
    template_name = 'herokudjangoapp/login.html'

# ログアウトページ
class Logout(LogoutView):
    template_name = 'herokudjangoapp/base.html'

# サインアップ
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'herokudjangoapp/signup.html', {'form': form})