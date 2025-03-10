from django import forms
from .models import Product, Category, Shop, ProductImage, Review, Order


# class AddProdForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Название')
#     # slug = forms.SlugField()
#     price = forms.IntegerField(label='Цена')
#     count = forms.IntegerField(label='Количество')
#     description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
#     is_published = forms.BooleanField(required=False, initial=True)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
#     shop = forms.ModelChoiceField(queryset=Shop.objects.all(), empty_label='Выберите продавца', label='Продавец')
#

class AddProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'count', 'description', 'prodcategory', 'logo_image', 'category']
        labels = {
            'title': 'Название',
            'price': 'Цена',
            'count': 'Количество в наличии',
            'description': 'Описание',
            'prodcategory': 'Категория',
            'logo_image': 'Аватарка',
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 1:
            raise forms.ValidationError('Цена не может быть меньше 1 рубля')
        return price

    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 0:
            raise forms.ValidationError('Количество не может быть отрицательным')
        return count

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError('Слишком короткое название')
        return title


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = ProductImage
        fields = ('image', )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'score', 'image',]
        labels = {
            'text': 'Текст отзыва',
            'score': 'Оценка',
            'image': 'Изображение',
        }

    def clean_score(self):
        score = self.cleaned_data['score']
        if score not in [1,2,3,4,5]:
            raise forms.ValidationError('Оценка должна быть от 1 до 5')
        return score


class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'track']
        labels = {
            'status': 'Статус',
            'track': 'Трек-номер',
        }