from unicodedata import numeric
import datetime
import json
import os

# Đọc dữ liệu từ file JSON
def load_data_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        data = []
    except FileNotFoundError:
        data = []
    return data

# Lọc các mục có cuisine là nation
def filter_by_cuisine(data, cuisine):
    filtered_data = [recipe for recipe in data if recipe.get('cuisine') == cuisine]
    return filtered_data

# Kiểm tra xem một mục có trong danh sách các mục hay không
def is_recipe_in_list(recipe_list, recipe):
    for existing_recipe in recipe_list:
        if existing_recipe['url'] == recipe['url']:
            return True
    return False

def add_data(input, output, nation):
    # Load dữ liệu từ file JSON
    data = load_data_from_json(input)

    # Lọc các mục có cuisine là nation
    indonesian_recipes = filter_by_cuisine(data, nation)

    # Đọc dữ liệu từ file JSON đầu vào
    if not os.path.exists(output):
        with open(output, 'w', encoding='utf-8') as output_file:
            json.dump([], output_file)
    with open(output, 'r', encoding='utf-8') as output_file:
        existing_data = json.load(output_file)

    # Kiểm tra và thêm dữ liệu mới vào danh sách nếu chưa tồn tại
    for recipe in indonesian_recipes:
        if not is_recipe_in_list(existing_data, recipe):
            existing_data.append(recipe)

    # Ghi dữ liệu đã được mở rộng vào file JSON đầu ra
    with open(output, 'w', encoding='utf-8') as output_file:
        json.dump(existing_data, output_file, ensure_ascii=False, indent=4)

def process_data_Vy():
    # Đường dẫn tới file JSON
    input_folder = '../../Data/Crawled/Recipes (Vy)/'
    output_folder = '../../Data/Preprocess Data/Recipes (Vy)/'
    nations = ['Chinese', 'Indian', 'Indonesian', 'Japanese', 'Korean', 'Malaysian', 'Thai', 'Vietnamese']
    for nation_1 in nations:
        for nation_2 in nations:
            input_file = input_folder + nation_1 + '.json'
            output_file = output_folder + nation_2 + '.json'
            add_data(input_file, output_file, nation_2)

def convert_duration(duration_str):
    # Tách giá trị số và đơn vị thời gian từ chuỗi
    duration_str = duration_str[2:]
    number_str, units = [""], [""]
    for char in duration_str:
        if char.isdigit():
            number_str[-1] += char
        else:
            number_str.append("")
            units[-1] += char
            units.append("")

    # Tạo đối tượng timedelta
    delta = datetime.timedelta(minutes=0, seconds=0)

    # # Duyệt qua từng đơn vị thời gian và cộng thêm vào timedelta
    for _ in range(len(units)):
        unit = units[_]
        if unit == "M":
            delta += datetime.timedelta(minutes=float(number_str[_]))
        elif unit == "S":
            delta += datetime.timedelta(seconds=float(number_str[_]))

    return delta

def process_data_Nhat():

    # Đường dẫn tới thư mục đầu vào
    input_folder_path = '../../Data/Crawled/Recipes (Nhat)/'
    output_folder_path = '../../Data/Preprocess Data/Recipes (Nhat)/'

    # Lặp qua tất cả các thư mục và tệp trong thư mục đầu vào
    for root, dirs, files in os.walk(input_folder_path):
        # Lặp qua các tệp trong thư mục hiện tại
        for file in files:
            # Kiểm tra nếu tệp là một tệp JSON
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                folder = file_path.split('/')[-1].split('\\')
                
                nation = folder[0].capitalize()
                tags = folder[1:-1]
                data = load_data_from_json(file_path)

                for item in data:
                    item['tags'] = tags
                    item['cook_time'] = f"{convert_duration(item['cook_time'])}"
                    item['prep_time'] = f"{convert_duration(item['prep_time'])}"
                    item['total_time'] = f"{convert_duration(item['total_time'])}"
                    item['video']['duration'] = f"{convert_duration(item['video']['duration'])}"

                    instructions = [step["text"] for step in item["instructions"]]
                    item["instructions"] = instructions

                    for ingredient in item["ingredient"]:
                        ingredient["prepare_type"] = ""

                        quantity = ingredient["quantity"]
                        try:
                            if quantity is None:
                                val = 0
                            elif len(quantity) == 1:
                                val = numeric(quantity)
                            elif quantity[0].isalpha():
                                val = 0
                            elif quantity[-1].isdigit():
                                val = float(quantity)
                            else:
                                val = float(quantity[:-1]) + numeric(quantity[-1])
                        except ValueError:
                            q = quantity.split()
                            if len(q) == 1:
                                whole_number, fraction = 0, q[0]
                            else:
                                whole_number, fraction = q

                            whole_number = float(whole_number)
                            numerator, denominator = map(float, fraction.split('/'))
                            fraction_float = numerator / denominator
                            
                            val = whole_number + fraction_float
                        
                        ingredient["quantity"] = val

                    item["ingredients"] = item["ingredient"]
                    del item["ingredient"]

                # Ghi dữ liệu đã được mở rộng vào file JSON đầu ra
                output_file_path = output_folder_path + nation + '.json'
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    json.dump(data, output_file, ensure_ascii=False, indent=4)
                
def process_merge_data(input1, input2, output):
    json1 = load_data_from_json(input1)
    json2 = load_data_from_json(input2)
    merged_data = json1.copy()

    # Duyệt qua mỗi mục trong kiểu dữ liệu thứ nhất
    for item2 in json2:
        if not is_recipe_in_list(json1, item2):
            item2['name'] = item2['title']
            item2['description'] = item2['summary']
            item2['image'] = item2['photos']
            item2['cook_time'] = ""
            item2['prep_time'] = ""
            item2['total_time'] = ""
            item2['nutrition'] = ""
            item2['video'] = ""
            item2['tags'] = ""

            del item2["title"]
            del item2["summary"]
            del item2["photos"]

            merged_data.append(item2)
    
    data_final = []
    for item in merged_data:
        desired_order = ["url", "name", "cook_time", "prep_time", "total_time", "description", "ingredients", "instructions", "nutrition", "image", "video", "cuisine", "category", "tags"]
        sorted_json = {key: item[key] for key in desired_order if key in item}
        data_final.append(sorted_json)

    # Lưu kết quả vào một tệp JSON mới
    with open(output, 'w', encoding='utf-8') as output_file:
        json.dump(data_final, output_file, ensure_ascii=False, indent=4)

def merge_data():
    json1_path = '../../Data/Preprocess Data/Recipes (Nhat)/'
    json2_path = '../../Data/Preprocess Data/Recipes (Vy)/'
    output_path = '../../Data/Preprocess Data/Recipes/'
    nations = ['Bangladeshi', 'Chinese', 'Filipino', 'Indian', 'Indonesian', 'Japanese', 'Korean', 'Malaysian', 'Pakistani', 'Persian','Thai', 'Vietnamese']
    for nation in nations:
        json1_data = json1_path + nation + '.json'
        json2_data = json2_path + nation + '.json'
        output_data = output_path + nation + '.json'
        process_merge_data(json1_data, json2_data, output_data)

merge_data()


