    
本模块主要进行数据校验：支持查表法和直接法。支持crc16常用校验法和自定义校验。详细用法可参照代码。

crc32仅仅实现了经典法。

```python
import unittest
from zp_pycrc import *
class crc_test(unittest.TestCase):
    def test_crc16(self):
        datas=b'\x01\x02\x03\x04\x05'
        print(len(datas),datas)
        crc=crc16_ccitt()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_ccitt_false()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_xmodem()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_x25()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_ibm()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_usb()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_maxim()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_modbus()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_dnp()
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
            
        crc=crc16( 0,0x8005, True, True, 0)
        print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
        crc=crc16_ibm()
        print("crc16_ibm __call__",hex(crc(datas)))
        b=cal_crc16_classcial(datas, 0,0x8005, True, True, 0)
        print("cal_crc16_classcial",hex(b))
        print('*******crc  ibm table*****')
        print([hex(i) for i in crc.crc_table])
        
    def test_crc32(self):
        datas=b'\x01\x02\x03\x04\x05'
        r=cal_crc32_classcial(datas, 0xffffffff, 0x04c11db7, True, True, 0xffffffff)
        print(hex(r))

if __name__ == '__main__':
    unittest.main()