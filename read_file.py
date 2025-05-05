import random

class ReadFile:
    def __init__(self, file_path):
        self.file_name = file_path
        #self.data = self.read_txt_file()
        #self.randomword = self.random_word()
        self.data = self.read_and_process_file()
        self.random_word()
        
    def read_and_process_file(self):
        processed_data = []
    
        with open(self.file_name, 'r', encoding='utf-8') as file:
            for line in file:
              parts = line.strip().split(": ")  # Split at ': '
              if len(parts) == 2:
                  processed_data.append([parts[0], parts[1], 0])
    
        return processed_data 
    
    def random_number(self) -> None:
        self.randomnumber = random.randint(0, len(self.data) - 1)
        return self.randomnumber
        
    def random_word(self)-> str:
        number= self.random_number()
        randomWord_es=self.data[number][0]
        randomWord_en=self.data[number][1]
        print(self.data[number][-1])
        self.data[number][-1]+=1
        print(self.data[number][-1])
        return randomWord_es, randomWord_en
    
    
    def remove_word(self, word: str)-> None:
        print(len(self.data))
        print(word)
        if word in self.data:
            self.data.remove(word)
            print('removed word')
        else:
            print('word not found')
        print(len(self.data))
        
        