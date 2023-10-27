from django.contrib import admin
from products.models import Product, ProductCategory,ProductImage
from core.models import Setting
from django.views.generic import DetailView
# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields =('name','image','order')
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__name']
    fields =('name','description','price','category','created','modified')
    inlines =[ProductImageInline,]
    list_display = ('name', 'price', 'category')
    autocomplete_fields = ['category']
    readonly_fields = ('created','modified')
    
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name','name_en']
    fields = ('name','name_en','description','description_en','created','modified','image')
    list_display = ('name',)
    readonly_fields = ('created','modified')

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'item'
    def get_template_names(self) -> list[str]:
        setting =Setting.object.get(id='zh-hant')
        template_name = 'product/detail/template1.html'
        if setting.detail_template == "Template-1":
            template_name ="products/detail/template1.html"
        elif setting.detail_template == "Template-2":
            template_name = "products/detail/template2.html"
        return [template_name]

    
admin.site.register(Product,ProductAdmin)         # 註冊 Product 模型
admin.site.register(ProductCategory,ProductCategoryAdmin) 