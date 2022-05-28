from datetime import datetime, date

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import translation
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import arctel.models as models


def index(request):
    news = models.New.objects.order_by("-date")[:4]
    context = {"news": news}
    return render(request, "arctel/index.html", context)



class CustomView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CustomView, self).dispatch(*args, **kwargs)


class BaseView(View):

    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get("__method", "").lower()
        if method == "delete":
            return self.delete(*args, **kwargs)
        if method == "put":
            return self.put(*args, **kwargs)
        return super(BaseView, self).dispatch(*args, **kwargs)

class BackOffice(BaseView):
    def get(self, req):
        if not req.user.is_authenticated:
            return redirect("login")

    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")


class Login(BaseView):
    def get(self, req):
        if not req.user.is_authenticated:
            return render(req, "arctel/login.html")
        else:
            redirect("backoffice")

    def delete(self, req):
        logout(req)
        return redirect("index")


@method_decorator(login_required, name="dispatch")
class BackOfficeNews(BaseView):
    def get(self, req):
        news = models.New.objects.all().order_by("-date")
        paginator = Paginator(news, 10)
        page_number = req.GET.get("page", 1)
        news = paginator.get_page(page_number)
        context = {"news": news, "page_numbers": range(1, paginator.num_pages + 1)}
        return render(req, "arctel/backoffice/news.html", context)

    def post(self, req):
        new = models.New()
        new.save()

        return redirect("backoffice-news-by-id", new.pk)


@method_decorator(login_required, name="dispatch")
class BackOfficeNewsByID(BaseView):
    def get(self, req, id):
        new = models.New.objects.get(pk=id)
        context = {}
        context["new"] = new
        return render(req, "arctel/backoffice/news-edit.html", context)

    def post(self, req, id):
        new = models.New.objects.get(pk=id)
        new.date = req.POST.get("date", datetime.now().strftime("%Y-%m-%d"))
        new.title = req.POST.get("title", "")
        new.text = req.POST.get("text", "")
        new.description = req.POST.get("description", "")
        file = req.FILES.get("image", "")
        if file:
            fs = FileSystemStorage()
            if new.image:
                fs.delete(new.image)
            file_name = fs.save(file.name, file)
            new.image = file_name
        new.save()
        return redirect("backoffice-news-by-id", id)

    def delete(self, req, id):
        new = models.New.objects.get(pk=id)
        new.delete()

        return redirect("backoffice-news")


def backoffice_news_create(req):
    return render(req, "arctel/backoffice/news-create.html")


def news(req):
    dates = models.New.objects.dates("date", "year", order="DESC")
    years = []
    for date in dates:
        years.append(int(date.year))
    return redirect("news-by-year", years[0])


def news_delete(req, id):
    models.New.objects.get(pk=id).delete()
    return redirect("backoffice-news")


def news_by_year(req, year):
    dates = models.New.objects.dates("date", "year", order="DESC")
    years = []
    for date in dates:
        years.append(int(date.year))
    news = models.New.objects.order_by("-date").filter(date__year=year)
    paginator = Paginator(news, 9)
    page_number = req.GET.get("page", 1)
    news = paginator.get_page(page_number)

    context = {}
    context["years"] = years
    context["news"] = news
    context["selected_year"] = int(year)
    context["paginator"] = paginator
    return render(req, "arctel/news.html", context=context)


def news_by_id(req, id):
    new = models.New.objects.get(pk=id)

    context = {}
    context["new"] = new
    return render(req, "arctel/new.html", context=context)


@method_decorator(login_required, name="dispatch")
class PublicationDirectories(BaseView):
    def get(self, req, directory_id):
        page_number = req.GET.get("page", 1)
        publications = Paginator(
            models.Publication.objects.filter(directory=directory_id)
                .all()
                .order_by("-order", "-pk"),
            10,
        ).get_page(page_number)
        context = {"publications": publications, "directory": models.Directory.objects.get(pk=directory_id)}
        return render(req, "arctel/backoffice/publications.html", context)

    def post(self, req, id):
        new = models.New.objects.get(pk=id)
        new.date = req.POST.get("date", datetime.now().strftime("%Y-%m-%d"))
        new.title = req.POST.get("title", "")
        new.text = req.POST.get("text", "")
        new.description = req.POST.get("description", "")
        file = req.FILES.get("image", "")
        if file:
            fs = FileSystemStorage()
            if new.image:
                fs.delete(new.image)
            file_name = fs.save(file.name, file)
            new.image = file_name
        new.save()
        return redirect("backoffice-news-by-id", id)


@method_decorator(login_required, name="dispatch")
class PublicationByID(BaseView):

    def get(self, req, publication_id):
        publication = get_object_or_404(models.Publication, pk=publication_id)
        context = {"publication": publication}
        return render(req, "arctel/backoffice/publication-edit.html", context)

    def delete(self, req, publication_id):
        print("test")
        models.Publication.objects.get(pk=publication_id).delete()
        return redirect(req.META.get("HTTP_REFERER"))


@method_decorator(login_required, name="dispatch")
class Publication(BaseView):
    def get(self, req):
        directory = int(req.GET.get("directory"))
        context = {
            'directory': models.Directory.objects.get(pk=directory)
        }
        print(context['directory'].name)
        return render(req, "arctel/backoffice/publication-edit.html", context)

    def post(self, req):
        publication_id = req.POST.get("publication_id")
        if not publication_id:
            publication = models.Publication()
        else:
            publication = models.Publication.objects.get(pk=publication_id)
        directory_id = req.POST.get("directory_id")
        publication.directory = models.Directory.objects.get(pk=directory_id)
        publication.title = req.POST.get("title", "")
        file = req.FILES.get("file", "")
        image = req.FILES.get("image", "")
        if file:
            fs = FileSystemStorage()
            if publication.file:
                fs.delete(publication.file)
            file_name = fs.save(file.name, file)
            publication.file = file_name

        if image:
            fs = FileSystemStorage()
            if publication.image:
                fs.delete(publication.image)
            image_name = fs.save(image.name, image)
            publication.image = image_name
        publication.save()
        return redirect("backoffice-publication-by-id", publication.pk)


