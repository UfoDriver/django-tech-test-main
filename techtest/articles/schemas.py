from marshmallow import validate, ValidationError
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load

from techtest.articles.models import Article
from techtest.authors.models import Author
from techtest.authors.schemas import AuthorSchema
from techtest.regions.models import Region
from techtest.regions.schemas import RegionSchema


class ArticleSchema(Schema):
    class Meta(object):
        model = Article

    id = fields.Integer()
    title = fields.String(validate=validate.Length(max=255))
    content = fields.String()
    regions = fields.Method(
        required=False, serialize="get_regions", deserialize="load_regions"
    )
    author = fields.Method(
        required=False, serialize="get_author", deserialize="load_author", allow_none=True,
    )

    def get_regions(self, article):
        return RegionSchema().dump(article.regions.all(), many=True)

    def load_regions(self, regions):
        return [
            Region.objects.get_or_create(id=region.pop("id", None), defaults=region)[0]
            for region in regions
        ]

    def get_author(self, article):
        return AuthorSchema().dump(article.author) or None

    def load_author(self, author):
        try:
            return Author.objects.get(pk=author)
        except Author.DoesNotExist:
            raise ValidationError("Author does not exist")

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        regions = data.pop("regions", None)
        article, _ = Article.objects.update_or_create(
            id=data.pop("id", None), defaults=data
        )
        if isinstance(regions, list):
            article.regions.set(regions)
        return article
