#importando pacotes
import grass.script as grass
import os


os.chdir(r'C:\_data\valfrido')
arquivo=open('cont.txt','w') 
cabecalho='id'',''cont' '\n'
arquivo.write(cabecalho)
temp_2=''
temp_3=''
for i in range(15):
    i=i+1
    frag=grass.read_command('v.db.select', flags='c', map='Buffer_1500_shp', column='id_2', where="cat="+`i`)
    grass.run_command('v.extract', input='Buffer_1500_shp', output='Temp', where="cat="+`i`, overwrite=True   )
    grass.run_command('g.region',vect='temp')
    grass.run_command('v.to.rast',input='temp', out='temp', use="cat" , overwrite=True)
    grass.run_command('r.mask',  input='temp',flags='o')
    grass.run_command('g.region',vect='temp')
    temp=grass.read_command('r.stats', input='uso_solo_tif_patch_clump_mata_limpa',quiet=True,fs='comma')
    temp=temp.replace('*','') 
    temp=temp.replace('\n','cc') 
    temp_2=temp.split('cc')
    
    del temp_2[-1]  
    del temp_2[-1]
    #print temp_2
    cont=len(temp_2)
    linha1=frag.replace('\n','')
    linha2=cont
    print cont
    arquivo.write(linha1+","+`linha2`+'\n')
    grass.run_command('r.mask',  flags='r')
    cont=0
arquivo.close() 