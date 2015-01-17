import mongo


bad = [
  "women_who_believe_a_husband_is_justified_in_beating_his_wife_when_she_goes_out_without_telling_him", 
  "women_who_believe_a_husband_is_justified_in_beating_his_wife_any_of_five_reasons",
  "unmet_need_for_contraception_of_married_women_ages_15_49",
  "teenage_mothers_of_women_ages_15_19_who_have_had_children_or_are_currently_pregnant",
  "school_enrollment_preprimary_gross"
]

mdb = mongo.MongoDB("wdi_data")
mongo.test_mongo(mdb)

def contains(s, coll):
  return all([s.find(w) != -1 for w in coll])

cool_indicators = []
for collection in mdb.collections():
  if contains(collection, ["employment", "female"]):
    cool_indicators.append( collection )

print cool_indicators