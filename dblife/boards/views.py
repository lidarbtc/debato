from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from accounts.models import User
from django.core.paginator import Paginator
from tag.models import Tag

def board_write(request):
    if not request.session.get('user'):
        return redirect('/accounts/login')

    if request.method =='POST': 
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user = User.objects.get(pk=user_id)
            tags = form.cleaned_data['tags'].split(',')

            board=Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user
            board.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, _ = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)
            
            
            return redirect('/boards/list')
    else:
        form = BoardForm()
    return render(request, 'board_write.html', {'form':form})

def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comments = CommentForm()
    comment_view = Comment.objects.filter(post=pk)
    return render(request, 'board_detail.html',{'board':board, 'comments':comments, 'comment_view':comment_view})

def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 5)
    boards = paginator.get_page(page)

    return render(request, 'board_list.html', {'boards':boards})

def comment_write(request, board_id):
    comment_write = CommentForm(request.POST)
    user_id = request.session['user']
    user = User.objects.get(pk=user_id)
    if comment_write.is_valid():
        comments = comment_write.save(commit=False)
        comments.post = get_object_or_404(Board, pk=board_id)
        comments.author = user
        comments.save()
    return redirect('board_detail', board_id)