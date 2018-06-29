from flask import request
from flask_potion import ModelResource, routes, fields
from flask_potion.schema import FieldSet
from flask_potion.contrib.alchemy import SQLAlchemyManager

from app import models, db

from datetime import datetime, date
from decimal import Decimal

class OverrideManger(SQLAlchemyManager):
    @staticmethod
    def _get_field_from_python_type(python_type):
        try:
            return {
                str: fields.String,
                fields.six.text_type: fields.String,
                int: fields.Integer,
                float: fields.Number,
                bool: fields.Boolean,
                list: fields.Array,
                dict: fields.Object,
                date: fields.DateString,
                datetime: fields.DateTimeString,
                Decimal: fields.Number,
            }[python_type]
        except KeyError:
            raise RuntimeError('No appropriate field class for "{}" type found'.format(python_type))

class G9ModelResource(ModelResource):
    class Meta:
        read_only_fields = ('created_at', 'updated_at')


class ViewResourceManger(OverrideManger):
    def create(self, properties, commit=True):
        view = super().create(properties, False)
        view.ip = request.remote_addr
        view.user_agent = request.user_agent.string
        if commit: db.session.commit()
        return view

class ViewResource(G9ModelResource):
    class Meta:
        manager = ViewResourceManger
        model = models.View
        read_only_fields = G9ModelResource.meta.read_only_fields + ('ip', 'user_agent')

    class Schema:
        video = fields.ToOne('app.resources.VideoResource')

class VideoResource(G9ModelResource):
    class Meta:
        model = models.Video
        read_only_fields = G9ModelResource.meta.read_only_fields + ('count',)

    class Schema:
        published = fields.DateString()
        count = fields.Integer()

    @routes.ItemRoute.POST('/add_view')
    def add_view(self, video) -> FieldSet({'count': fields.Integer(), 'view': fields.Inline(ViewResource)}):
        '''Create view and return view and count'''
        view = ViewResource().manager.create({
                'video_id': video.id
        })
        return {'count': video.count, 'view': view}

    @routes.ItemRoute.GET('/view_count')
    def view_count(self, video, date: fields.DateString(nullable=True)) -> fields.Integer():
        return video.views.filter(models.View.created_at >= date).count() if date else video.count
