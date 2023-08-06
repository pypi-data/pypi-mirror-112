import requests
from pathlib import Path
from datetime import datetime

class Seafile():
    def __init__(self, server, username, password):
        if server[-1] == '/':
            server = server[:-2]
            
        self.server = server
        data = {
          'username': username,
          'password': password,
        }
        response = requests.post(f'{self.server}/api2/auth-token/', data=data)
        self.token = response.json()['token']
        self.headers = {
            'Authorization': f'Token {self.token}',
            'Accept': 'application/json; charset=utf-8; indent=4'
        }
        
    def account_info(self):
        response = requests.get(f'{self.server}/api2/account/info/', headers=self.headers)
        return response.json()
    
    
    def repo_list(self):
        response = requests.get('https://keeper.mpdl.mpg.de/api2/repos/', headers=self.headers)
        return response.json()
    
    
    def repo_share(self, repo, userlist, permissions='rw'):
        if isinstance(userlist, str):
            userlist = [userlist]

        params = (
            ('p', '/'),
        )
        data = [
          ('share_type', 'user'),
          ('permission', permissions),
        ] + [('username', user) for user in userlist]
        response = requests.put(
            f'{self.server}/api2/repos/{repo}/dir/shared_items/', 
            headers=self.headers, 
            params=params, 
            data=data)
        return response
    
    
    def repo_unshare(self, repo, user):
        params = (
            ('p', '/'),
            ('share_type', 'user'),
            ('username', user),
        )
        response = requests.delete(
            f'{self.server}/api2/repos/{repo}/dir/shared_items/', 
            headers=self.headers, 
            params=params)
        return response
    
    
    def file_info(self, repo, file):
        params = (
            ('p', f'/{file}'),
        )
        response = requests.get(
            f'{self.server}/api2/repos/{repo}/file/detail/', 
            headers=self.headers, 
            params=params
        )     
        return response.json()

    def downloadlink(self, repo, file, reuse='1'):
        params = (
            ('p', f'/{file}'),
            ('reuse', reuse),
        )
        response = requests.get(
            f'{self.server}/api2/repos/1229f71b-a616-451e-9da2-b6fa4d5a47a7/file/', 
            headers=self.headers, 
            params=params)
        return response.json()
    
    
    def uploadlink(self, repo):
        response = requests.get(f'{self.server}/api2/repos/{repo}/upload-link/', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.ConnectionError
    
    
    def file_download(self, repo, file, local_dir):
        if file[0] == '/':
            file = file[1:]
        download_url = self.downloadlink(repo, file)
        response = requests.get(download_url)
        if response.status_code == 200:
            p = Path(local_dir).joinpath(file).parent
            p.mkdir(parents=True, exist_ok=True)
            p = Path(local_dir).joinpath(file)
            with open(p, 'wb') as fh:
                fh.write(response.content)
        else:
            raise requests.ConnectionError(f'Statuscode {response.status_code}')
        return response 
    
        
    def file_upload(self, repo, file, remote_dir, add_date=False):
        timestamp = ''
        filename = file
        if add_date:
            timestamp = datetime.now().strftime('_%Y_%m_%d')
            if '.' in filename:
                splitted_name = filename.split('.')
                splitted_name[-2] = splitted_name[-2] + timestamp
                filename = '.'.join(splitted_name)
            else:
                filename = filename + timestamp

        if remote_dir[0] == '/': remote_dir = remote_dir[1:]

        params = (
            ('ret-json', '1'),
        )
        files = {
            'file': (filename, open(file, 'rb')),
            'parent_dir': (None, '/'),
            'replace': (None, '1'),
        }

        if remote_dir != '/':
            files['relative_path'] = (None, remote_dir)

        url = self.uploadlink(repo)

        response = requests.post(url, headers=self.headers, params=params, files=files)
        return response
        
        
    def file_delete(self, repo, file):
        params = (
            ('p', f'/{file}'),
        )
        response = requests.delete(
            f'{self.server}/api2/repos/{repo}/file/', 
            headers=self.headers, 
            params=params)
        return response
        
    def file_search(self, repo, file):
        params = (
            ('repo_id', repo),
            ('q', file),
        )
        response = requests.get(f'{self.server}/api2/search/', headers=self.headers, params=params)
        return response.json()
    
    
    def file_rename(self):
        raise NotImplementedError
        
        
    def file_move(self):
        raise NotImplementedError
        
    
    def folder_list_content(self, repo, path, recursive = True):
        params = (
            ('p', f'/{path}'),
            ('recursive', '1' if recursive else '0'),
        )
        response = requests.get(f'{self.server}/api2/repos/{repo}/dir/', headers=self.headers, params=params)
        return response.json()
    

    def folder_download(self, repo, remote_dir, local_dir):
        for entry in self.folder_list_content(repo, remote_dir, recursive=True):
            if entry.get('type')=='dir': continue
            p = entry.get('parent_dir')[1:]
            file = entry.get('name')
            self.file_download(repo, str(Path(p).joinpath(file)), local_dir=local_dir )
        
    
    def folder_upload(self, repo, local_dir, remote_dir, add_date=False, add_date_recursive=False):
        timestamp = ''
        if add_date:
            timestamp = datetime.now().strftime('_%Y_%m_%d')
        local_dir = Path(local_dir)
        for i in local_dir.glob('**/*'):
            if(i.is_dir()): continue
            splitted_path = str(i).split('/')
            splitted_path[0] = splitted_path[0] + timestamp
            file_path = '/'.join(splitted_path)
            r_dir = Path(remote_dir).joinpath(file_path).parent
            self.file_upload(repo, file=str(i), remote_dir=str(r_dir), add_date=add_date_recursive)

    
    def folder_rename(self, repo, path, new_name):
        if path[0] == '/': path=path[1:]
        params = (
            ('p', f'/{path}'),
        )
        data = {
          'operation': 'rename',
          'newname': new_name
        }
        response = requests.post(
            f'{self.server}/api2/repos/{repo}/dir/', 
            headers=self.headers, 
            params=params, 
            data=data)
        return response

        
    def folder_delete(self, repo, path):
        if path[0] == '/': path=path[1:]
        params = (
            ('p', f'/{path}'),
        )
        response = requests.delete(
            f'{self.server}/api2/repos/{repo}/dir/', 
            headers=self.headers, 
            params=params)
        return response

    
    def folder_create(self, repo, path):
        params = (
            ('p', f'/{path}'),
        )

        data = {
          'operation': 'mkdir'
        }
        response = requests.post(
            f'{self.server}/api2/repos/{repo}/dir/', 
            headers=self.headers, 
            params=params, 
            data=data)
        return response

        
    def folder_detail(self, repo, path):
        params = (
            ('path', path),
        )
        response = requests.get(
            f'{self.server}/api/v2.1/repos/{repo}/dir/detail/', headers=self.headers, params=params)
        return response.json()
