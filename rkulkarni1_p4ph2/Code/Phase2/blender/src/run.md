# Steps to Generate Data

- Change the `MP_{shape}.csv` file (obtained) from matlab in `usercode.py`

- Run the main script using the blender scripting tab. `states.npy` and `states.mat` file will be saved in the `log` folder.

- Run the below script and then send `full_states_for_imuSensor.mat` to matlab for post proocessing
```
python src/export2imuSensor.py 
```

- After matlab processing store `full_states_refactored_with_imu.mat` in the `logs` folder and then run 
```
python src/convert_mat2npy.py
```
It will save `full_states_refactored_with_imu.npy` 

- Run the below script to generate final data which will generate `final_data_absolute_relative.npy` 
```
python src/final_data.py
```
