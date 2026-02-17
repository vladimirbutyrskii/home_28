from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product

    # app_name/<model_name>_<action>  -  правило формирования названия шаблона
    # catalog/product_list.html


# def products_list(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'catalog/products_list.html', context)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


# def products_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {'product': product}
#     return render(request, 'catalog/products_detail.html', context)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    # fields = ("name", "description", "photo", "category", "price", "created_at", "updated_at", "manufactured_at")
    success_url = reverse_lazy('catalog:products_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    # fields = ("name", "description", "photo", "category", "price", "created_at", "updated_at", "manufactured_at")
    success_url = reverse_lazy('catalog:products_list')

    def get_success_url(self):
        return reverse('catalog:products_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user  # Получаем текущего пользователя
        if user == self.object.owner:
            return ProductForm
        elif user.groups.filter(name="Модератор продуктов").exists():
            return ProductModeratorForm
        else:
            raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')

