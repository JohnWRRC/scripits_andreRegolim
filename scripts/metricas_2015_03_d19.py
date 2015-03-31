import grass.script as grass
import os
def rulesreclass(mapa):
  x=grass.read_command('r.stats',input=mapa,fs='comma')
  #print x
  y=x.split('\n')
  print y
  #print y
  contador_frags=len(y)
  print contador_frags
  #print y
  os.chdir(r"F:\data\Andre_regolin\Shapes_AndreRegolin\___Resultados")
  txtsaida=mapa+'_cont.txt'
  #txtreclass=open(txtsaida,'w')
  
          
    
    #txtreclass.close()      
  return txtsaida




def pacthSingle(Listmapspath):
  grass.run_command('g.region',rast=Listmapspath)
  expression1="MapaBinario="+Listmapspath
  grass.mapcalc(expression1, overwrite = True, quiet = True)    
 
  expression2="A=MapaBinario"
  grass.mapcalc(expression2, overwrite = True, quiet = True)
  
  #r.colors map=A color=wave
  expression3="MapaBinario_A=if(A[0,0]==0 && A[0,-1]==1 && A[1,-1]==0 && A[1,0]==1,1,A)"
  grass.mapcalc(expression3, overwrite = True, quiet = True)
  expression4="A=MapaBinario_A"
  grass.mapcalc(expression4, overwrite = True, quiet = True)
  expression5="MapaBinario_AB=if(A[0,0]==0 && A[-1,0]==1 && A[-1,1]==0 && A[0,1]==1,1,A)"
  grass.mapcalc(expression5, overwrite = True, quiet = True) 
  expression6="A=MapaBinario_AB"
  grass.mapcalc(expression6, overwrite = True, quiet = True)
  expression7="MapaBinario_ABC=if(A[0,0]==0 && A[0,1]==1 && A[1,1]==0 && A[1,0]==1,1,A)"
  grass.mapcalc(expression7, overwrite = True, quiet = True)
  expression8="A=MapaBinario_ABC"
  grass.mapcalc(expression8, overwrite = True, quiet = True)
  expression9="MapaBinario_ABCD=if(A[0,0]==0 && A[1,0]==1 && A[1,1]==0 && A[0,1]==1,1,A)"
  grass.mapcalc(expression9, overwrite = True, quiet = True)
  expression10="A=MapaBinario_ABCD"
  grass.mapcalc(expression10, overwrite = True, quiet = True)
  expression11=Listmapspath+"_patch=A"
  grass.mapcalc(expression11, overwrite = True, quiet = True)
  #r.colors map=$i"_patch" color=random
  grass.run_command('r.clump',input=Listmapspath+"_patch",output=Listmapspath+"_patch_clump",overwrite = True)
  expression12=Listmapspath+"_patch_clump_mata="+Listmapspath+"_patch_clump*"+Listmapspath
  grass.mapcalc(expression12, overwrite = True, quiet = True)
  expression13=Listmapspath+"_patch_clump_mata_limpa=if("+Listmapspath+"_patch_clump_mata>0,"+Listmapspath+"_patch_clump_mata,null())"
  rulesreclass(Listmapspath+"_patch_clump_mata_limpa")
  grass.mapcalc(expression13, overwrite = True, quiet = True)
  #r.colors map=$i"_patch_clump_mata_limpa" color=random
  
  #grass.run_command('r.reclass',input=Listmapspath+"_patch_clump_mata_limpa",output=Listmapspath+"_patch_clump_mata_limpa_AreaHA",rules=nametxtreclass,overwrite = True)
  grass.run_command('g.remove',flags='f',rast='A,MapaBinario,MapaBinario_A,MapaBinario_AB,MapaBinario_ABC,MapaBinario_ABCD')  




lista_rasts=grass.mlist_grouped ('rast', pattern='*0250*') ['PERMANENT']
temp=lista_rasts[0:2]
for i in temp:

      out_bin=i+'bin'
      expressao_mata=out_bin+'=if('+i+'==14 |'+i+'==13,'+i+',0)'
     # grass.mapcalc(expressao_mata, overwrite = True, quiet = True)
      #print expressao_mata
      pacthSingle(out_bin)
    #print frags