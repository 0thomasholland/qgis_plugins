-- takes an azimuth point and converts to eigth cardinal/intercardinal directions
-- e.g. 090 -> "E", 150 -> SE
-- NB this is Azimuth NOT Strike Values
-- for field move "Azimuth" needs to be converted to "dipAzimuth"

CASE 
  WHEN "Azimuth" >= 337.5 OR "Azimuth" < 22.5 THEN 'N' 
  WHEN "Azimuth" >= 22.5 AND "Azimuth" < 67.5 THEN 'NE' 
  WHEN "Azimuth" >= 67.5 AND "Azimuth" < 112.5 THEN 'E' 
  WHEN "Azimuth" >= 112.5 AND "Azimuth" < 157.5 THEN 'SE' 
  WHEN "Azimuth" >= 157.5 AND "Azimuth" < 202.5 THEN 'S' 
  WHEN "Azimuth" >= 202.5 AND "Azimuth" < 247.5 THEN 'SW' 
  WHEN "Azimuth" >= 247.5 AND "Azimuth" < 292.5 THEN 'W' 
  WHEN "Azimuth" >= 292.5 AND "Azimuth" < 337.5 THEN 'NW' 
END
