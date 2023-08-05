import matplotlib.pyplot as plt

#from functions import Functions
from cgpis.functions.functions import MorphologyFunctionSet

from skimage import data
import time


class FunctionViewer(object):
    def __init__(self):
        self.function_set = MorphologyFunctionSet()
        self.function_set.show()
        self.function_list = self.function_set.get_function_indices()

    def run(self, connections, parameters):
        fig, axs = plt.subplots(len(self.function_list), 3, figsize=(15, len(self.function_list)*3))
        for i, function in enumerate(self.function_list):
            start_time = time.time()
            img_out = self.function_set.execute(function, connections, parameters)
            print(function)
            print(img_out.shape)
            print(time.time()-start_time)
            axs[i, 0].imshow(connections[0], cmap=plt.get_cmap('gray'))
            axs[i, 1].imshow(connections[1], cmap=plt.get_cmap('gray'))
            axs[i, 2].imshow(img_out, cmap=plt.get_cmap('gray'))
            axs[i, 1].set_title('Function ' + str(function) + ', p0=' + str(parameters[0])+ ', p1=' + str(parameters[1])+ ', p2=' + str(parameters[2])+ ', p3=' + str(parameters[3])+ ', p4=' + str(parameters[4]))
        plt.axis('off')
        plt.savefig('test.png', dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    src_img = data.astronaut()
    img0 = src_img[:, :, 0]
    img1 = src_img[:, :, 1]
    FunctionViewer().run([img0, img1], [8, 8, 8, 0, 0])
