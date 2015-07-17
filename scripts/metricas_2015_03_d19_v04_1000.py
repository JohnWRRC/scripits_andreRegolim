import grass.script as grass
import os
import math

#tem que definir o diretotio de saida
outputfolder=r"E:\data_2015\Andre_regolin\Shapes_AndreRegolin\___Resultados\1000"

#------------------------------------------------------------------------------------------------------------------------------
# calcula a  area de cada classe "nao-floresta"/area total da paisagem.
def indice_antropi(i):
    # criando o nome do txt
    nome=i.replace('extracByMask_rast_img','')
    #-----------------------------------------
    
    # setando caminho de saida
    os.chdir(outputfolder)
    grass.run_command('g.region', rast=i)
    #-----------------------------------------
    # criando mapa retirando mapa retirando a floresta
    expressao1='mapa_antrop=if('+i+'!=13 && '+i+ '!=14,'+i+',0)'
    grass.mapcalc(expressao1, overwrite = True, quiet = True)
    #-----------------------------------------
    #pegando as classes do mapa de nao mata
    stats=grass.read_command('r.stats',input="mapa_antrop",flags='a')
    ListStats=stats.split('\n')
    
    del ListStats[-1]
    del ListStats[-1]
    #-----------------------------------------
    # criando o acumulado de area
    acumula=0
    for i in ListStats:
        
        split=i.split(' ')
        split=float(split[1]) 
        acumula=acumula+split    
    
    #-----------------------------------------
    
    
    # arbindo txt de AreaClass_div_areaTot 
    txt=open(nome+'AreaClass_div_areaTot.txt','w')
    txt.write('Class'',''Metrica\n')    

    for i in ListStats:
        #print i
        split=i.split(' ')
        ids=split[0]
        if ids!='0':
            
            m2=float(split[1])
            area_class=m2/acumula
            area_class=round(area_class,3)
            txt.write(ids+','+`area_class`+'\n')
            
    #-----------------------------------------
    txt.close()


#usando pra teste
##indice_antropi("AI_pts_buffer_0250_extracByMask_rast_img")
#-----------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------
#essa def cria o mapa de heterogeneidade
#onde pega o mapa original etrai todas as suas classes
#cria um novo codigo utilizando multiplos de 2
#ex:
#11=1
#12=2
#13=4
#-----------------------------------------
def heterogeneidade(i):
    grass.run_command('g.region',rast=i)
    # extraindo apensa as classes do mapa
    stats=grass.read_command('r.stats',input=i)
    ListStats=stats.split('\n')
    #-----------------------------------------
    
    
    del ListStats[-1]
    del ListStats[-1]
    lista_multplos2=[]
    #controlado de laco
    y=0
    #---------------------
    
    # criando multplos de 2
    while len(ListStats)>=y:
        if y==0:
            resulti=1
        else:
            resulti=resulti*2
        lista_multplos2.append(resulti)
        y=y+1
    #-----------------------------------------
    
    # controla as classes
    cont_reclasse=0
    lista_jucao_final=[]
    #-----------------------------------------
    
    # esse laco separa cada classe em um mapa
    #dissolv de acordo com aescala
    # e junta tudo no final
    for sts in ListStats:
        #formatando nome de saida
        formatname='000000'+`lista_multplos2[cont_reclasse]`
        
        formatname=formatname[-5:]
        #---------------------------------------------------------------
        
        # criando um mapa para cada classe
        expressao1=i+'_'+formatname+'_bin=if('+i+"=="+sts+","+`lista_multplos2[cont_reclasse]`+',0)'
        
        grass.mapcalc(expressao1, overwrite = True, quiet = True)
        #--------------------------------------------------------
        
        # criando mapa inteiro 
        expressao2=i+'_'+formatname+'_bin_int=int('+i+'_'+formatname+'_bin)'
        grass.mapcalc(expressao2, overwrite = True, quiet = True)
        #--------------------------------------------------
        
        # fazendo a dilatacao
        grass.run_command('g.region',rast=i+'_'+formatname+'_bin_int')
        grass.run_command('r.neighbors',input=i+'_'+formatname+'_bin_int',out=i+'_'+formatname+'_bin_int_dila_50m',method='maximum',size=5,overwrite = True)
        #------------------------
        cont_reclasse=cont_reclasse+1
        
        #removendo mapa de apoio
        grass.run_command('g.remove',flags='f',rast=i+'_'+formatname+'_bin')
        
        #--------------------------------------------------
        
        #incrementando alista de mapas
        lista_jucao_final.append(i+'_'+formatname+'_bin_int_dila_50m') 
        #---------------------------------------------
    
    #somando mapas    
    grass.run_command('r.series',input=lista_jucao_final,out='temp',overwrite = True,method='sum')
    #-------------------------
    
    # criando map inteiro e clipando
    expressao3=i+'_MapaHet_FINAL=int(if('+i+'>0,temp,null()))'
    grass.mapcalc(expressao3, overwrite = True, quiet = True)  
    #--------------------------------------------
    
    #removendo mapa de apoio 
    grass.run_command('g.remove',flags='f',rast='temp')
    
    #atribuindo cor    
    grass.run_command('r.colors',map=i+'_MapaHet_FINAL',color='random')
    #------------------------------------------
    
    
   # exportando mapa
    grass.run_command('r.out.gdal',input=i+'_MapaHet_FINAL',out=i+'_MapaHet_FINAL.tif')
    #------------------------------------------
    
    #removendo mapas
    for rm in lista_jucao_final:
        grass.run_command('g.remove',flags='f',rast=rm)  
    
    # removendo mapas
    lista_remove=grass.mlist_grouped ('rast', pattern='*bin_int*') ['PERMANENT']
    for a in lista_remove:
        grass.run_command('g.remove',flags='f',rast=a) 
        
        

