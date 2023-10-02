import os
import pickle


async def get_user_list():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    last_options_files = [file for file in files if file.startswith("last_options_")]

    users_id = []
    for options_files in last_options_files:
        user_id = options_files.split('_')[-1].split('.')[0]
        users_id.append(user_id)

    return users_id


async def save_to_pickle(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_from_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

print(load_from_pickle('last_options_674796107.pkl'))

