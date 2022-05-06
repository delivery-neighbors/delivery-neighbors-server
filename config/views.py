from django.shortcuts import redirect
from config.settings import SOCIAL_OAUTH_CONFIG


# code 요청
def kakao_login(request):
    client_id = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
    redirect_url = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type=code"\
        .format(client_id, redirect_url)
    return redirect(url)


# access token 요청
def kakao_callback(request):
    return "0"


