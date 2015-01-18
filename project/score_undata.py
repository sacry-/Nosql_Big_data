import sys
import rediss
import parsing
import undata
import json
from operator import itemgetter, attrgetter

rundata = rediss.RUnData()

germany = rundata.values_by_pattern("Germany.*")
keys_germany = rundata.keys("Germany.*")



indicators_germany = []

score_schema = {
        #Environment
        "environment_water": {"value_type":"percent","value_key":"Value","good":"high","weight":10.0},
        "environment_sanitation_facilities": {"value_type":"percent","value_key":"Value","good":"high","weight":10.0},
        "environment_forest":{"value_type":"percent","value_key":"Value","good":"high","weight":0.0},#Nicht Wichtig
        "environment_kg_co2_per_1usd_gdp":{"value_type":"percent_points","value_key":"Value","good":"low","weight":5.0},
        #Population
        "population_fertility_rate":{"value_type":"percent","value_key":"Value","good":"high","weight":3.0},
        #Gender
        "gender_gpi_primary":{"value_type":"percent_points","value_key":"Value","good":"high","weight":5.0},
        "gender_gpi_secondary":{"value_type":"percent_points","value_key":"Value","good":"high","weight":5.0},
        "gender_gpi_tertiary":{"value_type":"percent_points","value_key":"Value","good":"low","weight":5.0},
        "gender_seats_women_in_parliament_percent":{"value_type":"percent","value_key":"Value","good":"high","weight":5.0},
        #Education
        "education_tertiary":{"value_type":"absolute","value_key":"Observation Value","filter":{"Sex":"All genders"},"good":"high","weight":10.0},
        "education_primary":{"value_type":"absolute","value_key":"Observation Value","filter":{"Sex":"All genders"},"good":"high","weight":10.0},
        "education_total_secondary_net_enrolment_rate":{"value_type":"percent","value_key":"Observation Value","filter":{"Sex":"All genders"},"good":"high","weight":10.0},
        #Culture and communication
        "communication_internetusers":{"value_type":"percent","value_key":"Value","good":"high","weight":5.0},
        "communication_number_daily_newspapers_per_1mio":{"value_type":"percent_points","value_key":"Observation Value","good":"high","weight":5.0},
        "communication_mobile_subscriptions_per_100":{"value_type":"percent","value_key":"Value","good":"high","weight":5.0},
        "communication_telephone_subscriptions_per_100":{"value_type":"percent","value_key":"Value","good":"high","weight":5.0},
        # National accounts and industrial production
        "ind_prod_gpd_usd":{"value_type":"absolute","value_key":"Value","value_factor":0.0001,"good":"high","weight":1.0},
        "ind_prod_gni_ppp_usd":{"value_type":"absolute","value_key":"Value","value_factor":0.0001,"good":"high","weight":1.0},
        #Labour force
        "labour_unemployment_general_level":{"value_type":"absolute","value_key":"Value","value_factor":1000,"filter":{"Sex":"Total men and women"},"good":"high","weight":10.0},#hier mal 1000 weil der value in 1000 schritten angegeben ist
        #Wages and prices
        "wages_prices_wages":{"value_type":"percent","value_key":"Value","filter":{"Sex":"Total men and women"},"good":"high","weight":0.0},#nicht berechnet! kaum ein land hat diesen wert,
        #Manufacturing:
        #"manufacturing_beer":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_tobacco":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.0001},
        #"manufacturing_woven_woolen_fabrics":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_woven_cotton_fabrics":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_footwear_leather_uppers":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_pesticides":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_pigiron_spiegeleisen":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_radio_receivers":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_tv_receivers":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_cars":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_household":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_tools":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001},
        #"manufacturing_trucks":{"value_type":"absolute","value_key":"Value","value_factor":1000000,"filter":{"Unit":"Mil. USD"},"good":"high","weight":0.001}
  }

indicator_population = "population_total"
indicator_density = "population_density_km2"        

