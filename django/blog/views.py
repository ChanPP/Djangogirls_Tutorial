from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def post_list(request):
    # 1. 브라우저에서 요청
    # 2. 요청이 runserver로 실행중인 서버에 도착
    # 3. runserver는 요청을 Django code로 전달
    # 4. Django code중 config.urls모듈이 해당 요청을 받음
    # 5. config.urls모듈은 ''(admin/를 제외한 모든 요청)을 blog.urls모듈로 전달
    # 6. blog.urls모듈은 받은 요청의 URL과 일치하는 패턴이 있는지 검사
    # 7. 있다면 일치하는 패턴과 연결된 함수(view)를 실행
    #   7-1. settings모듈의 TEMPLATES속성 내의 DIRS목록에서
    #        blog/post_list.html파일의 내용을 가져옴
    #   7-2. 가져온 내용을 적절히 처리(렌더링, render()함수)하여 리턴
    # 8. 함수의 실행 결과(리턴값)를 브라우저로 다시 전달

    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    # HTTP프로토콜로 텍스트 데이터 응답을 반환
    # return HttpResponse('<html><body><h1>Post list</h1><p>Post목록을 보여줄 예정입니다</p></body></html>')

    # 'blog/post_list.html'템플릿 파일을 이용해 HTTP프로토콜로 응답
    return render(
        request=request,
        template_name='blog/post_list.html',
        context=context,
    )


def post_detail(request, pk):
    context = {
        'post': Post.objects.get(pk=pk),
    }
    return render(
        request,
        'blog/post_detail.html',
        context,
    )
