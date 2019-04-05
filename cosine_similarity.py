import math
def cosine_similarity_measure(vectorization1,vectorization2):
    sum_x_squared, sum_x_y, sum_y_squared = 0, 0, 0
    for i in range(len(vectorization1)): # both have the same length
        x = vectorization1[i]; y = vectorization2[i]
        sum_x_squared += x*x
        sum_y_squared += y*y
        sum_x_y += x*y
    return sum_x_y/math.sqrt(sum_x_squared*sum_y_squared)

print(cosine_similarity_measure([2,3,4],[2,3,4])) # equal 1.0