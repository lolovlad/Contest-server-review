# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MainServer/Models/protos/compiler.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'MainServer/Models/protos/compiler.proto\"4\n\x08\x43ompiler\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x65xtend\x18\x03 \x01(\t\"\'\n\x16GetListCompilerRequest\x12\r\n\x05\x63ount\x18\x01 \x01(\x03\"7\n\x17GetListCompilerResponse\x12\x1c\n\tcompilers\x18\x01 \x03(\x0b\x32\t.Compiler\" \n\x12GetCompilerRequest\x12\n\n\x02id\x18\x01 \x01(\x03\x32\x86\x01\n\x0b\x43ompilerApi\x12\x46\n\x0fGetListCompiler\x12\x17.GetListCompilerRequest\x1a\x18.GetListCompilerResponse\"\x00\x12/\n\x0bGetCompiler\x12\x13.GetCompilerRequest\x1a\t.Compiler\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MainServer.Models.protos.compiler_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMPILER._serialized_start=43
  _COMPILER._serialized_end=95
  _GETLISTCOMPILERREQUEST._serialized_start=97
  _GETLISTCOMPILERREQUEST._serialized_end=136
  _GETLISTCOMPILERRESPONSE._serialized_start=138
  _GETLISTCOMPILERRESPONSE._serialized_end=193
  _GETCOMPILERREQUEST._serialized_start=195
  _GETCOMPILERREQUEST._serialized_end=227
  _COMPILERAPI._serialized_start=230
  _COMPILERAPI._serialized_end=364
# @@protoc_insertion_point(module_scope)
