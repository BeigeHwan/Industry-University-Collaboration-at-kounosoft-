


'''import os
import shutil
import xml.etree.ElementTree as ET

def extract_info(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        ip_office_code_element = root.find('.//com:IPOfficeCode', namespaces={"com": "http://www.wipo.int/standards/XMLSchema/Common/1"})
        patent_number_element = root.find('.//pat:PatentNumber', namespaces={"pat": "http://www.wipo.int/standards/XMLSchema/Patent/1"})
        document_kind_code_element = root.find('.//com:PatentDocumentKindCode', namespaces={"com": "http://www.wipo.int/standards/XMLSchema/Common/1"})

        ip_office_code = ip_office_code_element.text.strip() if ip_office_code_element is not None else ""
        patent_number = patent_number_element.text.strip() if patent_number_element is not None else ""
        document_kind_code = document_kind_code_element.text.strip() if document_kind_code_element is not None else ""

        combined_text = f"{ip_office_code}_{patent_number}_{document_kind_code}"
        return combined_text
    except Exception as e:
        print(f"Error occurred while processing XML file: {e}")
        return None

def process_folder(folder_path, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, dirs, files in os.walk(folder_path):
        if not dirs:
            for file in files:
                if file == "fulldoc.xml":
                    xml_file_path = os.path.join(root, file)
                    combined_text = extract_info(xml_file_path)

                    if combined_text is not None:
                        # Copy the XML file to the destination folder with the combined text as the new name
                        xml_file_name = f"{combined_text}.xml"
                        destination_xml_file_path = os.path.join(destination_folder, xml_file_name)
                        shutil.copy(xml_file_path, destination_xml_file_path)
                    else:
                        print(f"Error occurred while processing XML file: {xml_file_path}")

# Specify the source folder path where the recursive traversal starts
source_folder_path = input('source 경로를 입력해주세요 >> ')
# Specify the destination folder path to save the renamed XML files
destination_folder_path = input('destination 경로를 입력해주세요 >> ')

process_folder(source_folder_path, destination_folder_path + '/xml')
'''

import os
import csv
from xml.etree import ElementTree as ET


