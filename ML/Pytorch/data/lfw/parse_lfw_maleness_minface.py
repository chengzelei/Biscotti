from sklearn.datasets import fetch_lfw_people
import numpy as np
import pdb
import matplotlib.pyplot as plt

# rescales a numpy array to be in [a, b]
def rescale(x, a, b):
    minNum = np.min(x)
    maxNum = np.max(x)
    return (b - a)*(x - minNum) / (maxNum - minNum) + a 


MALENESS_THRESHOLD = 0 # threshold at which the person is classified as a male
MIN_FACES = 50
TRAIN_CUT = 0.75

print("Fetching people with at least " + str(MIN_FACES) + " pictures.")
lfw_people = fetch_lfw_people(color=True, min_faces_per_person=MIN_FACES)

print("Loading maleness attributes")
maleness_lookup = np.load('lfw_maleness.npy').item()

# downloads all faces with more than 5 images
person = 3
target_names = lfw_people.target_names
target = lfw_people.target
data = lfw_people.data
data = lfw_people.data[lfw_people.target == person]
n,d = data.shape
y = np.zeros(n)  # 1 for male 0 for female
# plt.imshow( np.reshape(rescale(data[0], 0, 1), (62, 47, 3))); plt.show()
print("Labelling maleness")
for i in range(n):
    target_name = target_names[target[i]]    

    avg_maleness = np.mean(maleness_lookup[target_name])
    if avg_maleness > MALENESS_THRESHOLD:
        y[i] = 1
    else:
        y[i] = 0

print("Storing data and labels")

data_slice = np.hstack((data, y[:, None]))
np.save("lfw_maleness_person3_over50", data_slice)
# TODO: Randomly shuffle data_slice before
# np.save("lfw_maleness_train", data_slice[0:int(n*TRAIN_CUT)])
# split into num_client parts
# num_clients = 10
# for i in range(num_clients):
#     slice_size = int(n*TRAIN_CUT) / num_clients
#     left_idx = i*slice_size
#     right_idx = (i+1)*slice_size
#     np.save("lfw_maleness_train"+str(i), data_slice[left_idx:right_idx])
# np.save("lfw_maleness_test", data_slice[int(n*TRAIN_CUT):])

