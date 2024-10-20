from .models import Category

def categories(request):
    categories = list(Category.objects.all().order_by('category_name'))
    categories.append({'category_name': 'Recientes', 'slug': 'recientes'})

    return {'categories': categories}