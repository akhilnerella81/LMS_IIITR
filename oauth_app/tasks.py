from celery import shared_task
from .models import Book,IssueBook,Author,Profile,User,FinePerDay,RenewDay
from django.core.mail import send_mail
from lms_iiitr import settings
import datetime
from django.utils import timezone
from django.db import transaction

@shared_task(bind=True)
def test_func(self):
    with transaction.atomic():
        AllIssuedBooks = IssueBook.objects.filter(status = 0)
        Fines = FinePerDay.objects.all()
        Renew = RenewDay.objects.all()
        for book in AllIssuedBooks:
           

            if(book.expiry_date - datetime.timedelta(days=1) == datetime.date.today()):
                mail_subject = "Return the Issued Library Book IIITRAichur"
                message = f"Dear {book.student_id.user.first_name},This is a gentle reminder to return the book {book.book.title} taken  from library.If the book is not returned by tomorrow you will be fine Rs.{ Fines[0].Fine} per day.Thankyou"
                
                to_email = book.student_id.user.email
                send_mail(
                            subject = mail_subject,
                            message = message,
                            from_email = settings.EMAIL_HOST_USER,
                            recipient_list = [to_email],
                            fail_silently = True,

                        )
                
                print("return yesterday",)
            elif(book.expiry_date == datetime.date.today()):
                mail_subject = "Return the Issued Library Book IIITRaichur"
                print(book.times_renew)
                print(Renew[0].MaxRenewtimes)
                if(book.times_renew == Renew[0].MaxRenewtimes):
                    message = f"Dear {book.student_id.user.first_name},This is a gentle reminder to return the book {book.book.title} taken  from library.If the book is not returned  you will be fined Rs.{ Fines[0].Fine} per day.You can also Renew the book today ifneeded.Thankyou"
                else :
                    message = f"Dear {book.student_id.user.first_name},This is a gentle reminder to return the book {book.book.title} taken  from library.If the book is not returned today you will be fined Rs.{ Fines[0].Fine} per day.You can also Renew the book today ifneeded.Thankyou"

                to_email = book.student_id.user.email
                send_mail(
                            subject = mail_subject,
                            message = message,
                            from_email = settings.EMAIL_HOST_USER,
                            recipient_list = [to_email],
                            fail_silently = True,

                        )
                print("today")
            elif book.expiry_date < datetime.date.today() :
                print("should be fined")
                Fines = FinePerDay.objects.all()
                book.fine += Fines[0].Fine
                book.save(update_fields = ["fine"])
            

        # for i in range(10):
        #     print(i)
        return "Done"


# @app.task(name="FineCalculate", bind=True, max_retries=5)
# def FineCalculate(self,subj):
#     try:
#         AllIssuedBooks = IssueBook.objects.all()
#         for book in AllIssuedBooks:
#             if(book.expiry_date == datetime.date.today()):
#                 print("return today")
#             elif book.expiry_date < datetime.date.today() :
#                 print("should be fined")
#                 book.fine +=1
#                 book.save(update_fields = ["fine"])
#     except Exception:
#         self.retry(countdown=5)


#Send mails
# def test_func(self):
#     # IB = IssueBook.objects.all()
#     # users = []
#     # for i in IB:
#         # users[i] = IB.student_id.user.email
#     #y[0].student_id.user.email
    
#     users = User.objects.all()
#     for user in users :
#         mail_subject = "Hi!! ARE you testing"
#         message = "Do subscribe "
#         to_email = user.email
#         send_mail(
#             subject = mail_subject,
#             message = message,
#             from_email = settings.EMAIL_HOST_USER,
#             recipient_list = [to_email],
#             fail_silently = True,

#         )

#     for i in range(10):
#         print(i)
#     return "Donnne"