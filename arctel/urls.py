from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("backoffice/", views.BackOffice.as_view(), name="backoffice"),
    path("login/", views.Login.as_view(), name="login"),
    path(
        "backoffice/noticias/",
        login_required(views.BackOfficeNews.as_view()),
        name="backoffice-news",
    ),
    path(
        "backoffice/noticias/<id>",
        login_required(views.BackOfficeNewsByID.as_view()),
        name="backoffice-news-by-id",
    ),
    path(
        "backoffice/noticias/<id>/apagar",
        login_required(views.news_delete),
        name="backoffice-news-delete",
    ),
    path(
        "backoffice/noticias/criar/",
        login_required(views.backoffice_news_create),
        name="backoffice-news-create",
    ),
    path(
        "backoffice/publicacoes/diretorio/<int:directory_id>/",
        views.PublicationDirectories.as_view(),
        name="publication-directories",
    ),
    path(
        "backoffice/publicacao/",
        views.Publication.as_view(),
        name="backoffice-publication",
    ),
    path(
        "backoffice/publicacao/<int:publication_id>/",
        views.PublicationByID.as_view(),
        name="backoffice-publication-by-id",
    ),
    path(
        "backoffice/publicacao/<int:publication_id>/order/",
        login_required(views.publication_order),
        name="backoffice-publication-order",
    ),
    path(
        "backoffice/publicacao/editar/",
        login_required(views.Publication.as_view()),
        name="backoffice-publication-edit",
    ),
    path(
        "backoffice/formacao/",
        login_required(views.FormationOfferList.as_view()),
        name="backoffice-formation-offer-list",
    ),
    path(
        "backoffice/formacao/criar/",
        login_required(TemplateView.as_view(template_name="arctel/backoffice/formation_offer_create.html")),
        name="formation-offer-create",
    ),
    path(
        "backoffice/formacao/<int:id>/",
        login_required(views.FormationOffer.as_view()),
        name="backoffice-formation-offer",
    ),
    path("noticias/", views.news, name="news"),
    path("noticias/<int:id>/", views.news_by_id, name="news-by-id"),
    path("noticias/ano/<int:year>/", views.news_by_year, name="news-by-year"),
    path(
        "sobre-nos/historia/",
        TemplateView.as_view(template_name="arctel/history.html"),
        name="history",
    ),
    path(
        "sobre-nos/reunioes/",
        TemplateView.as_view(template_name="arctel/meetings.html"),
        name="meetings",
    ),
    path(
        "sobre-nos/estatutos/",
        TemplateView.as_view(template_name="arctel/status.html"),
        name="status",
    ),
    path(
        "sobre-nos/estrutura/",
        TemplateView.as_view(template_name="arctel/structure.html"),
        name="structure",
    ),
    path(
        "sobre-nos/protocolos/",
        TemplateView.as_view(template_name="arctel/protocols.html"),
        name="protocols",
    ),
    path(
        "atividades/",
        views.activities_view,
        name="activities",
    ),
    path(
        "publicacoes/",
        views.publications_view,
        name="publications",
    ),
    path(
        "newsletter/",
        views.newsletter_view,
        name="newsletter",
    ),
    path(
        "centro-formacao/",
        views.formation_offer,
        name="formation-center",
    ),
    path(
        "cms-news/",
        views.cms_news,
        name="cms-news",
    ),
    path(
        "cms-news/<int:id>/",
        views.cms_news_by_id,
        name="cms-new-by-id",
    ),
]