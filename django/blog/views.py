from django.http import HttpResponse
from django.shortcuts import render, redirect
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
    # posts = Post.objects.order_by('-created_date')

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

def post_edit(request, pk):
    """
    pk에 해당하는 Post인스턴스를
    context라는 dict에 'post'키에 할당
    위에서 생성한 dict는 render의 context에 전달
    사용하는 템플릿은 'blog/post_add.html'을 재사용
    url은 /3/edit/ 에 매칭되도록 urls.py작성
    이 위치로 올 수 있는 a요소를 post_detail.html에 작성
    """


def post_add(request):
    # localhost:8000/add로 접근시
    # 이 뷰가 실행되어서 Post add page라는 문구를 보여주도록 urls작성
    # HttpResponse가 아니라 blog/post_add.html을 출력
    # post_add.html은 base.html을 확장, title(h2)부분에 'Post add'라고 출력
    if request.method == 'POST':
        # 요청의 method가 post일때
        title = request.POST['title']
        content = request.POST['content']
        # ORM을 사용해서 title과 content에 해당하는 Post생성
        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
        )
        return redirect('post-detail', pk=post.pk)
        # return HttpResponse(f'{post.pk}, {posttitle}, {post.content}')
    else:
        # 요청의 method가 get일때
        return render(request, 'blog/post_add.html')


def post_delete(request, pk):
    """
    post_detail의 구조를 참고해서
    pk에 해당하는 post를 삭제하는 view를 구현하고 url과 연결
    pk가 3이면 url은 "3/delete/"
    이 view는 POST메서드에 대해서만 처리한다 (request.method == 'POST')

    삭제코드
    post = POST.objects.get(pk=pk)
    post.delete()
    """

    if request.method == 'POST' :
        post = Post.objects.get(pk=pk)
        if request.user == post.author:
            post.delete()
            return redirect('post-list')
        else:
            return redirect('post-list', pk=post.pk)