def extract_information_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespaces = {
        'pat': 'http://www.wipo.int/standards/XMLSchema/Patent/1',
        'com': 'http://www.wipo.int/standards/XMLSchema/Common/1',
        'rupat': 'urn:ru:rupto:patent',
    }

    IPOfficeCode_element = root.find('.//com:IPOfficeCode', namespaces=namespaces)
    IPOfficeCode = IPOfficeCode_element.text if IPOfficeCode_element is not None else ''

    PatentNumber_element = root.find('.//pat:PatentNumber', namespaces=namespaces)
    PatentNumber = PatentNumber_element.text if PatentNumber_element is not None else ''

    PatentDocumentKindCode_element = root.find('.//com:PatentDocumentKindCode', namespaces=namespaces)
    PatentDocumentKindCode = PatentDocumentKindCode_element.text if PatentDocumentKindCode_element is not None else ''

    InventionTitle_element = root.find('.//pat:InventionTitle[@com:languageCode="ru"]', namespaces=namespaces)
    InventionTitle = InventionTitle_element.text if InventionTitle_element is not None else ''

    InventionTitle_EN_element = root.find('.//pat:InventionTitle[@com:languageCode="en"]', namespaces=namespaces)
    InventionTitle_EN = InventionTitle_EN_element.text if InventionTitle_EN_element is not None else ''

    Assignee_element = root.find('.//pat:Assignee', namespaces=namespaces)
    if Assignee_element is not None:
        proprietor_name_element = Assignee_element.find('.//pat:OrganizationStandardName', namespaces=namespaces)
        proprietor_name = proprietor_name_element.text if proprietor_name_element is not None else ''
    else:
        proprietor_name = ''

    AbstractRU_elements = root.findall('.//pat:Abstract[@com:languageCode="ru"]/pat:P', namespaces=namespaces)
    abstract_RU = ' '.join([abstract_element.text.strip() for abstract_element in AbstractRU_elements])

    AbstractEN_elements = root.findall('.//pat:Abstract[@com:languageCode="en"]/pat:P', namespaces=namespaces)
    abstract_EN = ' '.join([abstract_element.text.strip() for abstract_element in AbstractEN_elements])

    IPCR_elements = root.findall('.//pat:IPCRClassification', namespaces=namespaces)
    ipcr_list = []
    for ipcr_element in IPCR_elements:
        section = ipcr_element.find('.//pat:Section', namespaces=namespaces).text.strip()
        _class = ipcr_element.find('.//pat:Class', namespaces=namespaces).text.strip()
        subclass = ipcr_element.find('.//pat:SubClass', namespaces=namespaces).text.strip()
        maingroup = ipcr_element.find('.//pat:MainGroup', namespaces=namespaces).text.strip()
        subgroup = ipcr_element.find('.//pat:SubGroup', namespaces=namespaces).text.strip()
        ipcr = f'{section}{_class}{subclass} {maingroup}/{subgroup}'

        # Extract SchemeDate from each IPCRClassification element (if available)
        scheme_date_element = ipcr_element.find('.//pat:PatentClassificationScheme/pat:SchemeDate',
                                                namespaces=namespaces)
        scheme_date = scheme_date_element.text.strip() if scheme_date_element is not None else ''
        a, b = scheme_date.split('-')[0], scheme_date.split('-')[1]

        # Combine SchemeDate with IPCR information
        ipcr_combined = f'{ipcr} ({a}.{b})' if scheme_date else ipcr
        ipcr_list.append(ipcr_combined)

    ipcr_combined = '; '.join(ipcr_list)

    CPC_elements = root.findall('.//rupat:CPCClassification', namespaces=namespaces)
    cpc_list = []
    for cpc_element in CPC_elements:
        section = cpc_element.find('.//rupat:CPCSection', namespaces=namespaces).text.strip()
        _class = cpc_element.find('.//rupat:Class', namespaces=namespaces).text.strip()
        subclass = cpc_element.find('.//rupat:Subclass', namespaces=namespaces).text.strip()
        maingroup = cpc_element.find('.//rupat:MainGroup', namespaces=namespaces).text.strip()
        subgroup = cpc_element.find('.//rupat:Subgroup', namespaces=namespaces).text.strip()
        cpc = f'{section}{_class}{subclass} {maingroup}/{subgroup}'

        # Extract SchemeDate from each CPCClassification element (if available)
        scheme_date_element = cpc_element.find('.//rupat:ClassificationVersionDate', namespaces=namespaces)
        scheme_date = scheme_date_element.text.strip() if scheme_date_element is not None else ''
        a, b = scheme_date.split('-')[0], scheme_date.split('-')[1]

        # Combine SchemeDate with CPC information
        cpc_combined = f'{cpc} ({a}.{b})' if scheme_date else cpc
        cpc_list.append(cpc_combined)

    cpc_combined = '; '.join(cpc_list)

    patent_number = IPOfficeCode + PatentNumber + PatentDocumentKindCode
    return abstract_RU, abstract_EN, InventionTitle, patent_number, proprietor_name, InventionTitle_EN, ipcr_combined, cpc_combined


def process_folder(folder_path, csv_writer):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                abstract_RU, abstract_EN, doc_name, data, proprietor_name, doc_name_EN, ipcr_combined, cpc_combined = extract_information_from_xml(
                    file_path)
                csv_writer.writerow(
                    [data, doc_name_EN, doc_name, proprietor_name, abstract_EN, abstract_RU, ipcr_combined,
                     cpc_combined])


def extract_information_and_save_to_csv(root_folder, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['patent_number', 'doc_name_EN', 'doc_name', 'proprietor_name', 'abstract_EN', 'abstract_RU', 'IPCR',
             'CPC'])
        process_folder(root_folder, writer)


# Usage:
root_folder = input('source 경로를 입력해주세요 >> ')
if not os.path.exists(root_folder+'\output'):
    os.makedirs(root_folder+'\output')
output_csv = root_folder + "\output\output.csv"

extract_information_and_save_to_csv(root_folder, output_csv)
