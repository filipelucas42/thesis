from arctel import models


def processor(request):
    publication_directories = models.Directory.objects.all()
    pages = models.Page.objects.live().in_menu().all()
    return {
        "publication_directories": publication_directories,
        "pages": pages,
    }
