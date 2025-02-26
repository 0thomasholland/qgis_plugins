-- outputs 'locality_name 8fig_UTM_coordinates  unit_name plane_type strike/dip dip_direction (as cardinal)'
-- e.g. '06E 3817 8963  Upper Slate  Bedding 296/45 NE'

concat(
right("localityName",3), ' ', 
left(right(round("x", 0),5), 4), ' ', 
left(right(round("y", 0), 5), 4), ' ', 
"unitId", ' ',
"planeType", ' ',
round("strike",0), '/', 
round("dip", 0), ' ',
CASE WHEN "dipAzimuth" >= 337.5 OR "dipAzimuth" < 22.5 THEN 'N' WHEN "dipAzimuth" >= 22.5 AND "dipAzimuth" < 67.5 THEN 'NE' WHEN "dipAzimuth" >= 67.5 AND "dipAzimuth" < 112.5 THEN 'E' WHEN "dipAzimuth" >= 112.5 AND "dipAzimuth" < 157.5 THEN 'SE' WHEN "dipAzimuth" >= 157.5 AND "dipAzimuth" < 202.5 THEN 'S' WHEN "dipAzimuth" >= 202.5 AND "dipAzimuth" < 247.5 THEN 'SW' WHEN "dipAzimuth" >= 247.5 AND "dipAzimuth" < 292.5 THEN 'W' WHEN "dipAzimuth" >= 292.5 AND "dipAzimuth" < 337.5 THEN 'NW' END)
