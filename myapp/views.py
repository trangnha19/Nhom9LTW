from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User, auth
from datetime import datetime, timedelta
from django.db.models import Sum, Max
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        title = 'Home'
        for user in User.objects.all():
            user.save()
        context = {'title': title}
        return render(request, 'pages/home.html', context)
    else:
        return redirect('login')

def login(request):
    title = 'Đăng nhập'
    form_li = SignInForm()
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user: 
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Tài khoản không hợp lệ!')
            return redirect('login')
    context = {'title': title,
               'form_li':form_li}
    return render(request, 'pages/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile_detail(request, username):
   try:
       user = User.objects.get(username=username)
   except User.DoesNotExist:
       user = None


   if user:
       if request.user.is_superuser or request.user.username == username:
           title = f'Hồ sơ {username}'
           departments = Department.objects.all()
           positions = Position.objects.filter(department=user.profile.position.department)


           context = {
               'title': title,
               'user': user,
               'positions': positions,
               'departments': departments
           }
           return render(request, 'pages/profile_detail.html', context)
       else:
           return redirect('profile-detail', username=request.user.username)
   else:
       return redirect('home')

def time_keeping(request):
    if request.user.is_authenticated:
        title = 'Check In'
        date = datetime.now().date()
        if request.POST:
            check = request.POST.get('check', '')
            if check == 'in':
                Sheet.objects.create(user=request.user,date=datetime.now().date(),checkin=datetime.now().time())
                messages.success(request, 'Check-in thành công, làm việc nào!!!')
            if check == 'out':
                sheet = Sheet.objects.filter(user=request.user, date=datetime.now().date()).order_by('-id').first()
                sheet.checkout = datetime.now().time()
                sheet.save()
                messages.success(request, 'Cảm ơn bạn đã đi làm ngày hôm nay!!!')
            return redirect('home')
        context = {'title': title, 'date': date}
        return render(request, 'pages/time_keeping.html', context)
    else:
        messages.error(request, 'Vui lòng đăng nhập')
        return redirect('login')
    
def sheet(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user and request.user.is_authenticated:
        if request.user.username == username:
            title = f'Bảng chấm công {username}'
            sheets = Sheet.objects.filter(user=user).order_by('-date')
            sheets.total_hour = sheets.aggregate(total_hour=Sum('work_hour'))['total_hour']
            sheets.count_late = sheets.filter(status='Muộn').count()
            status = request.GET.get('status', '')
            start_date = request.GET.get('start-date', '')
            end_date = request.GET.get('end-date', '')
            if status:
                sheets = sheets.filter(status=status)
            if start_date and end_date:
                sheets = sheets.filter(date__range=[start_date, end_date])
            elif start_date:
                sheets = sheets.filter(date__range=[start_date, datetime.now().date()])
            elif end_date:
                sheets = sheets.filter(date__range=[datetime.now().date(), end_date])

            paginator = Paginator(sheets, 6)
            page_number = request.GET.get('page', '')
            try:
                page_obj = paginator.get_page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            query_params = request.GET.copy()
            if 'page' in query_params:
                query_params.pop('page')
            context = {'title': title,
                       'start_date': start_date,
                       'end_date': end_date,
                       'status': status,
                       'page_obj': page_obj,
                       'query_params': query_params.urlencode()}

            return render(request, 'pages/sheet.html', context)
        else:
            messages.warning(request, 'Hãy vào tài khoản của mình để xem')
            return redirect('sheet', username=request.user.username)
    else:
        messages.error(request, 'Vui lòng đăng nhập')
        return redirect('home')

def letters(request):
    if request.user.is_authenticated:
        title = 'Hộp thư góp ý'
        my_letters = Letter.objects.filter(user=request.user)
        form = LetterForm(request.POST or None)
        if request.POST:
            if form.is_valid():
                letter = form.save(commit=False)
                letter.user = request.user
                letter.save()
                messages.success(request, 'Đã gửi đóng góp')
                return redirect('home')
        context = {'title': title, 'form': form, 'my_letters': my_letters}
        return render(request, 'pages/letters.html', context)
    else:
        return redirect('login')

def letter_detail(request, idletter):
    try:
        letter = Letter.objects.get(id=idletter)
        if request.user == letter.user or request.user.is_superuser:
            title = 'Chi tiết góp ý'
            if request.POST:
                letter.status = 'Đã xử lý'
                letter.save()
                messages.success(request, 'Đã xử lý thư góp ý')
                return redirect('main-letter')
            return render(request, 'pages/letter_detail.html', {'title': title, 'letter': letter})
        else:
            return redirect('letters')
    except Letter.DoesNotExist:
        return redirect('letters')

def request_day_off(request, username):
    try:
        title = 'Danh sách nghỉ phép'
        user = User.objects.get(username=username)
        day_off_requests = DayOffRequest.objects.filter(user=user).order_by('-start_date')
        max_end_date = day_off_requests.aggregate(max_end_date=Max('end_date'))['max_end_date'] or None
        if max_end_date:
            max_end_date += timedelta(days=1)
        form = DayOffRequestForm(request.POST or None, request.FILES or None)
        if request.POST:
            if form.is_valid():
                day_off = form.save(False)
                day_off.user = request.user
                day_off.save()
                messages.success(request, 'Gửi yêu cầu nghỉ thành công')
            return redirect('request-day-off', username=username)
        context = {'title': title,'day_off_requests': day_off_requests, 'form': form, 'max_end_date': max_end_date}
        return render(request, 'pages/request_day_off.html', context)
    except User.DoesNotExist:
        return redirect('home')