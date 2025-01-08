import os
import json
import pandas as pd

class StateManager:
    def __init__(self):
        # Dynamically resolve the base directory
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory containing this script
        self.data_dir = os.path.join(base_dir, 'data')  # Adjust if 'data' is deeper in the hierarchy
        self.leads_file = os.path.join(self.data_dir, 'leads.json')
        self.uploaded_data_file = os.path.join(self.data_dir, 'uploaded_data.csv')  # Add this line

        # Debug: Verify paths
        print(f"Resolved data directory: {self.data_dir}")
        print(f"Resolved leads file path: {self.leads_file}")
        print(f"Resolved uploaded data file path: {self.uploaded_data_file}")

        # Create directory and initialize the leads file
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating data directory: {e}")
        
        if not os.path.exists(self.leads_file):
            self.initialize_leads_file()

    def load_leads(self):
        try:
            if not os.path.exists(self.leads_file):
                print("Leads file does not exist. Initializing...")
                return self.initialize_leads_file()

            if os.path.getsize(self.leads_file) == 0:
                print("Leads file is empty. Initializing...")
                return self.initialize_leads_file()

            with open(self.leads_file, 'r') as f:
                leads = json.load(f)
                print(f"Loaded leads from file: {leads}")
                return leads if isinstance(leads, list) else []
        except Exception as e:
            print(f"Error loading leads: {e}")
            return []


    def save_leads(self, leads):
        print(f"Leads file path: {self.leads_file}")

        try:
            print(f"Attempting to save leads: {leads}")  # Debug log
            with open(self.leads_file, 'w') as f:
                json.dump(leads, f, indent=4)
                f.flush()
                os.fsync(f.fileno())
            print(f"Leads successfully saved to {self.leads_file}")  # Debug log
            return True
        except Exception as e:
            print(f"Error saving leads: {e}")  # Debug log
            return False



    def save_uploaded_data(self, df):
        df.to_csv(self.uploaded_data_file, index=False)
    
    def load_uploaded_data(self):
        if os.path.exists(self.uploaded_data_file):
            return pd.read_csv(self.uploaded_data_file)
        return None