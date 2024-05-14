import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again')
    return response


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    # print(first5_char, tail)
    # print(response)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password')
        else:
            print(f'{password} was NOT FOUND, Carry On!')
    return 'done!'

def main2(filename):
    # small update from above main function, here passwords are retrieved from a text file
    with open(filename, 'rb') as file:
        passwords = file.readlines()
    for password in passwords:
        password = password.strip() # strip white spaces
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password')
        else:
            print(f'{password} was NOT FOUND, Carry On!')
    return 'done!'

# if __name__ == '__main__':
#     sys.exit(main(sys.argv[1:]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please enter the format as: python3 PasswordChecker.py <file_path>')
        sys.exit(1)
    sys.exit(main2(sys.argv[1]))
