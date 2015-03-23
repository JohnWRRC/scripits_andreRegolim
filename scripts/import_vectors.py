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


for file in os.listdir(r'F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14'):
    if fnmatch.fnmatch(file, '*.shp'):
        lista_arquivos.append(file)
    

os.chdir(r'F:\data\Talitha\Mapas_classificados_final\SHP')
for i in lista_arquivos.append:
    out=i.replace('.shp','_shp')
    grass.run_command('v.in.ogr',dsn=i,out=out,overwrite=True)
    grass.run_command('g.region',vect=out2,res=10)
    grass.run_command('v.to.rast',input=out,out=out+'_rast',use='attr',column='id',overwrite=True)
    grass.run_command('v.to.rast',input=out2,out=out2+'_rast',use='attr',column='land_use',overwrite=True)
    x=x+1
    
    
    