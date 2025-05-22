import streamlit as st
import pandas as pd
from io import BytesIO
from xlsxwriter import Workbook
from datetime import datetime

# Initialize session state for the main data
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Date", "Wood Species", "Wood Collection Location", 
        "Wood Collection Zone", "Supplied Mill", "SUPPLIER PO RATE", "SUB SUPPLIER WB RATE", 
        "Freight","Other Expenses", "Balance", "Company Stock (in ASMT)","No_of_Trucks(Average)"
    ])
# Title
st.title("Weekly Wood Price Index - Paper Mills")
# Tab layout for entry and categorized display
tab1, tab2 = st.tabs(["Weekly Wood Price Index", "Transport rates"])
with tab1:
    # Input fields and form layout
    col1, col2 = st.columns(2)
    with col1:
        # Date Selection
        date = st.date_input("Select Date")        
        # Wood Species Selection
        st.markdown("### Select Wood Species:")
        wood_species = st.selectbox(
            "Select Wood Species:",
            ["Select Wood Species"] + ["Acacia Wood Debarked","Bamboo","Casurina Wood","DeBark Subabul", "Gliricidia with Bark Wood","Melia Dubia Wood With Bark","With Bark Subabul", "With Bark Eucalyptus", "Debark Eucalyptus","Veneer Waste","Wood Rolls","Wood Waste","Wood Chips"]
        )        
        # Dropdown for Wood Price Source
        # wood_price_source = st.selectbox(
        #     "Select Wood Price Source:",
        #     ["Select Wood Price Source"] + ["CPM Unit", "SPM Unit", "JKPM Unit"]
        # )        
        # State and District Selection
        zones = ["Zone 1", "Zone 2", "Zone 3"]
        state_district_map = {
            "Maharashtra": sorted(["Ahmednagar", "Akola", "Amravati", "Aurangabad", "Beed", "Bhandara", "Buldhana", "Chandrapur", "Dhule", 
                    "Gadchiroli", "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban", 
                    "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani", "Pune", "Raigad", 
                    "Ratnagiri", "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"]),
    "Telangana": sorted(["Telangana","Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", "Jayashankar Bhoopalpally", 
                  "Jogulamba Gadwal", "Kamareddy", "Karimnagar", "Khammam", "Komaram Bheem", "Mahabubabad", "Mahabubnagar", 
                  "Mancherial", "Medak", "Medchal", "Nagarkurnool", "Nalgonda", "Nirmal", "Nizamabad", "Peddapalli", 
                  "Rajanna Sircilla", "Ranga Reddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
                  "Warangal Rural", "Warangal Urban", "Yadadri Bhuvanagiri"]),
    "Karnataka": sorted(["Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban", "Bidar", "Chamarajanagar", 
                  "Chikballapur", "Chikkamagaluru", "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", 
                  "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru", "Raichur", "Ramanagara", 
                  "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"]),
    "Andhra Pradesh": sorted(["Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool", "Nellore", "Prakasam", 
                       "Srikakulam", "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa","Tirupati", "Ongole"]),
    "Odisha"   :  sorted(["Angul","Balangir","Bargarh","Deogarh","Dhenkanal","Jharsuguda","Kendujhar","Sambalpur","Subarnapur",
                          "Sundargarh","Balasore","Bhadrak","Cuttack","Jagatsinghpur","Jajpur","Kendrapada","Khordha","Mayurbhanj","Nayagarh	Puri","Boudh","Gajapati","Ganjam","Kalahandi","Kandhamal","Koraput","Malkangiri","Nabarangpur","Nuapada","Rayagada"]),
    "Tamil Nadu": sorted(["Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kanchipuram", "Kanyakumari", 
                   "Karur", "Madurai", "Nagapattinam", "Namakkal", "Perambalur", "Pudukkottai", "Ramanathapuram", "Salem", 
                   "Sivaganga", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tiruppur", "Tiruvallur", 
                   "Tiruvannamalai", "Vellore", "Viluppuram", "Virudhunagar"]),
    "Gujarat": sorted(["Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch", "Bhavnagar", "Botad", "Chhota Udaipur", 
                "Dahod", "Dang", "Devbhoomi Dwarka", "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda", 
                "Kutch", "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal", "Patan", "Porbandar", 
                "Rajkot", "Sabarkantha", "Surat", "Surendranagar", "Tapi", "Vadodara", "Valsad"]),
    "Madhya Pradesh":sorted(["Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", "Barwani", "Betul", "Bhind", 
                       "Bhopal", "Burhanpur", "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", "Dhar", "Dindori", 
                       "Guna", "Gwalior", "Harda", "Hoshangabad", "Indore", "Jabalpur", "Jhabua", "Katni", "Khandwa", 
                       "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur", "Neemuch", "Panna", "Raisen", "Rajgarh", 
                       "Ratlam", "Rewa", "Sagar", "Satna", "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", "Shivpuri", 
                       "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha"]),
    "Uttar Pradesh": sorted(["Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", "Auraiya", "Ayodhya", "Azamgarh", "Baghpat", 
                      "Bahraich", "Ballia", "Balrampur", "Banda", "Barabanki", "Bareilly", "Basti", "Bijnor", "Budaun", 
                      "Bulandshahr", "Chandauli", "Chitrakoot", "Deoria", "Etah", "Etawah", "Farrukhabad", "Fatehpur", 
                      "Firozabad", "Gautam Buddha Nagar", "Ghaziabad", "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", 
                      "Hapur", "Hardoi", "Hathras", "Jalaun", "Jaunpur", "Jhansi", "Kannauj", "Kanpur Dehat", 
                      "Kanpur Nagar", "Kasganj", "Kaushambi", "Kheri", "Kushinagar", "Lalitpur", "Lucknow", 
                      "Maharajganj", "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut", "Mirzapur", "Moradabad", 
                      "Muzaffarnagar", "Pilibhit", "Pratapgarh", "Prayagraj", "Raebareli", "Rampur", "Saharanpur", 
                      "Sambhal", "Sant Kabir Nagar", "Sant Ravidas Nagar", "Shahjahanpur", "Shamli", "Shrawasti", 
                      "Siddharthnagar", "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"])
        }        
        selected_state = st.selectbox("Select State:", ["Select State"] + list(state_district_map.keys()))        
        selected_districts = []
        selected_zone = None
        if selected_state != "Select State":
            selected_districts = st.multiselect(
                "Select Wood Collection Locations (Districts):", 
                state_district_map[selected_state]
            )
            if selected_districts:
                selected_zone = st.multiselect(
                    "Select Zone for the Selected Districts:", 
                    ["Select Zone"] + zones
                )    
        supplied_mill = st.multiselect(
            "Select Supplied Mill:",
            ["Select Supplied Mill"] + ["JK-CPM", "JK-SPM", "JKPM", "APL",
                                        "BILT","TNPL","Seshasayee","West Coast","ITC","Merino", "Orient",
                                        "HariHar","Green Panel","Century PLY","PLY/OTHERS"]
        )
    with col2:
        # Supplier Data Input
        st.markdown("### Enter Supplier Data")
        supplier_rate = st.number_input("Enter Supplier PO Rate:", value=0)
        sub_supplier_rate = st.number_input("Enter Sub Supplier WB Rate:", value=0)
        freight = st.number_input("Enter Freight:", value=0)
        balance = supplier_rate - freight
        other_exp = supplier_rate - sub_supplier_rate
        company_stock = st.number_input("Enter Company Stock (in ASMT):", value=0)
        no_of_trucks = st.number_input("Enter Average No. of Trucks:",value=0)
    # Add Row Button
    if st.button("Add Row"):
        if supplier_rate<0 or sub_supplier_rate<0 or freight < 0 or no_of_trucks <0 or company_stock <0:
            st.warning("Please ensure supplier data should be valid")
        elif sub_supplier_rate>supplier_rate:
            st.warning("Sub Supplier WB Rate Must be less than or Equal to  Supplier PO Rate")
        # elif supplier_rate!= sub_supplier_rate+other_exp:
        #     st.warning("Supplier PO Price Mismatch")
        elif (
            date and 
            wood_species != "Select Wood Species" and 
            # wood_price_source != "Select Wood Price Source" and 
            selected_state != "Select State" and 
            selected_districts and 
            # selected_zone and 
            supplied_mill != "Select Supplied Mill" and 
            supplier_rate > 0 and 
            sub_supplier_rate > 0 and 
            freight > 0 and 
            sub_supplier_rate < supplier_rate       
        ):
            new_row = {
                "Date": date, 
                "Wood Species": wood_species, 
                # "Wood Price Source": wood_price_source, 
                "Wood Collection Location": ", ".join(selected_districts), 
                "Wood Collection Zone": selected_zone, 
                "Supplied Mill": supplied_mill, 
                "SUPPLIER PO RATE": supplier_rate,
                "SUB SUPPLIER WB RATE": sub_supplier_rate,
                "Freight": freight, 
                "Balance": balance,
                "Other Expenses":other_exp,
                "Company Stock (in ASMT)": company_stock,
                "No_of_Trucks(Average)":no_of_trucks
            }
             # Append the new row directly to the DataFrame
            if "df" in st.session_state and not st.session_state.df.empty:
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                # If the DataFrame is empty or doesn't exist, create it with the new row
                st.session_state.df = pd.DataFrame([new_row])            
            st.success("Row added successfully!")
            current_timestamp = datetime.now()
            formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"Last Row Updated at:{formatted_timestamp}")
    else:
        st.warning("All fields are mandatory. Please fill in all required fields.")

        #     Delete Row Section
    st.markdown(" Delete Selected Rows")
    if "df" in st.session_state and not st.session_state.df.empty:
        # Display DataFrame and allow selection of rows to delete
        # st.dataframe(st.session_state.df)
        rows_to_delete = st.multiselect(
            "Select rows to delete:",
            st.session_state.df.index,
            format_func=lambda x: f"Row {x + 1}"
        )
        if st.button("Delete Selected Rows"):
            if rows_to_delete:
                # Drop selected rows and reset the index
                st.session_state.df.drop(rows_to_delete, inplace=True)
                st.session_state.df.reset_index(drop=True, inplace=True)
                st.success("Selected rows deleted successfully!")
            else:
                st.warning("No rows selected for deletion.")
    else:
        st.warning("No data available to delete.")
         
    # Display DataFrame

    st.dataframe(st.session_state.df, use_container_width=True)
    # Function to convert dataframe to Excel
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()
    # Download Button for Excel
    if not st.session_state.df.empty:
        st.download_button(
            label="Download Data as Excel",
            data=convert_df_to_excel(st.session_state.df),
            file_name="wood_procurement_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab2:
    # Categorized Data Display
    st.markdown("### Transport Rates")
    if not st.session_state.df.empty:
        # Filter data for Subabul and Eucalyptus
        subabul_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["DeBark Subabul", "With Bark Subabul"])
        ]
        eucalyptus_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["With Bark Eucalyptus", "DEBARK EUCALYPTUS"])
        ]
        casurina_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Casurina Wood"])
        ]
        acacia_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Acacia Wood Debarked"])
        ]
        gliricidia_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Gliricidia with Bark Wood"])
        ]
        melia_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Melia Dubia Wood With Bark"])
        ]    
        bamboo_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Bamboo"])
        ]
        veneer_waste_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Veneer Waste"])
        ]
        wood_rolls_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Wood Rolls"])
        ]
        wood_waste_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Wood Waste"])
        ]
        wood_chips_data = st.session_state.df[
            st.session_state.df["Wood Species"].isin(["Wood Chips"])
        ]
        # Combine "Wood Collection Location" and "Wood Collection Zone" into a single column
        subabul_data["Wood Collection Location"] = subabul_data["Wood Collection Location"].astype(str) + " - " + subabul_data["Wood Collection Zone"].astype(str)
        eucalyptus_data["Wood Collection Location"] = eucalyptus_data["Wood Collection Location"].astype(str) + " - " + eucalyptus_data["Wood Collection Zone"].astype(str)
        casurina_data["Wood Collection Location"] = casurina_data["Wood Collection Location"].astype(str) + " - " + casurina_data["Wood Collection Zone"].astype(str)
        acacia_data["Wood Collection Location"] = acacia_data["Wood Collection Location"].astype(str) + " - " + acacia_data["Wood Collection Zone"].astype(str)
        gliricidia_data["Wood Collection Location"] = gliricidia_data["Wood Collection Location"].astype(str) + " - " + gliricidia_data["Wood Collection Zone"].astype(str)
        melia_data["Wood Collection Location"] = melia_data["Wood Collection Location"].astype(str) + " - " + melia_data["Wood Collection Zone"].astype(str)
        bamboo_data["Wood Collection Location"] = bamboo_data["Wood Collection Location"].astype(str) + " - " + bamboo_data["Wood Collection Zone"].astype(str)
        veneer_waste_data["Wood Collection Location"] = veneer_waste_data["Wood Collection Location"].astype(str) + " - " + veneer_waste_data["Wood Collection Zone"].astype(str)
        wood_rolls_data["Wood Collection Location"] = wood_rolls_data["Wood Collection Location"].astype(str) + " - " + wood_rolls_data["Wood Collection Zone"].astype(str)
        wood_waste_data["Wood Collection Location"] = wood_waste_data["Wood Collection Location"].astype(str) + " - " + wood_waste_data["Wood Collection Zone"].astype(str)
        wood_chips_data["Wood Collection Location"] = wood_chips_data["Wood Collection Location"].astype(str) + " - " + wood_chips_data["Wood Collection Zone"].astype(str)
    
        subabul_data_display = subabul_data[["Date", "Wood Collection Location", "Freight"]]
        eucalyptus_data_display = eucalyptus_data[["Date", "Wood Collection Location", "Freight"]]
        acacia_data_display = acacia_data[["Date", "Wood Collection Location", "Freight"]]
        casurina_data_display = casurina_data[["Date", "Wood Collection Location", "Freight"]]
        gliricidia_data_display = gliricidia_data[["Date", "Wood Collection Location", "Freight"]]
        melia_data_display = melia_data[["Date", "Wood Collection Location", "Freight"]]
        bamboo_data_display = bamboo_data[["Date", "Wood Collection Location", "Freight"]]
        veneer_waste_data_display = veneer_waste_data[["Date", "Wood Collection Location", "Freight"]]
        wood_rolls_data_display = wood_rolls_data[["Date", "Wood Collection Location", "Freight"]]
        wood_waste_data_display = wood_waste_data[["Date", "Wood Collection Location", "Freight"]]
        wood_chips_data_display = wood_chips_data[["Date", "Wood Collection Location", "Freight"]]
        # Display Wood Data
        # Display the dataframes in the Streamlit app
        st.markdown("#### Subabul")
        st.dataframe(subabul_data_display, use_container_width=True)
        st.markdown("#### Eucalyptus")
        st.dataframe(eucalyptus_data_display, use_container_width=True)
        st.markdown("#### Acacia")
        st.dataframe(acacia_data_display, use_container_width=True)
        st.markdown("#### Casurina")
        st.dataframe(casurina_data_display, use_container_width=True)
        st.markdown("#### Gliricidia")
        st.dataframe(gliricidia_data_display, use_container_width=True)
        st.markdown("#### Melia")
        st.dataframe(melia_data_display, use_container_width=True)
        st.markdown("#### Bamboo")
        st.dataframe(bamboo_data_display, use_container_width=True)
        st.markdown("#### Veneer Waste")
        st.dataframe(veneer_waste_data_display, use_container_width=True)
        st.markdown("#### Wood Rolls")
        st.dataframe(wood_rolls_data_display, use_container_width=True)
        st.markdown("#### Wood Waste")
        st.dataframe(wood_waste_data_display, use_container_width=True)
        st.markdown("#### Wood Chips")
        st.dataframe(wood_chips_data_display, use_container_width=True)
    else:
        st.warning("No data available. Please add rows in the Data Entry tab.")
