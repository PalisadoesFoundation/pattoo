import collections

IDXTimestamp = collections.namedtuple(
    'IDXTimestamp', 'idx_checksum timestamp')

IDXTimestampValue = collections.namedtuple(
    'IDXTimestampValue', 'idx_checksum timestamp value')
