from util import check_account
from util import hash_password
from util import file_open
from util import input_password

def test_check_account1():
    assert check_account("qwesdЙЙЙЙЙЙЙfxcv") == False

def test_check_account2():
    assert check_account("qwesdfxcv") == True

def test_hash_password2():
    assert hash_password('qwerty') == '684189757914'

def test_hash_password1():
    assert hash_password('zxc') == '3411449360'

def test_open_file_1():
    data_dict = file_open('data.txt')
    user_data = data_dict['Andrey']
    assert user_data[4][0][0] == 1200

def test_input_password():
    assert input_password('vadon', 'qwerty') == True