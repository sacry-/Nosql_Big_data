import mongo


indicators = [
  # indicator, good countries, bad countries
  ("women_who_believe_a_husband_is_justified_in_beating_his_wife_when_she_goes_out_without_telling_him", [""], [""]),
  ("women_who_believe_a_husband_is_justified_in_beating_his_wife_any_of_five_reasons", [""], [""]),
  ("unmet_need_for_contraception_of_married_women_ages_15_49", [""], [""]),
  ("teenage_mothers_of_women_ages_15_19_who_have_had_children_or_are_currently_pregnant", [""], [""]),
  ("school_enrollment_preprimary_gross", [""], [""]), 
  ("unemployment_with_primary_education_of_total_unemployment", [""], [""]),
  ("unemployment_with_secondary_education_of_total_unemployment", [""], [""]),
  ("unemployment_total_of_total_labor_force_national_estimate", [""], [""]),
  ("tuberculosis_case_detection_rate_all_forms", [""], [""]),
  ("trained_teachers_in_primary_education_of_total_teachers", [""], [""]),
  ("telephone_lines_per_100_people", [""], [""]),
  ("roads_total_network_km", [""], [""]),
  ("public_spending_on_education_total_of_gdp", [""], [""]),
  ("prevalence_of_undernourishment_of_population", [""], [""]),
  ("prevalence_of_hiv_total_of_population_ages_15_49", [""], [""]),
  ("number_of_infant_deaths", [""], [""]),
  ("number_of_maternal_deaths", [""], [""]),
  ("number_of_neonatal_deaths", [""], [""]),
  ("number_of_under_five_deaths", [""], [""]),
  ("newborns_protected_against_tetanus", [""], [""]),
  ("net_official_development_assistance_and_official_aid_received_current_us", [""], [""]),
  ("mortality_rate_under_5_per_1_000_live_births", [""], [""]),
  ("mortality_rate_infant_per_1_000_live_births", [""], [""]),
  ("literacy_rate_adult_total_of_people_ages_15_and_above", [""], [""]),
  ("life_expectancy_at_birth_total_years", [""], [""]),
  ("firms_with_female_top_manager_of_firms", [""], [""]),
  ("firms_with_female_participation_in_ownership_of_firms", [""], [""]),
  ("prevalence_of_wasting_of_children_under_5", [""], [""]),
  ("poverty_headcount_ratio_at_national_poverty_lines_of_population", [""], [""]),
  ("military_expenditure_current_lcu", [""], [""]),
  ("military_expenditure_of_central_government_expenditure", [""], [""]),
  ("military_expenditure_of_gdp", [""], [""]),
  ("prevalence_of_severe_wasting_weight_for_height_female_of_children_under_5", [""], [""]),
  ("prevalence_of_severe_wasting_weight_for_height_male_of_children_under_5", [""], [""]),
  ("prevalence_of_severe_wasting_weight_for_height_of_children_under_5", [""], [""]),
  ("losses_due_to_theft_robbery_vandalism_and_arson_sales", [""], [""]),
  ("long_term_unemployment_of_total_unemployment", [""], [""]),
  ("investment_in_energy_with_private_participation_current_us", [""], [""]),
  ("investment_in_telecoms_with_private_participation_current_us", [""], [""]),
  ("investment_in_transport_with_private_participation_current_us", [""], [""]),
  ("investment_in_water_and_sanitation_with_private_participation_current_us", [""], [""]),
  ("health_expenditure_total_of_gdp", [""], [""]),
  ("gini_index", [""], [""]),
  ("gni_ppp_current_international", [""], [""]),
  ("employment_to_population_ratio_15_total_modeled_ilo_estimate", [""], [""]),
  ("employment_to_population_ratio_15_total_national_estimate", [""], [""])
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

def interpret(mdb, indicators):
  result = {}
  for (indicator, goods, bads) in indicators:
    coll = mdb.get(indicator)
    data = mongo.time_series_query(coll)
    g, b = [], []
    for entry in data:
      if entry["country"] in goods:
        g.append( average(entry) )
      if entry["country"] in bads:
        b.append( average(entry) )
    g = sum(g) / len(g)
    b = sum(b) / len(b)

    for entry in data:
      pass
  return result


mdb = mongo.MongoDB("wdi_data")
mongo.test_mongo(mdb)


interpret(mdb, indicators)





