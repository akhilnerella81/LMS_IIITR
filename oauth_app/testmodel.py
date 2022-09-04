from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profiles',on_delete=models.CASCADE)
    RollNumber = models.CharField(max_length=10)
    Totalfine = models.PositiveIntegerField(default=0)
    #user_first = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.RollNumber)

class Category(models.Model):
    categoryname = models.CharField(max_length=50)

    def __str__(self):
        return str(self.categoryname)


class Author(models.Model):
    author = models.CharField(max_length=200)
    book = models.ForeignKey(Book, related_name='authors',on_delete=models.SET_NULL,null = True)
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
    categoryaddr = models.ManyToManyField(Category,related_name="categories")
    authoraddr = models.ManyToManyField(Author,related_name="authors")
    students_interested = models.ManyToManyField(Profile,related_name="interest",null=True,blank=True)

    def __str__(self):
        return str(self.title)



def expiry():
    return datetime.today() + timedelta(days=10)

ISSUED = 0
RETURNED = 1
STATUS_CHOICES = (
    (ISSUED, 'Issued'),
    (RETURNED, 'Returned'),
    )

class IssueBook(models.Model):
    
    student_id = models.ForeignKey(Profile, related_name = 'issuedbooks',on_delete=models.SET_NULL,null = True)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    book = models.ForeignKey(Book,related_name = 'issuedbooks',on_delete=models.SET_NULL,null = True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,default = ISSUED)
    times_renew = models.PositiveIntegerField(default=0)
    fine = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-issued_date',)

    def save(self,*args,**kwargs):
        if(self._state.adding):
            print("tt")
            issued = self.student_id.issuedbooks.all()
            issued_books = [i.book for i in issued]
            if(not(self.book in issued_books)):
                print("ff")
                if(self.book.availability>=1):
                    print("kk")
                    self.book.availability -= 1
                    self.book.save()
                    super(IssueBook, self).save(*args, **kwargs)
        #Issue1[0].student_id.user.profiles.books.all()
        else:
            #print("d")
            if(self.status==RETURNED):
                #print("e")
                self.book.availability += 1
                super(IssueBook, self).save(*args, **kwargs)
            elif(self.status!=RETURNED):
                super(IssueBook, self).save(*args, **kwargs)
                

        
    def __str__(self):
        return str(self.student_id)

class RenewDay(models.Model):
    MaxRenewtimes = models.PositiveIntegerField(default=4)
    MaxRenewDays =  models.PositiveIntegerField(default=10)


    def __str__(self):
        return str(self.MaxRenewtimes)

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
    # course_qs = <whatever query gave you the queryset>
    # for e in user.objects.all():
    #     print(e.headline)
    user_ID = user.email.split('@')[0]
    # print(user_ID)
    #user_first = user.first_name
    Profile.objects.create(user=user,RollNumber=user_ID)
    


class Request(models.Model):
    book = models.ForeignKey(Book,related_name = 'request',on_delete=models.CASCADE,null = True)

    def __str__(self):
        return str(self.book.title)



        

