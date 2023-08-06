'''

'''
name='zp_pyCRC'
def reverse_data(data,bits=16):
    reverse_table=[0x0,0x8,0x4,0xc,     #0,1,2,3
                   0x2,0xa,0x6,0xe,     #4,5,6,7
                   0x1,0x9,0x5,0xd,     #8,9,a,b
                   0x3,0xb,0x7,0xf]     #c,d,e,f
    if bits==16 :
        data&=0xffff
        return (reverse_table[data&0xf]<<12)+(reverse_table[(data&0xf0)>>4]<<8)+(reverse_table[(data&0xf00)>>8]<<4)+(reverse_table[(data&0xf000)>>12])
    if bits==8:
        data&=0xff
        return (reverse_table[data&0xf]<<4)+(reverse_table[(data&0xf0)>>4])
    if bits==32:
        a=[]
        for _ in range(8):
            a.append(reverse_table[data&0x0f])
            data>>=4
        data=0
        for i in range(8):
            data<<=4
            data+=a[i]
        return data
    else :
        raise ValueError("bits param error ,it must be:8,16,32")
    


    
def cal_crc16_classcial(datas,init_reg,poly,reverse_input,reverse_output,xorout_reg):  
    reg=init_reg
    cal_poly=poly
    for i in datas:
        if reverse_input:
            data=reverse_data(i, 8)
        else:
            data=i
        reg^=(data<<8)
        for _ in range(8) :
            if reg&0x8000 :
                    reg=reg<<1
                    reg&=0xffff
                    reg^=cal_poly
            else :
                    reg=reg<<1
    if reverse_output:
        reg=  reverse_data(reg, 16)               
    reg^=xorout_reg       
    return reg   

def cal_crc32_classcial(datas,init_reg,poly,reverse_input,reverse_output,xorout_reg):  
    reg=init_reg
    cal_poly=poly
    for i in datas:
        if reverse_input:
            data=reverse_data(i, 8)
        else:
            data=i
        reg^=(data<<24)
        for _ in range(8) :
            if reg&0x80000000 :
                    reg=reg<<1
                    reg&=0xffffffff
                    reg^=cal_poly
            else :
                    reg=reg<<1
    if reverse_output:
        reg=  reverse_data(reg, 32)               
    reg^=xorout_reg       
    return reg    
    
class crc16(object):
    def __init__(self,init_reg,poly,reverse_input,reverse_output,xorout_reg):
        self.init_reg=init_reg
        self.xorout_reg=xorout_reg
        self.poly=poly
        self.reverse_input=reverse_input
        self.reverse_output=reverse_output
        self.crc_table=self.make_crc_table(self.poly,self.reverse_input)
        pass
    def make_crc_table(self,poly,reverse_input=False):
        table=[]
        if reverse_input:
            cal_poly=reverse_data(poly) 
            for i in range(256):
                reg=i
                for _ in range(8):
                    if reg&0x1 :
                        reg=reg>>1
                        reg^=cal_poly
                    else :
                        reg=reg>>1
                table.append(reg)     
        else:
            cal_poly=poly
            for i in range(256):
                reg=(i<<8)
                for _ in range(8):
                    if reg&0x8000 :
                        reg=reg<<1
                        reg&=0xffff
                        reg^=cal_poly
                    else :
                        reg=reg<<1
                table.append(reg)    
        return table

    def _cal_crc(self,datas,reg,table,reverse_input,reverse_output):
        if reverse_input:
            for a in datas :
                reg=(reg>>8)^table[(reg^a)&0xff]    
        else :
            for a in datas :
                reg=((reg&0xff)<<8)^table[((reg>>8)^a)&0xff]   
                
        if reverse_output != reverse_input :
            reg=reverse_data(reg, 16)      
        return reg
    def cal(self,datas):
        return self.__call__(datas)
    
    def __call__(self,datas):       
        reg=self.init_reg
        reg=self._cal_crc(datas, reg, self.crc_table, self.reverse_input,self.reverse_output)
        reg^=self.xorout_reg
        return reg 
    
class crc16_ccitt(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x1021, True,True, 0x0000)
        
class crc16_ccitt_false(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x1021, False,False, 0x0000)

class crc16_xmodem(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x1021, False,False, 0x0000)

class crc16_x25(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x1021, True,True, 0xffff)  
        
class crc16_ibm(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x8005, True,True, 0x0000) 
        
class crc16_usb(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x8005, True,True, 0xffff)
        
class crc16_maxim(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x8005, True,True, 0xffff)
                        
class crc16_modbus(crc16):
    def __init__(self):
        crc16.__init__(self, 0xffff,  0x8005, True,True, 0x0000)

class crc16_dnp(crc16):
    def __init__(self):
        crc16.__init__(self, 0x0000,  0x3d65, True,True, 0xffff)
              
