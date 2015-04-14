import grass.script as grass
import os

def heterogeneidade(i):
    grass.run_command('g.region',rast=i)
    stats=grass.read_command('r.stats',input=i)
    ListStats=stats.split('\n')
    #print ListStats
    del ListStats[-1]
    del ListStats[-1]
    lista_multplos2=[]
    y=0
    #print len(ListStats)
    while len(ListStats)>=y:
        if y==0:
            resulti=1
        else:
            resulti=resulti*2
        lista_multplos2.append(resulti)
        y=y+1
    cont_reclasse=0
    lista_jucao_final=[]
    for sts in ListStats:
        formatname='000000'+`lista_multplos2[cont_reclasse]`
        #print formatname
        formatname=formatname[-5:]
        #print formatname
        expressao1=i+'_'+formatname+'_bin=if('+i+"=="+sts+","+`lista_multplos2[cont_reclasse]`+',0)'
        #print expressao1
        grass.mapcalc(expressao1, overwrite = True, quiet = True)
        expressao2=i+'_'+formatname+'_bin_int=int('+i+'_'+formatname+'_bin)'
        grass.mapcalc(expressao2, overwrite = True, quiet = True)
        grass.run_command('g.region',rast=i+'_'+formatname+'_bin_int')
        grass.run_command('r.neighbors',input=i+'_'+formatname+'_bin_int',out=i+'_'+formatname+'_bin_int_dila_50m',method='maximum',size=5,overwrite = True)
        cont_reclasse=cont_reclasse+1
        grass.run_command('g.remove',flags='f',rast=i+'_'+formatname+'_bin')
        lista_jucao_final.append(i+'_'+formatname+'_bin_int_dila_50m') 
        
    grass.run_command('r.series',input=lista_jucao_final,out='temp',overwrite = True,method='sum')
    expressao3=i+'_MapaHet_FINAL=int(if('+i+'>0,temp,null()))'
    grass.mapcalc(expressao3, overwrite = True, quiet = True)  
    grass.run_command('g.remove',flags='f',rast='temp')
    grass.run_command('r.colors',map=i+'_MapaHet_FINAL',color='random')
    grass.run_command('r.out.gdal',input=i+'_MapaHet_FINAL',out=i+'_MapaHet_FINAL.tif')
    for rm in lista_jucao_final:
        grass.run_command('g.remove',flags='f',rast=rm)  
    
    
    lista_remove=grass.mlist_grouped ('rast', pattern='*bin_int*') ['PERMANENT']
    for a in lista_remove:
        grass.run_command('g.remove',flags='f',rast=a) 
        
        


def createtxtED(mapa):
    grass.run_command('g.region',rast=mapa)
    x=grass.read_command('r.stats',flags='a',input=mapa)
    y=x.split('\n')
    os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
    #nome
    txtreclass=open(mapa+'.txt','w')
    txtreclass.write('class'',''COD'',''A_M2'',''PCT\n')
    classe=['Matrix','EDGE','CORE']
    cont_class=0
    #print y
    del y[-1]
    del y[-1]
   # print y
    if y!=0:
        acumula=0
        for i in y:
            split=i.split(' ')
            split=float(split[1]) 
            acumula=acumula+split    
            #print acumula
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
                    m2=f[1]
                    m2=float(m2)
                
                
                
                    pct=m2/acumula*100
                    pct=round(pct,2)
                    
                    txtreclass.write(classe[cont_class]+','+`ids`+','+`m2`+','+`pct`+'\n')
                    cont_class=cont_class+1
          
        txtreclass.close()
  


def mapcalcED(expresao):
    grass.mapcalc(expresao, overwrite = True, quiet = True)  

  
def create_EDGE_single(ListmapsED):
    grass.run_command('g.region',rast=ListmapsED)
    expressao2='mapa_bin=if('+ListmapsED+'>0,1,0)'
    grass.mapcalc(expressao2, overwrite = True, quiet = True)  
    grass.run_command('r.neighbors',input='mapa_bin',output=ListmapsED+"_eroED_50m",method='minimum',size=5,overwrite = True)
    inputs=ListmapsED+"_eroED_50m,mapa_bin"
    out=ListmapsED+"_eroED_50m_EDGE"
    grass.run_command('r.series',input=inputs,out=out,method='sum',overwrite = True)
    espressaoEd=ListmapsED+'_eroED_50m_EDGE_FINAL=int('+ListmapsED+"_eroED_50m_EDGE)"
    mapcalcED(espressaoEd)
    createtxtED(ListmapsED+'_eroED_50m_EDGE_FINAL')
    grass.run_command('g.remove',flags='f',rast='mapa_bin,'+ListmapsED+"_eroED"','+ListmapsED+"_eroED_50m_EDGE,"+ListmapsED+"_eroED_50m")  



