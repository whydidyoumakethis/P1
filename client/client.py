import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
session = requests.Session()



def register():
    username = input('Enter username: ')
    email = input('Enter email: ')
    password = input('Enter password: ')
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    response = session.post(f'{BASE_URL}/users/', json=data)

    if response.status_code == 201:
        print('\n -----------------')
        print('User registered successfully')
    else:
        print('\n -----------------')
        print('Error registering user')
        print(response.json())

def login(url=None):
    global BASE_URL
    if url and url.strip():
        BASE_URL = url.strip()
        print(f'Base URL set to {BASE_URL}')
        
    username = input('Enter username: ')
    password = input('Enter password: ')
    data = {
        'username': username,
        'password': password
    }
    response = session.post(f'{BASE_URL}/api/token-login/', json=data)

    if response.status_code == 200:
        print('\n -----------------')
        print('User logged in successfully')
        token = response.json()['token']
        
        session.headers.update({'Authorization': f'Token {token}'})
    else:
        print('\n')
        print('Error logging in')
        print(response.json())

def logout():
    response = session.post(f'{BASE_URL}/api/logout/')

    if response.status_code == 200:
        print('\n -----------------')
        print('User logged out successfully')
        session.headers.pop('Authorization', None)
        session.cookies.clear()
    else:
        print('\n -----------------')
        print('Error logging out')
        print(response.json())

def list_modules():
    response = session.get(f'{BASE_URL}/modules/')

    if response.status_code == 200:
        modules = response.json()
        print('--------------------------------------------')
        print('code | name | year | semester | professors')
        print('--------------------------------------------')
        for module in modules:
            print(module['code'] + ' | ' + module['name'] + ' | ' + str(module['year']) + ' | ' + str(module['semester']) + ' | ' + ', '.join([professor['name'] + '('+ professor['code'] +')' for professor in module['professors']]))
    else:
        print('Error fetching modules')
        print(response.json())

def list_professors_ratings():
    response = session.get(f'{BASE_URL}/professors/')

    if response.status_code == 200:
        professors = response.json()
        print('--------------------------------------------')
        print('name | avg_rating | stars')
        print('--------------------------------------------')
        for professor in professors:
            print(professor['name'] + '('+professor['code']+')' + ' | ' + str(professor['avg_rating']) + ' | ' + professor['stars'])
    else:
        print('Error fetching professors')
        print(response.json())


def get_professor_module_rating(args):

    if args is None:
        print('Please provide professor and module codes')
        return
    
    professor_code, module_code = args.split(' ')

    response = session.get(f'{BASE_URL}/professors/{professor_code}/modules/{module_code}/')

    if response.status_code == 200:
        data = response.json()
        print('--------------------------------------------')
        print('professor | module | avg_rating | stars')
        print('--------------------------------------------')
        print(data['professor'] +'('+data['professor_code']+')' + ' | ' + data['module'] + ' | ' + str(data['avg_rating']) + ' | ' + data['stars'])
    else:
        print('Error fetching rating')
        print(response.json())


def rate_professor(args):
    if args is None:
        print('Please provide professor, module, and a rating from 1 to 5')
        return
    proffessor_code, module_code, year, semester, rating, = args.split(' ')
    data = {
        'professor': proffessor_code,
        'module': module_code,
        'year': int(year),
        'semester': int(semester),
        'rating': int(rating)
    }
    response = session.post(f'{BASE_URL}/ratings/', json=data)

    if response.status_code == 201:
        print('Rating submitted successfully')
    else:
        print('Error submitting rating')
        print(response.json())

def main():

    while True:
        print('\n')
        print('====================')

        usr_input = input('Enter command: ').split(' ', 1)
        choice = usr_input[0].strip()
        args = usr_input[1].strip() if len(usr_input) > 1 else None
        print(f"choice: {choice}")
        print(f"args: {repr(args)}")
        if choice == 'register':
            register()
        elif choice == 'login':
            login(args)
        elif choice == 'logout':
            logout()
        elif choice == 'list':
            list_modules()
        elif choice == 'view':
            list_professors_ratings()
        elif choice == 'average':
            get_professor_module_rating(args)
        elif choice == 'rate':
            rate_professor(args)
        else:
            print('Invalid choice')
        

if __name__ == '__main__':
    main()
