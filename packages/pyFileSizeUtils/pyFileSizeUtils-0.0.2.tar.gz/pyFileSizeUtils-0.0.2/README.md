# File Size Utils

A library provide function converting file size or memory size between different unit byte, kilo byte, mega byte...

# Installation

```
pip install pyFileSizeUtils
```

# Demo

```python
import pyFileSizeUtils 
```

```python
from pyFileSizeUtils import BinarySize,SizeUnit

oneMB = BinarySize.ofMBFromInt(1).inByte()
print(oneKB.inByte()) # 1024


```