import json

from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from activity.models import Action
from .models import PlantDetails, STATUS_CHOICES, Comment


# create your views here
def plant_list_search(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        loggeduser = get_object_or_404(User, username=request.session['username'])
        actions = Action.objects.all().filter(
            user=loggeduser).order_by("-created")[:10]
        plants_list = PlantDetails.objects.all().order_by('-lastUpdateOn')
        return render(request, "plant-sharing/plants/home.html", {"actions": actions, "plants_list": plants_list})
    else:
        return redirect("ps:landing_page");


def plant_add(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        if request.method == 'POST':
            # process the form
            name = request.POST.get('pname')
            description = request.POST.get('description')
            notes = request.POST.get('notes')
            plant = PlantDetails()
            verb = ""
            if request.POST.get('plantId'):
                plant = PlantDetails.objects.get(id=request.POST.get('plantId'))
                plant.status = request.POST.get('status')
                verb = "updated the plant listing"
                if name != plant.name:
                    verb += " by changing the name"
                if description != plant.description:
                    verb += " and description changed"
            else:
                plant.postedBy = request.session['username']
                verb = "created the plant listing"

            plant.name = name
            plant.description = description
            plant.notes = notes
            plant.updatedBy = request.session['username']
            plant.user = User.objects.get(username=request.session['username'])
            plant.save()

            action = Action(
                user=plant.user,
                verb=verb,
                target=plant
            )
            action.save()
            if request.POST.get('plantId'):
                messages.add_message(request, messages.INFO, "The data saved successfully for %s!" % plant.name)
                return redirect("ps:my_listings")
            else:
                messages.add_message(request, messages.SUCCESS,
                                     "The plant data added successfully for %s!" % plant.name)
                return redirect("ps:plant_details", plant.id)
        else:
            return render(request, "plant-sharing/plants/details.html")
    else:
        return redirect("ps:landing_page");


def my_messages(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        return render(request, "plant-sharing/plants/messages.html")
    else:
        return redirect("ps:landing_page");


def plant_edit(request, plant_id):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        plant = PlantDetails.objects.get(id=plant_id)
        if plant:
            json = {"plant": plant, "statuses": STATUS_CHOICES}
        return render(request, "plant-sharing/plants/details.html", json)
    else:
        return redirect("ps:landing_page")


def plant_details(request, plant_id):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        plant = PlantDetails.objects.get(id=plant_id)
        if plant:
            comments = Comment.objects.filter(plant=plant).order_by("-lastUpdateOn")
            return render(request, "plant-sharing/plants/detailed-view.html", {"plant": plant, "comments": comments})
        else:
            messages.add_message(request, messages.ERROR, "The plant details not found!")
    else:
        return redirect("ps:landing_page")


def landing_page(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        return redirect('ps:homepage')
    else:
        request.session.clear()
        return render(request, "plant-sharing/plants/landing.html")


def plant_list(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        if request.session['role'] == 'admin':
            plants_list = PlantDetails.objects.all().order_by('-lastUpdateOn')[:5]
        else:
            plants_list = PlantDetails.objects.filter(postedBy=request.session['username']).order_by('-lastUpdateOn')[
                          :5]
        return render(request, "plant-sharing/plants/list.html", {"plants_list": plants_list})
    else:
        request.session.clear()
        return render(request, "plant-sharing/plants/landing.html")


def plant_details_list(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn']:
        plants_list = PlantDetails.objects.all()
        return render(request, "plant-sharing/plants/list.html", {"plants_list": plants_list})
    else:
        request.session.clear()
        return render(request, "plant-sharing/plants/landing.html")


def global_search_results(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        return render(request, "plant-sharing/plants/search-results.html")
    else:
        request.session.clear()
        return render(request, "plant-sharing/plants/landing.html")


def plant_delete(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        plant_id = request.POST.get('plant_Id')
        try:
            obj = PlantDetails.objects.get(id=plant_id)
            action = Action(
                user=obj.user,
                verb="deleted the plant listing " + obj.name,
                target=obj
            )
            action.save()
            obj.delete()
            messages.add_message(request, messages.WARNING, "The data deleted successfully for %s!" % obj.name)
        except PlantDetails.DoesNotExist:
            messages.add_message(request, messages.WARNING, "The data deletion unsuccessful for ID %s as it doesn't "
                                                            "exist!" % plant_id)
        return redirect("ps:my_listings")
    else:
        request.session.clear()
        return render(request, "plant-sharing/plants/landing.html")


def full_list(request):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if is_ajax and request.method == "GET":
            try:
                order = "-lastUpdateOn";
                allrecords = True;
                if request.GET.get('sortBy') == 'name':
                    order = "name"
                    if request.GET.get('records') == 'less':
                        allrecords = False;

                if request.session['role'] == 'admin':
                    plants_list = PlantDetails.objects.all().order_by(order)
                else:
                    plants_list = PlantDetails.objects.filter(postedBy=request.session['username']).order_by(order)

                data = serializers.serialize('json', plants_list)
                return JsonResponse({'success': 'success', 'list': data}, status=200)
            except PlantDetails.DoesNotExist:
                messages.add_message(request, messages.ERROR, "No plants found to display!")
                return JsonResponse({'error': 'No plants found!'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Ajax request!'}, status=400)
    else:
        return render(request, "plant-sharing/plants/landing.html")


def save_details(request, plant_id):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if is_ajax and request.method == "POST":
            try:
                plant = PlantDetails.objects.get(id=plant_id)
                if request.session['role'] != 'admin':
                    if plant.postedBy != request.session['username']:
                        messages.add_message(request, messages.ERROR,
                                             "You are unauthorised to update the plant details!")
                        return JsonResponse({'error': 'You are unauthorised to update the plant details!'}, status=401)

                name = request.POST.get('plant_name')
                plant.name = name
                plant.save()
                return JsonResponse({'success': 'success', 'message': plant.name + ' name updated successfully'},
                                    status=200)
            except PlantDetails.DoesNotExist:
                messages.add_message(request, messages.ERROR, "No plant found with the ID: %s" % plant_id)
                return JsonResponse({'error': 'Invalid ID!'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Ajax request!'}, status=400)
    else:
        return render(request, "plant-sharing/plants/landing.html")


def post_comments(request, plant_id):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if is_ajax and request.method == "POST":
            comment = Comment()
            comment.commentText = request.POST.get('comment')
            comment.plant = PlantDetails.objects.get(id=plant_id)
            comment.updatedBy = request.session.get('username')
            comment.postedBy = User.objects.get(username=request.session['username'])
            comment.save()
            action = Action(
                user= get_object_or_404(User, username=request.session['username']),
                verb=" posted a new comment on the plant: ",
                target=comment.plant
            )
            action.save()
            return JsonResponse({"comment_id": comment.id, "profile_url": comment.get_user_profile(),
                                 "edit_url": comment.get_edit_url(), "delete_url": comment.get_delete_url()},
                                status=200)
        else:
            messages.add_message(request, messages.ERROR, "Could not save the comment. Please try again!")
            return JsonResponse({'error': 'Invalid Ajax request!'}, status=400)
    else:
        messages.add_message(request, messages.ERROR, "Could not save the comment. Please login and try again!")
        return redirect(request.META['HTTP_REFERER'])


def edit_comment(request, comment_id):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if is_ajax and request.method == "POST":
            comment = Comment.objects.get(id=comment_id)
            if request.session.get('username') == comment.postedBy.username or request.session.get('role') == 'admin':
                if 'comment' in request.POST and request.POST.get('comment') != '':
                    comment.commentText = request.POST.get('comment')
                comment.updatedBy = request.session.get('username')
                comment.save()
                messages.add_message(request, messages.SUCCESS, "Comment saved successfully!")
                return JsonResponse({"success": True}, status=200)
            else:
                messages.add_message(request, messages.ERROR, "Could not save the comment. Please try again!")
                return JsonResponse({'error': 'Could not update the comment as you dont have correct privileges'},
                                    status=200)
        else:
            messages.add_message(request, messages.ERROR, "Could not save the comment. Please try again!")
            return JsonResponse({'error': 'Invalid Ajax request!'}, status=400)
    else:
        messages.add_message(request, messages.ERROR, "Could not save the comment. Please login and try again!")
        return redirect(request.META['HTTP_REFERER'])


def delete_comment(request, comment_id):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if is_ajax and request.method == "POST":
            comment = Comment.objects.get(id=comment_id)
            if request.session.get('username') == comment.postedBy.username or request.session.get('role') == 'admin':
                comment.delete()
                messages.add_message(request, messages.SUCCESS, "Comment deleted successfully!")
                return JsonResponse({"success": True, "comment_id": comment_id}, status=200)
            else:
                messages.add_message(request, messages.ERROR, "Could not delete comment as you are not authorised!")
                return JsonResponse({'error': 'Could not delete comment as you are not authorised!'}, status=200)
        else:
            messages.add_message(request, messages.ERROR, "Could not delete the comment. Please try again!")
            return JsonResponse({'error': 'Invalid Ajax request!'}, status=400)
    else:
        messages.add_message(request, messages.ERROR, "Could not delete the comment. Please login and try again!")
        return redirect(request.META['HTTP_REFERER'])
