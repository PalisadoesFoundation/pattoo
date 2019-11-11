import collections

TimestampValue = collections.namedtuple(
    'TimestampValue', 'idx_datapoint timestamp')

IDXTimestampValue = collections.namedtuple(
    'IDXTimestampValue', 'idx_datapoint timestamp value')
