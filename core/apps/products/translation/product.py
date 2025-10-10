from modeltranslation import translator

from core.apps.products.models import Product, Unity


@translator.register(Product)
class ProductTranslation(translator.TranslationOptions):
    fields = [
    ]


@translator.register(Unity)
class UnityTranslation(translator.TranslationOptions):
    fields = [
    ]