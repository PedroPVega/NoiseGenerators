import matplotlib.pyplot as plt

def ShowFourNoises(noises, titles):
    f, axes = plt.subplots(2, 2)
    axes[0, 0].imshow(noises[0], cmap = 'gray')
    axes[0, 0].set_title(titles[0])
    axes[0, 1].imshow(noises[1], cmap = 'gray')
    axes[0, 1].set_title(titles[1])
    axes[1, 0].imshow(noises[2], cmap = 'gray')
    axes[1, 0].set_title(titles[2])
    axes[1, 1].imshow(noises[3], cmap = 'gray')
    axes[1, 1].set_title(titles[3])
    plt.tight_layout()
    plt.show()
        
def ShowMap(mat):
    image = plt.imshow(mat, cmap = 'gray')
    plt.show()