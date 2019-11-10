import collections

TimestampValue = collections.namedtuple(
    'TimestampValue', 'idx_datavariable timestamp')

IDXTimestampValue = collections.namedtuple(
    'IDXTimestampValue', 'idx_datavariable timestamp value')
