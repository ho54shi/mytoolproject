from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import ProjectModel, LabelModel, AnnotationModel, CustomeUser
from django.core.paginator import Paginator
from rules.contrib.views import PermissionRequiredMixin
from config.settings import BASE_DIR
import MeCab
import subprocess
import os
from mytoolapp.my_scripts import n3er_parse, ann2iob
from json import dumps
from django.http import HttpResponse
import urllib
import csv


@login_required
def indexview(request):
    return render(request, 'index.html', {})


def signupview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        expert_data = request.POST['expert_data']
        print("Expert_data: ", end='')
        print(expert_data)
        try:
            signupUser = CustomeUser.objects.create_user(
                username_data, '', password_data, expert=expert_data)

            user = authenticate(request, username=username_data,
                                password=password_data)
            login(request, user)
            return redirect('projects')
        except IntegrityError:
            return render(request, 'signup.html', {'error': "すでに登録されています．"})
    else:
        return render(request, 'signup.html', {})
    return render(request, 'signup.html', {})


def logoutview(request):
    logout(request)
    return redirect('login')


def loginview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request, username=username_data,
                            password=password_data)
        if user is not None:
            login(request, user)
            # return redirect('projects')
            print('login Success!')
            return redirect('projects')
        else:
            print('login failure')
            return redirect('login')
    return render(request, 'login.html')


@login_required
def projectsview(request):
    user_id = request.user.id
    # path = request.get_full_path
    all_flag = request.GET.get('all')
    print(all_flag)

    if all_flag == "true":
        all_project_list = ProjectModel.objects.all()
        paginator = Paginator(all_project_list, 3)  # 10 :item per a page
        p = request.GET.get('p')
        print('p:', p)
        project_list = paginator.get_page(p)
    else:
        my_project_list = ProjectModel.objects.filter(author_id=user_id)
        paginator = Paginator(my_project_list, 3)  # 10 :item per a page
        p = request.GET.get('p')
        project_list = paginator.get_page(p)
    context = {'project_list': project_list,
               'user': request.user, 'all_flag': request.GET.get('all')}
    return render(request, 'projects.html', context)


@login_required
def projectdetailview(request, pk):
    object = ProjectModel.objects.get(pk=pk)
    chopped_lines = []
    with open(object.text_file.path) as f:
        for line in f.readlines():
            if len(line) > 1:
                chopped_line = line.lstrip()
                chopped_lines.append(chopped_line)

    content = {
        'object': object,
        'text': chopped_lines,
        'project_pk': pk
    }
    return render(request, 'project_detail.html', content)


@login_required
def labelview(request, pk):
    project = ProjectModel.objects.get(pk=pk)
    print('project_id: ', end='')
    print(project.id)
    label_list = LabelModel.objects.filter(projects_id=project.id)
    print('label_list')
    print(label_list)
    for label in label_list:
        print(label.id)
    return render(request, 'label.html', {'label_list': label_list, 'project_pk': pk})


@login_required
def annsview(request):
    user_id = request.user.id
    print(user_id)
    all_anns_flag = request.GET.get('all_anns')
    print(all_anns_flag)
    if all_anns_flag == 'true':
        anns_list = AnnotationModel.objects.all()
    else:
        anns_list = AnnotationModel.objects.filter(annotator_id=user_id)
    context = {'anns_list': anns_list}
    return render(request, 'anns.html', context)


@login_required
def anndetailview(request, pk):
    data = AnnotationModel.objects.get(pk=pk)
    text = data.text
    anns = data.anns
    # script_path = os.path.dirname(os.path.abspath(__file__))
    # project_path = '/'.join(script_path.split('/')[0:-1])
    # ann_detail_path = os.path.join(project_path, 'NER/results/ann_detail.iob2')
    IOB = ann2iob.ann_detail(text, anns)
    return render(request, 'ann_detail.html', {'data': data, 'IOB': IOB})


