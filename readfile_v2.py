import json

class ReadFile:
    def __init__(self, file_path: str):
        self.filepath=file_path
        self.read_and_process_file()
        
        
    def read_and_process_file(self)->list:
        processed_data = []

        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(": ")  # Split at ': '
                if len(parts) == 2:
                    processed_data.append([parts[0], parts[1], 0])
        return print(processed_data)

data=ReadFile("/Users/simoneich/Desktop/Projects/Code/Python/Automation/Cards/cards/cards/txt/es_en.txt")