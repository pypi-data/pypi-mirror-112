import struct

import crc32c
import numpy as np

import tfrecords_pb2

kmask_delta = 0xA282EAD8


def mask_crc(crc):
    return (((crc >> 15) | (crc << 17)) + kmask_delta) & 0xFFFFFFFF


class RecordReader:
    def __init__(self):
        self.example = tfrecords_pb2.Example()

    def decode_example(self, buffer):
        ret = {}
        self.example.ParseFromString(buffer)
        for name in self.example.features.feature:
            feature = self.example.features.feature[name]
            if len(feature.bytes_list.value) > 0:
                ret[name] = feature.bytes_list.value
            elif len(feature.int64_list.value) > 0:
                ret[name] = np.asarray(list(feature.int64_list.value), dtype=np.int64)
            elif len(feature.float_list.value) > 0:
                ret[name] = np.asarray(list(feature.float_list.value), dtype=np.float32)
        return ret

    # From https://github.com/jongwook/tfrecord_lite
    def read_from_tfrecord(self, filename):
        with open(filename, "rb") as file_handle:
            while True:
                # Read the header
                header_str = file_handle.read(8)
                if len(header_str) != 8:
                    # Hit EOF so exit
                    break
                header = struct.unpack("Q", header_str)

                # Read the crc32, which is 4 bytes, and disregard
                crc_header_bytes = file_handle.read(4)

                # The length of the header tells us how many bytes the Event
                # string takes
                header_len = int(header[0])
                event_bytes = file_handle.read(header_len)

                # The next 4 bytes contain the crc32 of the Event string,
                # which we check for integrity. Sometimes, the last Event
                # has no crc32, in which case we skip.
                crc_event_bytes = file_handle.read(4)
                yield self.decode_example(event_bytes)


class RecordWriter:
    def __init__(self):
        self.example = tfrecords_pb2.Example
        self.feature = tfrecords_pb2.Feature
        self.features = lambda d: tfrecords_pb2.Features(feature=d)

    def bytes_feature(self, values):
        if not isinstance(values, (tuple, list)):
            values = [values]
        return self.feature(bytes_list=tfrecords_pb2.BytesList(value=values))

    def int64_feature(self, values):
        if not isinstance(values, (tuple, list)):
            values = [values]
        return self.feature(int64_list=tfrecords_pb2.Int64List(value=values))

    def float_feature(self, values):
        if not isinstance(values, (tuple, list)):
            values = [values]
        return self.feature(float_list=tfrecords_pb2.FloatList(value=values))

    def encode_example(self, data_feature):
        data = self.example(features=self.features(data_feature)).SerializeToString()

        # Calculate data size
        data_len = struct.pack("Q", len(data))

        # Calculate data size crc
        len_crc = mask_crc(crc32c.crc32c(data_len))
        len_crc = struct.pack("I", len_crc)

        # Calculate data crc 
        data_crc = mask_crc(crc32c.crc32c(data))
        data_crc = struct.pack("I", data_crc)

        # Append everything
        # Following record_writer.cc
        return (data_len + len_crc) + data + (data_crc)