@login_required
def labellingview(request, pk):
    project = ProjectModel.objects.get(pk=pk)
    sentence_id = request.GET.get('sentence')
    print('sentence={}'.format(sentence_id))
    # with open(project.text_file.path) as f:
    #    text = f.readlines()
    chopped_lines = []
    with open(project.text_file.path) as f:
        for line in f.readlines():
            print("line={}".format(line))
            chopped_lines.append(line)
    label_list = LabelModel.objects.filter(projects_id=project.id)
    context = {'project': project, 'text': chopped_lines,
               'label_list': label_list, 'project_pk': pk, 'pk': pk}

    return render(request, 'labelling.html', context)


class ProjectCreateClass(CreateView):
    template_name = 'projectcreate.html'
    model = ProjectModel
    fields = ('title', 'description', 'author', 'text_file')
    success_url = reverse_lazy('projects')


"""
    def form_valid(self, form):
        text_file = self.request.FILES['text_file']
        print("text_file")
        print(text_file)
        print(type(text_file))
        with open(text_file) as f:
            lines = f.readlines()
        print(lines)
        return super().form_valid(form)
"""


class ProjectUpdateClass(UpdateView):
    template_name = 'project_update.html'
    model = ProjectModel
    fields = ('title', 'description', 'text_file')
    # success_url = reverse_lazy('project_detail')

    def get_object(self):
        project_data = ProjectModel.objects.get(pk=self.kwargs['pk'])
        text_url = BASE_DIR + project_data.text_file.url
        with open(text_url) as f:
            lines = f.readline()
        print(lines)
        return project_data

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={"pk": self.kwargs["pk"]})


class ProjectDeleteClass(PermissionRequiredMixin, DeleteView):
    template_name = 'project_delete.html'
    model = ProjectModel
    fields = ('title', 'description', 'author', 'text_file')
    success_url = reverse_lazy('projects')
    permission_required = 'mytoolapp.can_delete_project'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


