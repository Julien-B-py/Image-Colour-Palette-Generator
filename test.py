from PIL import Image
import numpy

I = numpy.asarray(Image.open('Face_nord_de_la_Grande_Casse.JPG'))

print(I)
print(I.shape)


print('****')
# 3 to group r, g and b values, -1 to let numpy determine the number for rows
print(I.reshape(-1, 3))

colors, counts = numpy.unique(I.reshape(-1, 3),
                              return_counts=True,
                              axis=0)
print('****')
print(colors)
print(counts)

print(colors.shape)

# Reshape count to have as many lines as colors
counts =counts.reshape(colors.shape[0],-1)
print('****')
# Add count in the 4th column for each row
test = numpy.concatenate((colors, counts), axis=1)
print(test)


sorted_array = test[numpy.argsort(test[:, 3])]
print('****')
print(sorted_array)


# Sorted values in descending order of occurrences
print('****')
print(sorted_array[::-1])


