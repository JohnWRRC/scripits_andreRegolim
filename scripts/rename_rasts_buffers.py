import grass.script as grass
from PIL import Image
import wx
import random
import re
import time
import math

 

lista_vects=grass.mlist_grouped ('rast', pattern='*0250*') ['PERMANENT']
x=0
for i in lista_vects:
    #if "QQ" in i :
        #out=i.replace('QQ_pts_2_buf2km_merge_v0_Join_rast2000m_img','QQ_pts_2_buffer_2000_extracByMask_rast_img')
    print i
        #grass.run_command('g.rename',rast=i+','+out,overwrite=True)
    
