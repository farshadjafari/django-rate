import ast
import json
import re
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.agency


class BaseController(object):
    def __init__(self, doc):
        self.docType = doc
        self.doc = eval('db.' + self.docType)

    def get_all(self):
        return self.doc.find()

    def get_by_id(self, id):
        return self.doc.find_one({'_id': ObjectId(id)})

    def create(self, **parameters):
        newdoc = {p: parameters[p] for p in parameters}
        return self.doc.save(newdoc)

    def update(self, id, **parameters):
        return self.doc.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': {p: parameters[p] for p in parameters}})

    def delete(self, id):
        self.doc.remove({'_id': ObjectId(id)})
        return True

    def get_list_of(self, **parameters):
        reslist = self.doc.find({p: parameters[p] for p in parameters})
        return reslist
