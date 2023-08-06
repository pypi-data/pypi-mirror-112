# -*- coding: utf-8 -*-

import datetime

import pymongo
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.errors import PyMongoError
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from monkey.dao.core import DAO, PersistenceError, ObjectNotFoundError

_SEQ_COLLECTION_NAME: str = 'sequences'
"""The name used for sequences collection, by default"""

_SEQ_NUM_FIELD: str = '_seq_num'
"""The name used for sequence number field, by default"""

ASC = pymongo.ASCENDING
"""Ascending sort order"""

DESC = pymongo.DESCENDING
"""Descending sort order"""


class PyMongoDAO(DAO):
    """PyMongoDAO manages persistence on MongoDDB using PyMongo."""

    # TODO: Add upsert, replace, update_many, delete_many, insert_many, replace

    def __init__(self, database: Database, collection_name: str, seq_enabled=False, seq_num_field: str = _SEQ_NUM_FIELD,
                 seq_collection_name: str = _SEQ_COLLECTION_NAME):
        """Instantiates a new PyMongo DAO
        :param database: a MongoDB database provide by pymongo.MongoClient
        :param collection_name: the name of the collection in which documents persist
        :param seq_enabled: if True, DAO will add a sequence number to each newly inserted documents
        :param seq_num_field: the name of document field used for sequence number
        :param seq_collection_name: the name of the collection in which last sequence number is stored
        """
        super().__init__()
        self.database: Database = database
        self.collection: Collection = database[collection_name]
        self.seq_enabled: bool = seq_enabled
        if seq_enabled:
            self.seq_num_field: str = seq_num_field
            self.sequences: Collection = database[seq_collection_name]
            self.sequence_name: str = collection_name

    def find_one(self, query=None, projection=None):
        """Finds a document matching the specified query
        :param query: the filter used to query the collection
        :param projection: a list of field names that should be returned in the result set or a dict specifying the
        fields to include or exclude.
        :return: The first document found matching the query
        """
        try:
            doc = self.collection.find_one(query, projection=projection)
            if doc is not None:
                return doc
            else:
                raise ObjectNotFoundError(self.collection.name, query)
        except PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def find_one_by_id(self, _id, projection=None):
        """Finds a document by its '*Object*' id (i.e. by filtering on the '*_id*' field of the collection).
        :param _id: id of the document
        :param projection: a list of field names that should be returned in the result set or a dict specifying the
        fields to include or exclude.
        :return: the found document (if there is one)
        :raise: ObjectNotFoundError
        """
        return self.find_one({'_id': _id}, projection)

    def find_one_by_key(self, key, projection=None):
        """Finds a document by its key (synonym of find_one_by_id)
        :param key: id of the document
        :param projection: a list of field names that should be returned in the result set or a dict specifying the
        fields to include or exclude.
        :return: the found document (if there is one)
        :raise: ObjectNotFoundError
        """
        return self.find_one_by_id(key, projection)

    def find(self, query=None, projection=None, skip=0, limit=0, sort=None):
        """Finds records matching the specified query
        :param query: the filter used to query the collection
        :param projection: a list of field names that should be returned in the result set or a dict specifying the
        fields to include or exclude.
        :param skip: the number of record to omit (from the start of the result set) when returning the results
        :param limit: the maximum number of records to return
        :param sort: a list of (key, direction) pairs specifying the sort order for this list
        :return: a list of records
        """
        cursor = None
        try:
            cursor = self.collection.find(filter=query, projection=projection, skip=skip, limit=limit, sort=sort)
            # TODO: Use list comprehension or lambda expression
            result = []
            for doc in cursor:
                result.append(doc)
            return result
        except PyMongoError as e:
            raise PersistenceError('Unexpected error', e)
        finally:
            cursor.close()

    def lookup(self, query=None, skip=0, limit=0, sort=None):
        """Retrieves ids of documents matching the specified query
        :param query: the filter used to query the collection
        :param skip: the number of record to omit (from the start of the result set) when returning the results
        :param limit: the maximum number of records to return
        :param sort: a list of (key, direction) pairs specifying the sort order for this list
        :return: List of matching document ids
        """
        # return self.find(query, ['_id'], skip, limit, sort)
        try:
            cursor = self.collection.find(filter=query, projection=['_id'], skip=skip, limit=limit, sort=sort)
            # TODO: Use list comprehension or lambda expression
            result = []
            for doc in cursor:
                result.append(doc['_id'])
            return result
        except PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def count(self, query_filter=None):
        """Counts the number of documents that match query filter
        :param query_filter: a filter expression
        :return: the total number of documents
        """
        if not query_filter:
            query_filter = {}
        try:
            return self.collection.count_documents(query_filter)
        except PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def count_all(self, fast_count=False):
        if fast_count:
            return self.collection.estimated_document_count()
        else:
            return self.count({})

    def delete(self, _id):
        """Deletes the document matching the specified key
        :param _id: id of the document to delete
        :return: count of deleted document (0 or 1)
        """
        try:
            result: DeleteResult = self.collection.delete_one({'_id': _id})
            return result.deleted_count
        except PyMongoError as e:
            self.logger.error(f'Failed to delete document {{\'_id\': {_id}}}')
            raise PersistenceError('Unexpected error', e)

    def update(self, _id, **change_set):
        """Updates the document matching the specified key applying change set
        :param _id: id of the document to delete
        :param change_set: change set to apply to the document
        :return: count of updated document (0 or 1)
        """
        # TODO : Verify if the change_set is merge with persistent data or replace it.
        try:
            result = self.collection.update_one({'_id': _id}, {'$set': self._encode_dict(change_set)})
            return result.modified_count
        except PyMongoError as e:
            self.logger.error('Failed to update document {\'_id\': {}} applying change set {}'.format(_id, change_set))
            raise PersistenceError('Unexpected error', e)

    def insert(self, **data_set):
        """Inserts the data set as a new document
        :param data_set: data set defining the document
        :return: id of the inserted document
        """
        document = {}
        if self.seq_enabled:
            document = {self.seq_num_field: self._get_next_seq_num()}
        document.update(data_set)
        try:
            result: InsertOneResult = self.collection.insert_one(self._encode_dict(document))
            return result.inserted_id
        except PyMongoError as e:
            self.logger.error(f'Failed to insert new document with data: {document}')
            raise PersistenceError('Unexpected error', e)

    def _get_next_seq_num(self):
        """Gets the next sequence number value
        :return: the next sequence number
        """
        result = self.sequences.find_one_and_update({'_id': self.sequence_name}, {'$inc': {'seq': 1}},
                                                    projection={'seq': True, '_id': False}, upsert=True,
                                                    return_document=ReturnDocument.AFTER)
        return result['seq']

    def _encode_dict(self, data_set):
        encoded_data_set = {}
        for key, value in data_set.items():
            if isinstance(value, datetime.date):
                if not isinstance(value, datetime.datetime):
                    value = datetime.datetime.combine(value, datetime.time().min)
            elif isinstance(value, datetime.time):
                value = value.isoformat()
            elif isinstance(value, dict):
                value = self._encode_dict(value)
            encoded_data_set[key] = value
        return encoded_data_set
