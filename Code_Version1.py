import os
import shutil
import xml.etree.ElementTree as ET

source_dir = input("source directory를 입력해주세요 >> ")

if not os.path.exists(source_dir+'\output'):
    os.makedirs(source_dir+'\output')
destination_dir = source_dir + "\output"
#source_dir = 'C:/Users/User/Desktop/배지환/crawl/20190102_20190108/RU/ETC_PATENT009'
#destination_dir = 'C:/Users/User/Desktop/배지환/crawl/crawled_data'

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)



#파일 경로가 이상한거 고치기

import os
import shutil
import xml.etree.ElementTree as ET

def visit_folders(root_folder, save_directory):
    for folder_name, subfolders, files in os.walk(root_folder):
        if not subfolders:
            for file_name in files:
                if file_name.endswith('.xml'):
                    folder_path = os.path.abspath(folder_name)
                    patent_number = get_patent_number(os.path.join(folder_path, file_name))
                    if patent_number:
                        xml_file_path = os.path.join(folder_path, file_name)
                        new_file_name = f"{patent_number}.xml"
                        new_file_path = os.path.join(save_directory, new_file_name)
                        shutil.copy2(xml_file_path, new_file_path)

def get_patent_number(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        country = root.attrib['country']
        doc_number = root.find('.//B100/B110').text.strip('0')
        kind = root.find('.//B100/B130').text
        patent_number = country + doc_number + kind
        return patent_number
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return None

# Usage
if not os.path.exists(destination_dir+'/xml'):
    os.makedirs(destination_dir+'/xml')
visit_folders(source_dir, destination_dir+'/xml')


import os
import shutil
import xml.etree.ElementTree as ET

def visit_folders_pdf(root_folder, save_directory):
    for folder_name, subfolders, files in os.walk(root_folder):
        if not subfolders:
            for file_name in files:
                if file_name == 'DOCUMENT.PDF':
                    folder_path = os.path.abspath(folder_name)
                    patent_number = get_patent_number(os.path.join(folder_path, 'document.xml'))
                    if patent_number:
                        new_file_name = f"{patent_number}.pdf"
                        copy_and_rename_file(os.path.join(folder_path, file_name), os.path.join(save_directory, new_file_name))

def get_patent_number(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        country = root.attrib['country']
        doc_number = root.find('.//B100/B110').text.strip('0')
        kind = root.find('.//B100/B130').text
        patent_number = country + doc_number + kind
        return patent_number
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return None

def copy_and_rename_file(src, dst):
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"Error occurred while copying and renaming the file: {e}")

# Usage

if not os.path.exists(destination_dir+'/pdf'):
    os.makedirs(destination_dir+'/pdf')
visit_folders_pdf(source_dir, destination_dir+'/pdf')



#이미지 파일 따로 추출하기
import os
import shutil
import xml.etree.ElementTree as ET

def visit_folders_images(root_folder, save_directory):
    for folder_name, subfolders, files in os.walk(root_folder):
        if not subfolders:
            image_files = [file_name for file_name in files if is_image_file(file_name)]
            if image_files:
                folder_path = os.path.abspath(folder_name)
                patent_number = get_patent_number(os.path.join(folder_path, 'document.xml'))
                if patent_number:
                    copy_images(folder_path, image_files, patent_number, save_directory)

def is_image_file(file_name):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    _, ext = os.path.splitext(file_name)
    return ext.lower() in image_extensions

def get_patent_number(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        country = root.attrib['country']
        doc_number = root.find('.//B100/B110').text.strip('0')
        kind = root.find('.//B100/B130').text
        patent_number = country + doc_number + kind
        return patent_number
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return None

def copy_images(folder_path, image_files, patent_number, save_directory):
    for i, file_name in enumerate(image_files):
        _, ext = os.path.splitext(file_name)
        new_file_name = f"{patent_number}-{i+1}{ext}"
        shutil.copy2(os.path.join(folder_path, file_name), os.path.join(save_directory, new_file_name))


# Usage
if not os.path.exists(destination_dir+'/image'):
    os.makedirs(destination_dir+'/image')
visit_folders_images(source_dir, destination_dir+'/image')



import csv
import os
import xml.etree.ElementTree as ET


def extract_ru_b540_info(root):
    ru_b540_elements = root.findall(".//ru-b540")
    extracted_info = ''
    for ru_b540_element in ru_b540_elements:
        b541_element = ru_b540_element.find('B541')
        if b541_element is not None and b541_element.text == 'en':
            ru_b542_element = ru_b540_element.find('ru-b542')
            if ru_b542_element is not None:
                extracted_info = ru_b542_element.text
                break
    return extracted_info


def visit_folders(root_folder, tags):
    output_directory = destination_dir + 'tag_extracted'
    os.makedirs(output_directory, exist_ok=True)

    for folder_name, subfolders, files in os.walk(root_folder):
        if not subfolders:
            for file_name in files:
                if file_name == 'document.xml':
                    folder_path = os.path.abspath(folder_name)
                    doc_number = get_doc_number(os.path.join(folder_path, file_name))
                    if doc_number:
                        data = extract_data(folder_path, tags)
                        save_data_as_csv(data, doc_number, output_directory, tags)


def get_doc_number(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        doc_number = root.find('.//B210').text
        return doc_number
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return None


def extract_data(folder_path, tags):
    data = {}
    try:
        tree = ET.parse(os.path.join(folder_path, 'document.xml'))
        root = tree.getroot()

        extracted_ru_b540_info = extract_ru_b540_info(root)
        if extracted_ru_b540_info:
            data['doc_name_EN'] = extracted_ru_b540_info[0]
        else:
            data['doc_name_EN'] = ''

        data.update(extract_ru_b542(os.path.join(folder_path, 'document.xml')))

        for tag in tags:
            tag_data = root.find(f".//{tag}").text
            data[tag] = tag_data
    except Exception as e:
        print(f"Error occurred while extracting data: {e}")
    return data


def save_data_as_csv(data, doc_number, output_directory, tags):
    file_name = os.path.join(output_directory, f"{doc_number}.csv")
    try:
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['doc_name_EN'] + tags)
            writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"Error occurred while saving data as CSV: {e}")


def extract_ru_b542(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find all <ru-b542> elements
    ru_b542_elements = root.findall(".//ru-b542")

    # Extract the information between <ru-b542> tags
    extracted_info = {}
    for index, element in enumerate(ru_b542_elements, start=1):
        extracted_info[f'ru-b542_{index}'] = element.text

    return extracted_info


def get_doc_name_and_patent_number_and_proprietor(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        doc_name_en_element = root.find('.//B541')
        doc_name_en = doc_name_en_element.text if doc_name_en_element is not None else ""
        temp = []
        doc_name_ru_elements = root.findall('.//ru-b540/ru-b542')
        for i in doc_name_ru_elements:
            temp.append(i)
        print(temp)
        doc_name_ru = temp[0].text if temp[0] is not None else ""

        country = root.attrib['country']
        doc_number = root.find('.//B100/B110').text.strip('0')
        kind = root.find('.//B100/B130').text
        patent_number = country + doc_number + kind

        proprietor_ru_elements = root.findall('.//B700/B710/B711/ru-name-text')
        proprietor_ru = ', '.join([element.text for element in proprietor_ru_elements])

        return doc_name_en, doc_name_ru, patent_number, proprietor_ru
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return None, None, None, None


def extract_abstract(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        abstract_ru_element = root.find('.//abstract[@lang="ru"]')
        abstract_en_element = root.find('.//abstract[@lang="en"]')

        abstract_ru = ""
        abstract_en = ""

        if abstract_ru_element is not None:
            abstract_ru = abstract_ru_element.find("p").text.strip()

        if abstract_en_element is not None:
            abstract_en = ' '.join([p.text.strip() for p in abstract_en_element.findall("p")])

        return abstract_ru, abstract_en
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return "", ""


def preprocess_cpc(cpc_element):
    section = cpc_element.find('.//section').text.strip()
    class_ = cpc_element.find('.//class').text.strip()
    subclass = cpc_element.find('.//subclass').text.strip()
    main_group = cpc_element.find('.//main-group').text.strip()
    subgroup = cpc_element.find('.//subgroup').text.strip()
    date = cpc_element.find('.//date').text.strip()

    cpc_info = f"{section}{class_}{subclass} {main_group}/{subgroup} ({date[:4]}.{date[4:6]})"
    return cpc_info


def preprocess_ipcr(ipcr_element):
    section = ipcr_element.find('.//section').text.strip()
    class_ = ipcr_element.find('.//class').text.strip()
    subclass = ipcr_element.find('.//subclass').text.strip()
    main_group = ipcr_element.find('.//main-group').text.strip()
    subgroup = ipcr_element.find('.//subgroup').text.strip()
    date = ipcr_element.find('.//date').text.strip()

    ipcr_info = f"{section}{class_}{subclass} {main_group}/{subgroup} ({date[:4]}.{date[4:6]})"
    return ipcr_info


def extract_cpc_and_ipcr(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        cpc_elements = root.findall('.//classifications-cpc/main-cpc/classification-cpc')
        ipcr_elements = root.findall('.//classification-ipcr')

        cpc_set = set()
        ipcr_set = set()

        for cpc_element in cpc_elements:
            cpc_info = preprocess_cpc(cpc_element)
            cpc_set.add(cpc_info)

        for ipcr_element in ipcr_elements:
            ipcr_info = preprocess_ipcr(ipcr_element)
            ipcr_set.add(ipcr_info)

        cpc = ';'.join(cpc_set)
        ipcr = ';'.join(ipcr_set)

        return cpc, ipcr
    except Exception as e:
        print(f"Error occurred while parsing XML: {e}")
        return "", ""


def process_folder(folder_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "document.xml":
                xml_file_path = os.path.join(root, file)
                extracted_info = extract_ru_b542(xml_file_path)
                doc_name_en, doc_name_ru, patent_number, proprietor_ru = get_doc_name_and_patent_number_and_proprietor(
                    xml_file_path)
                abstract_ru, abstract_en = extract_abstract(xml_file_path)
                cpc, ipcr = extract_cpc_and_ipcr(xml_file_path)

                # Save the extracted information as a CSV file
                csv_file_path = os.path.join(output_folder, "extracted_info.csv")
                with open(csv_file_path, "a", newline="", encoding="utf-8-sig") as csvfile:
                    writer = csv.writer(csvfile)
                    if os.path.getsize(csv_file_path) == 0:
                        writer.writerow(
                            ["doc_name_EN", "doc_name_RU", "patent_number", "proprietor_RU", "abstract_RU",
                             "abstract_EN",
                             "cpc", "ipcr"])  # Write header only once
                    writer.writerow(
                        [doc_name_en, doc_name_ru, patent_number, proprietor_ru, abstract_ru, abstract_en, cpc, ipcr])


# Clear existing CSV file if it exists
csv_file_path = os.path.join(destination_dir, "extracted_info.csv")
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)
process_folder(source_dir, destination_dir)
