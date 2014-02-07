#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import riak
import threading
import Queue


MAX_STRING_LENGTH = 500
FLOAT_PRECISION_LEVEL = 1000

JS_MAP_FUNCTION = """
function(v) {
    var data = JSON.parse(v.values[0].data);
    return [[v.key, data]];
}
"""

JS_REDUCE_ORDER_FUNC = """
function(values, arg) {
    var field = arg.by;
    var reverse = arg.order == 'desc';
    values.sort(function(a, b) {
        a = a[1]; b = b[1];
        if (reverse) {
            var _ref = [b, a];
            a = _ref[0];
            b = _ref[1];
        }
        if (a[field] < b[field]) {
            return -1;
        } else if (a[field] == b[field]) {
            return 0;
        } else if (a[field] > b[field]) {
            return 1;
        }
    });
    return values;
}
"""


class InvalidFilterOperation(Exception):
    def __init__(self, op):
        self._op = op
        Exception.__init__(self, 'Invalid Operator %r' % self._op)


class RiakMultiIndexQuery(object):
    """This class implements a Muti-Query interface for
    Riak Indexes which makes use of Index queries and MapReduce.
    """
    def __init__(self, client, bucket):
        self._client = client
        self._bucket = bucket
        self.reset()

    def reset(self):
        """Reset the RiakMultiIndexQuery object for further use.
        """
        self._mr_query = riak.RiakMapReduce(self._client)
        self._mr_inputs = set()
        self._filters = []
        self._offset = 0
        self._limit = 0
        self._order = ()

    def filter(self, field, op, value):
        """Add a query condition. eg: filter('age', '>=', 25)
        """
        self._filters.append((field, op, value))
        return self

    def offset(self, offset):
        """Query result offset.
        """
        self._offset = offset
        return self

    def limit(self, limit=0):
        """Number of results to return for this query. a value of
        0 means fetch all records.
        """
        self._limit = limit
        return self

    def order(self, sort_key, order='ASC'):
        """Sort (ASC or DESC) the results based on sort_key.
        """
        self._order = (sort_key, order)
        return self

    def _filter_to_index_query(self, field, op, value, queue):
        """Convert a filter query to Riak index query.
        """
        if isinstance(value, basestring):
            index_type = 'bin'
            min = chr(0) * MAX_STRING_LENGTH
            max = chr(127) * MAX_STRING_LENGTH
            if op == '>':
                value = value + ((MAX_STRING_LENGTH - len(value)) * chr(0))
            elif op == '<':
                value = value[:-1] + chr(ord(value[-1]) - 1)
        else:
            if isinstance(value, float):
                value = int(value * FLOAT_PRECISION_LEVEL)
            index_type = 'int'
            max = int(sys.float_info.max)
            min = -max
            if op == '>':
                value += 1
            elif op == '<':
                value -= 1

        field = '%s_%s' % (field, index_type)
        results = set()

        if op == '==':
            [results.add(res.get_key())
             for res in self._client.index(self._bucket, field, value).run()]
        elif op == '>' or op == '>=':
            [results.add(res.get_key())
             for res in self._client.index(self._bucket, field, value,
                                           max).run()]
        elif op == '<' or op == '<=':
            [results.add(res.get_key())
             for res in self._client.index(self._bucket, field, min,
                                           value).run()]
        else:
            raise InvalidFilterOperation(op)
        # push the results to the queue
        queue.put(results)

    def run(self, timeout=9000):
        """Run this Query. This will first query the bucket using indexes and
        get the intersection of these keys. Later this keys are passed to
        MapReduce phase to fetch and sort the data.
        """

        index_key_sets = []
        index_query_threads = []
        queue = Queue.Queue()
        for (field, op, value) in self._filters:
            # spin off threads to do index queries
            thd = threading.Thread(target=self._filter_to_index_query,
                                   args=(field, op, value, queue))
            index_query_threads.append(thd)
            thd.start()

        # wait for the threads to finish the job
        [thd.join() for thd in index_query_threads]

        # get the results back from the queue
        while not queue.empty():
            key_set = queue.get()
            index_key_sets.append(key_set)

        # find the intersection of the key sets.
        if index_key_sets:
            mr_inputs = reduce(lambda x, y: x.intersection(y), index_key_sets)
        else:
            mr_inputs = set()

        if self._filters and not mr_inputs:
            yield []

        if not mr_inputs:
            self._mr_query = self._client.add(self._bucket)
        for key in mr_inputs:
            self._mr_query.add(self._bucket, key)

        self._mr_query.map(JS_MAP_FUNCTION)

        if self._order:
            self._mr_query.reduce(JS_REDUCE_ORDER_FUNC,
                                  {'arg': {'by': self._order[0],
                                           'order': self._order[1].lower()
                                           }
                                   })

        if self._limit:
            start = self._offset
            end = self._offset + self._limit
            if (end > len(mr_inputs)) and self._filters:
                end = 0
            self._mr_query.reduce('Riak.reduceSlice', {'arg': [start, end]})

        for result in self._mr_query.run(timeout):
            yield result

    def __repr__(self):
        return 'RiakMultiIndexQuery(bucket=%s).%s' % (
            self._bucket,
            '.'.join(('.'.join(
                ['filter(%s %s %r)' % filter for filter in self._filters]),
                'order(%s, %r)' % (self._order or ('None', 'ASC')),
                'offset(%s)' % self._offset,
                'limit(%s)' % self._limit)))


def test_multi_index_query():
    client = riak.RiakClient('localhost', 8091)
    bucket = client.bucket('test_multi_index')

    bucket.new('sree', {'name': 'Sreejith', 'age': 25}).\
        add_index('name_bin', 'Sreejith').\
        add_index('age_int', 25).store()
    bucket.new('vishnu', {'name': 'Vishnu', 'age': 31}).\
        add_index('name_bin', 'Vishnu').\
        add_index('age_int', 31).store()

    query = RiakMultiIndexQuery(client, 'test_multi_index')
    for res in query.filter('name', '==', 'Sreejith').run():
        print res
    print 'Last executed query: %r' % query

    query.reset()
    for res in query.filter('age', '<', 50).filter('name', '==',
                                                   'Vishnu').run():
        print res
    print 'Last executed query: %r' % query

    query.reset()
    for res in query.filter('age', '<', 50).order('age', 'DESC').run():
        print res
    print 'Last executed query: %r' % query

    query.reset()
    for res in query.limit(1).run():
        print res
    print 'Last executed query: %r' % query

    query.reset()
    for res in query.order('age', 'DESC').offset(1).limit(1).run():
        print res
    print 'Last executed query: %r' % query

    query.reset()
    # delete the test data
    for (key, _) in query.run():
        bucket.get(key).delete()


if __name__ == '__main__':
    test_multi_index_query()