def calculate_stats(year):

  for indicator,schema in score_schema.iteritems():
    #Calculating AVG for alls countrys
    #indicator_dict = undata.key_to_dict(indicator)
    value_sum = 0
    entrys = 0
    value_max = 0
    value_min = float("inf")

    pattern = "*."+indicator+"."+str(year)
    key_dict = undata.key_to_dict(pattern)
    key_dict["year"] = find_nearest_year(key_dict)
    pattern = undata.dict_to_key(key_dict)

    for key in rundata.keys(pattern):
      value = find_value(undata.key_to_dict(key))
      if value==0 or value:
        value_sum += value
        entrys += 1
        if value < value_min:
          value_min = value
        if value > value_max:
          value_max = value

    if entrys>50: 
      score_schema[indicator]["max"] = value_max
      score_schema[indicator]["min"] = value_min
      avg = value_sum/entrys
      score_schema[indicator]["avg"] = avg
      print "%d entrys for: %s (max: %f / min: %f / avg: %f)" % (entrys, pattern, value_max, value_min, avg)
    else:
      print "%d entrys for: %s" % (entrys,pattern)

def find_nearest_year(key_dict):
  year = False
  max_diff = 5
  if rundata.get_key(undata.dict_to_key(key_dict)):
    year = key_dict["year"]
  else:
    for key in rundata.keys(key_dict["country"]+"."+key_dict["indicator"]+".*"):
      curr_key_dict = undata.key_to_dict(key)
      diff = abs(curr_key_dict["year"]-key_dict["year"])
      if diff<max_diff:
        year = curr_key_dict["year"]
        max_diff = diff
  
  
  return year


def convert_value(value_type,value_factor,value,country,year):
  value = float(value)
  value = value * value_factor
  if value_type == "absolute":
      population = get_population(country,year)
      if population:
        #wenn value_type = "absolute" durch poplation teilen und mal 100 nehmen
        return float((value/population)*100)
      else:
        return False
  elif value_type == "percent_points":
    #wenn value_type = "percent_points" dann vor gewichtung mal 100 nehmen
    return float(value*100)
  elif value_type == "percent":
    return float(value)  


#finds value and convert for key_dict
def find_value(key_dict):
  indicator = key_dict["indicator"]
  value_key = score_schema[indicator]["value_key"]
  value_type = score_schema[indicator]["value_type"]
  if "value_factor" in score_schema[indicator]:
    value_factor = score_schema[indicator]["value_factor"]
  else:
    value_factor = 1

  filter_exists = "filter" in score_schema[indicator]

  data = rundata.get_key(undata.dict_to_key(key_dict))
  
  for entry in data:
    if value_key in entry:
      if filter_exists:
        condition = True
        for condition_key,condition_val in score_schema[indicator]["filter"].iteritems():
          if not (condition_key in entry and entry[condition_key]==condition_val):
            condition = False
        if condition:
          return convert_value(value_type,value_factor,entry[value_key],key_dict["country"],key_dict["year"])
      else:
        return convert_value(value_type,value_factor,entry[value_key],key_dict["country"],key_dict["year"])
  return False



def get_population(country,year):
  key_dict = dict()
  key_dict["indicator"] = indicator_population
  key_dict["country"] = country
  key_dict["year"] = year
  key_dict["year"] = find_nearest_year(key_dict)
  key = undata.dict_to_key(key_dict)
  population = rundata.get_key(key)
  if len(population)>0:
    return float(population[0]["Value"])*1000 # mal 1000, da in der Datenbank in 1000 schritten abgespeichert
  else:
    return False

def calculate_points(schema,value):
  points = False
  if "avg" in schema:
    if schema["weight"]!=0:
      if schema["good"] == "high":
        points = value-schema["avg"]
      elif schema["good"] == "low":
        points = schema["avg"]-value
      points = points * schema["weight"]    
  return points

