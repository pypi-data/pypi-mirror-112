import numpy as np
import cv2

from cania_utils.disk import Disk
from cania_utils.imagej import read_ellipses_from_csv
from cania_utils.image import imnew, fill_ellipses, fill_ellipses_as_labels, overlay, bgr2hsv, split_channels, imread_grayscale, bgr2rgb, BINARY_FILL_COLOR
# TODO: huge refactoring on this module


class DatasetLoader(Disk):
    def __init__(self, location):
        super(DatasetLoader, self).__init__(location)
        self.preview = True

    def load_testing_set(self, testing_df, dataset, split_mode, counting, gt_scale):
        for img_input in np.unique(testing_df['input.filename']):
            df_img_input = testing_df[testing_df['input.filename'] == img_input]
            x, w, h, rgb = self.load_input(img_input, split_mode)

            y = []

            for index, row in df_img_input.iterrows():
                label_type = row['label.type']
                scale = row['scale']
                if label_type == 'STATS':
                    y.append(row['label.stat'])

                else:
                    filename = row['label.filename']
                    if filename == "None":
                        continue
                    label, count = self.load_label(filename, label_type, w, h, scale=scale, gt_scale=gt_scale)
                    y.append(label)
                    if counting:
                        y.append(count)
                    if self.preview:
                        preview_image = overlay(rgb, (label > 0).astype('uint8'))
                        self.next('dataset_preview').write(f"{row['label.name']}_test_{index}.png", preview_image)
            dataset.append_testing_element(x, y)
            dataset.append_testing_image(rgb)

    def load_training_set(self, training_df, dataset, split_mode, counting, gt_scale):
        for img_input in np.unique(training_df['input.filename']):
            df_img_input = training_df[training_df['input.filename'] == img_input]
            x, w, h, rgb = self.load_input(img_input, split_mode)
            dataset.n_inputs = len(x)
            y = []

            for index, row in df_img_input.iterrows():
                label_type = row['label.type']
                scale = row['scale']
                if label_type == 'STATS':
                    y.append(row['label.stat'])

                else:
                    filename = row['label.filename']
                    label, count = self.load_label(filename, label_type, w, h, scale=scale, gt_scale=gt_scale)
                    y.append(label)
                    if counting:
                        y.append(count)
                    if self.preview:
                        preview_image = overlay(rgb, (label > 0).astype('uint8'))
                        self.next('dataset_preview').write(f"{row['label.name']}_train_{index}.png", preview_image)
            dataset.append_training_element(x, y)
            dataset.append_training_image(rgb)
        return dataset

    def load(self, counting=False, preview=False, gt_scale=1.):
        # df = self.read('dataset_stats.csv')
        df = self.read('dataset.csv')
        split_mode = np.unique(df['input.splitting'])
        assert len(split_mode) == 1, 'error'
        split_mode = split_mode[0]
        testing_df = df[df['set'] == 'TESTING']
        training_df = df[df['set'] == 'TRAINING']
        labels = list(np.unique(training_df['label.name']))
        dataset = Dataset(self.location.name, labels, split_mode)
        self.load_testing_set(testing_df, dataset, split_mode, counting, gt_scale)
        self.load_training_set(training_df, dataset, split_mode, counting, gt_scale)
        return dataset

    def load_label(self, filename, label_type, w, h, scale=1., gt_scale=1.):
        labels = self.read(filename)
        if label_type == 'ELLIPSE':
            ellipses = read_ellipses_from_csv(labels, scale=scale, ellipse_scale=gt_scale)
            label_mask = imnew((h, w))
            fill_ellipses_as_labels(label_mask, ellipses)
            return label_mask, len(ellipses)

        elif label_type == 'LABELS':
            label_image = cv2.imread(str(self.location / filename), cv2.IMREAD_ANYDEPTH)
            if len(np.unique(label_image)) == 2:
                mask, _, count, labels = EndpointMaskToLabels().execute([label_image])
            else:
                count = label_image.max()
                labels = label_image
            return labels, count

        elif label_type == 'LABELS2ELLIPSES':
            label_image = cv2.imread(str(self.location / filename), cv2.IMREAD_ANYDEPTH)
            count = label_image.max()
            label_mask = imnew((h, w))
            for i in np.unique(label_image):
                if i == 0:
                    continue
                contours, _ = cv2.findContours(((label_image == i)*1).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    rect = cv2.minAreaRect(cnt)
                    cv2.ellipse(label_mask, rect, 255, -1)

            return label_mask, count

        elif label_type == 'MASK':
            label_mask = imnew((h, w))
            count = 0
            for img_path in self.next(filename).ls(regex='*.png'):
                img = imread_grayscale(str(img_path))
                label_mask = overlay(label_mask, img, color=[BINARY_FILL_COLOR], alpha=1.)
                count += 1
            return label_mask, count
        print('Label type ' + label_type + ' is not handled for now...')

    def load_input(self, filename, split_mode):
        x = []

        if split_mode == 'GRAY':
            image = imread_grayscale(str(self.location / filename))
        else:
            image = self.read(filename)

        if split_mode == 'RGB':
            assert len(image.shape) == 3, "error"
            assert image.shape[-1] == 3, "error"
            [x.append(channel) for channel in split_channels(image)]
            image_rgb = bgr2rgb(image.copy())
            w, h = image.shape[1], image.shape[0]

        elif split_mode == 'CHANNELS':
            if len(image.shape) == 2:
                x.append(image)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                w, h = image.shape[1], image.shape[0]

            else:
                [x.append(channel) for channel in image]
                image_rgb = cv2.merge((image[0], image[1], imnew(image[0].shape)))
                w, h = image.shape[2], image.shape[1]

        elif split_mode == 'DAPI':
            if len(image.shape) == 2:
                x.append(image)
            else:
                if image.shape[2] == 3:
                    x.append(image[:, :, 2])
                else:
                    DAPI_CHANNEL = 3
                    x.append(image[DAPI_CHANNEL])
            h, w = x[-1].shape
            image_rgb = cv2.merge((imnew((h, w)), imnew((h, w)), x[-1]))  # only blue channel

        elif split_mode == 'HSV':
            assert len(image.shape) == 3, "error"
            assert image.shape[-1] == 3, "error"
            new_image = bgr2hsv(image.copy())
            [x.append(channel) for channel in split_channels(new_image)]
            image_rgb = bgr2rgb(image.copy())
            w, h = image.shape[1], image.shape[0]

        elif split_mode == 'RGBHSV':
            assert len(image.shape) == 3, "error"
            assert image.shape[-1] == 3, "error"
            new_image_rgb = bgr2rgb(image.copy())
            new_image_hsv = bgr2hsv(image.copy())
            [x.append(channel) for channel in split_channels(new_image_rgb)]
            [x.append(channel) for channel in split_channels(new_image_hsv)]
            image_rgb = new_image_rgb.copy()
            w, h = image.shape[1], image.shape[0]

        elif split_mode == 'GRAY':
            assert len(image.shape) == 2, "error"
            x.append(image)
            x.append(image)
            image_rgb = self.read(filename)
            #  [x.append(channel) for channel in image_rgb]
            w, h = image.shape[1], image.shape[0]
        else:
            print('Split mode ' + split_mode + ' is not handled for now...')
        return x, w, h, image_rgb


class Subset(object):
    def __init__(self):
        self.x = []
        self.y = []
        self.preview_images = []

    def append(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def rescale(self, factor):
        self.x = self.__rescale(self.x, factor)
        self.y = self.__rescale(self.y, factor)
        self.y = self.__rescale(self.y, 1. / factor)
        self.preview_images = [cv2.resize(pi, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA) for pi in self.preview_images]
        self.preview_images = [cv2.resize(pi, None, fx=1./factor, fy=1./factor, interpolation=cv2.INTER_CUBIC) for pi in self.preview_images]

    def __rescale(self, to_rescale, factor):
        new_x = []
        for x in to_rescale:
            sub_new_x = []
            for xi in x:
                if type(xi) == int:
                    sub_new_x.append(xi)
                else:
                    if factor > 1.:
                        sub_new_x.append(cv2.resize(xi, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC))
                    else:
                        sub_new_x.append(cv2.resize(xi, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA))
            new_x.append(sub_new_x)
        return new_x


class Dataset(object):
    def __init__(self, name, labels, split_mode):
        self.__training_set = Subset()
        self.__testing_set = Subset()
        self.__labels = labels
        self.name = name
        self.n_inputs = 0
        self.n_outputs = len(self.__labels)

    def append_training_element(self, x, y):
        self.__training_set.append(x, y)

    def append_testing_element(self, x, y):
        self.__testing_set.append(x, y)

    def append_testing_image(self, image):
        self.__testing_set.preview_images.append(image)

    def append_training_image(self, image):
        self.__training_set.preview_images.append(image)

    def get_training_set(self):
        return self.__training_set

    def get_testing_set(self):
        return self.__testing_set

    def get_train_x(self):
        return self.get_training_set().x

    def get_train_y(self):
        return self.get_training_set().y

    def get_test_x(self):
        return self.get_testing_set().x

    def get_test_y(self):
        return self.get_testing_set().y

    def get_labels(self):
        return self.__labels

    def get_name(self):
        return self.name

    def rescale(self, factor):
        self.__training_set.rescale(factor)


class DatasetFactory(object):
    @staticmethod
    def create(filepath, counting, preview, gt_scale=1.):
        dataset_loader = DatasetLoader(filepath)
        dataset = dataset_loader.load(counting=counting, preview=preview, gt_scale=gt_scale)
        return dataset
