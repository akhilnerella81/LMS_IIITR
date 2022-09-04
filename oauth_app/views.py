from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book,IssueBook,Author,Profile,RenewDay,Suggestion,Request,OnlineResource
from django.urls import reverse
import datetime
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, permission_required

from django.conf import settings
from django.core.mail import send_mail
from .tasks import test_func
from .forms import SuggestionForm,BookSearchForm,TypeSearchForm
from django.views.generic.edit import CreateView

# Create your views here.
from django.views.generic import TemplateView
import datetime

def test(request):
    test_func.delay()
    return HttpResponse("done")

class LoginView(TemplateView):
    template_name = "oauth_app/index.html"

@never_cache
def home(request):
  
    if (request.user.is_authenticated) :
        Profile_Id = Profile.objects.get(user = request.user)
        print(Profile_Id.RollNumber)
        BooksIssued = Profile_Id.issuedbooks.all()
        print(request.POST)
        Profile_Id.Totalfine=0
        for Books in BooksIssued :
            Profile_Id.Totalfine += Books.fine
            # print(Books.fine)   
        Profile_Id.save(update_fields=['Totalfine'])
        # print(len(BooksIssued))
        BooksIssuedNR = Profile_Id.issuedbooks.filter(status = 0)
        BooksReturned = Profile_Id.issuedbooks.filter(status = 1)
        print(BooksIssuedNR,BooksReturned)
        return render(request,"oauth_app/books.html",{'BooksIssued':BooksIssuedNR,'BooksReturned':BooksReturned,'Profile_ID':Profile_Id})
    else:
        return render(request,"oauth_app/index.html")
        # return HttpResponse(f"<h1>Welcome to Library IIITR,Please Login")

@login_required
@never_cache
def renew_book(request,pk):
    book_instance = get_object_or_404(IssueBook, pk=pk)
    Profile_Id = Profile.objects.get(user = request.user)
    flag = int(Profile_Id.is_Faculty)
    print(flag)
    BooksIssued = book_instance.student_id.issuedbooks.all()
    Renew = RenewDay.objects.all()
    # print(Renew[0].MaxRenewDays)#student
    # print(Renew[1].MaxRenewDays)#faculty
    # flags =  int(True)
    # print(flags)
    if book_instance.times_renew == Renew[flag].MaxRenewtimes :
        messages.warning(request, "Renewal Limit Exceed " )
        subject = 'LMS - IIIT RAICHUR'
        message = f'Hi {book_instance.student_id.user.first_name}, Book from Library that you have taken "{book_instance.book.title}" has alread exceeded its limit .You have to return the book to library by  {book_instance.expiry_date}.Thank you. '
        email_from = settings.EMAIL_HOST_USER
        recipient_list =[ book_instance.student_id.user.email, ]
        send_mail( subject, message, email_from, recipient_list )
    
        return redirect ("books:homepage")
    else :
        if datetime.date.today() == book_instance.expiry_date :
            # print(Renew[0].MaxRenewDays)
            book_instance.expiry_date = book_instance.expiry_date + datetime.timedelta(days=Renew[flag].MaxRenewDays)
            book_instance.times_renew += 1
            book_instance.save(update_fields = ["expiry_date","times_renew"])
            subject = 'LMS - IIIT RAICHUR'
            message = f'Hi {book_instance.student_id.user.first_name}, Book from Library that you have taken {book_instance.book.title} is renewed.New renewal date of the book is {book_instance.expiry_date}.Thank you. '
            email_from = settings.EMAIL_HOST_USER
            recipient_list =[ book_instance.student_id.user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, "Renewed Succesfully" )
            return redirect ("books:homepage")
        elif datetime.date.today() < book_instance.expiry_date:
            messages.info(request, "You can only renew on the renew date" )
            return redirect ("books:homepage")
        else:
            messages.info(request, "Please return the book immediately." )
            return redirect ("books:homepage")


    
    # last_renewal_date = book_instance.issued_date + datetime.timedelta(days=40)
    # # print(last_renewal_date)
    # # print("aaaaaa")
    # # print(book_instance.issued_books)
    # now_renewal_date = book_instance.expiry_date + datetime.timedelta(days=10)
   
    # if (now_renewal_date > last_renewal_date):
    #     messages.warning(request, "Renewal Limit Exceed " )
    #     subject = 'LMS - IIIT RAICHUR'
    #     message = f'Hi {book_instance.student_id.user.first_name}, Book from Library that you have taken "{book_instance.book.title}" is  already renewed 4 times .You have to return the book to library by  {book_instance.expiry_date}.Thank you. '
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list =[ book_instance.student_id.user.email, ]
    #     send_mail( subject, message, email_from, recipient_list )
    
    #     return redirect ("books:homepage")

    # else:
    #     # print("ok")
    #     book_instance.expiry_date = now_renewal_date
    #     book_instance.save(update_fields = ["expiry_date"])
    #     # print("After")
    #     # print(book_instance.expiry_date)
    #     # return HttpResponseRedirect(reverse('books:homepage'))
    #     subject = 'LMS - IIIT RAICHUR'
    #     message = f'Hi {book_instance.student_id.user.first_name}, Book from Library that you have taken {book_instance.book.title} is renewed.New renewal date of the book is {book_instance.expiry_date}.Thank you. '
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list =[ book_instance.student_id.user.email, ]
    #     send_mail( subject, message, email_from, recipient_list )
    #     messages.success(request, "Renewed Succesfully" )
    #     return redirect ("books:homepage")
    #     # return render(request,"oauth_app/books.html",{'BooksIssued':BooksIssued})
