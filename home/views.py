from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home.models import Post,BlogComment
from django.contrib import messages
from django.utils.timezone import now
from home.templatetags import extras





# HTML Pages
def index(request):
    context = {
        "variable1":"Harry is great",
        "variable2":"Rohan is great"
    } 
    return render(request, 'index.html', context)
    # return HttpResponse("this is homepage")

def about(request):
    return render(request, 'about.html') 

def blog(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, "blog.html", context)

   
def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    context={"post":post}
    return render(request, "blogPost.html", context)


# Search Function
def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'search.html', params)
 

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')

#SignUp Modal Authentication

def handlesignup(request):
    if request.method == "POST":
        # Get the post parameter
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Check for errorneous inputs
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters!')
            return redirect('home')

        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers!')
            return redirect('home')


        if pass1 != pass2:
            messages.error(request, 'Password do not match!')
            return redirect('home')
    

        #Creat The User
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        
        messages.success(request, 'Your BlogCorner account has been successfully created!')
        return redirect('home')
    else:
        return HttpResponse('401 - Not Found')

# Login modal Authentication
def handlelogin(request):

    if request.method == "POST":
        # Get the post parameter
        loginusername = request.POST.get('loginusername')
        loginpass = request.POST.get('loginpass')
        user = authenticate(username=loginusername, password= loginpass)

        if user is not None:
            login(request,user)
            messages.success(request, 'successfully logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials, Please try again')
            return redirect('home')

    return HttpResponse('404 - Not found')

# Logout Authentication

def handlelogout(request):
        logout(request)
        messages.success(request, 'successfully logged Out')
        
        return redirect('home')

# BlogPost
def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    post.views= post.views +1
    post.save()
    
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blogPost.html", context)

# PostComment
def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/{post.slug}")