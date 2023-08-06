# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 11:08:45 2021

@author: xcwhung
"""
from fileSizeUtils import BinarySize,SizeUnit
from decimal import Decimal

def test_getBaseInByte():
    assert BinarySize.getBaseInByte(SizeUnit.Byte) == Decimal(1)
    assert BinarySize.getBaseInByte(SizeUnit.KB) == Decimal(1024)
    assert BinarySize.getBaseInByte(SizeUnit.MB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.KB)
    assert BinarySize.getBaseInByte(SizeUnit.GB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.MB)
    assert BinarySize.getBaseInByte(SizeUnit.TB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.GB)
    assert BinarySize.getBaseInByte(SizeUnit.PB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.TB)
    assert BinarySize.getBaseInByte(SizeUnit.EB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.PB)
    assert BinarySize.getBaseInByte(SizeUnit.ZB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.EB)
    assert BinarySize.getBaseInByte(SizeUnit.YB) == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.ZB)

def test_inByte():
    assert BinarySize.ofByteFromInt(1).inByte() == Decimal(1)
    assert BinarySize.ofKBFromInt(1).inByte() == Decimal(1024)
    assert BinarySize.ofMBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.KB)
    assert BinarySize.ofGBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.MB)
    assert BinarySize.ofTBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.GB)
    assert BinarySize.ofPBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.TB)
    assert BinarySize.ofEBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.PB)
    assert BinarySize.ofZBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.EB)
    assert BinarySize.ofYBFromInt(1).inByte() == Decimal(1024) * BinarySize.getBaseInByte(SizeUnit.ZB)
