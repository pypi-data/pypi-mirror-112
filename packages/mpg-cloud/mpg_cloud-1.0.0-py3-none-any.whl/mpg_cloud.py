import subprocess
from bs4 import BeautifulSoup
import pathlib
from pathlib import Path
from urllib.parse import unquote, quote
from datetime import datetime

class Nextcloud():
    def __init__(self, server , username, password, webdav_token):
        self.server = server
        self.username = username
        self.password = password
        self.webdav_token = webdav_token
        
    def list_dir(self, path):
        xml = subprocess.check_output(
            f'curl -X PROPFIND -H "Depth: 1" -u {self.username}:{self.password} {self.server}{self.webdav_token}/{quote(path)}'.split()
        )
        soup = BeautifulSoup(xml, 'lxml') 
        
        if soup.find('d:error'):
            print(soup.find('s:message').text)
        
        for item in soup.find_all('d:response'):
            print(
                unquote(item.find('d:href').text.split(self.webdav_token)[1]),
                item.find('d:getlastmodified').text)

    def make_dir(self, path):
        xml = subprocess.check_output(
            f'curl -u {self.username}:{self.password} -X MKCOL {self.username}:{self.password} {self.server}{self.webdav_token}/{path}'.split()
        )
        soup = BeautifulSoup(xml, 'lxml')
        if soup.find('d:error'):
            print(soup.find('s:message').text)
            
        
    def download_file(self, path, filename, target_dir):
        binary = self.read_file(path, filename)
            
        p = Path(target_dir)
        p.mkdir(parents=True, exist_ok=True)
        p = p.joinpath(filename)
        with open(p, 'wb') as file:
            file.write(binary)
        
        
    def read_file(self, path, filename):
        p = Path(path).joinpath(filename)
        binary = subprocess.check_output(f'curl -X GET -u {self.username}:{self.password} {self.server}{self.webdav_token}/{quote(str(p))}'.split())
        if r'<s:exception>Sabre\\DAV\\Exception\\NotFound</s:exception>' in str(binary):
            soup = BeautifulSoup(binary, 'lxml')
            print(soup.find('s:message').text)
        return binary
    
    
    def upload_file(self, local_file, path, filename, add_date=False):
        timestamp = ''
        if add_date:
            timestamp = datetime.now().strftime('_%Y_%m_%d')
            if '.' in filename:
                splitted_name = filename.split('.')
                splitted_name[-2] = splitted_name[-2] + timestamp
                filename = '.'.join(splitted_name)
            else:
                filename = filename + timestamp
        p = Path(path).joinpath(filename)
        xml = subprocess.check_output(f'curl -u {self.username}:{self.password} -T {local_file} {self.server}{self.webdav_token}/{quote(str(p))}'.split())
        soup = BeautifulSoup(xml, 'lxml')
        if soup.find('d:error'):
            print(soup.find('s:message').text)
    

    def upload_folder(self, local_folder, target_folder, add_date=False, add_date_recursive=False): 
        timestamp = ''
        if add_date:
            timestamp = datetime.now().strftime('_%Y_%m_%d')
        local_folder = Path(local_folder) 
        self.make_dir(Path(target_folder).joinpath(local_folder.name + timestamp))

        for i in local_folder.glob('**/*'):
            splitted_path = str(i).split('/')
            splitted_path[0] = splitted_path[0] + timestamp
            p = '/'.join(splitted_path)
            rel_path = Path(target_folder).joinpath(p)
            if i.is_dir():
                #print(f'Make dir: {rel_path}')
                self.make_dir(path=rel_path)
            if i.is_file():
                splitted_path = str(rel_path).split('/')
                filename = splitted_path.pop()
                path = Path('/'.join(splitted_path))
                #print(path, filename)
                #print(f'Upload file {i}')
                self.upload_file(local_file=i, path=path, filename=filename, add_date=add_date_recursive)
                
    
    def delete_file(self, path):
        if path is None or path == '' or path ==' ':
            print('Do not delete the root dir!')
            return
        xml = subprocess.check_output(f'curl -u {self.username}:{self.password} -X DELETE {self.server}{self.webdav_token}/{quote(path)}'.split())
        soup = BeautifulSoup(xml, 'lxml')
        if soup.find('d:error'):
            print(soup.find('s:message').text)