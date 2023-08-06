import numpy as np
import math
import abc
from tflite_runtime.interpreter import Interpreter
# noinspection PyPackageRequirements
import cv2
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.models import BaseModel
from wizzi_utils.models import models_configs as cfg


def get_object_detection_models(ack: bool = False, tabs: int = 1) -> list:
    model_names = []
    count = 0
    for i, (m_name, m_dict) in enumerate(cfg.MODELS_CONFIG.items()):
        if m_dict['job'] == cfg.Jobs.OBJECT_DETECTION.value:
            if ack:
                count += 1
                mt.dict_as_table(table=m_dict, title='{}){}'.format(count, m_name), tabs=tabs)
            model_names.append(m_name)
    return model_names


class OdBaseModel(BaseModel):
    DEFAULT_COLOR_DICT = {
        'label_bbox': 'black',  # if draw_labels - text bg color
        'text': 'white',  # if draw_labels - text bg color
        'sub_image': 'blue',  # if draw_sub_image - sub image bbox color
        'default_bbox': 'red',  # bbox over the detection
    }

    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            allowed_class: list = None,
    ):
        super().__init__(save_load_dir=save_load_dir, model_name=model_name)
        if not self.model_name_valid(model_name):
            exit(-1)
        self.model_cfg = cfg.MODELS_CONFIG[model_name]
        self.labels = self.model_cfg['labels_dict']['labels']
        self.allowed_classes = self.labels if allowed_class is None else allowed_class
        return

    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def to_string(self, tabs: int = 1) -> str:
        print('abs method - needs implementation')
        exit(-1)
        return ''

    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def detect_cv_img(
            self,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            img_title: str = None
    ) -> list:
        """
        :param cv_img: open cv image
        :param fp: float precision on the score percentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts. see extract_results()
        """
        print('abs method - needs implementation')
        exit(-1)
        return []

    def draw_detections(
            self,
            detections: list,
            cv_img: np.array,
            colors_d: dict = None,
            draw_labels: bool = False,
            draw_tl_image: bool = False,
            draw_sub_image: bool = False
    ) -> None:
        """
        :param detections: output of self.classify_cv_img() on od models
        :param colors_d: colors in str form:
            bbox color
            label_bbox color
            text color
            if class_id_bbox exist - color the bbox of that class in the given color
            e.g. colors_d={
                    'label_bbox': 'black',  # if draw_labels - text bg color
                    'text': 'white',  # if draw_labels - text bg color
                    'sub_image': 'blue',  # if draw_sub_image - sub image bbox color
                    'default_bbox': 'red',  # bbox over the detection
                    'person_bbox': 'black', # custom color per class person
                    'dog_bbox': 'lime',  # custom color per class dog
                    'cat_bbox': 'magenta',  # custom color per class cat
                },
        :param cv_img: the same that was given input to self.classify_cv_img()
        :param draw_labels: draw label(label_bbox and text on it) on the bbox
        :param draw_tl_image: draw traffic light if exists - has colors in it
        :param draw_sub_image: draw sub image if exists
        :return:
        """
        if colors_d is None:
            colors_d = self.DEFAULT_COLOR_DICT
        for detection in detections:
            label = detection['label']
            score_percentage = detection['score_percentage']
            x0 = detection['bbox']['x0']
            y0 = detection['bbox']['y0']
            x1 = detection['bbox']['x1']
            y1 = detection['bbox']['y1']
            traffic_light_d = detection['traffic_light'] if 'traffic_light' in detection else {}
            bbox_sub_image_d = detection['bbox_sub_image'] if 'bbox_sub_image' in detection else None

            # DRAW BBOX
            k = '{}_bbox'.format(label)  # check custom color for this class
            color_bgr = pyplt.get_BGR_color(colors_d[k]) if k in colors_d else pyplt.get_BGR_color(
                colors_d['default_bbox'])
            cv2.rectangle(img=cv_img, pt1=(x0, y0), pt2=(x1, y1), color=color_bgr, thickness=2)

            if draw_tl_image:  # DRAW TL
                for loc, point_and_color in traffic_light_d.items():
                    cv2.circle(cv_img, center=tuple(point_and_color['point']), radius=2,
                               color=pyplt.get_BGR_color(point_and_color['color']), thickness=-1)

            if draw_sub_image and bbox_sub_image_d is not None:  # DRAW sub image
                pt1 = (bbox_sub_image_d['x0'], bbox_sub_image_d['y0'])
                pt2 = (bbox_sub_image_d['x1'], bbox_sub_image_d['y1'])
                cv2.rectangle(img=cv_img, pt1=pt1, pt2=pt2, color=pyplt.get_BGR_color(colors_d['sub_image']),
                              thickness=1)  # sub image

            if draw_labels:
                label_conf = '{}({}%)'.format(label, score_percentage)  # DRAW labels
                cvt.add_text(cv_img, header=label_conf, pos=(x0, y1), text_color=colors_d['text'], with_rect=True,
                             bg_color=colors_d['label_bbox'], bg_font_scale=2)
        return

    @staticmethod
    def add_traffic_light_to_detections(detections: list, traffic_light_p: dict) -> list:
        """
        :param detections: detections from classify_cv_img()
        :param traffic_light_p: dict of loc to float percentage
            if not none get 3 2d points in a traffic_light form
            e.g. traffic_light={
                    # x of all traffic_light points is frame_width / 2
                    'up': 0.2,  # red light will be take from y = frame_height * 0.2
                    'mid': 0.3,  # yellow light will be take from y = frame_height * 0.3
                    'down': 0.4  # green light will be take from y = frame_height * 0.3
                }
        :return: for each detection in detections: add entry 'traffic_light' with a dict with keys up, mid, down
                    each has location to dict of point and color:
            e.g.
                'traffic_light'= { # x_mid = frame_width / 2
                'up': {'point': [x_mid, y_up], 'color': 'red'},  # y_up = frame_height * traffic_light['up']
                'mid': {'point': [x_mid, y_mid], 'color': 'yellow'},
                'down': {'point': [x_mid, y_down], 'color': 'green'}
                }
        """
        for detection_d in detections:
            # label = detection_d['label']
            # score = detection_d['score_percentage']
            x0 = detection_d['bbox']['x0']
            y0 = detection_d['bbox']['y0']
            x1 = detection_d['bbox']['x1']
            y1 = detection_d['bbox']['y1']
            y_dist = y0 - y1  # image is flipped on y axis
            x_dist = x1 - x0
            # prepare 'traffic_light' points
            # on x middle
            # on y 20% 30% 40% from the top
            x_mid = int(x0 + 0.5 * x_dist)
            y_up = int(y0 - traffic_light_p['up'] * y_dist)
            y_mid = int(y0 - traffic_light_p['mid'] * y_dist)
            y_down = int(y0 - traffic_light_p['down'] * y_dist)
            traffic_light_out = {
                'up': {'point': [x_mid, y_up], 'color': 'red'},
                'mid': {'point': [x_mid, y_mid], 'color': 'yellow'},
                'down': {'point': [x_mid, y_down], 'color': 'green'}
            }
            detection_d['traffic_light'] = traffic_light_out
        return detections

    @staticmethod
    def add_sub_sub_image_to_detection(detections: list, cv_img: np.array, bbox_image_p: dict) -> list:
        """
        :param detections:
        :param cv_img:
        :param bbox_image_p: dict that specify how much from the bbox to save
                bbox_image_p={  # all bbox
                    'x_start': 0,
                    'x_end': 1,
                    'y_start': 0,
                    'y_end': 1,
                },
                bbox_image_p={  # sub bbox
                    'x_start': 0.5,  # start from middle
                    'x_end': 0.9,     # go to the right until 90% of the width
                    'y_start': 0,  # 0 start from the bottom
                    'y_end': 0.4,  # end at 40% from bottom
                },
        :return: for each detection in detections: add entry 'bbox_sub_image' with a dict with keys image,x0,x1,y0,y1
                    if you imshow - you will get the bbox of the detection (according to bbox_image_p)
        """
        for detection_d in detections:
            # label = detection_d['label']
            # confidence = detection_d['score_percentage']
            x0 = detection_d['bbox']['x0']
            y0 = detection_d['bbox']['y0']
            x1 = detection_d['bbox']['x1']
            y1 = detection_d['bbox']['y1']
            y_dist = y0 - y1  # image is flipped on y axis
            x_dist = x1 - x0
            # prepare sub sub image (a part of the bbox)
            # y1 is the bottom
            sub_y0 = int(y1 + bbox_image_p['y_start'] * y_dist)
            sub_y1 = int(y1 + bbox_image_p['y_end'] * y_dist)
            sub_x0 = int(x0 + bbox_image_p['x_start'] * x_dist)
            sub_x1 = int(x0 + bbox_image_p['x_end'] * x_dist)
            detection_d['bbox_sub_image'] = {
                'image': cv_img[sub_y0:sub_y1, sub_x0:sub_x1].tolist(),
                'x0': sub_x0,
                'y0': sub_y0,
                'x1': sub_x1,
                'y1': sub_y1,
            }
        return detections


