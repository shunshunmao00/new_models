import imageio,os
images = []
img_path = 'output/'
filenames=sorted((fn for fn in os.listdir('output') if fn.endswith('.png')))
idx = 0
while idx < len(filenames):
    filename = img_path + 'generated' + str(idx) + '.png'
    idx += 1
    print(filename)
    images.append(imageio.imread( filename))
imageio.mimsave('gif.gif', images, duration=0.1)
