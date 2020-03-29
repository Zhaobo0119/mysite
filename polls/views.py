from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

# Create your views here.
# 在这里创建您的视图
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# --------------------------------------------改良视图---------------------------------------------------------
# 我们在这里使用两个通用视图： ListView 和 DetailView 。这两个视图分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”这两种概念。
#
# 每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供。 DetailView 期望从 URL 中捕获名为 "pk" 的主键值，所以我们为通用视图把 question_id 改成 pk 。
# 默认情况下，通用视图 DetailView 使用一个叫做 <app name>/<model name>_detail.html 的模板。在我们的例子中，它将使用 "polls/question_detail.html" 模板。template_name 属性是用来告诉 Django
# 使用一个指定的模板名字，而不是自动生成的默认名字。 我们也为 results 列表视图指定了 template_name —— 这确保 results 视图和 detail 视图在渲染时具有不同的外观，即使它们在后台都是同一个 DetailView 。
#
# 类似地，ListView 使用一个叫做 <app name>/<model name>_list.html 的默认模板；我们使用 template_name 来告诉 ListView 使用我们创建的已经存在的 "polls/index.html" 模板。
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # 译： 成功处理POST数据后，始终返回HttpResponseRedirect。如果用户单击“后退”按钮，这将防止数据两次发布
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
