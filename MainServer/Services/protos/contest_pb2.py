# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MainServer/Models/protos/contest.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&MainServer/Models/protos/contest.proto\"+\n\x15GetReportTotalRequest\x12\x12\n\nid_contest\x18\x01 \x01(\x03\"(\n\x16GetReportTotalResponse\x12\x0e\n\x06result\x18\x01 \x01(\x0c\x32Q\n\nContestApi\x12\x43\n\x0eGetReportTotal\x12\x16.GetReportTotalRequest\x1a\x17.GetReportTotalResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MainServer.Models.protos.contest_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETREPORTTOTALREQUEST._serialized_start=42
  _GETREPORTTOTALREQUEST._serialized_end=85
  _GETREPORTTOTALRESPONSE._serialized_start=87
  _GETREPORTTOTALRESPONSE._serialized_end=127
  _CONTESTAPI._serialized_start=129
  _CONTESTAPI._serialized_end=210
# @@protoc_insertion_point(module_scope)
