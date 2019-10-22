import scipy.io
mat = scipy.io.loadmat('interfaces.mat')
# print all info in interfaces.mat
print(mat)
# print only the 'simulation_data'
print(mat['simulation_data'])
# print only the 'measured_data'
print(mat['measured_data'])
