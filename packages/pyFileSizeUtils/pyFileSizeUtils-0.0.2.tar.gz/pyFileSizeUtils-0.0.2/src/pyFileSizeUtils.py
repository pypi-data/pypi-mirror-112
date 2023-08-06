# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 09:43:54 2021

@author: xcwhung
"""

from enum import Enum, unique
from decimal import Decimal

@unique
class SizeUnit(Enum):
    Byte = 1
    KB = 2
    MB = 3
    GB = 4
    TB = 5
    PB = 6
    EB = 7
    ZB = 8
    YB = 9

class BinarySize:
    __size:SizeUnit
    __value:Decimal
    def __init__(self, sizeUnit: SizeUnit, value: Decimal):
        self.__sizeUnit = sizeUnit
        self.__value = value
    
    def unit(self) -> SizeUnit:
        return self.__sizeUnit
    
    def value(self) -> Decimal:
        return self.__value
    
    @staticmethod
    def ofByte(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.Byte,value)
    
    @staticmethod
    def ofByteFromInt(value: int)->'BinarySize':
        return BinarySize.ofByte(Decimal(value))

    @staticmethod
    def ofKB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.KB,value)
    
    @staticmethod
    def ofKBFromInt(value: int)->'BinarySize':
        return BinarySize.ofKB(Decimal(value))

    @staticmethod
    def ofMB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.MB,value)
    
    @staticmethod
    def ofMBFromInt(value: int)->'BinarySize':
        return BinarySize.ofMB(Decimal(value))

    @staticmethod
    def ofGB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.GB,value)
    
    @staticmethod
    def ofGBFromInt(value: int)->'BinarySize':
        return BinarySize.ofGB(Decimal(value))

    @staticmethod
    def ofTB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.TB,value)
    
    @staticmethod
    def ofTBFromInt(value: int)->'BinarySize':
        return BinarySize.ofTB(Decimal(value))

    @staticmethod
    def ofPB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.PB,value)
    
    @staticmethod
    def ofPBFromInt(value: int)->'BinarySize':
        return BinarySize.ofPB(Decimal(value))

    @staticmethod
    def ofEB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.EB,value)
    
    @staticmethod
    def ofEBFromInt(value: int)->'BinarySize':
        return BinarySize.ofEB(Decimal(value))

    @staticmethod
    def ofZB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.ZB,value)
    
    @staticmethod
    def ofZBFromInt(value: int)->'BinarySize':
        return BinarySize.ofZB(Decimal(value))

    @staticmethod
    def ofYB(value: Decimal)->'BinarySize':
        return BinarySize(SizeUnit.YB,value)
    
    @staticmethod
    def ofYBFromInt(value: int)->'BinarySize':
        return BinarySize.ofYB(Decimal(value))
    
    @staticmethod
    def getBaseInByte(sizeUnit: SizeUnit)->Decimal:
        if sizeUnit == SizeUnit.Byte:
            return Decimal(1)
        elif sizeUnit == SizeUnit.KB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.Byte)
        elif sizeUnit == SizeUnit.MB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.KB)
        elif sizeUnit == SizeUnit.GB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.MB)
        elif sizeUnit == SizeUnit.TB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.GB)
        elif sizeUnit == SizeUnit.PB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.TB)
        elif sizeUnit == SizeUnit.EB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.PB)
        elif sizeUnit == SizeUnit.ZB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.EB)
        elif sizeUnit == SizeUnit.YB:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.ZB)
        else:
            return Decimal(1024)*BinarySize.getBaseInByte(SizeUnit.YB)
        
        
    def asUnit(self, sizeUnit: SizeUnit) -> 'BinarySize':
        if sizeUnit.value == self.__sizeUnit.value:
            return self
        elif sizeUnit.value < self.__sizeUnit.value:
            b1 = BinarySize.getBaseInByte(sizeUnit)
            b2 = BinarySize.getBaseInByte(self.unit())
            return BinarySize(sizeUnit, self.value() * (b2 / b1))
        else:
            b1 = BinarySize.getBaseInByte(sizeUnit)
            b2 = BinarySize.getBaseInByte(self.unit())
            return BinarySize(sizeUnit, self.value() / (b1 / b2))
        
    def inByte(self) -> Decimal:
        return self.asUnit(SizeUnit.Byte).value()

    def inKB(self) -> Decimal:
        return self.asUnit(SizeUnit.KB).value()

    def inMB(self) -> Decimal:
        return self.asUnit(SizeUnit.MB).value()

    def inGB(self) -> Decimal:
        return self.asUnit(SizeUnit.GB).value()

    def inTB(self) -> Decimal:
        return self.asUnit(SizeUnit.TB).value()

    def inPB(self) -> Decimal:
        return self.asUnit(SizeUnit.PB).value()

    def inEB(self) -> Decimal:
        return self.asUnit(SizeUnit.EB).value()

    def inZB(self) -> Decimal:
        return self.asUnit(SizeUnit.ZB).value()

    def inYB(self) -> Decimal:
        return self.asUnit(SizeUnit.YB).value()
