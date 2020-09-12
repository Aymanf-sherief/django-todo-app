from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from dateutil import parser
# import todo form and models

from .forms import TodoForm
from .models import TodoModel

###############################################


def index(request):

    item_list = TodoModel.objects.order_by("-date")
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo')
    form = TodoForm()

    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, 'todolist/index.html', page)

  ### function to remove item, it recive todo item id from url ##


def remove(request, item_id):
    item = TodoModel.objects.get(id=item_id)
    item.delete()
    messages.info(request, "item removed")
    return redirect('todo')


def update(request, item_id):
    print(item_id)

    if request.method == "POST":
        instance = TodoModel.objects.get(id=item_id)
        form = TodoForm(request.POST or None, instance=instance)
        new_data = form.data.copy()
        new_data['date'] = parser.parse(
            form.data['date']).strftime('%Y-%m-%d %H:%M:%S')
        form.data = new_data

        if form.is_valid():
            form.save()
            messages.info(request, "item updated")
            return redirect('todo')
    messages.warning(request, "Bad Request", )
    return redirect('todo')
