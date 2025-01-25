import random
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from markdown import Markdown

from . import util

markdowner = Markdown()

class NewSearchForm(forms.Form):
    query = forms.CharField(label="New Query")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Title")
    data = forms.CharField(label = "New Entry", widget=forms.Textarea(attrs={'rows':4,'cols':50}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm
    })

def markdown_to_html(md_title):
    entry = util.get_entry(md_title)
    if entry == None:
        return None
    else:
        return markdowner.convert(entry)

    
def entryPage(request, title):
    content = markdown_to_html(title)
    if content != None:
        exists = 1
        return render(request, "encyclopedia/results.html", {
            "title": title,
            "exists": exists,
            "data": markdown_to_html(title)
        })
    else:
        exists = 0
        return render(request, "encyclopedia/results.html", {
            "exists": exists
        }) 
        
def search(request):
    form = NewSearchForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data["query"]
            data = markdown_to_html(name)
            if (data != None):
                return render(request, "encyclopedia/results.html", {
                    "title": name,
                    "data": data
                })
            else:
                name = form.cleaned_data["query"]
                substrings = []
                entries = util.list_entries()
                for entry in entries:
                    if name.lower() in entry.lower():
                        substrings.append(entry)
                return render(request, "encyclopedia/matching.html",{
                    "substrings": substrings
                })

def create_entry(request):
    form = NewEntryForm(request.POST)
    if request.method == "GET":
        return render(request, "encyclopedia/add.html", {
            "entryForm": NewEntryForm
        })
    elif request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['title']
            data = form.cleaned_data['data']
            entry_exists = util.get_entry(title)
            if entry_exists != None:
                exists = 2
                return render(request, "encyclopedia/results.html", {
                    "title": title,
                    "exists": exists
                })
            else:
                exists = 1
                util.save_entry(title, data)
                return render(request, "encyclopedia/results.html", {
                    "exists": exists,
                    "title": title,
                    "data": markdown_to_html(title)
                })
        
def edit_entry(request, entry_title):
    form = NewEntryForm(request.POST)
    if request.method == "GET":
        initialForm = NewEntryForm({'title':entry_title, 'data':util.get_entry(entry_title)})
        return render(request, "encyclopedia/edit.html", {
            "title": entry_title,
            "entryForm": initialForm   
        })
    elif request.method == 'POST':
        if form.is_valid():
            entry_title = form.cleaned_data['title']
            data = form.cleaned_data['data']
            util.save_entry(entry_title, data)
            return render(request, "encyclopedia/results.html", {
                "title": entry_title,
                "data": markdown_to_html(entry_title)
            })
    
def random_entry(request):
    entries = util.list_entries()
    random_choice = random.choice(entries)
    return render(request, "encyclopedia/results.html", {
        "title": random_choice,
        "data": markdown_to_html(random_choice)
    })