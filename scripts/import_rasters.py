import grass.script as grass
from grass.script import raster as grassR
import os
import string
import glob
import re
import fnmatch
lista_arquivos=[]
LISTA=[]
LISTA2=[]  


for file in os.listdir(r'E:\data_2015\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters_extract'):
    if fnmatch.fnmatch(file, '*.img'):
        lista_arquivos.append(file)
  

             
os.chdir(r'E:\data_2015\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters_extract')
for i in lista_arquivos:
    if "PEA" in i:
        print i
        out=i.replace('.img','_img')
        grass.run_command('r.in.gdal',input=i,out=out,overwrite=True)
   
    
    
    