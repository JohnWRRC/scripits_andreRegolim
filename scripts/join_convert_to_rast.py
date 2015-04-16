# join tables
import arcpy
from arcpy import env
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14"
fc=arcpy.ListFeatureClasses()
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join"
for i in fc:
    inp=i.replace('.shp','')
    out=inp+'_Join'
    arcpy.AddJoin_management( inp, "CLASSE", "legenda.csv", "CLASSE")
    arcpy.CopyFeatures_management(inp,out)
    arcpy.DeleteField_management(out,'legenda_cs')
    arcpy.AddField_management(out, 'COD', "SHORT",10)
    arcpy.CalculateField_management(out,"COD","!legenda__1!","PYTHON")
    arcpy.DeleteField_management(out,'legenda__1')
    
    
#vector to raster
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join"
fc=arcpy.ListFeatureClasses()
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters"
for i in fc:
    inp=i.replace('.shp','')
    out=inp+'_rast.img'
    arcpy.PolygonToRaster_conversion(inp,"COD",out,"CELL_CENTER","NONE",5)



#-----------------------------------------------------------------------------------------------------------------------------------------
# consertando PL
arcpy.env.extent = "734883.014988 7101052.500931 741216.421047 7110192.000000"
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters"
arcpy.PolygonToRaster_conversion("PI_pts_buf2k_v0","COD",'PI_pts_buf2k_v0_rast.img',"CELL_CENTER","NONE",5)












  
#create buffer 250,500,1000,1500  
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Todos_os_pontos"
fc=arcpy.ListFeatureClasses()
env.workspace = "F:\data\Andre_regolin\Shapes_AndreRegolin\Buffers_250_500_1000_1500"

escalas=[250,500,1000,1500]

for i in fc:
    inp=i.replace('.shp','')
    #arcpy.AddField_management(inp, 'dissolv', "SHORT",10)

    for a in escalas:
        formato='000'+`a`
        formato=formato[-4:]
        
        out=inp+'_buffer_'+formato
        print inp
        arcpy.CalculateField_management(inp,"dissolv",1,"PYTHON")
        arcpy.Buffer_analysis(inp,out,a,"FULL","ROUND","ALL","dissolv")
        
#extract by mask 
# join tables
import arcpy
from arcpy import env
#arcpy.env.extent = "343557.189089385 7051410.09946609 345677.189089385 7052830.09946609"
env.workspace = r"F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters"
rt=arcpy.ListRasters()
env.workspace = r"F:\data\Andre_regolin\Shapes_AndreRegolin\Buffers_250_500_1000_1500\temp"
fc=arcpy.ListFeatureClasses()
env.workspace = r"F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters_extract"
cont=0
for i in fc:
    inp=i.replace(".shp",'')
    out=inp+'extracByMask_rast.img'
    cond=i[0:8]
    
    for a in rt:
        if cond in a:
            print i,"*",a

            arcpy.gp.ExtractByMask_sa(a, inp , out)
    
    
    

        
        
import arcpy
from arcpy import env
raster="CA_pts_selecionados_buf2km_Join_rast.img"
env.workspace = r"F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14"
fc_temp=arcpy.ListFeatureClasses()
ca_2000=[]
for i in fc_temp:
    if "CA" in i:
        ca_2000.append(i)
        inp=i.replace(".shp",'')
        print inp
        out_mask=inp+'_extracByMask_rast.img'
        arcpy.gp.ExtractByMask_sa(raster, inp , out_mask)
    
lisa_ca=[]
env.workspace = r"F:\data\Andre_regolin\Shapes_AndreRegolin\Todos_os_pontos"
escalas=[250,500,1000,1500]
fc=arcpy.ListFeatureClasses()
env.workspace=r"F:\data\Andre_regolin\Shapes_AndreRegolin\Mapas_finalizados_2015_03_d14\Mapas_finaliazdos_join_rasters_extract\temp"

for i in fc:
    if "CA" in i:
        inp=i.replace(".shp",'')
        arcpy.AddField_management(i, 'dissolv', "SHORT",10)
        for a in escalas:
            formato='000'+`a`
            formato=formato[-4:]
            out=inp+'_buffer_'+formato
            #print out
            out_mask=out+'_extracByMask_rast.img'
            #print out_mask
            #print inp
            arcpy.CalculateField_management(inp,"dissolv",1,"PYTHON")
            arcpy.Buffer_analysis(inp,out,a,"FULL","ROUND","ALL","dissolv")
            arcpy.gp.ExtractByMask_sa(raster, out , out_mask)
        
        


        
        
    