class TflOdModel(OdBaseModel):
    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            allowed_class: list = None,
            threshold: float = None,
            nms: dict = None,
            check_type: bool = True
    ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        :param threshold: only detection above this threshold will be pass first filter
        :param nms: non maximum suppression threshold 2 thresholds
            score_threshold and nms_threshold
            can be None in the cfg - if None pass and None on cfg: no nms
        :param allowed_class: ignore rest of class. list of strings
        example:
        model = od.TflOdModel(
            save_load_dir=m_save_dir,
            model_name=model_name,
        )
        """
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, allowed_class=allowed_class)
        if check_type and not self.model_type_valid(self.model_cfg['model_type'], cfg.ModelType.OdTflNormal.value):
            exit(-1)
        if threshold is not None:
            self.model_cfg['threshold'] = threshold
        if threshold is not None:
            self.model_cfg['nms'] = nms

        model_fp = "{}/{}.tflite".format(self.local_path, self.model_name)
        self._download_if_needed(local_path=model_fp, url_dict=self.model_cfg['tflite'])
        self.model_size = mt.file_or_folder_size(model_fp)
        # print('Loading {}(size {}, {} classes)'.format(self.model_name, self.model_size, len(self.labels)))
        self.interpreter = Interpreter(model_path=model_fp, num_threads=4)
        # allocate input output placeholders
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        _, input_height, input_width, _ = self.interpreter.get_input_details()[0]['shape']
        self.model_cfg['in_dims'] = (input_width, input_height)
        self.model_cfg['input_type'] = self.interpreter.get_input_details()[0]['dtype']
        quantization = self.interpreter.get_input_details()[0]['quantization']
        # need to normalize if model doesn't do quantization (then quantization == (0.0, 0))
        # else e.g. quantization == (0.0078125, 128) - no need to normalize
        self.model_cfg['normalize_RGB'] = True if quantization == (0.0, 0) else False

        # # you can print this to get more details on the model
        # mt.dict_as_table(self.interpreter.get_input_details()[0], title='input')
        # mt.dict_as_table(self.interpreter.get_output_details()[0], title='output')
        # mt.dict_as_table(self.interpreter.get_tensor_details()[0], title='tensor')
        return

    def to_string(self, tabs: int = 1) -> str:
        tabs_s = tabs * '\t'
        string = '{}{}'.format(tabs_s, mt.add_color(string='TflOdModel:', ops='underlined'))
        string += '\n\t{}name= {} (size {})'.format(tabs_s, self.model_name, self.model_size)
        string += '\n\t{}local_path= {}'.format(tabs_s, self.local_path)
        string += '\n\t{}{}'.format(tabs_s, mt.to_str(self.allowed_classes, 'allowed_classes'))
        string += '\n{}'.format(mt.dict_as_table(self.model_cfg, title='cfg', fp=6, ack=False, tabs=tabs + 1))
        return string

    def prepare_input(self, cv_img: np.array) -> np.array:
        """
        :param cv_img:
        resize and change dtype to predefined params
        :return:
        """
        img_RGB = cvt.BGR_img_to_RGB(cv_img)
        if self.model_cfg['normalize_RGB']:
            # normalization is done via the authors of the MobileNet SSD implementation
            center = 127.5
            img_RGB = (img_RGB - center) / center  # normalize image
        img = cv2.resize(img_RGB, self.model_cfg['in_dims'])  # size of this model input
        img_processed = np.expand_dims(img, axis=0).astype(self.model_cfg['input_type'])  # a,b,c -> 1,a,b,c
        return img_processed

    def run_network(self, img_preprocessed: np.array) -> None:
        self.interpreter.set_tensor(self.input_details[0]['index'], img_preprocessed)  # set input tensor
        self.interpreter.invoke()  # run
        return

    def extract_results(
            self,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            img_title: str = None
    ) -> list:
        """
        :param cv_img: cv image
        :param fp: float precision on the score precentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts:
        dict is a detection of an object above threshold.
            has items:
                label:str e.g. 'person'
                score_percentage: float e.g. 12.31
                bbox: dict with keys x0,y0,x1,y1
                #  pt1 = (x0, y0)  # obj frame top left corner
                #  pt2 = (x1, y1)  # obj frame bottom right corner
        """
        # get results
        boxes_np = self.interpreter.get_tensor(self.output_details[0]['index'])[0]  # bboxes
        labels_ids_np = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # labels as list of floats
        scores_np = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # confidence
        # count_np = interpreter.get_tensor(output_details[3]['index'])[0]  # number of detections

        if ack:
            title_suffix = '' if img_title is None else '{} '.format(img_title)
            title = '{} detections({}) on image {}{}:'.format(self.model_name, len(scores_np), title_suffix,
                                                              cv_img.shape)
            print('{}{}'.format(tabs * '\t', title))
            print('\n{}Meta_data(all detections):'.format(tabs * '\t'))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(labels_ids_np, 'labels_ids_np')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(scores_np, 'scores')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(boxes_np, 'boxes')))

            print('\n{}Detections post first threshold and allowed_class:'.format(tabs * '\t'))
        if len(scores_np) <= 0:
            # no detections made
            if ack:
                print('{}\tNo detections found'.format(tabs * '\t'))
            return []
        boxes_nms_form_list = []  # x,y,w,h in proportion to the image, UNLIKE boxes_np which is x0,y0,x1,y1
        passed_first_filter = []  # threshold <= confidence and label in self.allowed_class
        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        for i, (bbox, label_id, confidence) in enumerate(zip(boxes_np, labels_ids_np, scores_np)):
            if self.model_cfg['threshold'] <= confidence <= 1.0 and label_id is not math.isnan(label_id):
                label = self.labels[int(label_id)]
                if label in self.allowed_classes:
                    # prepare box nms form and save index passed
                    center_x = int(bbox[0] * img_w)
                    center_y = int(bbox[1] * img_h)
                    w = int(bbox[2] * img_w)
                    h = int(bbox[3] * img_h)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    boxes_nms_form_list.append([x, y, w, h])
                    passed_first_filter.append(i)
                    if ack:
                        msg = '{}\t{})Detected class {}: {}({:.2f}%)'
                        print(msg.format(tabs * '\t', i, int(label_id), label, confidence * 100))

        boxes_np = boxes_np[passed_first_filter]
        labels_ids_np = labels_ids_np[passed_first_filter]
        scores_np = scores_np[passed_first_filter]
        if len(scores_np) <= 0:
            if ack:
                print('{}\tNo detections passed first filter'.format(tabs * '\t'))
            return []
        if ack:
            print('{}Meta_data:'.format(tabs * '\t'))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(labels_ids_np, 'labels_ids_np')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(scores_np, 'scores')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(boxes_np, 'boxes')))

        if self.model_cfg['nms'] is not None:  # activate nms
            # https://gist.github.com/leandrobmarinho/26bd5eb9267654dbb9e37f34788486b5
            passed_nms_filter = cv2.dnn.NMSBoxes(
                bboxes=boxes_nms_form_list,
                scores=scores_np.tolist(),
                score_threshold=self.model_cfg['nms']['score_threshold'],
                nms_threshold=self.model_cfg['nms']['nms_threshold']
            )
            if len(passed_nms_filter) > 0:
                passed_nms_filter = passed_nms_filter.flatten()
                boxes_np = boxes_np[passed_nms_filter]
                labels_ids_np = labels_ids_np[passed_nms_filter]
                scores_np = scores_np[passed_nms_filter]
            else:
                scores_np = []

            if ack:
                print('\n{}Meta_data(post-nms):'.format(tabs * '\t'))
                print('{}\t{}'.format(tabs * '\t', mt.to_str(passed_nms_filter, 'pick indices')))
                print('{}\t{}'.format(tabs * '\t', mt.to_str(labels_ids_np, 'labels_ids_np')))
                print('{}\t{}'.format(tabs * '\t', mt.to_str(scores_np, 'scores')))
                print('{}\t{}'.format(tabs * '\t', mt.to_str(boxes_np, 'boxes')))
                print('{}Detections:'.format(tabs * '\t'))
            if len(scores_np) <= 0:
                if ack:
                    print('{}\tNo detections passed nms filter'.format(tabs * '\t'))
                return []

        detections = []
        for i, (bbox, label_id, confidence) in enumerate(zip(boxes_np, labels_ids_np, scores_np)):
            if self.model_cfg['threshold'] <= confidence <= 1.0 and label_id is not math.isnan(label_id):
                label = self.labels[int(label_id)]
                if label in self.allowed_classes:
                    x0 = max(int(bbox[1] * img_w), 0)  # dont exceed 0
                    y0 = max(int(bbox[0] * img_h), 0)  # dont exceed 0
                    x1 = min(int(bbox[3] * img_w), img_w)  # dont exceed frame width
                    y1 = min(int(bbox[2] * img_h), img_h)  # dont exceed frame height
                    score_percentage = round(confidence * 100, fp)

                    detection_d = {
                        'label': label,
                        'score_percentage': score_percentage,
                        'bbox': {
                            #  pt1 = (x0, y0)  # obj frame top left corner
                            #  pt2 = (x1, y1)  # obj frame bottom right corner
                            'x0': x0,
                            'y0': y0,
                            'x1': x1,
                            'y1': y1,
                        },
                    }
                    detections.append(detection_d)
                    if ack:
                        d_msg = '{}\t{})Detected {}({}%) in top left=({}), bottom right=({})'
                        print(d_msg.format(tabs * '\t', i, label, score_percentage, (x0, y0), (x1, y1)))
        return detections

    def detect_cv_img(
            self,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            img_title: str = None
    ) -> list:
        """
        :param cv_img: open cv image
        :param fp: float precision on the score precentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts. see extract_results()
        """

        img_preprocessed = self.prepare_input(cv_img)
        self.run_network(img_preprocessed)
        detections = self.extract_results(
            cv_img=cv_img,
            fp=fp,
            ack=ack,
            tabs=tabs,
            img_title=img_title
        )
        return detections


class Cv2OdModel(OdBaseModel):
    def __init__(self,
                 save_load_dir: str,
                 model_name: str,
                 allowed_class: list = None,
                 threshold: float = None,
                 nms_threshold: float = None,
                 in_dims: tuple = None,
                 scalefactor: float = None,
                 mean: tuple = None,
                 swapRB: bool = None,
                 crop: bool = None,
                 check_type: bool = True
                 ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        :param allowed_class: ignore rest of class. list of strings
            if None - all classes allowed
        for all the following - if is None: take default value from MODELS_DNN_OBJECT_DETECTION_META_DATA['model_name']
        :param threshold: only detection above this threshold will be returned
        :param nms_threshold: non maximum suppression threshold
        :param in_dims:
        :param scalefactor:
        :param mean:
        :param swapRB:
        :param crop:
        example:
        model = od.Cv2OdModel(
            save_load_dir=m_save_dir,
            model_name=model_name,
            allowed_class=['dog', 'cat'],
            threshold=0.1,
            nms_threshold=0.3,
            in_dims=(416, 416),
            scalefactor=1 / 127.5,
            mean=(0, 0, 0),
            swapRB=True,
            crop=False,
        )
        see:
        best_model_images_test()
        best_model_video_test()
        best_model_cam_test()
        models_compare_images_test()
        models_compare_video_test()
        models_compare_cam_test()
        """
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, allowed_class=allowed_class)
        if check_type and not self.model_type_valid(self.model_cfg['model_type'], cfg.ModelType.OdCvNormal.value):
            exit(-1)
        net = None
        if self.model_cfg['family'] == cfg.DnnFamily.Caffe.value:
            model_prototxt = "{}/{}.prototxt".format(self.local_path, self.model_name)
            model_caffe = "{}/{}.caffemodel".format(self.local_path, self.model_name)
            self._download_if_needed(local_path=model_prototxt, url_dict=self.model_cfg['prototxt'])
            self._download_if_needed(local_path=model_caffe, url_dict=self.model_cfg['caffemodel'])
            self.model_resources_sizes = [mt.file_or_folder_size(model_prototxt), mt.file_or_folder_size(model_caffe)]
            net = cv2.dnn.readNetFromCaffe(prototxt=model_prototxt, caffeModel=model_caffe)

        elif self.model_cfg['family'] == cfg.DnnFamily.Darknet.value:
            model_cfg = "{}/{}.cfg".format(self.local_path, self.model_name)
            model_weights = "{}/{}.weights".format(self.local_path, self.model_name)
            self._download_if_needed(local_path=model_cfg, url_dict=self.model_cfg['cfg'])
            self._download_if_needed(local_path=model_weights, url_dict=self.model_cfg['weights'])
            self.model_resources_sizes = [mt.file_or_folder_size(model_cfg), mt.file_or_folder_size(model_weights)]
            net = cv2.dnn.readNetFromDarknet(cfgFile=model_cfg, darknetModel=model_weights)

        elif self.model_cfg['family'] == cfg.DnnFamily.TF.value:
            model_pbtxt = "{}/{}.pbtxt".format(self.local_path, self.model_name)
            model_pb = "{}/{}.pb".format(self.local_path, self.model_name)
            self._download_if_needed(local_path=model_pbtxt, url_dict=self.model_cfg['pbtxt'])
            self._download_if_needed(local_path=model_pb, url_dict=self.model_cfg['pb'])
            self.model_resources_sizes = [mt.file_or_folder_size(model_pbtxt), mt.file_or_folder_size(model_pb)]
            net = cv2.dnn.readNetFromTensorflow(model=model_pb, config=model_pbtxt)

        if net is None:
            mt.exception_error('Failed to create network', real_exception=False)
            exit(-1)

        self.model = cv2.dnn_DetectionModel(net)

        if threshold is not None:
            self.model_cfg['threshold'] = threshold
        if nms_threshold is not None:
            self.model_cfg['nms_threshold'] = nms_threshold
        if in_dims is not None:
            self.model_cfg['in_dims'] = in_dims
        if scalefactor is not None:
            self.model_cfg['scalefactor'] = scalefactor
        if mean is not None:
            self.model_cfg['mean'] = mean
        if swapRB is not None:
            self.model_cfg['swapRB'] = swapRB
        if crop is not None:
            self.model_cfg['crop'] = crop

        # self.model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        self.model.setInputParams(
            scale=self.model_cfg['scalefactor'],
            size=self.model_cfg['in_dims'],
            mean=self.model_cfg['mean'],
            swapRB=self.model_cfg['swapRB'],
            crop=self.model_cfg['crop']
        )

        # TODO test GPU with cuda 11 installed
        # count = cv2.cuda.getCudaEnabledDeviceCount()
        # print(count)
        # self.network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        return

    def to_string(self, tabs: int = 1) -> str:
        tabs_s = tabs * '\t'
        string = '{}{}'.format(tabs_s, mt.add_color(string='Cv2OdModel:', ops='underlined'))
        string += '\n\t{}name= {} (resources size: {})'.format(tabs_s, self.model_name, self.model_resources_sizes)
        string += '\n\t{}local_path={}'.format(tabs_s, self.local_path)
        string += '\n\t{}{}'.format(tabs_s, mt.to_str(self.allowed_classes, 'allowed_class'))
        string += '\n{}'.format(mt.dict_as_table(self.model_cfg, title='conf', fp=6, ack=False, tabs=tabs + 1))
        return string

    def detect_cv_img(
            self,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            img_title: str = None
    ) -> list:
        """
        :param cv_img: open cv image
        :param fp: float precision on the score precentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts. see extract_results()
        """
        classes, scores, boxes = self.model.detect(cv_img, self.model_cfg['threshold'], self.model_cfg['nms_threshold'])
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(classes, 'classes')))
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(scores, 'scores')))
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(boxes, 'boxes')))
        if len(classes) > 0 and len(scores) > 0:
            classes = classes.flatten()
            scores = scores.flatten()

        detections = self.extract_results(
            classes=classes,
            scores=scores,
            boxes=boxes,
            cv_img=cv_img,
            fp=fp,
            ack=ack,
            tabs=tabs,
            img_title=img_title
        )

        return detections

    def extract_results(
            self,
            classes: np.array,
            scores: np.array,
            boxes: np.array,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            img_title: str = None
    ) -> list:
        """
        :param classes: result of classes, scores, boxes = self.model.detect(cv_img, self.threshold, self.nms_threshold)
        :param scores: result of classes, scores, boxes = self.model.detect(cv_img, self.threshold, self.nms_threshold)
        :param boxes: result of classes, scores, boxes = self.model.detect(cv_img, self.threshold, self.nms_threshold)
        :param cv_img: cv image
        :param fp: float precision on the score precentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts:
        dict is a detection of an object above threshold.
            has items:
                label:str e.g. 'person'
                score_percentage: float e.g. 12.31
                bbox: dict with keys x0,y0,x1,y1
                #  pt1 = (x0, y0)  # obj frame top left corner
                #  pt2 = (x1, y1)  # obj frame bottom right corner
        """

        if ack:
            title_suffix = '' if img_title is None else '{} '.format(img_title)
            title = '{} detections({}) on image {}{}:'.format(self.model_name, len(classes), title_suffix, cv_img.shape)

            print('{}{}'.format(tabs * '\t', title))
            print('{}Meta_data:'.format(tabs * '\t'))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(classes, 'classes')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(scores, 'scores')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(boxes, 'boxes')))
            print('{}Detections:'.format(tabs * '\t'))

        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        detections = []
        for i, (class_id, score_frac, bbox) in enumerate(zip(classes, scores, boxes)):
            label = self.labels[class_id]
            if label in self.allowed_classes:
                score_percentage = round(score_frac * 100, fp)

                (x0, y0) = (bbox[0], bbox[1])
                (w, h) = (bbox[2], bbox[3])

                x1 = min(x0 + w, img_w)  # dont exceed frame width
                y1 = min(y0 + h, img_h)  # dont exceed frame height

                if 'need_normalize' in self.model_cfg:
                    in_dims_w, in_dims_h = self.model_cfg['in_dims']
                    x0 = int(x0 * (img_w / in_dims_w))
                    x1 = int(x1 * (img_w / in_dims_w))
                    y0 = int(y0 * (img_h / in_dims_h))
                    y1 = int(y1 * (img_h / in_dims_h))

                detection_d = {
                    'label': label,
                    'score_percentage': score_percentage,
                    'bbox': {
                        #  pt1 = (x0, y0)  # obj frame top left corner
                        #  pt2 = (x1, y1)  # obj frame bottom right corner
                        'x0': int(x0),
                        'y0': int(y0),
                        'x1': int(x1),
                        'y1': int(y1),
                    },
                }

                detections.append(detection_d)
                if ack:
                    d_msg = '{}\t{})Detected {}({}%) in top left=({}), bottom right=({})'
                    print(d_msg.format(tabs * '\t', i, label, score_percentage, (x0, y0), (x1, y1)))

        return detections