@login_required
@never_cache
def avail_books(request):
    Books = Book.objects.all()
    
    form = BookSearchForm()

    return render(request,"oauth_app/availbooks.html",{'AvailableBooks':Books,'form':form})


# class SuggestionFunc(CreateView):
#     model = Suggestion
#     # form_class = PostForm
#     form_class = SuggestionForm
#     template_name = 'oauth_app\suggestions.html'


@login_required
@never_cache
def SuggestionFunc(request):
    form = SuggestionForm()
    if request.method == 'POST' :
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Submitted Succesfully" )


    context ={'form':form}
    return render(request,"oauth_app/suggestions.html",context)



def article_overview(request):
    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        articles = Book.objects.all().filter(feeder__icontains=search_term) 

    articles = Book.objects.all()

    return render(request, 'overviews/overview.html', {'articles' : articles, 'search_term': search_term })    

@login_required
@never_cache
def search_fun(request):
    # if request.method == "POST":
    # searched = request.POST['searched']
    return render(request,"oauth_app/search.html",{})
@login_required
@never_cache
def searched_fun(request):
    if request.method == 'POST':
        # if 'submit' in request.POST:
        #     print('yes')
        #     form = TypeSearchForm(request.POST)
        #     if form.is_valid():
        #     Searchtype = form.cleaned_data['Search_type']
        # print(request.POST)
        ResourceType = request.POST.get('inlineRadioresource')
        Searchedname = request.POST.get('searched_id')
        Searchedby = request.POST.get('inlineRadioOptions2')
        Selectby = request.POST.get('inlineRadioOptions')
        # form = BookSearchForm()
       
        # Searchedname = form.cleaned_data['Search_for']
        # Searchedby = form.cleaned_data['Search_by']
        # Selectby = form.cleaned_data['Select']
        data = [1, 2, 3]
        
        if (ResourceType == "Online"):
            A = OnlineResource
            flag = 0
        else :
            A = Book
            flag =1
        print(Selectby,Searchedby,Searchedname)
        if(Searchedby == 'booktitle'):
           
            items = A.objects.filter(title__contains=Searchedname , Type__contains=Selectby) 
            
            # return render(request,"oauth_app/availbooks.html",{'searched':Searchedname,'items':items,'data':data})
        elif(Searchedby == 'isbn'):
            items = A.objects.filter(ISBN__contains=Searchedname,Type__contains=Selectby) 
            
            # return render(request,"oauth_app/availbooks.html",{'searched':Searchedname,'items':items,'data':data})
        elif(Searchedby == 'author'):
            items = A.objects.filter(authoraddr__author__contains=Searchedname,Type__contains=Selectby) 
            # print(items)
            # return render(request,"oauth_app/availbooks.html",{'searched':Searchedname,'items':items,'data':data})
        else:
            items = A.objects.filter(categoryaddr__categoryname__contains=Searchedname,Type__contains=Selectby)
        print(flag)
        return render(request,"oauth_app/availbooks.html",{'searched':Searchedname,'items':items,'data':data,'ResourceType':flag})
        # form = BookSearchForm(request.POST)
        # if form.is_valid():
        #     Searchedname = form.cleaned_data['Search_for']
        #     Searchedby = form.cleaned_data['Search_by']
        #     Selectby = form.cleaned_data['Select']
        #     data = [1, 2, 3]
    
        #     print(Searchedby,Searchedname)
        #     if(Searchedby == 'booktitle'):
        #         items = Book.objects.filter(title__contains=Searchedname , Type__contains=Selectby) 
        #         return render(request,"oauth_app/availbooks.html",{'form':form,'searched':Searchedname,'items':items,'data':data})
        #     elif(Searchedby == 'isbn'):
        #         items = Book.objects.filter(ISBN__contains=Searchedname,Type__contains=Selectby) 
        #         return render(request,"oauth_app/availbooks.html",{'form':form,'searched':Searchedname,'items':items,'data':data})
        #     # elif(Searchedby == 'author'):
        #     #     items = Author.objects.filter(author__contains=Searchedname) 
        #     #     print(items)
        #     #     return render(request,"oauth_app/searchedresults.html",{'searched':Searchedname,'items':items})
        #     else:
        #         items = Book.objects.filter(categoryaddr__categoryname__contains=Searchedname,Type__contains=Selectby)
        #         return render(request,"oauth_app/availbooks.html",{'form':form,'searched':Searchedname,'items':items,'data':data})
           




    # if request.method == "POST":

    #     searched = request.POST['searched']
    #     print(searched)
    #     items = Book.objects.filter(title__contains=searched) 
    #     return render(request,"oauth_app/searchedresults.html",{'searched':searched,'items':items})

