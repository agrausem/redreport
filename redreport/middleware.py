"""
"""


from . import models


class BaseRedreportFormatMiddleware(object):
    """
    """
    list_key = ''
    object_key = ''
    model = None

    @property
    def name(self):
        return self.__class__.__name__
    
    def process_response(self, response):
        """
        """
        super(BaseRedreportFormatMiddleware, self).process_response(response)

        if not hasattr(response, 'data'):
            raise ImproperlyConfigured('Your britney client should activate a '
                                       'format middleware to make redreport '
                                       '%s middlewares work' % self.name)


        # objects list part that adds an objects attibute to response
        response.objects = self.process_list(response.data)

        # object part that adds a object attribute to response
        response.object = self.process_object(response.data)

        if not response.objects and not response.object:
            raise ImproperlyConfigured('The %s middleware should define '
                                       'list_key or object_key or both '
                                       'attributes' % self.name)

        # pagination part that adds a pagination attribute to response
        response.paginate = self.process_pagination(response.data)

    def process_list(self, data):
        """ Extracts data to instantiate the appropriate objects as a list
        """
        if self.list_key in data:
            return [self.model(**object) for object in data[self.list_key]]
        return []

    def process_object(self, data):
        """ Extract data to instantiate the appropriate object as a single
        object
        """
        if self.object_key in data:
            return self.model(**data[self.object_key])
        return None

    def process_pagination(self, data):
        """ Extract the pagination information to instantiate the Pagination
        model
        """
        if 'limit' in data:
            return models.Pagination(limit=data['limit'],
                                     offset=data['offset'],
                                     total_count=data['total_count'])
        return None


class Group(BaseRedreportFormatMiddleware):
    """
    """
    list_key = 'groups'
    object_key = 'group'
    model = models.Group


class ImproperlyConfigured(Exception):
    """
    """
    pass
