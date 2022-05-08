import requests
from django.shortcuts import redirect

from config.settings import SOCIAL_OAUTH_CONFIG


# code 요청
def kakao_login(request):
    client_id = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
    response_type = 'code'
    url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type={2}"\
        .format(client_id, redirect_uri, response_type)
    return redirect(url)


# access token 요청
def kakao_callback(request):
    # 1 GET 방식
    """
    client_id = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
    code = request.GET.get('code')
    print("code: {}".format(code))
    url = "https://kauth.kakao.com/oauth/token?grant_type={0}&client_id={1}&redirect_uri={2}&code={3}"\
        .format("authorization_code", client_id, redirect_uri, code)
    token_request = requests.get(url)
    print("토큰 응답: {}".format(token_request))
    token_json = token_request.json()
    print("토큰 응답 json 변환: {}".format(token_json))
    """

    # 2 POST 방식
    code = request.GET.get('code')
    token_api = "https://kauth.kakao.com/oauth/token"  # 토큰 받기 api
    data = {
        'grant_type': 'authorization_code',
        'client_id': SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_url': SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': SOCIAL_OAUTH_CONFIG['KAKAO_SECRET_KEY'],
        'code': code
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    token_response = requests.post(token_api, data=data, headers=headers)
    print("토큰 응답: {}".format(token_response))
    token_json = token_response.json()
    print("토큰 응답 json 변환: {}".format(token_json))

    return 0