#create_EDGE_single('ARV_pts_buffer_0250_extracByMask_rast_imgbin')
def mean(mapa_mean):
    grass.run_command('g.region',rast=mapa_mean)
    mean=grass.read_command('r.univar',map=mapa_mean,fs='comma')
    mean_split=mean.split('\n')
    #print mean_split[9]
    mean_split_write=mean_split[9].replace('mean: ','')
    namesaidatxt=mapa_mean.replace("_extracByMask_rast_imgbin_patch_clump_mata_limpa_AreaHA",'_Mean_FLT.txt')
    os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
    txt=open(namesaidatxt,'w')
    cabecalho='Mean\n'
    txt.write(cabecalho)
    txt.write(mean_split_write)
    txt.close()
    
  

#mean('ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa_AreaHA')
def pct_flt(mapa_bin,mapa_limpo):
   
  
  
    # pct
    grass.run_command('g.region',rast=mapa_bin)
    nome_saida_pct=mapa_bin.replace('extracByMask_rast_imgbin','DENSITY_PCT_FLT.txt')
    x=grass.read_command('r.stats',input=mapa_bin,fs='comma',flags='nap')
    #print x
     
    y=x.split('\n')
    del y[-1]  
    #print y
    os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
      
    txt=open(nome_saida_pct,'w')
    cabecalho='id'',''area_m2'',''pct'',''density\n'
    txt.write(cabecalho)
    #laco pra pegar a soma
    acumula=0
    for i in y:
        split=i.split('c')
        acumula=acumula+float(split[1])
    #print acumula
    
    #cont_n_frags
    grass.run_command('g.region',rast=mapa_limpo)
    nome_saida=mapa_limpo.replace('extracByMask_rast_imgbin_patch_clump_mata_limpa','reclass.txt')
    x=grass.read_command('r.stats',input=mapa_limpo,fs='comma',flags='l')
    nfrag_split=x.split('\n')
    del nfrag_split[-1];del nfrag_split[-1]
    nfrags=lenNfrags=len(nfrag_split)   
    densidade=nfrags/acumula
    
    #laco pra pegar p pct
    
    for i in y:
        split=i.split('c')
        id=split[0]
        m2=float(split[1])
        pct=round(float(split[1])/acumula*100,3)
        
        txt.write(id+','+`m2`+','+`pct`+','+`densidade`+'\n')
    txt.close() 

#pct_flt('ARV_pts_buffer_0250_extracByMask_rast_imgbin','ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa')




def rulesreclass(mapa_limpo):

    grass.run_command('g.region',rast=mapa_limpo)
    nome_saida=mapa_limpo.replace('extracByMask_rast_imgbin_patch_clump_mata_limpa','reclass.txt')
    x=grass.read_command('r.stats',input=mapa_limpo,fs='comma',flags='na')
    #print x
     
    y=x.split('\n')
    del y[-1]
    os.chdir(r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados")
    
    txt=open(nome_saida,'w')
    
    
    for i in y:
        split=i.split('c')
         
        id=split[0]
        m2=float(split[1])
        ha=(m2/10000)+1
        txt.write(id+'='+`ha`+'\n')
      
    txt.close()
    return nome_saida
    
    
  
    
    
    
  #rulesreclass('ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa')
  
def pacthSingle(Listmapspath):
    y=0
    
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
    grass.mapcalc(expression13, overwrite = True, quiet = True)
    txt_reclass=rulesreclass(Listmapspath+"_patch_clump_mata_limpa")
    grass.run_command('r.reclass',input=Listmapspath+"_patch_clump_mata_limpa",output=Listmapspath+"_patch_clump_mata_limpa_AreaHA",rules=txt_reclass,overwrite = True)
    mean(Listmapspath+"_patch_clump_mata_limpa_AreaHA")
    pct_flt(Listmapspath,Listmapspath+"_patch_clump_mata_limpa")
    grass.run_command('g.remove',flags='f',rast='A,MapaBinario,MapaBinario_A,MapaBinario_AB,MapaBinario_ABC,MapaBinario_ABCD')  
    os.remove(txt_reclass)


lista_rasts=grass.mlist_grouped ('rast', pattern='*0250*') ['PERMANENT']
temp=lista_rasts[0:2]
for i in temp:
    out_bin=i+'bin'
    expressao_mata=out_bin+'=if('+i+'==14 |'+i+'==13,'+i+',0)'
    grass.run_command('g.region',rast=i)
    grass.mapcalc(expressao_mata, overwrite = True, quiet = True)
    #print expressao_mata
    create_EDGE_single(out_bin)
    pacthSingle(out_bin)
    heterogeneidade(i)
    
  ##print frags