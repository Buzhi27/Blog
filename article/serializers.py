from rest_framework import serializers
from article.models import Article, Category, Tag, Avatar
from user_info.serializers import UserDescSerializer
from comment.serializers import CommentSerializer

# # 继承了ModelSerializer类
# class ArticleListSerializer(serializers.ModelSerializer):
#     # 添加超链接
#     # 只需要在参数里提供路由的名称，就会自动完成动态地址的映射  -> "url": "http://127.0.0.1:8000/api/article/11",
#     # view_name 是路由的名称，也就是在 path(... name='xxx') 里的那个 name
#     url = serializers.HyperlinkedIdentityField(view_name="article:detail")

#     # read_only 参数设置为只读
#     author = UserDescSerializer(read_only=True)

#     class Meta:
#         # 指定的模型是Article
#         model = Article
#         # 指定要序列化的字段
#         fields = [
#             # 有了url之后，id就不需要了
#             # 'id',
#             'url',
#             'title',
#             'created',
#             'author',
#         ]
#         # 嵌套序列化器已经设置了只读，所以这个就不要了
#         # read_only_field = ['author']
# --------------------------------------------------------------------------------------------------

# HyperlinkedModelSerializer 自动提供了外键字段的超链接，并且默认不包含模型对象的 id 字段。

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签序列化器"""
    # 防止出现重复的标签对象
    # 检查标签对象是否已经存在于数据库中
    def check_tag_obj_exists(self, validated_data):
        # 从传入的 validated_data 中获取标签的文本内容。
        text = validated_data.get('text')
        # 查数据库中是否已经存在具有相同文本内容的标签对象。如果存在，则抛出一个 ValidationError 异常，提示标签已经存在。
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))
        
    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        # 调用父类的 create 方法，执行标准的创建操作。
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        # 调用父类的 update 方法，执行标准的更新操作。
        return super().update(instance, validated_data)


    class Meta:
        model = Tag
        fields ='__all__'


class AvatarSerializer(serializers.ModelSerializer):
    """标题图序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """分类的序列化器"""
    # HyperlinkedIdentityField 作用是将路由间的表示转换为超链接
    # view_name 参数是路由名，必须指定
    # category-detail 是自动注册路由时，Router默认帮你设置的详情页面的名称
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']
  

class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    # 嵌套序列化是指在序列化过程中，将一个模型中的关联模型的数据也进行序列化，并将其嵌套到主模型的序列化中
    
    id = serializers.IntegerField(read_only=True)
    # 对作者信息进行嵌套序列化
    author = UserDescSerializer(read_only=True)

    # category 的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # category 的id字段，用于创建/更新 category 外键
    # 定义了一个 category_id 字段，它是一个整数字段，用于创建/更新文章时指定分类的外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    # tag字段
    tags = serializers.SlugRelatedField(
        queryset = Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    # 图片字段
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True,
        allow_null=True,
        required=False
    )
    

    # 覆写方法，如果输入的标签不存在则创建它
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)
    

    # # 验证图片 id 是否存在
    # # 不存在返回验证错误
    # def validate_avatar_id(self, value):
    #     if not Avatar.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError("Avatar with id {} not exists.".format(value))
        
    #     return value

    # # category_id 字段的验证器，用于验证传入的 category_id 是否有效
    # def validate_category_id(self, value):
    #     # 检查是否存在具有给定 id 的 Category 对象 或 传入的 value 是否为 None
    #     if not Category.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError('Category with id {} not exists.'.format(value))
    #     return value
    
    #  重构
    #   |
    #   |
    #   ↓

    # 自定义错误信息
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    # 检查了数据对象是否存在，若不存在则调用钩子方法 fail() 引发错误。
    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )

        return value

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(
            model=Category,
            value=value,
            message='incorrect_category_id'
        )

        return value



class ArticleSerializer(ArticleBaseSerializer):
    """博文序列化器"""

    class Meta:
        model = Article
        fields ='__all__'
        #在列表接口连 body 字段也不需要显示的话，可以传入 extra_kwargs 使其变成仅可写却不显示的字段。
        extra_kwargs = {'body': {'write_only': True}}
    


# ///////////////////////////////////////////////////////////////////////////////////////////////////

class ArticleDetailSerializer(ArticleBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    # many=True 表示这是一个多对多的关系
    comments = CommentSerializer(many=True, read_only=True)
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'

# 希望分类的列表页面不显示其链接的文章以保持数据清爽，但是详情页面则展示出链接的所有文章，方便接口的使用。因此就需要同一个视图集用到两个不同的序列化器
class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title'
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]


