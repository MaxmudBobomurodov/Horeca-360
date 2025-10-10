from modeltranslation import translator

from core.apps.products.models import Category


@translator.register(Category)
class CategoryTranslation(translator.TranslationOptions):
    fields = [
    ]