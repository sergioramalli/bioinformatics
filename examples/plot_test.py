# import numpy as np
# from matplotlib.pylab import plt #load plot library
# # indicate the output of plotting function is printed to the notebook


# def create_random_walk():
#     x = np.random.choice([-1,1],size=100, replace=True) # Sample with replacement from (-1, 1)
#     return np.cumsum(x) # Return the cumulative sum of the elements
# X = create_random_walk()
# Y = create_random_walk()
# Z = create_random_walk()

# # Plotting functionality starts here
# plt.plot(X)
# plt.plot(Y)
# plt.plot(Z)
# plt.show()


# 10 
# 1.0
# 0.65

# 30 
# 1.0
# 0.71154

# 1.0
# 0.79245

# 1.0
# 0.7375

# 1.0
# 0.75248

# 1.0
# 0.73554
# 9actn

# import matplotlib.pyplot as plt
# import pandas as pd
# girls_grades = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# boys_grades = [0.65, 0.71154, 0.79245, 0.7375, 0.75248, 0.73554]
# grades_range = [10, 30, 60, 90, 120, 150]
# plt.plot(grades_range, girls_grades, color='r')
# plt.plot(grades_range, boys_grades, color='g')
# plt.ylabel('Average Score')
# plt.xlabel('Total Hits Returned')
# plt.title('A) 9actn');
# plt.show()


# 1.0
# 0.28833

# 0.66667
# 0.32639

# 0.55556
# 0.37585

# 0.55556
# 0.37879

# 0.55556
# 0.3692

# 0.67089
# 0.37017

# girls_grades = [1.0, 0.66667, 0.55556, 0.55556, 0.55556, 0.67089]
# boys_grades = [0.28833, 0.32639, 0.37585, 0.37879, 0.3692, 0.37017]
# grades_range = [10, 30, 60, 90, 120, 150]
# plt.plot(grades_range, girls_grades, color='r')
# plt.plot(grades_range, boys_grades, color='g')
# plt.ylabel('Average Score')
# plt.xlabel('Total Hits Returned')
# plt.title('B) NP_414543_1');
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np

# label = ['0 (Contains Query)', '1', 'All']
# no_movies = [
#     0.5555556,
#     0.127907,
#     0.3787879,
# ]

# # cluster-0 0.5555556
# # cluster-1 0.127907
# # 0.3787879
# # MAX Domains 3
# # Min Domains 1

# def plot_bar_x():
#     # this is for plotting purpose
#     index = np.arange(len(label))
#     plt.bar(index, no_movies)
#     plt.xlabel('Cluster / Group', fontsize=12)
#     plt.ylabel('% EJS', fontsize=12)
#     plt.xticks(index, label, fontsize=8, rotation=0)
#     plt.title('The EJS score of each cluster and the % EJS of all sequences \n NP_414543')
#     plt.show()

# plot_bar_x()


import matplotlib.pyplot as plt
import numpy as np

label = ['0', '1 (Contains Query)', 'All']
no_movies = [
    0.5121951,
    1.0,
    0.7375,
]

# cluster-0 0.5121951
# cluster-1 1.0
# 0.7375
# MAX Domains 2
# Min Domains 1

def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(label))
    plt.bar(index, no_movies)
    plt.xlabel('Cluster / Group', fontsize=12)
    plt.ylabel('% EJS', fontsize=12)
    plt.xticks(index, label, fontsize=8, rotation=0)
    plt.title('The EJS score of each cluster and the % EJS of all sequences \n 9actn')
    plt.show()

plot_bar_x()