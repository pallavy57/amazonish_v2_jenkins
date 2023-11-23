import graphene
from graphene import Mutation, Field
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id
from .models import Category, Products


class CategoryType(DjangoObjectType):
    class Meta():
        model = Category
        fields = ('id', 'name',
                  'parent_category',
                  'slug',
                  'description',
                  'tags', 'created_at', 'updated_at')


class ProductType(DjangoObjectType):
    class Meta():
        model = Products

        fields = ('category_id',  'title',
                  'picture',
                  'summary',
                  'description',
                  'price',
                  'discount_type',
                  'discount_value',
                  'created_at',
                  'updated_at')


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    categories = graphene.List(CategoryType)

    def resolve_cats(self, info, **kwargs):
        # Querying a list
        return Category.objects.all()

    def resolve_cat(root, info, id):
        return Category.objects.get(id=id)

    def resolve_products(self, info):
        return Products.objects.all()

    def resolve_product(self, info, id):
        return Products.objects.get(id=id)


class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=False, default_value='')
    parent_category = graphene.String(required=False, default_value='')
    slug = graphene.String(required=False, default_value='')
    tags = graphene.String(required=False, default_value='')
    description = graphene.String(required=False, default_value='')


class CategoryInputUpdate(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=False, default_value='')
    parent_category = graphene.String(required=False, default_value='')
    slug = graphene.String(required=False, default_value='')
    tags = graphene.String(required=False, default_value='')
    description = graphene.String(required=False, default_value='')


class UpdateCategory(graphene.Mutation):
    class Arguments:
        inputCat = CategoryInputUpdate()
    category = graphene.Field(CategoryType)

    def mutate(self, info, inputCat):
        category = Category.objects.get(pk=inputCat.id)
        Category.objects.filter(id=category.id).update(name=inputCat.name,
                                                       parent_category=inputCat.parent_category,
                                                       slug=inputCat.slug,
                                                       description=inputCat.description,
                                                       tags=inputCat.tags)

        category_new = Category.objects.get(pk=inputCat.id)
        return UpdateCategory(category=category_new)


class CreateCategory(graphene.Mutation):
    class Arguments():
        # Mutation to create a category
        inputCat = CategoryInput()

    # Class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    def mutate(self, info, inputCat):
        category = Category(name=inputCat.name, parent_category=inputCat.parent_category,
                            slug=inputCat.slug, description=inputCat.description, tags=inputCat.tags)
        category.save()
        return CreateCategory(category=category)


class ProductInput(graphene.InputObjectType):
    category_id = graphene.ID()
    title = graphene.String()
    picture = graphene.String()
    summary = graphene.String()
    description = graphene.String()
    price = graphene.String()
    discount_type = graphene.String()
    discount_value = graphene.String()
    stocks =  graphene.String()


class ProductInputUpdate(graphene.InputObjectType):
    id = graphene.ID()
    category_id = graphene.ID()
    title = graphene.String()
    picture = graphene.String()
    summary = graphene.String()
    description = graphene.String()
    price = graphene.String()
    discount_type = graphene.String()
    discount_value = graphene.String()
    stocks = graphene.String()
    


class CreateProduct(graphene.Mutation):
    class Arguments():
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, input):
        category_obj = Category.objects.get(id=input.category_id)
        product = Products(category_id=category_obj, title=input.title,
                           picture=input.picture, summary=input.summary, description=input.description, price=input.price, discount_type=input.discount_type,
                           discount_value=input.discount_value,stocks=input.stocks)
        product.save()
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments():
        input = ProductInputUpdate()

    product = graphene.Field(ProductType)
    
    @classmethod
    def mutate(cls, root, info, input):
        category_obj = Category.objects.get(id=input.category_id)
        product = Products.objects.get(pk=input.id)
        Products.objects.filter(id=product.id).update(category_id=category_obj, title=input.title,
                                                      picture=input.picture, 
                                                      summary=input.summary, 
                                                      description=input.description,
                                                      price=input.price, 
                                                      discount_type=input.discount_type,
                                                      discount_value=input.discount_value,stocks=input.stocks)

        product_new = Products.objects.get(pk=input.id)
        return UpdateProduct(product=product_new)


class Mutation(graphene.ObjectType):
    update_category = UpdateCategory.Field()
    create_category = CreateCategory.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
