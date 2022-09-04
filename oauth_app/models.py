from django.db import models
from django.contrib.auth.models import User

from datetime import datetime,timedelta
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profiles',on_delete=models.CASCADE)
    RollNumber = models.CharField(max_length=10)
    Totalfine = models.PositiveIntegerField(default=0)
    is_Faculty = models.BooleanField(default=False)
    BooksIssued = models.PositiveIntegerField(default=0)
    #user_first = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.RollNumber)

class Category(models.Model):
    categoryname = models.CharField(max_length=50)

    def __str__(self):
        return str(self.categoryname)


class Author(models.Model):
    author = models.CharField(max_length=200)
    # book = models.ForeignKey(Book, related_name='authors',on_delete=models.SET_NULL,null = True)
    #book = models.ManyToManyField(Book,related_name='authors')
    def __str__(self):
        return str(self.author)

class Book(models.Model):
    BOOK_CHOICES = (
        ('Book', 'Book'),
        ('Journal', 'Journal'),
        ('Thesis', 'Thesis'),

    )
    
    title = models.CharField(max_length=200)
    Type = models.CharField(max_length=50,choices=BOOK_CHOICES,default='Book')
    category = models.CharField(max_length=50,blank=True)
    price = models.PositiveIntegerField()
    availability = models.PositiveIntegerField()
    ISBN = models.CharField(max_length=50,default="NULL",verbose_name='ISBN/ISSN')
    image = models.URLField(max_length=1000,default = '')
    student = models.ManyToManyField(Profile,through='IssueBook',related_name='books')
    categoryaddr = models.ManyToManyField(Category,related_name="categories",verbose_name='Categories')
    authoraddr = models.ManyToManyField(Author,related_name="authors",verbose_name='Authors')
    students_interested = models.ManyToManyField(Profile,related_name="interest",blank=True)

    def __str__(self):
        return str(self.title)

class RenewDay(models.Model):
    RenewalType = models.CharField(max_length=200,default="Student")
    MaxRenewtimes = models.PositiveIntegerField(default=4)
    MaxRenewDays =  models.PositiveIntegerField(default=10)
    BooksLimit = models.PositiveIntegerField(default=4)


    def __str__(self):
        return str(self.RenewalType)
class OnlineResource(models.Model):
    BOOK_CHOICES = (
        ('Book', 'Book'),
        ('Journal', 'Journal'),
        ('Thesis', 'Thesis'),

    )
    
    title = models.CharField(max_length=200)
    Type = models.CharField(max_length=50,choices=BOOK_CHOICES,default='Book')
    # category = models.CharField(max_length=50,blank=True)
    ISBN = models.CharField(max_length=50,default="NULL",verbose_name='ISBN/ISSN')
    image = models.URLField(max_length=1000,default = '')
    Resourcelink = models.URLField(max_length=1000,default = '')
    # student = models.ManyToManyField(Profile,through='IssueBook',related_name='books')
    categoryaddr = models.ManyToManyField(Category,related_name="categoriesOnline",verbose_name='Categories')
    authoraddr = models.ManyToManyField(Author,related_name="authorsOnline",verbose_name='Authors')
    students_interested = models.ManyToManyField(Profile,related_name="interestOnline",blank=True)

    def __str__(self):
        return str(self.title)

def expiry(self):
    if(self.student_id.is_Faculty == True):
        obj = RenewDay.objects.get(RenewalType = "Faculty")
        
    else :
        obj = RenewDay.objects.get(RenewalType = "Student")
    print(obj.MaxRenewDays)
    return datetime.today() + timedelta(days=obj.MaxRenewDays)

def defaultfun():
    
    return datetime.today() + timedelta(days=10)

def defaultfun2():
    
    return datetime.today() 
ISSUED = 0
RETURNED = 1
STATUS_CHOICES = (
    (ISSUED, 'Issued'),
    (RETURNED, 'Returned'),
    )

class IssueBook(models.Model):
    
    student_id = models.ForeignKey(Profile, related_name = 'issuedbooks',on_delete=models.SET_NULL,null = True)
    issued_date = models.DateField(default= defaultfun2)
    expiry_date = models.DateField(default= defaultfun)
    return_date = models.DateField(default= defaultfun)
    book = models.ForeignKey(Book,related_name = 'issuedbooks',on_delete=models.SET_NULL,null = True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,default = ISSUED)
    times_renew = models.PositiveIntegerField(default=0)
    fine = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-issued_date',)

    def save(self,*args,**kwargs):
        
        if(self._state.adding):
            print("tt")
            issued = self.student_id.issuedbooks.filter(status = 0)
            issued_books = [i.book for i in issued]
            print(issued_books)
            if (not (self.student_id.is_Faculty)):
                obj = RenewDay.objects.get(RenewalType = "Student")
            else :
                obj = RenewDay.objects.get(RenewalType = "Faculty")
            print(self.student_id.is_Faculty,self.student_id.BooksIssued)
           
            if((not(self.book in issued_books)) and self.student_id.BooksIssued < obj.BooksLimit):
                
                if(self.book.availability>=1):
                    self.book.availability -= 1
                    self.student_id.BooksIssued += 1
                    self.student_id.save()
                    self.book.save()
                    
                    super(IssueBook, self).save(*args, **kwargs)
        else:
            
            if(self.status==RETURNED):
                #print("e")
                self.student_id.BooksIssued -= 1
                self.book.availability += 1
                self.book.save()
                self.student_id.save()
                super(IssueBook, self).save(*args, **kwargs)
            elif(self.status!=RETURNED):
                super(IssueBook, self).save(*args, **kwargs)
                

        
    def __str__(self):
        return str(self.student_id)

@receiver(post_save,sender = IssueBook)
def update_renewal_date(sender,created,instance,**kwargs):
    if created:
        instance.expiry_date = expiry(instance)
        instance.return_date = expiry(instance)
        print("post save",instance.expiry_date)
        instance.save(update_fields=['expiry_date','return_date'])

class FinePerDay(models.Model):
    Fine = models.PositiveIntegerField(default=5)

    def __str__(self):
        return str(self.Fine)
    
class Suggestion(models.Model):
    BookTitle = models.CharField(max_length=200)
    Category = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=50)

    def __str__(self):
        return str(self.BookTitle)




@receiver(user_signed_up)
def profile_create(sender=User,**kwargs):
    print("user signed up")
    username = kwargs['user'].username
    print(username)
    user =  User.objects.get(username=username)
    print(user)
    print(user.email)
    
    user_ID = user.email.split('@')[0]
    x = re.findall("^[a-zA-Z][a-zA-Z][0-9][0-9]b[0-9][0-9][0-9][0-9]$", user_ID)
    if len(x):
        is_Faculty = False
    else:
        is_Faculty = True

    # print(user_ID)
    #user_first = user.first_name
    Profile.objects.create(user=user,RollNumber=user_ID,is_Faculty=is_Faculty)
    


class Request(models.Model):
    book = models.ForeignKey(Book,related_name = 'request',on_delete=models.CASCADE,null = True)

    def __str__(self):
        return str(self.book.title)



        

