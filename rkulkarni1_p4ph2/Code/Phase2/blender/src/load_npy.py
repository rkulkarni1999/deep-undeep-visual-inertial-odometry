import numpy as np

def load_logged_data():
    # Loads the data from the .npy file
    data = np.load('./log/final_data_relative.npy', allow_pickle=True).item()
    return data

logged_data = load_logged_data()

data_array = logged_data['data']
rotation_matrices = logged_data['rotation_matrices']


print(rotation_matrices.shape)
# print(np.round(data_array[:10,:], decimals=2))
