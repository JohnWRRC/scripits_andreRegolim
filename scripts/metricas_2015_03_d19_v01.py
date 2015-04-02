import grass.script as grass
import os
def createtxtED(mapa):
  grass.run_command('g.region',rast=mapa)
  x=grass.read_command('r.stats',flags='a',input=mapa)
  y=x.split('\n')
  os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
  txtsaida=mapa+'PCT_Borda.txt'
  txtreclass=open(mapa+'_EDGE.txt','w')
  
  txtreclass.write('COD'',''HA\n')
  if y!=0:
  
    for i in y:
      if i !='':
        ##print i
        f=i.split(' ')
        if '*' in f :
          break
        else:
          ##print f
          ids=f[0]
          ids=int(ids)
          ##print ids
          ha=f[1]
          ha=float(ha)
          haint=int(ha)
          haint=haint/10000+1
          ##print haint
          
          ##print haint
          
          txtreclass.write(`ids`+','+`haint`+'\n')
    
    txtreclass.close()



def mapcalcED(expresao):
  grass.mapcalc(expresao, overwrite = True, quiet = True)  

  
def create_EDGE_single(ListmapsED):
  grass.run_command('g.region',rast=ListmapsED)
  expressao2='mapa_bin=if('+ListmapsED+'>0,1,0)'
  grass.mapcalc(expressao2, overwrite = True, quiet = True)  
  grass.run_command('r.neighbors',input='mapa_bin',output=ListmapsED+"_eroED_50m",method='minimum',size=5,overwrite = True)
  inputs=ListmapsED+"_eroED_50m,"+ListmapsED
  out=ListmapsED+"_eroED_50m_EDGE"
  grass.run_command('r.series',input=inputs,out=out,method='sum',overwrite = True)
  espressaoEd=ListmapsED+'_eroED_50m_EDGE_FINAL=int('+ListmapsED+"_eroED_50m_EDGE)"
  mapcalcED(espressaoEd)
  createtxtED(ListmapsED+'_eroED_50m_EDGE_FINAL')
  ##grass.run_command('g.remove',flags='f',rast=ListmapsED+"_eroED_"+`apoioname`+'m,'+ListmapsED+'_EDGE'+`apoioname`+'m')  



create_EDGE_single('ARV_pts_buffer_0250_extracByMask_rast_imgbin')
#def mean(mapa_mean):
  #grass.run_command('g.region',rast=mapa_mean)
  #mean=grass.read_command('r.univar',map=mapa_mean,fs='comma')
  #mean_split=mean.split('\n')
  ##print mean_split[9]
  #mean_split_write=mean_split[9].replace('mean: ','')
  #namesaidatxt=mapa_mean.replace("_extracByMask_rast_imgbin_patch_clump_mata_limpa_AreaHA",'_Mean_FLT.txt')
  #os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
  #txt=open(namesaidatxt,'w')
  #cabecalho='Mean\n'
  #txt.write(cabecalho)
  #txt.write(mean_split_write)
  #txt.close()
  
  

##mean('ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa_AreaHA')
#def pct_flt(mapa_bin,mapa_limpo):
   
  
  
  ## pct
  #grass.run_command('g.region',rast=mapa_bin)
  #nome_saida_pct=mapa_bin.replace('extracByMask_rast_imgbin','DENSITY_PCT_FLT.txt')
  #x=grass.read_command('r.stats',input=mapa_bin,fs='comma',flags='nap')
  ##print x
   
  #y=x.split('\n')
  #del y[-1]  
  ##print y
  #os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
    
  #txt=open(nome_saida_pct,'w')
  #cabecalho='id'',''area_m2'',''pct'',''density\n'
  #txt.write(cabecalho)
  ##laco pra pegar a soma
  #acumula=0
  #for i in y:
      #split=i.split('c')
      #acumula=acumula+float(split[1])
  ##print acumula
  
  ##cont_n_frags
  #grass.run_command('g.region',rast=mapa_limpo)
  #nome_saida=mapa_limpo.replace('extracByMask_rast_imgbin_patch_clump_mata_limpa','reclass.txt')
  #x=grass.read_command('r.stats',input=mapa_limpo,fs='comma',flags='l')
  #nfrag_split=x.split('\n')
  #del nfrag_split[-1];del nfrag_split[-1]
  #nfrags=lenNfrags=len(nfrag_split)   
  #densidade=nfrags/acumula
  
  ##laco pra pegar p pct
  
  #for i in y:
    #split=i.split('c')
    #id=split[0]
    #m2=float(split[1])
    #pct=round(float(split[1])/acumula*100,3)
    
    #txt.write(id+','+`m2`+','+`pct`+','+`densidade`+'\n')
  #txt.close() 