def points_for_country(country,year):
  key_dict = dict()
  key_dict["country"] = country
  key_dict["year"] = year
  
  result = dict()

  for indicator,schema in score_schema.iteritems():
    key_dict["indicator"] = indicator
    key_dict["year"] = year
    key_dict["year"] = find_nearest_year(key_dict)
    value = False

    result[indicator] = dict()

    if key_dict["year"]:
      value = find_value(key_dict)
      if value==0 or value:
        result[indicator]["value"] = value
        points = calculate_points(schema,value)
        if points:
          result[indicator]["points"] = points
        #print "%s get %f Points for %s value: %f" % (country,points,indicator,value)
    
    if value!=0 and not value:
      result[indicator] = False
      #print "no indicator %s for %s" % (indicator,country)

  return result
  
def print_points_country(country,year):
  indicator_count = 0
  points_sum = 0

  for indicator,data in points_for_country(country,year).iteritems():
    if "points" in data:
      indicator_count += 1
      points_sum += data["points"]
      print "%s get %f Points for %s value: %f" % (country,data["points"],indicator,data["value"])  
    else:
      print "no data for indicator %s" % (indicator)
  print "============================"
  relativ_points = (points_sum/indicator_count)
  print "%s got %f Points with %d indicators" % (country,relativ_points,indicator_count)   


def all_year_points_for_country(country,start,end):
  result = dict()
  for year in range(start,end):
    calculate_stats(year)
    points_sum = 0
    indicator_count = 0
    for indicator,data in points_for_country(country,year).iteritems(): 
      if "points" in data: 
        points_sum += data["points"]
        indicator_count+=1
    if indicator_count:    
      result[year] = (points_sum/indicator_count)     
  return result   

def print_all_year_points_for_country(country,start,end):
  all_year_points = all_year_points_for_country(country,start,end)
  print "Points for %s from %d to %d:" % (country,start,end)
  for year,points in all_year_points.iteritems():
    print "%d: %f" % (year,points)
        
def points_all_countrys(year):   
  countrys = set()
  countrys_without_points = list()
  for key in rundata.keys("*"):
    key_dict = undata.key_to_dict(key)
    countrys.add(key_dict["country"])
  
  
  country_points = dict()
  country_indicator_count = dict()

  result = dict()

  for country in countrys:
    points_sum = 0
    indicator_count = 0
    key_dict = dict()
    key_dict["country"] = country
    key_dict["year"] = year

    for indicator,schema in score_schema.iteritems():
      if "avg" in schema:
        key_dict["indicator"] = indicator
        key_dict["year"] = year
        key_dict["year"] = find_nearest_year(key_dict)

        if key_dict["year"]:
          value = find_value(key_dict)

          #Value kann Float oder False sein, da 0==False wird vorher auf 0 ueberprueft  
          if value==0 or value:
            points = calculate_points(schema,value)
            if points:
              indicator_count += 1
              points_sum += points
  
    result[country] = dict()
    if indicator_count:
      result[country]["relativ_points"] = points_sum/indicator_count
    else:
      result[country]["relativ_points"] = 0

    result[country]["points"] = points_sum
    result[country]["indicator_count"] = indicator_count
      
  return result  
  #print "Countrys without Points (less then 10 indicators):"
  #print countrys_without_points    

def print_points_all_countrys(year):
  country_points = points_all_countrys(year)

  countrys_sorted_by_points = sorted(country_points.items(), key=lambda x:x[1]['relativ_points'], reverse=True)
  
  for country,data in countrys_sorted_by_points:
    indicator_count = data["indicator_count"]
    relativ_points = data["relativ_points"]
    if indicator_count>=10:
      print "%s got %f Points with %d indicators" % (country,relativ_points,indicator_count)


calculate_stats(2011)     
#print_points_for_country("Germany",2011)
print_points_all_countrys(2011)
#print_all_year_points_for_country("Germany",2005,2016)
#print_points_country("Germany",2011)
#points_for_country("Qatar",2011)
#points_for_country("Afghanistan",2011)
#points_for_country("India",2011)


#for country in countrys:
  #stats_for_country(country,2011)
#stats_for_country("Germany",2011)
#print score_schema
#for key in keys_germany:
#  indicator = key.split(".")
#  print  indicator[1]