from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.lookups import IsNull
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User, listing, watchlist,Bid,Comment
import datetime
from django.db.models import OuterRef,Subquery
#from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
     

def index(request):  
    activelist = listing.objects.all()      
    return render(request, "auctions/index.html",{"auctions":activelist})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request, "auctions/categories.html")

#@login_required(login_url='/login')
def activelist(request):
   # user = User
  #  activelist = listing.objects.get(id=listing_id)
    context ={}
    context["data"]=listing.objects.filter(closed=False)

    return render(request, "auctions/activelist.html",context)
  
def category(request,catag):
    product=listing.objects.filter(category=catag)
    return render(request,"auctions/category.html",{"product":product,"catag":catag})   

def createauction(request):
    if request.method == "POST":
        new_list = listing()
        new_list.user = User.objects.get(username=request.user) 
        new_list.title = request.POST["title"]
        new_list.description = request.POST["description"]
        new_list.price = request.POST["price"]
        new_list.category = request.POST["category"]
        new_list.closed = False
       
        if request.POST.get('url'):
          new_list.image = request.POST["url"]
        else:
          new_list.image = "no image found"

        new_list.save()

        return HttpResponseRedirect(reverse("index"))
    
    return render(request,"auctions/createauction.html")   

@login_required(login_url='/login')
def viewlist(request,listing_id):
    
    #comment = Comment.objects.filter(list_id = listing_id)
    view_list = listing.objects.get(id=listing_id)
    if request.method == "POST":
        havebid = int(request.POST.get('havebid'))

        if view_list.price >= havebid:

          return render(request,"auctions/viewlist.html",{
            "iteam":view_list,
            "message":"BID should be Higher!"
           #"comment": comment 
          })
        else:
            view_list.price=havebid
            view_list.save()

            new_bid = Bid.objects.filter(list_id = listing_id) 
            if new_bid:
                new_bid.delete()
            new=Bid()
            new.user = request.user.username 
            new.title = view_list.title
            new.list_id = listing_id
            new.bid = havebid
            new.save()
            return render(request,"auctions/viewlist.html",{
            "iteam":view_list,
            "message": "BID Added",
            #"watchlist":
            #"comment":comment
            })

    else:
         view_list = listing.objects.get(id=listing_id)
         listadd = watchlist.objects.filter(list_id=listing_id,user=request.user.username)
         return render(request,"auctions/viewlist.html",{
             "iteam":view_list,
             "addlist":listadd 
             #"comment":comment
         })          

@login_required(login_url='/login') 
def addwatchlist(request,listing_id):
    
    #listadd = watchlist.objects.filter(list_id=listing_id,user=request.user.username)
    listadd = watchlist() 
    listadd.user = request.user.username    
    listadd.list_id = listing_id
    listadd.save()
      
    view_list = listing.objects.get(id=listing_id)
    listadd = watchlist.objects.filter(list_id=listing_id,user=request.user.username)
    
    return render(request,"auctions/viewlist.html",{
        "iteam":view_list,
        "addlist":listadd,
      })

@login_required(login_url='/login') 
def dltwatchlist(request,listing_id):
     
    listadd = watchlist.objects.filter(list_id=listing_id,user=request.user.username)     
    listadd.delete()
    #list = listing.objects.get(id=listing_id)
   # listadd = watchlist.objects.filter(list_id=listing_id,user=request.user.username)
    
    return redirect("viewlist", listing_id)


@login_required(login_url='/login') 
def viewwatchlist(request):
    data_subquery = watchlist.objects.filter(list_id = OuterRef("pk")) 
    data = listing.objects.annotate(watch_user = Subquery(data_subquery.values("user")[:1])).exclude(watch_user__isnull = True)
    return render( request,"auctions/viewwatchlist.html",{
        "data":data
    })

@login_required(login_url='/login') 
def comment(request,listing_id):
    view_list = listing.objects.get(id=listing_id)
    if request.method == "POST":
        comm = Comment()
        comm.comment = request.POST.get('comment') 
        comm.user=request.user.username
        comm.list_id=listing_id
        comm.save()

        comments=Comment.objects.filter(list_id=listing_id,user=request.user.username).values_list("comment",flat=True)    
   
    return render(request,"auctions/viewlist.html",{
       "iteam":view_list,
       "comments":comments
    })            

def closeauction(request,listing_id):
    view_list = listing.objects.get(id=listing_id)
    bid = Bid.objects.filter(list_id = listing_id).order_by("-bid")[0:1]
    
    # if request.user == view_list.user:
    view_list.closed = True
    view_list.winner = bid[0].user
    view_list.save()    
    
    print(request.user) 
   
    return render(request,"auctions/viewlist.html",{
       "iteam":view_list,
       "list_status":"Closed",
     #  "bid":bid
    })