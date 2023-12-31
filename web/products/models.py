from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy as _ 
from core.helpers import upload_handle
from django.utils.translation import get_language

class Product(models.Model):
    '''
    商品模型
    '''
    name = models.CharField(_('Product Name'), max_length=50)
    description = models.TextField(_('Product Description'), max_length=500, null=True, blank=True)
    price = models.PositiveIntegerField(_('Product Price'), default=0)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True)
    category = models.ForeignKey(
        'products.ProductCategory', blank=True, null=True, 
        on_delete=models.RESTRICT, verbose_name=_('Product Category'), related_name='product_set'
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Product')
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'
    
class ProductCategory(models.Model):
    name = models.CharField('商品分類名稱',max_length=50)
    name_en = models.CharField('商品分類名稱(英)', max_length=50, null=True, blank=True) 
    description = models.TextField('商品分類描述',max_length=500,null=True,blank=True)
    description_en = models.TextField('商品分類描述(英)', max_length=500, null=True, blank=True) # new
    created = models.DateTimeField('建立日期',auto_now_add=True)
    modified = models.DateTimeField('修改日期',auto_now=True)
    image =models.ImageField('圖片',null=True,blank=True ,upload_to=upload_handle)

    @property
    def name_locale(self):
        language = get_language()
        if language== 'zh-hant':
            return f'{self.name}'
        elif language == 'en':
            return f'{self.name_en}'
        return f"{self.name}"

    @property
    def description_locale(self):
        language = get_language()
        if language== 'zh-hant':
            return f'{self.description}'
        elif language == 'en':
            return f'{self.description_en}'
        return f"{self.description}"
    
    class Meta:
        verbose_name='商品分類'
        verbose_name_plural='商品分類'
        ordering=['-created']    
        
    def __str__(self) -> str:
        return f'{self.name}'

class ProductImage(models.Model):
    name = models.CharField('商品圖片說明',max_length=50)
    product = models.ForeignKey('products.Product',on_delete=models.CASCADE,related_name='product_image_set')
    image = models.ImageField('圖片',null=True,blank=True,upload_to=upload_handle)
    order = models.PositiveBigIntegerField(null=True,blank=True)
    class Meta:
        verbose_name= '商品圖片'
        verbose_name_plural='商品圖片'
        ordering=['order']
    def __str__(self) -> str:
        return f'{self.name}'