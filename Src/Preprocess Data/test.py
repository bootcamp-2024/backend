from fractions import Fraction
# Dữ liệu ban đầu
data = {
    "ingredient": [
        {"quantity": "1", "unit": "(8 ounce) package", "name": "spaghetti"},
        {"quantity": "3", "unit": "tablespoons", "name": "low-sodium soy sauce"},
        {"quantity": "2", "unit": "tablespoons", "name": "teriyaki sauce"},
        {"quantity": "2", "unit": "tablespoons", "name": "honey"},
        {"quantity": "¼", "unit": "teaspoon", "name": "ground ginger"},
        {"quantity": "2", "unit": "tablespoons", "name": "vegetable oil"},
        {"quantity": "3", "unit": "stalks", "name": "celery, sliced"},
        {"quantity": "2", "unit": "large", "name": "carrots, cut into large matchsticks"},
        {"quantity": "½", "unit": None, "name": "sweet onion, thinly sliced"},
        {"quantity": "2", "unit": None, "name": "green onions, sliced"}
    ]
}
import unicodedata


# Thêm trường "prepare_type" cho mỗi thành phần trong trường "ingredient"
for ingredient in data["ingredient"]:
    ingredient["prepare_type"] = ""

    ingredient["quantity"] = unicodedata.numeric(f'{ingredient["quantity"]}')

# In ra dữ liệu đã được cập nhật
print(data)
