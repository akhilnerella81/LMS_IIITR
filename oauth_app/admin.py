from django.contrib import admin

# Register your models here.
from .models import Book,IssueBook,Author,Profile,RenewDay,FinePerDay,Suggestion,Category,Request,OnlineResource
from import_export.admin import ImportExportModelAdmin,ImportExportMixin
from import_export import resources

# class AuthorInline(admin.StackedInline):
#     model = Author
#     extra = 1
#     insert_after = 'title'
admin.site.site_header = "Library Management System"
class AuthorAdmin(admin.ModelAdmin):
   search_fields=('author',)
class ProfileAdmin(admin.ModelAdmin):
    #list_display = ('title','availability')
    list_display= ('RollNumber','Totalfine')
    search_fields = ('RollNumber',)   


class categoryAdmin(admin.ModelAdmin):
    search_fields = ('categoryname',) 

class OnlineResourceAdmin(admin.ModelAdmin):
    list_display = ('title','Type')
    # inlines =[ 
    #      AuthorInline,
    # ]
    list_filter = ('Type',)
    search_fields = ('title',)
    autocomplete_fields =  ('categoryaddr','authoraddr')

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        exclude = ('id','students_interested','category','categoryaddr','image','student',)



class BookAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('title','availability','Type')
    # inlines =[ 
    #      AuthorInline,
    # ]
    list_filter = ('Type',)
    search_fields = ('title',)
    autocomplete_fields =  ('categoryaddr','authoraddr')
    resource_class = BookResource
    # change_list_template = 'admin/book/books_change_list.html'


@admin.register(Request)
class RequestAdmin(ImportExportModelAdmin):
    pass

class IssueBookResource(resources.ModelResource):
    # published = Field(attribute='student_id__RollNumber', column_name='RollNumber')
    class Meta:
        model = IssueBook
        # exclude = ('id','students_interested','category','categoryaddr','image','student',)
        fields = ('student_id__RollNumber','issued_date','expiry_date','book__title','fine','times_renew','status')
        export_order = ('student_id__RollNumber','issued_date','expiry_date','book__title','fine','times_renew','status')
class IssueBookAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('student_id','book','expiry_date','status','fine','times_renew',)
    list_filter = ['expiry_date','status']
    # search_fields = ["book"]
    search_fields = ('book__title','student_id__RollNumber',)
    # raw_id_fields = ('book',)
    autocomplete_fields =  ('student_id',"book")
    #'expiry_date',
    fieldsets = [
        (None, {'fields':['student_id','book','expiry_date','times_renew']}),
        ('Book Status',{'fields':['status','return_date']}),
    ]
    resource_class = IssueBookResource



class RenewDayAdmin(admin.ModelAdmin):
    list_display = ('RenewalType','MaxRenewDays','MaxRenewtimes')

    # def has_add_permission(self, request, obj=None):
    #     return False

class FinePerDayAdmin(admin.ModelAdmin):
    list_display = ('Fine',)

    def has_add_permission(self, request, obj=None):
        return False

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('BookTitle','Category','ISBN')


    

admin.site.register(IssueBook,IssueBookAdmin)
admin.site.register(OnlineResource,OnlineResourceAdmin)

admin.site.register(Author,AuthorAdmin)

admin.site.register(Book,BookAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(FinePerDay,FinePerDayAdmin)
admin.site.register(Category,categoryAdmin)

admin.site.register(RenewDay,RenewDayAdmin)
admin.site.register(Suggestion,SuggestionAdmin)

# admin.site.register(Request)
