from django.shortcuts import render
from django.http import JsonResponse
import requests

# Create your views here.
def search(reequest, keyword):
    result = requests.post('https://www.juso.go.kr/addrlink/addrLinkApi.do', {
        'confmKey':'devU01TX0FVVEgyMDIyMDMxNDE4MTEwMjExMjM0NTE=',
        'keyword' : keyword,
        'resultType':'json',
    })

    
    return JsonResponse(result.json(), json_dumps_params={'ensure_ascii': False})
