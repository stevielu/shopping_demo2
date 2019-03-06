"""shopping_demo2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url,include
from django.views.static import serve
from shopping_demo2.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from goods.views import GoodsListViewSet,CategoryViewset
from users.views import UserViewSet
from user_operation.views import UserFavoriteViewSet,UserAddressViewSet
from trade.views import ShoppingCartViewSet,OrderViewSet
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin
from django.contrib import admin

router = DefaultRouter()
router.register(r'goods',GoodsListViewSet, base_name="goods")
router.register(r'categorys',CategoryViewset, base_name="categorys")
router.register(r'users',UserViewSet, base_name="users")
router.register(r'fav',UserFavoriteViewSet,base_name='fav')
router.register(r'address',UserAddressViewSet,base_name='address')
router.register(r'shopcart',ShoppingCartViewSet,base_name='shopcart')
router.register(r'order',OrderViewSet,base_name='order')
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    url(r'^docs/', include_docs_urls(title='小黑的澳新直购店')),
    url(r'^',include(router.urls)),
    # url(r'^goods/$', GoodsListView.as_view(), name="goods-list"),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^jwt-auth/', obtain_jwt_token)
]
