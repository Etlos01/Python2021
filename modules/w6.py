import requests as req
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


class TextComparer:
    
    def __init__(self,url_list):
        self.url_list = url_list
        self.filenames = []
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        current_index = self.index
        if current_index < len(self.filenames):
            self.index += 1
            return self.filenames[current_index]
        else:
            raise StopIteration
        
    def download(self,url):
        filename = 'title_unavailable'
        try:
            r = req.get(url)
            r.raise_for_status()
            filename = r.text.partition("Title: ")[2].splitlines()[0] + ".txt"
            with open("modules/books/" + filename, "w") as f:
                f.write(r.text)
        except req.exceptions.HTTPError as e:
            print(e.response.text)
        return filename
        
    def multi_download(self):
        urls = self.url_list
        with ThreadPoolExecutor(len(urls)) as ex:
            res = ex.map(self.download, urls)
        self.filenames = list(res)
        
    def urllist_generator(self):
        for url in self.url_list:
            yield url
            
    def avg_vowels(self, filename):
        vowels = ["A", "E", "I", "O", "U", "Y"]

        with open("modules/books/" + filename) as input_file:
            text = input_file.read()

        words = text.split()
        number_of_words = len(words)

        number_of_vowels = 0

        for word in words:
            for letter in word:
                if letter.upper() in vowels:
                    number_of_vowels += 1

        score = round(number_of_vowels / number_of_words, 5)
        return score, filename

    def hardest_read(self):        
        with ProcessPoolExecutor(multiprocessing.cpu_count()) as ex:
            results = ex.map(self.avg_vowels, self.filenames)
            
        highest_avg = None

        for result in results:
            if highest_avg is None or highest_avg[0] < result[0]:
                highest_avg = result

        return highest_avg[1]
            
    
    
    
    
    
    
    
    
    