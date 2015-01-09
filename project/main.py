# Un Daten
# World Bank Daten
# CIA Daten


#Populate Redis with UnData
import rediss
import parsing
import undata
import json

rundata = rediss.RUnData()
indicator_population = undata.UnDataIndicator("undata_population.xml","population")
indicator_gpi_tertiary = undata.UnDataIndicator("undata_gpi_tertiary.xml","gpi_tertiary")
indicator_gpi_secondary = undata.UnDataIndicator("undata_gpi_secondary.xml","gpi_secondary")
indicator_gpi_primary = undata.UnDataIndicator("undata_gpi_primary.xml","gpi_primary")
indicator_internetusers = undata.UnDataIndicator("undata_internetusers.xml","internetusers")

#print indicator.data
rundata.puts(indicator_population.data)
rundata.puts(indicator_gpi_tertiary.data)
rundata.puts(indicator_gpi_secondary.data)
rundata.puts(indicator_gpi_primary.data)
rundata.puts(indicator_internetusers.data)

germany = rundata.values_by_pattern("Germany.*")
keys_germany = rundata.keys("Germany.*")
for item in germany:
    print item

#print "key", germany , "key"