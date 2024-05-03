from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics, permissions
from rest_framework import viewsets
# from rest_framework.permissions import IsAdminUser
from rest_framework import filters
from article.models import Article, Category, Tag, Avatar
from article.serializers import ArticleDetailSerializer, ArticleSerializer, AvatarSerializer
from article.serializers import CategorySerializer, CategoryDetailSerializer, TagSerializer
from article.permissions import IsAdminUserOrReadOnly









# -------------------------------------------------------------------------------------------------- 


# # 使用@api_view装饰器指定视图可以处理的HTTP请求
# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         # 获得数据库中所有文章
#         articles = Article.objects.all()
#         # 对查询到的文章数据进行序列化，转换成Json格式
#         serializer = ArticleListSerializer(articles, many=True)
#         # 将序列化后的Json数据作为相应内容，通过Response返回客户端
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ArticleListSerializer(data=request.data)
#         # 验证反序列化是否有效
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# --------------------------------------------------------------------------------------------------  

# # 文章列表
# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializer

#     # 由于是个人博客， 所以只允许管理员发布文章
#     # 指定该视图需要的权限类
#     # permission_classes 可以接收一个列表，所以权限控制类可以设置多个，请求必须满足所有控制条件才允许放行
#     permission_classes = [IsAdminUserOrReadOnly]

#     # perform_create 从 ListCreateAPIView 继承而来，它在序列化数据真正保存之前调用，因此可以在这里添加额外的数据（即用户对象）
#     def perform_create(self, serializer):
#         # 在保存对象时将当前请求的用户设置为对象的作者。
#         serializer.save(author=self.request.user)



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    # 指定了过滤器后端，这里使用了 SearchFilter，允许在文章标题字段上执行搜索。
    filter_backends = [filters.SearchFilter]
    # 指定了用于搜索的字段，这里是文章标题
    search_fields = ['title']
    # 这个属性不需要了
    # filterset_fields = ['author__username', 'title']

    # 将请求的用户和新创建的对象关联起来
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # # 根据请求参数动态地过滤查询集，以满足客户端的查询需求。
    # def get_queryset(self):
    #     queryset = self.queryset
    #     username = self.request.query_params.get('username', None)

    #     if username is not None:
    #         queryset = queryset.filter(author__username=username)

    #     return queryset
    
    # 文章详情接口
    def get_serializer_class(self):
        # 如果是列表操作（list），则返回 ArticleSerializer，否则返回 ArticleDetailSerializer。
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer
    
# # -------------------------------------------------------------------------------------------------- 
# DRF类视图与传统 Django 的区别，.get()、.put()多了一个将对象序列化（或反序列化）的步骤。
# .delete()方法不用返回实际数据，所以执行完删除动作就行。
# class ArticleDetail(APIView):
#     """文章详情试图"""

    # def get_object(self, pk):
    #     """获取单个文章对象"""
    #     try:
    #         # pk是主键，默认状态下就是id
    #         return Article.objects.get(pk=pk)
    #     except:
    #         raise Http404
        

    # def get(self, request, pk):
    #     article = self.get_object(pk)
    #     serializer = ArticleDetailSerializer(article)
    #     # 返回Json数据
    #     return Response(serializer.data)
    

    # def put(self, request, pk):
    #     article = self.get_object(pk)
    #     serializer = ArticleDetailSerializer(article, data=request.data)
    #     #验证提交的数据是否合法，不合法返回400
    #     if serializer.is_valid():
    #         # 序列化器将持有的数据反序列化后，保存到数据库中
    #         serializer.save()
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # def delete(self, request, pk):
    #     article = self.get_object(pk)
    #     article.delete()
    #     # 删除成功后返回204
    #     return Response(status=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------------------------------------------

# class ArticleDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     """文章详情图"""
#     # 指定查询集queryset，获取数据库中的所有文章对象
#     queryset = Article.objects.all()
#     # 指定序列化器类serializer_class，定义了对于文章对象的序列化方式
#     serializer_class = ArticleDetailSerializer

#     # 加上*args, **kwargs，保证代码的灵活性，可能会添加额外的参数
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
# --------------------------------------------------------------------------------------------------

# # 文章详情
# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer
#     permission_classes = [IsAdminUserOrReadOnly]

# ///////////////////////////////////////////////////////////////////////////////////////////////////


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    """标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None


class AvatarViewSet(viewsets.ModelViewSet):
    """标题图视图集"""
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]