def publication_delete(req, publication_id):
    models.Publication.objects.get(pk=publication_id).delete()
    return redirect(req.META.get("HTTP_REFERER"))
    # return redirect("backoffice-news")


@method_decorator(login_required, name="dispatch")
class PublicationNew(BaseView):
    def get(self, req):
        return render(req, "arctel/backoffice/publication-edit.html")


def publications_view(req):
    sector_publications = models.Publication.objects.filter(directory__identifier='publications-sector').order_by(
        '-order', '-pk').all()
    communications_anuary = models.Publication.objects.filter(directory__identifier='publications-directory').order_by(
        '-order', '-pk').all()
    context = {
        'sector_publications': sector_publications,
        'communications_anuary': communications_anuary
    }
    return render(req, "arctel/publications.html", context)


def activities_view(req):
    context = {
        'activities_plans': models.Publication.objects.filter(directory__identifier='activities-plan').order_by(
            '-order', "-pk").all(),
        'activities_reports': models.Publication.objects.filter(directory__identifier='activity-reports').order_by(
            '-order', "-pk").all(),
        'reports': models.Publication.objects.filter(directory__identifier='reports').order_by('-order', "-pk").all(),
    }
    return render(req, 'arctel/activities.html', context)


@method_decorator(login_required, name="dispatch")
class Publication(BaseView):
    def get(self, req):
        directory = int(req.GET.get("directory"))
        context = {
            'directory': models.Directory.objects.get(pk=directory)
        }
        print(context['directory'].name)
        return render(req, "arctel/backoffice/publication-edit.html", context)

    def post(self, req):
        publication_id = req.POST.get("publication_id")
        if not publication_id:
            publication = models.Publication()
        else:
            publication = models.Publication.objects.get(pk=publication_id)
        directory_id = req.POST.get("directory_id")
        publication.directory = models.Directory.objects.get(pk=directory_id)
        publication.title = req.POST.get("title", "")
        file = req.FILES.get("file", "")
        image = req.FILES.get("image", "")
        if file:
            fs = FileSystemStorage()
            if publication.file:
                fs.delete(publication.file)
            file_name = fs.save(file.name, file)
            publication.file = file_name

        if image:
            fs = FileSystemStorage()
            if publication.image:
                fs.delete(publication.image)
            image_name = fs.save(image.name, image)
            publication.image = image_name
        publication.save()
        return redirect("backoffice-publication-by-id", publication.pk)


@method_decorator(login_required, name="dispatch")
class FormationOfferList(BaseView):
    def get(self, req):
        formation_offers = models.FormationOffer.objects.all().order_by("-end_date")
        paginator = Paginator(formation_offers, 10)
        page_number = req.GET.get("page", 1)
        formation_offers = paginator.get_page(page_number)
        context = {"formation_offers": formation_offers, "page_numbers": range(1, paginator.num_pages + 1)}
        return render(req, "arctel/backoffice/formation_offers.html", context)

    def post(self, req):
        formation_offer = models.FormationOffer()
        formation_offer.start_date = req.POST.get("start_date")
        formation_offer.end_date = req.POST.get("end_date")
        formation_offer.title = req.POST.get("title")
        formation_offer.description = req.POST.get("description")
        formation_offer.save()

        return redirect("backoffice-formation-offer-list")


@method_decorator(login_required, name="dispatch")
class FormationOffer(BaseView):
    def get(self, req, id):
        formation_offer = models.FormationOffer.objects.get(id=id)
        context = {
            "formation_offer": formation_offer
        }
        return render(req, "arctel/backoffice/formation_offer_edit.html", context)

    def post(self, req):
        formation_offer = models.FormationOffer()
        formation_offer.start_date = req.POST.get("start_date")
        formation_offer.end_date = req.POST.get("end_date")
        formation_offer.title = req.POST.get("title")
        formation_offer.description = req.POST.get("description")
        formation_offer.save()

        return redirect("backoffice-formation-offer-list")

    def put(self, req, id):
        print("test")
        formation_offer = models.FormationOffer.objects.get(pk=id)
        formation_offer.start_date = req.POST.get("start_date")
        formation_offer.end_date = req.POST.get("end_date")
        formation_offer.title = req.POST.get("title")
        formation_offer.description = req.POST.get("description")
        formation_offer.save()
        return redirect("backoffice-formation-offer", formation_offer.id)


def newsletter_view(req):
    publications = models.Publication.objects.all(directory__identifier='')
    context = {
        'publications': publications
    }
    return render(req, 'arctel/newsletter.html', context)


def publication_order(req, publication_id):
    publication = models.Publication.objects.get(pk=publication_id)
    new_order = int(req.POST.get("order"))
    if new_order:
        publication.order = new_order
        publication.save()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))


def formation_offer(req):
    today = date.today()

    formation_offers = models.FormationOffer.objects.filter(end_date__lte=today)
    context = {
        "formation_offers": formation_offers
    }
    return render(req, "arctel/formation_offer_list.html", context)


def cms_news(req):
    news = models.News.objects.live().all()
    context = {}
    context["news"] = news

    return render(req, "arctel/cms-news.html", context=context)

def cms_news_by_id(req, id):
    new = models.BlogPage.objects.get(pk=id)
    context = {}
    context["new"] = new
    return render(req, "arctel/cms-news.html", context=context)