Steps:

Download FAO shapefiles from:

Southeast Asia - http://www.fao.org/geonetwork/srv/en/main.home?uuid=ee616dc4-3118-4d67-ba05-6e93dd3e962f
Near East - http://www.fao.org/geonetwork/srv/en/main.home?uuid=7ae00a40-642b-4637-b1d3-ffacb13360db
Australia & New Zealand - http://www.fao.org/geonetwork/srv/en/main.home?uuid=a1a0e9ee-5062-4950-a6b9-fdd2284b2607
Africa - http://www.fao.org/geonetwork/srv/en/main.home?uuid=e54e2014-d23b-402b-8e73-c827628d17f4
Europe - http://www.fao.org/geonetwork/srv/en/main.home?uuid=1849e279-67bd-4e6f-a789-9918925a11a1
South America - http://www.fao.org/geonetwork/srv/en/main.home?uuid=d47ba28e-31be-470d-81cf-ad3d5594fafd
Central America - http://www.fao.org/geonetwork/srv/en/main.home?uuid=bc9139e6-ccc9-4ded-a0c4-93b91cb54dde
North America - http://ref.data.fao.org/map?entryId=b06dc828-3166-461a-a17d-26f4dc9f9819

Merged using QGIS, MMQGIS (Import with Latin-1 encoding!, FAO Specifies UTF-8 but this is WRONG!)

Create a negative buffer in QGIS with -0.005 degree radius (to avoid weird touching polygons)(UTF-8)

add unique Identifyer column in Qgis (random integer called rID2)

Join in ArcGIS (settings below) 

Exported as: hybas6JoinedFAOV02.shp            old(Hybas6_joinedWithFAONamesV01.shp)

save as csv using QGIS (UTF-8): hybas6JoinedFAOV02.csv


# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "hybas_merged_custom_level6_V02", "hydrobasins_FAO_globalV02Buffer005"
arcpy.SpatialJoin_analysis(target_features="hybas_merged_custom_level6_V02", join_features="hydrobasins_FAO_globalV02Buffer005", out_feature_class="C:/Users/Rutger.Hofste/Desktop/werkmap/testJoin02Intersect.shp", join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping='HYBAS_ID "HYBAS_ID" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,HYBAS_ID,-1,-1;NEXT_DOWN "NEXT_DOWN" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,NEXT_DOWN,-1,-1;NEXT_SINK "NEXT_SINK" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,NEXT_SINK,-1,-1;MAIN_BAS "MAIN_BAS" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,MAIN_BAS,-1,-1;DIST_SINK "DIST_SINK" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,DIST_SINK,-1,-1;DIST_MAIN "DIST_MAIN" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,DIST_MAIN,-1,-1;SUB_AREA "SUB_AREA" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,SUB_AREA,-1,-1;UP_AREA "UP_AREA" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,UP_AREA,-1,-1;PFAF_ID "PFAF_ID" true true false 10 Long 0 10 ,First,#,hybas_merged_custom_level6_V02,PFAF_ID,-1,-1;ENDO "ENDO" true true false 10 Long 0 10 ,First,#,hybas_merged_custom_level6_V02,ENDO,-1,-1;COAST "COAST" true true false 10 Long 0 10 ,First,#,hybas_merged_custom_level6_V02,COAST,-1,-1;ORDER_ "ORDER_" true true false 10 Long 0 10 ,First,#,hybas_merged_custom_level6_V02,ORDER_,-1,-1;SORT "SORT" true true false 19 Double 11 18 ,First,#,hybas_merged_custom_level6_V02,SORT,-1,-1;SUB_BAS "SUB_BAS" true true false 9 Long 0 9 ,First,#,hydrobasins_FAO_globalV02Buffer005,SUB_BAS,-1,-1;TO_BAS "TO_BAS" true true false 9 Long 0 9 ,First,#,hydrobasins_FAO_globalV02Buffer005,TO_BAS,-1,-1;MAJ_BAS "MAJ_BAS" true true false 9 Long 0 9 ,First,#,hydrobasins_FAO_globalV02Buffer005,MAJ_BAS,-1,-1;SUB_NAME "SUB_NAME" true true false 75 Text 0 0 ,First,#,hydrobasins_FAO_globalV02Buffer005,SUB_NAME,-1,-1;MAJ_NAME "MAJ_NAME" true true false 75 Text 0 0 ,First,#,hydrobasins_FAO_globalV02Buffer005,MAJ_NAME,-1,-1;SUB_AREA_1 "SUB_AREA_1" true true false 9 Long 0 9 ,First,#,hydrobasins_FAO_globalV02Buffer005,SUB_AREA,-1,-1;MAJ_AREA "MAJ_AREA" true true false 9 Long 0 9 ,First,#,hydrobasins_FAO_globalV02Buffer005,MAJ_AREA,-1,-1;LEGEND "LEGEND" true true false 4 Short 0 4 ,First,#,hydrobasins_FAO_globalV02Buffer005,LEGEND,-1,-1', match_option="INTERSECT", search_radius="", distance_field_name="")

Unfortunately it turned out that some of the FAO data was not dissolved (damn you FAO), dissolving polygons and repeating all steps

Dissolve in QGIS as batch process on SUB_BAS

Renamed basins with no Name to "SUB_NAME missing" and MAJ_NAME missing" in QGIS
