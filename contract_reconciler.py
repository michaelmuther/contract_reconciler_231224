from pathlib import Path
import pandas as pd
import re


class Company:

    def __init__(self, name, contact_email_address, esa_required, sea_required):
        self.name = name
        self.contact_email_address = contact_email_address
        self.esa_required = esa_required
        self.sea_required = sea_required
        self.esa_digital_copy_received: bool
        self.sea_digital_copy_received: bool
        self.esa_hard_copy_received: bool
        self.sea_hard_copy_received: bool


class ContractReconciler:

    def __init__(self, data_path, contracts_path, output_path):
        self.companies = {}
        self.companies_missing_signed_ESA_contract = []
        self.companies_missing_signed_SEA_contract = []
        self.companies_missing_only_ESA_hard_copy = []
        self.companies_missing_only_SEA_hard_copy = []

        self.get_companies_from_data(data_path)
        self.get_contracts_from_folder(contracts_path)
        self.reconcile_data_and_contracts()
        self.output_data(output_path)

    def get_companies_from_data(self, data_path):
        data_frame = pd.read_excel(data_path)
        # print(data_frame)
        for row in data_frame.iterrows():
            number = row[1]['Co. Number']
            name = row[1]['Co. Name']
            email = row[1]['Contact Email']
            esa_required = row[1]['ESA Required'] == 'X'
            sea_required = row[1]['SEA Required'] == 'X'
            self.companies[number] = Company(name, email, esa_required, sea_required)
        # print(self.companies)
        # for key, company in self.companies.items():
        #     name = company.name
        #     esa = company.esa_required
        #     sea = company.sea_required
        #     email = company.contact_email_address
        #
        #     print(f'Number: {key} Name: {name} esa: {esa} sea: {sea} email {email}')

    def get_contracts_from_folder(self, contracts_path):
        pattern = r'(SEA|ESA)_(\d\d)(_?).pdf'
        folder = Path(contracts_path)
        for file_path in folder.iterdir():
            if file_path.is_file() and file_path.suffix == '.pdf':
                # print(file_path.name)
                match = re.search(pattern, file_path.name)
                # print(match[1]) # type ESA, SEA
                # print(int(match[2])) # company number
                # print(match[3])  # only digital flag
                type = match[1]
                company_number = match[2]
                digital_only = match[3] == '_'

    def reconcile_data_and_contracts(self):
        pass

    def output_data(self, output_path):
        pass


if __name__ == "__main__":
    master_data_path: str = "master_data/contract_data.xlsx"
    contracts_folder_path: str = "new_contracts_2024"
    output_data_path: str = "output"
    app = ContractReconciler(master_data_path, contracts_folder_path, output_data_path)