#---------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------#

 #nessa def sera o txt com as infos dos mapas de borda
 #area em M2 e PCT
#--------------------------------------------------
def createtxtED(mapa):
    pct_edge=0
    grass.run_command('g.region',rast=mapa)
    x=grass.read_command('r.stats',flags='a',input=mapa)
    y=x.split('\n')
    os.chdir(outputfolder)
    nome=mapa.replace("extracByMask_rast_imgbin_eroED_50m_EDGE_FINAL",'')
    
    txtreclass=open(nome+'PCT_EDGE.txt','w')
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
                # indice de matheron
                
                if ids==1:
                    pct_edge=m2/acumula*100
                    pct_edge=round(pct_edge,2)
                if ids==2:
                    pctflt=m2/acumula*100
                    pctflt=round(pctflt,2)
                    txt_Matheron=open(nome+'_Matheron.txt','w')
                    if pct_edge>0:
                        txt_Matheron.write('Matheron\n')
                        #pct de edge por pct de flt
                        Matheron=pct_edge/pctflt
                        txt_Matheron.write(`Matheron`)
                    txt_Matheron.close()
                        
                    
        txtreclass.close()
  

#complemento da def
def mapcalcED(expresao):
    grass.mapcalc(expresao, overwrite = True, quiet = True)  
#-----------------------------------
#essa def cria o mapa de bordas  
def create_EDGE_single(ListmapsED):
    grass.run_command('g.region',rast=ListmapsED)
    expressao2='mapa_bin=if('+ListmapsED+'>0,1,0)'
    grass.mapcalc(expressao2, overwrite = True, quiet = True)  
    grass.run_command('r.neighbors',input='mapa_bin',output=ListmapsED+"_eroED_50m",method='minimum',size=5,overwrite = True)
    inputs=ListmapsED+"_eroED_50m,mapa_bin"
    out=ListmapsED+"_eroED_50m_EDGE"
    grass.run_command('r.series',input=inputs,out='temp',method='sum',overwrite = True)
    expressao_clip=ListmapsED+"_eroED_50m_EDGE=if("+ListmapsED+">=0,temp,null())"
    grass.mapcalc(expressao_clip, overwrite = True, quiet = True)  
    espressaoEd=ListmapsED+'_eroED_50m_EDGE_FINAL=int('+ListmapsED+"_eroED_50m_EDGE)"
    mapcalcED(espressaoEd)
    createtxtED(ListmapsED+'_eroED_50m_EDGE_FINAL')
    grass.run_command('g.remove',flags='f',rast='mapa_bin,'+ListmapsED+"_eroED"','+ListmapsED+"_eroED_50m_EDGE,"+ListmapsED+"_eroED_50m")  



#create_EDGE_single('ARV_pts_buffer_0250_extracByMask_rast_imgbin')

#---------------------------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------

#essa def cria o txt com o tamanho media dos fragmentos por paisagem
def mean(mapa_mean):
    grass.run_command('g.region',rast=mapa_mean)
    mean=grass.read_command('r.univar',map=mapa_mean,fs='comma')
    mean_split=mean.split('\n')
    #print mean_split[9]
    mean_split_write=mean_split[9].replace('mean: ','')
    namesaidatxt=mapa_mean.replace("_extracByMask_rast_imgbin_patch_clump_mata_limpa_AreaHA",'_Mean_size_patch.txt')
    os.chdir(outputfolder)
    txt=open(namesaidatxt,'w')
    cabecalho='Mean\n'
    txt.write(cabecalho)
    txt.write(mean_split_write)
    txt.close()
    
  

##mean('ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa_AreaHA')

#---------------------------------------------------------------------------------------------------------------------------------






