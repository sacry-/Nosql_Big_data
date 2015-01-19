import mongo

good = ["sweden", "norway", "netherlands", "germany", "australia", "canada", "new zealand", "switzerland", "japan", "south korea", "singapore", "denmark"]
bad = ["sudan", "afghanistan", "mauritania", "libya", "ethiopia", "colombia", "peru", "senegal", "chad", "rwanda", "bangladesh", "pakistan"]

indicators = [
  # indicator, good countries, bad countries
  ("women_who_believe_a_husband_is_justified_in_beating_his_wife_when_she_goes_out_without_telling_him", good, bad),
  ("women_who_believe_a_husband_is_justified_in_beating_his_wife_any_of_five_reasons", good, bad),
  ("unmet_need_for_contraception_of_married_women_ages_15_49", good, bad),
  ("teenage_mothers_of_women_ages_15_19_who_have_had_children_or_are_currently_pregnant", good, bad),
  ("school_enrollment_preprimary_gross", good, bad), 
  ("unemployment_with_primary_education_of_total_unemployment", good, bad),
  ("unemployment_with_secondary_education_of_total_unemployment", good, bad),
  ("unemployment_total_of_total_labor_force_national_estimate", good, bad),
  ("tuberculosis_case_detection_rate_all_forms", good, bad),
  ("trained_teachers_in_primary_education_of_total_teachers", good, bad),
  ("telephone_lines_per_100_people", good, bad),
  ("roads_total_network_km", good, bad),
  ("public_spending_on_education_total_of_gdp", good, bad),
  ("prevalence_of_undernourishment_of_population", good, bad),
  ("prevalence_of_hiv_total_of_population_ages_15_49", good, bad),
  ("number_of_infant_deaths", good, bad),
  ("number_of_maternal_deaths", good, bad),
  ("number_of_neonatal_deaths", good, bad),
  ("number_of_under_five_deaths", good, bad),
  ("newborns_protected_against_tetanus", good, bad),
  ("net_official_development_assistance_and_official_aid_received_current_us", good, bad),
  ("mortality_rate_under_5_per_1_000_live_births", good, bad),
  ("mortality_rate_infant_per_1_000_live_births", good, bad),
  ("literacy_rate_adult_total_of_people_ages_15_and_above", good, bad),
  ("life_expectancy_at_birth_total_years", good, bad),
  ("firms_with_female_top_manager_of_firms", good, bad),
  ("firms_with_female_participation_in_ownership_of_firms", good, bad),
  ("prevalence_of_wasting_of_children_under_5", good, bad),
  ("poverty_headcount_ratio_at_national_poverty_lines_of_population", good, bad),
  ("military_expenditure_current_lcu", good, bad),
  ("military_expenditure_of_central_government_expenditure", good, bad),
  ("military_expenditure_of_gdp", good, bad),
  ("prevalence_of_severe_wasting_weight_for_height_female_of_children_under_5", good, bad),
  ("prevalence_of_severe_wasting_weight_for_height_male_of_children_under_5", good, bad),
  ("prevalence_of_severe_wasting_weight_for_height_of_children_under_5", good, bad),
  ("losses_due_to_theft_robbery_vandalism_and_arson_sales", good, bad),
  ("long_term_unemployment_of_total_unemployment", good, bad),
  ("investment_in_energy_with_private_participation_current_us", good, bad),
  ("investment_in_telecoms_with_private_participation_current_us", good, bad),
  ("investment_in_transport_with_private_participation_current_us", good, bad),
  ("investment_in_water_and_sanitation_with_private_participation_current_us", good, bad),
  ("health_expenditure_total_of_gdp", good, bad),
  ("gini_index", good, bad),
  ("gni_ppp_current_international", good, bad),
  ("employment_to_population_ratio_15_total_modeled_ilo_estimate", good, bad),
  ("employment_to_population_ratio_15_total_national_estimate", good, bad)
]

def average(data):
  years = data["years"]
  result, c = 0.0, 0.0
  for entry in years:
    for year, num in entry.items():
      try:
        num = float(num)
        result += num
        c += 1
      except:
        pass
  return result / c

def average_list(l):
  try:
    return sum(l) / len(l)
  except:
    return 0

def interpret(mdb, indicators):
  result = {}
  for (indicator, goods, bads) in indicators:
    coll = mdb.get(indicator)
    data = mongo.time_series_query(coll)
    g, b = [], []
    for entry in data:
      if entry["country"].lower() in goods:
        g.append( average(entry) )
      if entry["country"].lower() in bads:
        b.append( average(entry) )
    g = average_list(g)
    b = average_list(b)

    good_countries, bad_countries = [], []
    for entry in data:
      c = entry["country"]
      a = average(entry)
      near_to_g = a - g 
      near_to_b = a - b 
      print near_to_b
      if near_to_g < near_to_b:
        good_countries.append( c )
      else:
        bad_countries.append ( c ) 
  return result


mdb = mongo.MongoDB("wdi_data")
mongo.test_mongo(mdb)


interpret(mdb, indicators)

