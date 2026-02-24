import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON

# ------------------------------
# SPARQL Endpoint Configuration
# ------------------------------
sparql = SPARQLWrapper("http://localhost:3030/agri/query")

def query_ontology(sparql_query):
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        st.error(f"SPARQL Query Error: {e}")
        return []

# ------------------------------
# Streamlit Page Setup
# ------------------------------
st.set_page_config(page_title="Smart Farm Monitoring", layout="wide")
st.title("🌾 Smart Farm Monitoring System")

# ------------------------------
# Sidebar for User Input
# ------------------------------
st.sidebar.header("Farm Query Options")

# Fetch all crop individuals dynamically
crop_individuals_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sasfo: <http://www.example.org/sasfo#>
SELECT ?cropInd WHERE {
  ?cropInd rdf:type sasfo:Crop .
}
"""
crop_individuals_results = query_ontology(crop_individuals_query)
crop_options = [c["cropInd"]["value"].split("#")[-1] for c in crop_individuals_results]

# Dropdown for selecting crop individual
crop = st.sidebar.selectbox("Select Crop", crop_options)

# Dropdown for selecting nutrient deficiency
nutrient = st.sidebar.selectbox("Select Nutrient Deficiency", ["Nitrogen", "Phosphorus", "Potassium"])

# Refresh button
if st.sidebar.button("Refresh"):
    st.experimental_rerun()

# ------------------------------
# Show Nutrient Deficiency of Selected Crop
# ------------------------------
deficiency_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sasfo: <http://www.example.org/sasfo#>
SELECT ?nutrientDef WHERE {{
  sasfo:{crop} sasfo:requiresNutrient ?nutrientDef .
}}
"""
deficiency_results = query_ontology(deficiency_query)

st.subheader(f"⚠️ Nutrient Deficiencies for {crop}:")
if deficiency_results:
    for d in deficiency_results:
        nutrient_name = d["nutrientDef"]["value"].split("#")[-1]
        st.warning(f"{nutrient_name}")
else:
    st.success("No nutrient deficiencies reported for this crop.")

# ------------------------------
# Fertilizer Recommendation
# ------------------------------
fert_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sasfo: <http://www.example.org/sasfo#>
SELECT ?fertilizer ?percentage WHERE {{
  ?fertilizer rdf:type sasfo:Fertilizer .
  ?fertilizer sasfo:treatsDeficiency ?nutrient .
  ?nutrient rdf:type sasfo:{nutrient} .
  OPTIONAL {{ ?fertilizer sasfo:hasNutrientPercentage ?percentage }}
}}
"""
fert_results = query_ontology(fert_query)

st.subheader(f"💡 Recommended Fertilizers for {nutrient} Deficiency:")
if fert_results:
    for res in fert_results:
        name = res["fertilizer"]["value"].split("#")[-1]
        percentage = res.get("percentage", {}).get("value", "N/A")
        st.markdown(f"- **{name}** (Nutrient %: {percentage})")
else:
    st.info("No fertilizers found for this nutrient deficiency.")

# ------------------------------
# Pest Warnings
# ------------------------------
pest_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sasfo: <http://www.example.org/sasfo#>
SELECT ?pest WHERE {{
  sasfo:{crop} sasfo:affectedByPest ?pest .
}}
"""
pests = query_ontology(pest_query)

st.subheader(f"⚠️ Pest Warnings for {crop}:")
if pests:
    for p in pests:
        pest_name = p["pest"]["value"].split("#")[-1]
        st.warning(f"{pest_name} detected!")
else:
    st.success(f"No pests reported for {crop}.")

# ------------------------------
# Soil and Climate Indicators
# ------------------------------
soil_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sasfo: <http://www.example.org/sasfo#>
SELECT ?soil ?moisture ?ph WHERE {{
  sasfo:{crop} sasfo:growsInSoil ?soil .
  ?soil sasfo:hasMoistureLevel ?moisture ;
        sasfo:hasPHLevel ?ph .
}}
"""
soil_results = query_ontology(soil_query)

climate_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sasfo: <http://www.example.org/sasfo#>
SELECT ?climate ?rainfall ?temperature WHERE {{
  sasfo:{crop} sasfo:suitableClimate ?climate .
  OPTIONAL {{ ?climate sasfo:hasRainfallValue ?rainfall }}
  OPTIONAL {{ ?climate sasfo:hasTemperatureValue ?temperature }}
}}
"""
climate_results = query_ontology(climate_query)

# Soil Indicators
st.subheader("🌱 Soil Conditions")
if soil_results:
    for s in soil_results:
        soil_name = s["soil"]["value"].split("#")[-1]
        moisture = float(s.get("moisture", {}).get("value", 0))
        ph = float(s.get("ph", {}).get("value", 0))
        moisture_color = "green" if 40 <= moisture <= 60 else "orange" if 30 <= moisture < 40 or 60 < moisture <= 70 else "red"
        ph_color = "green" if 5.5 <= ph <= 7.0 else "orange" if 5.0 <= ph < 5.5 or 7.0 < ph <= 7.5 else "red"
        st.markdown(f"- **{soil_name}** | Moisture: <span style='color:{moisture_color}'>{moisture}%</span> | pH: <span style='color:{ph_color}'>{ph}</span>", unsafe_allow_html=True)
else:
    st.info("No soil information available.")

# Climate Indicators
st.subheader("☀️ Climate Conditions")
if climate_results:
    for c in climate_results:
        climate_name = c["climate"]["value"].split("#")[-1]

        # Convert rainfall and temperature safely
        try:
            rainfall = float(c.get("rainfall", {}).get("value", 0))
        except (ValueError, TypeError):
            rainfall = None

        try:
            temperature = float(c.get("temperature", {}).get("value", 0))
        except (ValueError, TypeError):
            temperature = None

        # Determine colors with checks for None
        if rainfall is not None:
            if 800 <= rainfall <= 2500:
                rainfall_color = "green"
            elif 500 <= rainfall < 800 or 2500 < rainfall <= 3000:
                rainfall_color = "orange"
            else:
                rainfall_color = "red"
            rainfall_str = f"<span style='color:{rainfall_color}'>{rainfall}</span> mm"
        else:
            rainfall_str = "N/A"

        if temperature is not None:
            if 20 <= temperature <= 30:
                temp_color = "green"
            elif 15 <= temperature < 20 or 30 < temperature <= 35:
                temp_color = "orange"
            else:
                temp_color = "red"
            temp_str = f"<span style='color:{temp_color}'>{temperature}</span> °C"
        else:
            temp_str = "N/A"

        st.markdown(f"- **{climate_name}** | Rainfall: {rainfall_str} | Temperature: {temp_str}", unsafe_allow_html=True)
else:
    st.info("No climate information available.")