@login_required
@never_cache
def contact(request):
    
    form = BookSearchForm()
    return render(request,'oauth_app/new.html',{'form':form})

@login_required
@never_cache
def add_wishlist(request,pk):
    book_instance = get_object_or_404(Book, pk=pk)


    Profile_Id = Profile.objects.get(user = request.user)
   
    if(book_instance.availability == 0 and not(Request.objects.filter(book = book_instance)) ):
        req = Request(book = book_instance)
        req.save()

    
    if(book_instance.students_interested.filter(RollNumber=Profile_Id.RollNumber)) :
        messages.success(request, "Book already present in wishlist successfully" )

    else:
        book_instance.students_interested.add(Profile_Id)
        messages.success(request, "Added to wishlist successfully" )

        book_instance.save()
    return redirect ("books:avail_books")

    # return render(request,"oauth_app/availbooks.html",{'form':form,'searched':Searchedname,'items':items,'data':data})



@login_required
@never_cache
def see_wishlist(request):
    Profile_Id = Profile.objects.get(user = request.user)
    Wishlist = Profile_Id.interest.all()
    # print(Wishlist[0])
    # print(Wishlist[0].authoraddr.all())
    for book in Wishlist:
        book.AuthorName = book.authoraddr.all()
    return render(request,'oauth_app/wishlist.html',{'wishlist':Wishlist,'Profile':Profile_Id})

@login_required
@never_cache
def remove_from_wishlist(request,pk):
    Profile_Id = Profile.objects.get(user = request.user)
    book_instance = get_object_or_404(Book, pk=pk)

    Profile_Id.interest.remove(book_instance)
    Profile_Id.save()
    Wishlist = Profile_Id.interest.all()

    for book in Wishlist:
        book.AuthorName = book.authoraddr.all()
    return render(request,'oauth_app/wishlist.html',{'wishlist':Wishlist})



@never_cache
def guidelines(request):
    
    return render(request,'oauth_app/guidelines.html')