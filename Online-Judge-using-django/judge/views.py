from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import problem,solution
from .our_forms import code_form, problem_form, testcase_form
from .code_validation1 import check_code

def display_problems(request):
    context={
        'probs': problem.objects.all()
    }
    return render (request, 'problem_page.html',context)


def problem_detail(request, prob_id):
    obj=get_object_or_404(problem, id = prob_id)
    if request.method == 'POST':
        form=code_form(request.POST)
        if(form.is_valid()):
            sub=form.save()
            sub.curr_problem=obj
            sub.save()
            check_code(sub)
        return redirect('past_submissions',prob_id)
    else:
        form=code_form()
        context = {
            'data': problem.objects.get(id=prob_id),
            'form': form,
        }
        # print(form.is_valid())
        # print(problem.objects.get(id=prob_id).name)
        # print(form.errors.as_data)
        template='detail_problem.html'
        return  render (request, template, context)

@staff_member_required
def add_problem(request):
    if(request.method=='POST'):
        form=problem_form(request.POST)
        if(form.is_valid()):
            sub=form.save()
        return redirect ('add_testcase',sub.id)
    else:
        form=problem_form()
        context= {
            'form': form
        }
        template='add_prob.html'
        return render(request,template,context)

@staff_member_required
def add_testcase(request,prob_id):
    if(request.method=='POST'):
        obj=get_object_or_404(problem, id = prob_id)
        form=testcase_form(request.POST)
        if(form.is_valid()):
            sub=form.save()
            sub.curr_problem=obj
            sub.save()
        return redirect('problem_page')
    else:
        form=testcase_form()
        context= {
            'form': form
        }
        template = 'add_test.html'
        return render(request,template,context)

@staff_member_required
def del_prob(request, prob_id):
    obj=problem.objects.get(id=prob_id)
    obj.delete()
    return redirect('problem_page')


def submit(request,prob_id):
    obj=problem.objects.get(id=prob_id)
    qs=solution.objects.filter(curr_problem=obj)
    if(len(qs)==0):
        template='no_submission.html'
        return render(request,template)
    context= {
        'qs': qs
    }
    template='submission.html'
    return render(request,template,context)

def show_code(request,prob_id,submission_id):
    obj=solution.objects.get(id=submission_id)
    context= {
        'obj': obj
    }
    template='display_code.html'
    return render(request,template,context)



# def problem_detail(request, prob_id):
#     context = {
#         'data': problem.objects.get(id=prob_id),
#     }
#     template='temporary.html'
#     return render (request, template, context)
