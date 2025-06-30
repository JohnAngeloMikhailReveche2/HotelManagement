import os
import json



class RoomTypeService:
    def __init__(self, file=None):
        # Get absolute path of this file (DataLogic.py)
        this_file = os.path.abspath(__file__)
        # Go up 3 directories to get to Project root (adjust if needed)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
        # Define the source folder
        source_dir = os.path.join(base_dir, "source")
        # Make sure source_dir exists
        os.makedirs(source_dir, exist_ok=True)

        # Use given file or default path inside source_dir
        self.file = file if file else os.path.join(source_dir, "room_type_data.json")

        print("JSON file path:", self.file)  # For debug: will print full path

        # Create file if doesn't exist
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump([], f)

    def read_all(self):
        with open(self.file, 'r') as f:
            return json.load(f)

    def write_all(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=4)

    def add(self, name, base_price):
        data = self.read_all()
        # Append dict with name and base_price
        data.append({
            "name": name,
            "base_price": float(base_price)
        })
        self.write_all(data)
        return True, "Added successfully."

    def update(self, index, new_name, new_base_price):
        data = self.read_all()
        if 0 <= index < len(data):
            data[index] = {
                "name": new_name,
                "base_price": float(new_base_price)
            }
            self.write_all(data)
            return True, "Updated successfully."
        return False, "Invalid selection."

    def delete(self, index):
        data = self.read_all()
        if 0 <= index < len(data):
            del data[index]
            self.write_all(data)
            return True, "Deleted successfully."
        return False, "Invalid selection."