#---------------------------------------------------------------------------------------------------------------------------------
# nesse bloco existem duas metricas juntas.
# onde e calculado a pct de floresta
# e area de floresta/area total da paisagem;
#-------------------------------------------------
def pct_flt(mapa_bin,mapa_limpo):
    
    #definindo a regiao de trabalho
    grass.run_command('g.region',rast=mapa_bin)
    #--------------------------------------------
    
    #criando nome de saida para p txt 
    nome_saida_pct=mapa_bin.replace('extracByMask_rast_imgbin','DENSITY_PCT_FLT.txt')
    nome_saida_Are_p_Floresta=mapa_bin.replace('extracByMask_rast_imgbin','AreaFLT_sob_TOT.txt')
    #-------------------------------------------------------
    
    # exatrindo as classes do raster
    x=grass.read_command('r.stats',input=mapa_bin,fs='comma',flags='nap')
    #------------------------------------------------
    
    # tratamento de string 
    y=x.split('\n')
    del y[-1]  
    #----------------------------------------------------
    
    # mundanmdo diretorio de saida
    os.chdir(outputfolder)
    #---------------------------------------------------------

       
    
    #abrindo o txt de saida
    txt=open(nome_saida_pct,'w')
    #---------------------------------
    
    # escrevendo o cabecalho do txt
    cabecalho='id'',''area_m2'',''pct'',''density\n'
    txt.write(cabecalho)
    #----------------------------------
    
    # acumlando areas
    acumula=0
    for i in y:
        split=i.split('c')
        acumula=acumula+float(split[1])
    
    
    #abrindo txt areaflt/areato 
    txt_areafltPareatot=open(nome_saida_Are_p_Floresta,'w')
    #gravando cabecalho
    cabecalho2='id'',''M2'',''AFLT_ATT\n'
    txt_areafltPareatot.write(cabecalho2)
    #----------------------------------
    
    # calculando areaflt/areatot
    for i in y:
        split=i.split('c')
        id=split[0]
        if id!='0':
            m2=float(split[1])
            areafltPareatot=m2/acumula   
            areafltPareatot=round( areafltPareatot,3)
            # gravando txt
            txt_areafltPareatot.write(id+','+`m2`+','+`areafltPareatot`+'\n')
        #----------------------------------
          
    
    txt_areafltPareatot.close();
    #----------------------------------
    
    #redefinindo regiao
    grass.run_command('g.region',rast=mapa_limpo)
    #----------------------------------
    
    # nomde de saida do mapa
    nome_saida=mapa_limpo.replace('extracByMask_rast_imgbin_patch_clump_mata_limpa','reclass.txt')
    #----------------------------------
    
    #extraidno os fragementos dos mapas para contar quantos tem por paisagem
    x=grass.read_command('r.stats',input=mapa_limpo,fs='comma',flags='l')
    #----------------------------------
    
    #criando um lista 
    nfrag_split=x.split('\n')
    #----------------------------------
    
    #removendo os dois ultimos item que sao vazis
    del nfrag_split[-1];del nfrag_split[-1]
    #----------------------------------
    
    #pegando  quantos frags tem na lista
    nfrags=lenNfrags=len(nfrag_split) 
    #----------------------------------
    
    #calculando a desidade
    densidade=nfrags/acumula
    
    #----------------------------------
    
    
    # calculando a pct 
    for i in y:
        split=i.split('c')
        id=split[0]
        m2=float(split[1])
        pct=round(float(split[1])/acumula*100,3)
        
        # gravando txt
        txt.write(id+','+`m2`+','+`pct`+','+`densidade`+'\n')
        #----------------------------------
    txt.close() 

#pct_flt('ARV_pts_buffer_0250_extracByMask_rast_imgbin','ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa')

#---------------------------------------------------------------------------------------------------------------------------------





#---------------------------------------------------------------------------------------------------------------------------------

#essa def cria o txt de reclassificao para gerar o mapa de area
def rulesreclass(mapa_limpo):

    grass.run_command('g.region',rast=mapa_limpo)
    nome_saida=mapa_limpo.replace('extracByMask_rast_imgbin_patch_clump_mata_limpa','reclass.txt')
    x=grass.read_command('r.stats',input=mapa_limpo,fs='comma',flags='na')
    #print x
     
    y=x.split('\n')
    del y[-1]
    os.chdir(outputfolder)
    
    txt=open(nome_saida,'w')
    
    
    for i in y:
        split=i.split('c')
         
        id=split[0]
        m2=float(split[1])
        ha=(m2/10000)+1
        txt.write(id+'='+`ha`+'\n')
      
    txt.close()
    return nome_saida
  #------------------------------------------------------------------ 
    
  
    
    
    
#rulesreclass('ARV_pts_buffer_0250_extracByMask_rast_imgbin_patch_clump_mata_limpa')

#---------------------------------------------------------------------------------------------------------------------------------






#---------------------------------------------------------------------------------------------------------------------------------

# essa defe calcula area para cada fragmento
# cria mapa de ids
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
    #os.remove(txt_reclass)
#---------------------------------------------------------------------------------------------------------------------------------





#---------------------------------------------------------------------------------------------------------------------------------
lista_rasts=grass.mlist_grouped ('rast', pattern='*1000*') ['PERMANENT']

for i in lista_rasts:
    out_bin=i+'bin'
    expressao_mata=out_bin+'=if('+i+'==14 |'+i+'==13,'+i+',0)'
    grass.run_command('g.region',rast=i)
    grass.mapcalc(expressao_mata, overwrite = True, quiet = True)
    #print expressao_mata
    create_EDGE_single(out_bin)
    pacthSingle(out_bin)
    heterogeneidade(i)
    indice_antropi(i)
    
  #print frags