class LabelCreateClass(CreateView):
    template_name = 'label_create.html'
    model = LabelModel
    fields = ('name', 'keybind', 'color', 'user')
    # success_url = reverse_lazy('label')

    def get_success_url(self):
        return reverse_lazy('label', kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        projects = get_object_or_404(ProjectModel, pk=self.kwargs.get('pk'))
        form.instance.projects = projects
        return super().form_valid(form)


class LabelUpdateClass(UpdateView):
    template_name = 'label_update.html'
    model = LabelModel
    fields = ('name', 'keybind', 'color')

    def get_success_url(self):
        return reverse_lazy('label', kwargs={"pk": self.kwargs["pk"]})

    def get_object(self):
        label_data = LabelModel.objects.get(pk=self.kwargs['label_pk'])
        return label_data


class LabelDeleteClass(DeleteView):
    template_name = 'label_delete.html'
    model = LabelModel
    fields = ('name', 'keybind', 'color', 'project')
    """
    def get_from_kwargs(self):
        kwargs = {"label_pk": self.kwargs["label_pk"]}
        return kwargs
    """

    def get_success_url(self):
        return reverse_lazy('label', kwargs={"pk": self.kwargs["pk"]})

    def get_object(self):
        label_data = LabelModel.objects.get(pk=self.kwargs['label_pk'])
        return label_data

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


class AnnotationCreateClass(CreateView):
    model = AnnotationModel
    fields = ('text', 'anns', 'annotator', 'start_time', 'end_time')
    template_name = 'labelling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tmp_pk = self.kwargs['pk']
        context['pk'] = self.kwargs['pk']
        project = ProjectModel.objects.get(pk=tmp_pk)
        sentence_id_str = self.request.GET.get('sentence')
        sentence_id = int(sentence_id_str)

        chopped_lines = []
        t_lines = []
        with open(project.text_file.path) as f:
            for line in f.readlines():
                t_lines.append(line)
                if len(line) > 1:
                    chopped_line = line.lstrip()
                    chopped_lines.append(chopped_line)
        tagger = MeCab.Tagger("-Owakati")
        words = tagger.parse(chopped_lines[sentence_id]).split()
        splitted_line = " ".join(words)
        temp_file_path = "./NER/data/splitted_text.txt"
        with open(temp_file_path, mode="w") as f:
            f.write(splitted_line)

        script_path = os.path.dirname(os.path.abspath(__file__))
        # print('script_path:: {}'.format(script_path))
        project_path = '/'.join(script_path.split('/')[0:-1])
        # print('project_path:: {}'.format(project_path))
        bash_path = os.path.join(project_path, 'NER/bash/my_test.bash')
        # print("bash_path:: {}".format(bash_path))
        subprocess.run(['bash', bash_path])
        n3ered_text_path = os.path.join(project_path, 'NER/results/temp.iob2')
        with open(n3ered_text_path) as f:
            n3ered_line = f.read()

        indices, words_list, refs_list = n3er_parse.parse(
            n3ered_line)  # 関数テスト用
        words_list2, refs_list2 = n3er_parse.new_parse(n3ered_line)  # パーステスト用

        display_text = n3er_parse.display_text(n3ered_line)
        #label_list = LabelModel.objects.filter(projects_id=project.id)
        label_list = LabelModel.objects.filter(
            user__username="root")  # アンダーバーx2でリレーションキー先参照する

        context['project'] = project
        context['text'] = display_text
        context['label_list'] = label_list
        context['project_pk'] = tmp_pk

        refs_json = {}
        for ref in refs_list:
            refs_json[ref] = ref
        dataJSON = dumps(refs_json)

        send_data = {}
        for key, (index, word, ref) in enumerate(zip(indices, words_list, refs_list)):
            send_data[key] = [index, word, ref]
        send_data['text'] = words_list
        sendJSON = dumps(send_data)

        test_data = {}
        test_data['words'] = words_list2
        test_data['refs'] = refs_list2
        testjson = dumps(test_data)

        context['json_data'] = dataJSON
        context['send_data'] = sendJSON
        context['test_data'] = testjson

        # print(send_data)
        return context

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        projects = get_object_or_404(ProjectModel, pk=self.kwargs.get('pk'))
        form.instance.projects = projects

        return super().form_valid(form)


class AnnotationDeleteClass(DeleteView):
    template_name = 'anns_delete.html'
    model = AnnotationModel
    fields = ('text', 'anns')

    def get_success_url(self):
        return reverse_lazy('anns')

    def get_object(self):
        ann_data = AnnotationModel.objects.get(pk=self.kwargs['pk'])
        return ann_data

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


# test
proc = None


@login_required
def trainview(request):
    global proc

    if(request.user.is_superuser):  # root 権限のみ
        if proc is not None:
            state = "active"
            print("proc.poll: ", end="")
            print(proc.poll())
            if(proc.poll() == 0):
                state = "deactive"

        else:
            state = "deactive"
        return render(request, 'train.html', {"state": state})
    else:
        return render(request, 'cannot_train.html', {})


@login_required
def train_done_view(request):
    global proc
    ann_data = AnnotationModel.objects.all()
    script_path = os.path.dirname(os.path.abspath(__file__))
    project_path = '/'.join(script_path.split('/')[0:-1])
    train_iob_path = os.path.join(project_path, 'NER/anns/train.iob')
    recipe_iob_path = os.path.join(project_path, 'NER/data/parsed_train.iob')
    merged_iob_path = os.path.join(project_path, 'NER/anns/merged_train.iob')

    ann2iob.file_merge(train_iob_path, recipe_iob_path, merged_iob_path)
    ann2iob.train_parse(ann_data, train_iob_path)

    train_bash_path = os.path.join(project_path, 'NER/bash/my_train.bash')
    proc = subprocess.Popen(['bash', train_bash_path])

    return render(request, 'train_done.html', {})


def AnnotationExport(request):
    content = ""
    rows = []
    for ann in AnnotationModel.objects.all():
        cols = []
        cols += [str(ann.pk)]
        cols += [ann.text]
        cols += [ann.anns]
        cols += [str(ann.projects.pk)]
        cols += [ann.projects.title]
        cols += [str(ann.annotator.pk)]
        cols += [ann.annotator.username]
        cols += [str(ann.start_time)]
        cols += [str(ann.end_time)]
        rows += [";".join(cols)]

    content = "\n".join(rows)
    response = HttpResponse(content, content_type="text/text; charset=utf-8")
    filename = urllib.parse.quote((u'downloaded_anns.text').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(
        filename)

    return response
