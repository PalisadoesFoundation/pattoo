import collections

IDXTimestamp = collections.namedtuple(
    'IDXTimestamp', 'idx_datapoint timestamp')

IDXTimestampValue = collections.namedtuple(
    'IDXTimestampValue', 'idx_datapoint timestamp value')