##pct_flt('ARV_pts_buffer_0250_extracByMask_rast_imgbin','ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa')




#def rulesreclass(mapa_limpo):

  #grass.run_command('g.region',rast=mapa_limpo)
  #nome_saida=mapa_limpo.replace('extracByMask_rast_imgbin_patch_clump_mata_limpa','reclass.txt')
  #x=grass.read_command('r.stats',input=mapa_limpo,fs='comma',flags='na')
  ##print x
   
  #y=x.split('\n')
  #del y[-1]
  #os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
  
  #txt=open(nome_saida,'w')
  
  
  #for i in y:
    #split=i.split('c')
     
    #id=split[0]
    #m2=float(split[1])
    #ha=(m2/10000)+1
    #txt.write(id+'='+`ha`+'\n')
    
  #txt.close()
  #return nome_saida
  
  

  
  
  
#rulesreclass('ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa')

#def pacthSingle(Listmapspath):
  #y=0
  
  #grass.run_command('g.region',rast=Listmapspath)
  #expression1="MapaBinario="+Listmapspath
  #grass.mapcalc(expression1, overwrite = True, quiet = True)    
 
  #expression2="A=MapaBinario"
  #grass.mapcalc(expression2, overwrite = True, quiet = True)
  
  ##r.colors map=A color=wave
  #expression3="MapaBinario_A=if(A[0,0]==0 && A[0,-1]==1 && A[1,-1]==0 && A[1,0]==1,1,A)"
  #grass.mapcalc(expression3, overwrite = True, quiet = True)
  #expression4="A=MapaBinario_A"
  #grass.mapcalc(expression4, overwrite = True, quiet = True)
  #expression5="MapaBinario_AB=if(A[0,0]==0 && A[-1,0]==1 && A[-1,1]==0 && A[0,1]==1,1,A)"
  #grass.mapcalc(expression5, overwrite = True, quiet = True) 
  #expression6="A=MapaBinario_AB"
  #grass.mapcalc(expression6, overwrite = True, quiet = True)
  #expression7="MapaBinario_ABC=if(A[0,0]==0 && A[0,1]==1 && A[1,1]==0 && A[1,0]==1,1,A)"
  #grass.mapcalc(expression7, overwrite = True, quiet = True)
  #expression8="A=MapaBinario_ABC"
  #grass.mapcalc(expression8, overwrite = True, quiet = True)
  #expression9="MapaBinario_ABCD=if(A[0,0]==0 && A[1,0]==1 && A[1,1]==0 && A[0,1]==1,1,A)"
  #grass.mapcalc(expression9, overwrite = True, quiet = True)
  #expression10="A=MapaBinario_ABCD"
  #grass.mapcalc(expression10, overwrite = True, quiet = True)
  #expression11=Listmapspath+"_patch=A"
  #grass.mapcalc(expression11, overwrite = True, quiet = True)
  ##r.colors map=$i"_patch" color=random
  #grass.run_command('r.clump',input=Listmapspath+"_patch",output=Listmapspath+"_patch_clump",overwrite = True)
  #expression12=Listmapspath+"_patch_clump_mata="+Listmapspath+"_patch_clump*"+Listmapspath
  #grass.mapcalc(expression12, overwrite = True, quiet = True)
  #expression13=Listmapspath+"_patch_clump_mata_limpa=if("+Listmapspath+"_patch_clump_mata>0,"+Listmapspath+"_patch_clump_mata,null())"
  #grass.mapcalc(expression13, overwrite = True, quiet = True)
  #txt_reclass=rulesreclass(Listmapspath+"_patch_clump_mata_limpa")
  #grass.run_command('r.reclass',input=Listmapspath+"_patch_clump_mata_limpa",output=Listmapspath+"_patch_clump_mata_limpa_AreaHA",rules=txt_reclass,overwrite = True)
  #mean(Listmapspath+"_patch_clump_mata_limpa_AreaHA")
  #pct_flt(Listmapspath,Listmapspath+"_patch_clump_mata_limpa")
  #grass.run_command('g.remove',flags='f',rast='A,MapaBinario,MapaBinario_A,MapaBinario_AB,MapaBinario_ABC,MapaBinario_ABCD')  
  #os.remove(txt_reclass)


#lista_rasts=grass.mlist_grouped ('rast', pattern='*0250*') ['PERMANENT']
#temp=lista_rasts[0:2]
#for i in temp:
      #out_bin=i+'bin'
      #expressao_mata=out_bin+'=if('+i+'==14 |'+i+'==13,'+i+',0)'
      #grass.run_command('g.region',rast=i)
      #grass.mapcalc(expressao_mata, overwrite = True, quiet = True)
      ##print expressao_mata
      #create_EDGE_single(out_bin)
      #pacthSingle(out_bin)
    ###print frags