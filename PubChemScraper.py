import requests #this module handles HTTP requests
import pandas as pd #structures the data for a CSV

def online_chem_data(compound_name):
    u_r_l = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" #web where compounds will be searched
    properties = "MolecularWeight,MolecularFormula,IUPACName,InChIKey" #properties to look for

    api_url = f"{u_r_l}{compound_name}/property/{properties}/JSON"
    print(f"Fetching: {api_url}")
    
    api_request = requests.get(api_url)

    if api_request.status_code == 200: #status_code indicates whether the request was successful, 200 is status code for successful
        chem_data = api_request.json() #converts the HTTP response from json format to python dictionary

        #the respose from PubChem exists in api_request as a json format
        #using.json() converts api_request into a python dictionary format
        
        try:
            chem_properties = chem_data["PropertyTable"]["Properties"][0] #TRY ATTEMPTS TO EXTRACT THE Properties dictionary

            #In the chem_data dictionary, PropertyTable is a key, Properties is a value, in that value exists a list of dictionaries
            #in these second dictionaries exist the chemical properties. Each dictionary would correspond to each compound
            #since this code only extracts properties for one compound, we use [0] as there is one dictionary
            #In a hierachal table structure, PropertyTable will be table heading/title,
            #Properties will be the column heading that contains rows of compound names
            return chem_properties
        except KeyError:
            print(f"No chemical properties found for '{compound_name}'.")
            return None #if the PropertyTable or Properties does not exists
    elif api_request.status_code == 404:
        print(f" Error: Compound '{compound_name}' not found in PubChem.")
    elif api_request.status_code == 500:
        print(f"Server error while retrieving '{compound_name}'. Try again later.")
    else:
        print(f"Unexpected error ({api_request.status_code}) for '{compound_name}'.")

    return None #if the request fails and the status code is not 200


def save_csv(comp_list, filename="Chemical_Properties.csv"): #taking a list of compound names and a filname
    results = [] #will take the dictionary results of the chem properties and put them in this list, ie a list of dictionaries

    #compound_name and comp_list are placeholders for any values that will passed when calling the function
    
    for comp in comp_list:
        chem_data2 = online_chem_data(comp) #online_chem_data() goes and fetches the properties data for the sepecific compound, this data is a dictionary
                                            #this data (dictionary) is then stored in chem_data2
        if chem_data2:
            results.append(chem_data2)     #if the data (dictionary) exists it is added to the results list
        else:
            print(f"Skipping '{comp}' due to missing data")
    if results:
        df = pd.DataFrame(results) #use the pandas library to convert the list of dictionaries in results into a structured table
        df.to_csv(filename, index=False) #saves the dataframe as a CSV, False prevents an index column
        print(f"Chemical Properties saved to '{filename}'") #adding filename to the function means we can pass a custom filename when calling the function
    else:
        print("No data to save.")

compounds = ["Aspirin", "Caffeine", "Paracetamol", "xyz123"]
save_csv(compounds)

#ensure properties (line 6) include chemical properties recognised by PubChem (ie LogP is not). Add more recognised properties as needed
    
