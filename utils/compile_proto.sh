#!/bin/bash
# A small helper script to compile protobufs.

compile()
{
  protoc -I=. --python_out=. pyvfs/proto/$1
}

compile transmission.proto
