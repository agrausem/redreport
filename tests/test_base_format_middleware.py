import unittest
from redreport.middleware import BaseRedreportFormatMiddleware
from redreport.models import Pagination
from collections import namedtuple


class FakeResponse(object):

    def __init__(self, text):
        self.text = text


Model = namedtuple('Model', ['attr1', 'attr2'])
ModelMiddleware = type('ModelObject', (BaseRedreportFormatMiddleware, ),
                       dict(list_key='objects', object_key='object',
                            model=Model))


class TestLoadingBasicObjects(unittest.TestCase):
    """
    """

    def setUp(self):
        self.middleware = ModelMiddleware()

    def test_load_objects(self):
        data = {
            "objects": 
                    [
                        {
                            "attr1": "test",
                            "attr2": 0
                        },
                        {   
                            "attr1": "test", 
                            "attr2": 1
                        }
                    ]
            }
        objects = self.middleware.process_list(data)
        self.assertTrue(len(objects) == 2)
        self.assertTrue(isinstance(objects[0], Model))
        self.assertEqual(objects[0].attr1, "test")
        self.assertEqual(objects[1].attr1, "test")
        self.assertEqual(objects[0].attr2, 0)
        self.assertEqual(objects[1].attr2, 1)

    def test_load_object(self):
        data = {
            "object": 
                {
                    "attr1": "test",
                    "attr2": 0
                }
            }
        object = self.middleware.process_object(data)
        self.assertTrue(isinstance(object, Model))
        self.assertEqual(object.attr1, "test")
        self.assertEqual(object.attr2, 0)


    def test_load_pagination(self):
        data = {
            "limit": 25,
            "offset": 0,
            "total_count": 89
        }
        
        pagination = self.middleware.process_pagination(data)
        self.assertTrue(isinstance(pagination, Pagination))
        self.assertEqual(pagination.limit, 25)
        self.assertEqual(pagination.offset, 0)
        self.assertEqual(pagination.total_count, 89)


class TestProcessingResponse(unittest.TestCase):

    def test_with_objects(self):
        pass

    def test_with_object(self):
        pass

    def test_with_pagination(self):
        pass

    def test_with_no_format_middleware_activated(self):
        pass

    def test_with_bad_middleware_implementation(self):
        pass
