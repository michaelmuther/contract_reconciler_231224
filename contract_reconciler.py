from pathlib import Path
import pandas as pd
import re


class Company:

    def __init__(self, name, contact_email_address, esa_required, sea_required):
        self.name = name
        self.contact_email_address = contact_email_address
        self.esa_required = esa_required
        self.sea_required = sea_required
        self.esa_hard_copy_received = False
        self.sea_hard_copy_received = False
        self.esa_digital_copy_received = False
        self.sea_digital_copy_received = False

    def __repr__(self):
        return f'{self.esa_required} {self.sea_required} {self.esa_hard_copy_received} {self.sea_hard_copy_received}'


class Contract:

    def __init__(self, company_number, contract_type, digital_only):
        self.company_number = company_number
        self.contract_type = contract_type
        self.digital_only = digital_only

    def __repr__(self):
        return f'Co.: {self.company_number}  type: {self.contract_type}  digital-only: {self.digital_only}'


class ContractReconciler:

    def __init__(self, data_path, contracts_path, output_path):
        self.companies = {}
        self.contracts_in_folder = []
        self.companies_missing_signed_ESA_contract = []
        self.companies_missing_signed_SEA_contract = []
        self.companies_missing_only_ESA_hard_copy = []
        self.companies_missing_only_SEA_hard_copy = []

        self.get_companies_from_data(data_path)
        self.print_companies()  # for testing
        # self.get_contracts_from_folder(contracts_path)
        # self.print_contracts()  # for testing
        # self.add_contract_data_to_companies()
        # print('AFTER---------')
        # self.print_companies()  # for testing
        # self.output_data(output_path)

    def get_companies_from_data(self, data_path):
        data_frame = pd.read_excel(data_path)
        # print(data_frame)  # For testing
        for row in data_frame.iterrows():
            number = row[1]['Co. Number']
            name = row[1]['Co. Name']
            email = row[1]['Contact Email']
            esa_required = row[1]['ESA Required'] == 'X'
            sea_required = row[1]['SEA Required'] == 'X'
            self.companies[number] = Company(name, email, esa_required, sea_required)
        # print(self.companies)  # For testing
        # for key, company in self.companies.items():  # For testing
        #     name = company.name
        #     esa = company.esa_required
        #     sea = company.sea_required
        #     email = company.contact_email_address
        #     print(f'Number: {key} Name: {name} ESA: {esa} SEA: {sea} email {email}')

    def get_contracts_from_folder(self, contracts_path):
        pattern = r'(SEA|ESA)_(\d\d)(_?).pdf'  # groups: 1st: SEA or ESA, 2nd: Co. Number, 3rd: digital-only flag
        folder = Path(contracts_path)
        file_count = 0
        for file_path in folder.iterdir():
            if file_path.is_file() and file_path.suffix == '.pdf':
                file_count += 1
                # print(file_path.name)
                match = re.search(pattern, file_path.name)
                # print(match[1])  # type ESA, SEA
                # print(int(match[2]))  # company number
                # print(match[3])  # only digital flag
                contract_type = match[1]
                company_number = int(match[2])
                digital_only = match[3] == '_'
                self.contracts_in_folder.append(Contract(company_number, contract_type, digital_only))
        print(f'file_count: {file_count}\n')
        # print(self.contracts_in_folder)

    def add_contract_data_to_companies(self):
        for contract in self.contracts_in_folder:
            if contract.contract_type == 'ESA':
                self.companies[contract.company_number].esa_hard_copy_received = not contract.digital_only
                self.companies[contract.company_number].esa_digital_copy_received = True
            else:
                self.companies[contract.company_number].sea_hard_copy_received = not contract.digital_only
                self.companies[contract.company_number].sea_digital_copy_received = True

    # def reconcile_companies_and_contracts(self):
    #     # self.companies_missing_signed_ESA_contract = []
    #     # self.companies_missing_signed_SEA_contract = []
    #     # self.companies_missing_only_ESA_hard_copy = []
    #     # self.companies_missing_only_SEA_hard_copy = []
    #     for number, company in self.companies.items():
    #         if company.esa_required:
    #             if not company.esa_hard_copy_received and not company.esa_digital_copy_received:
    #                 self.companies_missing_signed_ESA_contract.append(number)
    #             elif not company
    #         if company.sea_required:

    def output_data(self, output_path):
        pass

    def print_companies(self):
        for key, value in self.companies.items():
            print(f'Co. Number: {key} Co. Name: {value.name}')
            print(f'ESA Required: {value.esa_required}  Hard-copy: {value.esa_hard_copy_received}  Digital-copy: {value.esa_digital_copy_received}')
            print(f'SEA Required: {value.sea_required}  Hard-copy: {value.sea_hard_copy_received}  Digital-copy: {value.sea_digital_copy_received}\n')

    def print_contracts(self):
        for contract in sorted(self.contracts_in_folder, key=lambda c: c.company_number):
            print(contract)


if __name__ == "__main__":
    master_data_path: str = "master_data/contract_data.xlsx"
    contracts_folder_path: str = "new_contracts_2024"
    output_data_path: str = "output"
    app = ContractReconciler(master_data_path, contracts_folder_path, output_data_path)
