import numpy as np
import abc
from tflite_runtime.interpreter import Interpreter
# noinspection PyPackageRequirements
import cv2
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.models import BaseModel
from wizzi_utils.models import models_configs as cfg


def get_pose_detection_models(ack: bool = False, tabs: int = 1) -> list:
    model_names = []
    count = 0
    for i, (m_name, m_dict) in enumerate(cfg.MODELS_CONFIG.items()):
        if m_dict['job'] == cfg.Jobs.POSE_DETECTION.value:
            if ack:
                count += 1
                mt.dict_as_table(table=m_dict, title='{}){}'.format(count, m_name), tabs=tabs)
            model_names.append(m_name)
    return model_names


class PdBaseModel(BaseModel):
    DEFAULT_COLOR_DICT = {
        'joint_c': 'red',  # joint color
        'edge_c': 'lightgreen',  # line color
        'text_c': 'white',  # label index color
    }
    NOT_FOUND_VALUE = -1
    NOT_FOUND_PAIR = [NOT_FOUND_VALUE, NOT_FOUND_VALUE]

    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            allowed_joint_names: list = None,
    ):
        super().__init__(save_load_dir=save_load_dir, model_name=model_name)
        if not self.model_name_valid(model_name):
            exit(-1)
        self.model_cfg = cfg.MODELS_CONFIG[model_name]
        self.joint_names = self.model_cfg['joint_names']
        self.pairs_indices = self.model_cfg['pairs_indices']
        self.allowed_joint_names = list(
            self.joint_names.values()) if allowed_joint_names is None else allowed_joint_names
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
            colors_d: dict,
            draw_labels: bool,
    ) -> None:
        """
        :param detections: output of self.classify_cv_img()
        :param colors_d: colors in str form:
            bbox color
            label_bbox color
            text color
            e.g. colors_d={
                    'joint_c': 'red',
                    'edge_c': 'lightgreen',
                    'text_c': 'white',
                },
        :param cv_img: the same that was given input to self.classify_cv_img()
        :param draw_labels: draw part index
        :return:
        """
        if colors_d is None:
            colors_d = PdBaseModel.DEFAULT_COLOR_DICT
        edge_c = pyplt.get_BGR_color(colors_d['edge_c'])
        joint_c = pyplt.get_BGR_color(colors_d['joint_c'])
        text_c = colors_d['text_c']
        for detection in detections:  # each detection is a pose - currently supports just 1
            names = detection['joint_names_list']
            ids = detection['joint_ids_list']
            xys = detection['joint_x_y_list']
            # zs = detection['joint_z_list'] if 'joint_z_list' in detection else [self.NOT_FOUND_VALUE] * len(names)
            scores = detection['score_percentages_list']

            # DRAW LINES: lines connecting the edges
            for pair in self.pairs_indices:
                partA, partB = pair
                if xys[partA] != self.NOT_FOUND_PAIR and xys[partB] != self.NOT_FOUND_PAIR:
                    cv2.line(cv_img, pt1=tuple(xys[partA]), pt2=tuple(xys[partB]), color=edge_c, thickness=2)

            # DRAW JOINTS: circle and joint id if asked
            for name, jid, xy, score in zip(names, ids, xys, scores):
                if xy != self.NOT_FOUND_PAIR:
                    cv2.circle(cv_img, center=tuple(xy), radius=3, color=joint_c, thickness=-1)
                    if draw_labels:
                        label_xy = (xy[0] - 5, xy[1])
                        label = '{}'.format(jid)
                        cvt.add_text(cv_img, header=label, pos=label_xy, text_color=text_c, with_rect=False,
                                     bg_font_scale=2)
        return


class TflPdModel(PdBaseModel):
    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            threshold: float = None,
            allowed_joint_names: list = None
    ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        :param threshold: only detection above this threshold will be pass first filter
        :param allowed_joint_names: joint_names to track from the joint_names of the model
        example:
        see:
        """
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, allowed_joint_names=allowed_joint_names)
        if not self.model_type_valid(self.model_cfg['model_type'],
                                     [cfg.ModelType.PdTflNormal.value, cfg.ModelType.PdTflPoseNet.value]):
            exit(-1)
        if threshold is not None:
            self.model_cfg['threshold'] = threshold
        self.pairs_indices = self.model_cfg['pairs_indices']

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
        string = '{}{}'.format(tabs_s, mt.add_color(string='TflPdModel:', ops='underlined'))
        string += '\n\t{}name= {} (size {})'.format(tabs_s, self.model_name, self.model_size)
        string += '\n\t{}local_path= {}'.format(tabs_s, self.local_path)
        string += '\n\t{}{}'.format(tabs_s, mt.to_str(self.allowed_joint_names, 'allowed_classes'))
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
            center = 127.5
            img_RGB = (img_RGB / center) - 1  # normalize image
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
        :param fp: float precision on the score percentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts:
        dict is a detection of pose
            each has items:
                'joint_names_list':  - all joint names like in the config
                'joint_ids_list': - all joint ids like in the config
                'joint_x_y_list': - if joint found: it's x,y values
                'joint_z_list': - if joint found: it's z value
                'score_percentages_list': - if joint found: it's confidence in 0-100%,
        """
        # get results
        depth = 5  # each points has x,y,z,visibility,presence
        # full pose -> 195/5=39. but i think there are only 33
        outputs = self.interpreter.get_tensor(self.output_details[0]['index'])[0]  # points numpy

        if ack:
            title_suffix = '' if img_title is None else '{} '.format(img_title)
            title = '{} detection on image {}{}:'.format(self.model_name, title_suffix, cv_img.shape)
            print('{}{}'.format(tabs * '\t', title))
            print('{}Meta_data:'.format(tabs * '\t'))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(outputs, 'outputs')))
            print('{}Detections:'.format(tabs * '\t'))

        detections = []  # each detection is a set of joint
        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        net_w, net_h = self.model_cfg['in_dims']
        for pose_id in range(1):  # currently supports 1 pose
            detection_d = {
                'joint_names_list': [],
                'joint_ids_list': [],
                'joint_x_y_list': [],
                'joint_z_list': [],
                'score_percentages_list': [],
            }
            for joint_id, joint_name in self.joint_names.items():
                detection_d['joint_names_list'].append(joint_name)
                detection_d['joint_ids_list'].append(joint_id)
                x = int(outputs[joint_id * depth + 0] * img_w / net_w)
                y = int(outputs[joint_id * depth + 1] * img_h / net_h)
                z = int(outputs[joint_id * depth + 2])

                visibility = outputs[joint_id * depth + 3]
                visibility = 1 / (1 + np.exp(visibility))  # reverse sigmoid
                presence = outputs[joint_id * depth + 4]
                presence = 1 / (1 + np.exp(presence))  # reverse sigmoid
                score_frac = 1 - max(visibility, presence)  # change from err to acc: acc = 1-err
                score_percentage = round(score_frac * 100, fp)

                if self.model_cfg['threshold'] <= score_frac <= 1.0 and joint_name in self.allowed_joint_names:
                    detection_d['joint_x_y_list'].append([x, y])
                    detection_d['joint_z_list'].append(z)
                    detection_d['score_percentages_list'].append(score_percentage)
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['joint_z_list'].append(self.NOT_FOUND_VALUE)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)

                if ack:
                    d_msg = '{}\tpose {}: {}({}): xy={}, z={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['joint_z_list'][-1], detection_d['score_percentages_list'][-1]))
            detections.append(detection_d)
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


class TflPdModelPoseNet(TflPdModel):

    @staticmethod
    def mod(a: np.array, b: int) -> np.array:
        """ find a % b """
        floored = np.floor_divide(a, b)
        return np.subtract(a, np.multiply(floored, b))

    @staticmethod
    def sigmoid(x: np.array) -> np.array:
        """ apply sigmoid activation to numpy array """
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_and_argmax2d(heatmap: np.array, threshold: float) -> np.array:
        """
        :param heatmap: 9x9x17 (17 joints)
        :param threshold:
        :return: y,x coordinates 17x2
        """
        # v1 is 9x9x17 heatmap
        # v1 = interpreter.get_tensor(output_details[0]['index'])[0]
        height, width, depth = heatmap.shape
        reshaped = np.reshape(heatmap, [height * width, depth])
        reshaped = TflPdModelPoseNet.sigmoid(reshaped)
        # apply threshold
        reshaped = (reshaped > threshold) * reshaped
        coords = np.argmax(reshaped, axis=0)
        yCoords = np.round(np.expand_dims(np.divide(coords, width), 1))
        xCoords = np.expand_dims(TflPdModelPoseNet.mod(coords, width), 1)
        ret = np.concatenate([yCoords, xCoords], 1)
        return ret

    @staticmethod
    def get_offsets(offsets: np.array, coords: np.array, num_key_points: int = 17) -> np.array:
        """
        :param offsets: 9x9x34 - probably yx heatmap per joint(17*2)
        :param coords: 17x2
        :param num_key_points: number of joints
        :return: get offset vectors from all coordinates
        """
        # offsets = interpreter.get_tensor(output_details[1]['index'])[0]
        offset_vectors = []
        for i, (heatmap_y, heatmap_x) in enumerate(coords):
            # print(i, y, x)
            heatmap_y = int(heatmap_y)
            heatmap_x = int(heatmap_x)
            # print(heatmap_y, heatmap_x)
            # make sure indices aren't out of range
            heatmap_y = min(8, heatmap_y)
            heatmap_x = min(8, heatmap_x)
            y_off = offsets[heatmap_y, heatmap_x, i]
            x_off = offsets[heatmap_y, heatmap_x, i + num_key_points]
            # ov = get_offset_point(heatmap_y, heatmap_x, offsets, i, num_key_points)
            offset_vectors.append([y_off, x_off])
        offset_vectors = np.array(offset_vectors)
        return offset_vectors

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
        :param fp: float precision on the score percentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts:
        dict is a detection of pose
            each has items:
                'joint_names_list':  - all joint names like in the config
                'joint_ids_list': - all joint ids like in the config
                'joint_x_y_list': - if joint found: it's x,y values
                'joint_z_list': - if joint found: it's z value
                'score_percentages_list': - if joint found: it's confidence in 0-100%,
        """
        outputs = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        offsets = self.interpreter.get_tensor(self.output_details[1]['index'])[0]

        if ack:
            title_suffix = '' if img_title is None else '{} '.format(img_title)
            title = '{} detection on image {}{}:'.format(self.model_name, title_suffix, cv_img.shape)
            print('{}{}'.format(tabs * '\t', title))
            print('{}Meta_data:'.format(tabs * '\t'))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(outputs, 'outputs')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(offsets, 'offsets')))
            print('{}Detections:'.format(tabs * '\t'))

        # get y,x positions from heat map
        yx = TflPdModelPoseNet.sigmoid_and_argmax2d(outputs, threshold=self.model_cfg['threshold'])
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(yx, 'yx')))

        # points below threshold (value is [0, 0])
        drop_pts = list(np.unique(np.where(yx == 0)[0]))
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(drop_pts, 'drop_pts')))

        # get offsets from positions
        offset_vectors = TflPdModelPoseNet.get_offsets(offsets, yx)
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(offset_vectors, 'offset_vectors')))

        # use stride to get coordinates in image coordinates
        output_stride = 32
        yx_values = yx * output_stride + offset_vectors
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(yx_values, 'yx_values')))

        for bad_joint_ind in drop_pts:
            yx_values[bad_joint_ind] = self.NOT_FOUND_PAIR
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(yx_values, 'yx_values')))

        detections = []  # each detection is a set of joint
        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        net_w, net_h = self.model_cfg['in_dims']
        for pose_id in range(1):  # currently supports 1 pose
            detection_d = {
                'joint_names_list': [],
                'joint_ids_list': [],
                'joint_x_y_list': [],
                'score_percentages_list': [],
            }
            for joint_id, joint_name in self.joint_names.items():
                detection_d['joint_names_list'].append(joint_name)
                detection_d['joint_ids_list'].append(joint_id)

                if yx_values[joint_id].tolist() == self.NOT_FOUND_PAIR:
                    score_frac = 0
                    x, y, score_percentage = None, None, None
                else:
                    y = int(yx_values[joint_id][0] * img_h / net_h)
                    x = int(yx_values[joint_id][1] * img_w / net_w)
                    score_frac = 0.99  # for now till i will extract the confidence from the detection
                    # score_percentage = round(score_frac * 100, fp)
                    score_percentage = 'TODO ???'

                if self.model_cfg['threshold'] <= score_frac <= 1.0 and joint_name in self.allowed_joint_names:
                    detection_d['joint_x_y_list'].append([x, y])
                    detection_d['score_percentages_list'].append(score_percentage)
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)

                if ack:
                    d_msg = '{}\tpose {}: {}({}): xy={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['score_percentages_list'][-1]))
            detections.append(detection_d)
        return detections


class Cv2PdModel(PdBaseModel):
    BAD_P = (-1, -1)

    def __init__(self,
                 save_load_dir: str,
                 model_name: str,
                 allowed_joint_names: list = None,
                 threshold: float = None,
                 in_dims: tuple = None,
                 scalefactor: float = None,
                 mean: tuple = None,
                 swapRB: bool = None,
                 crop: bool = None,
                 ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        for all the following - if is None: take default value from MODELS_DNN_OBJECT_DETECTION_META_DATA['model_name']
        :param threshold: only detection above this threshold will be returned
        :param in_dims:
        :param scalefactor:
        :param mean:
        :param swapRB:
        :param crop:
        example:
        see:
        """
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, allowed_joint_names=allowed_joint_names)
        if not self.model_type_valid(self.model_cfg['model_type'], [cfg.ModelType.PdCvNormal.value]):
            exit(-1)
        self.pose_net = None
        if self.model_cfg['family'] == cfg.DnnFamily.Caffe.value:
            model_prototxt = "{}/{}.prototxt".format(self.local_path, self.model_name)
            model_caffe = "{}/{}.caffemodel".format(self.local_path, self.model_name)
            self._download_if_needed(local_path=model_prototxt, url_dict=self.model_cfg['prototxt'])
            self._download_if_needed(local_path=model_caffe, url_dict=self.model_cfg['caffemodel'])
            self.model_resources_sizes = [mt.file_or_folder_size(model_prototxt), mt.file_or_folder_size(model_caffe)]
            self.pose_net = cv2.dnn.readNetFromCaffe(prototxt=model_prototxt, caffeModel=model_caffe)

        elif self.model_cfg['family'] == cfg.DnnFamily.Darknet.value:
            model_cfg = "{}/{}.cfg".format(self.local_path, self.model_name)
            model_weights = "{}/{}.weights".format(self.local_path, self.model_name)
            self._download_if_needed(local_path=model_cfg, url_dict=self.model_cfg['cfg'])
            self._download_if_needed(local_path=model_weights, url_dict=self.model_cfg['weights'])
            self.model_resources_sizes = [mt.file_or_folder_size(model_cfg), mt.file_or_folder_size(model_weights)]
            self.pose_net = cv2.dnn.readNetFromDarknet(cfgFile=model_cfg, darknetModel=model_weights)

        elif self.model_cfg['family'] == cfg.DnnFamily.TF.value:
            model_pbtxt = "{}/{}.pbtxt".format(self.local_path, self.model_name)
            model_pb = "{}/{}.pb".format(self.local_path, self.model_name)
            self._download_if_needed(local_path=model_pbtxt, url_dict=self.model_cfg['pbtxt'])
            self._download_if_needed(local_path=model_pb, url_dict=self.model_cfg['pb'])
            self.model_resources_sizes = [mt.file_or_folder_size(model_pbtxt), mt.file_or_folder_size(model_pb)]
            self.pose_net = cv2.dnn.readNetFromTensorflow(model=model_pb, config=model_pbtxt)

        if self.pose_net is None:
            mt.exception_error('Failed to create network', real_exception=False)
            exit(-1)

        self.pairs_indices = self.model_cfg['pairs_indices']

        if threshold is not None:
            self.model_cfg['threshold'] = threshold
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

        return

    def to_string(self, tabs: int = 1) -> str:
        tabs_s = tabs * '\t'
        string = '{}{}'.format(tabs_s, mt.add_color(string='Cv2PdModel:', ops='underlined'))
        string += '\n\t{}name= {} (resources size: {})'.format(tabs_s, self.model_name, self.model_resources_sizes)
        string += '\n\t{}local_path={}'.format(tabs_s, self.local_path)
        string += '\n\t{}{}'.format(tabs_s, mt.to_str(self.allowed_joint_names, 'allowed_joint_names'))
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
        inpBlob = cv2.dnn.blobFromImage(
            image=cv_img,
            scalefactor=self.model_cfg['scalefactor'],
            size=self.model_cfg['in_dims'],
            mean=self.model_cfg['mean'],
            swapRB=self.model_cfg['swapRB'],
            crop=self.model_cfg['crop'])
        self.pose_net.setInput(inpBlob)
        outputs = self.pose_net.forward()
        # print('{}\t{}'.format(tabs * '\t', mt.to_str(outputs, 'outputs')))

        if len(outputs) > 0:
            outputs = outputs[0]

        detections = self.extract_results(
            outputs=outputs,
            cv_img=cv_img,
            fp=fp,
            ack=ack,
            tabs=tabs,
            img_title=img_title
        )
        return detections

    def extract_results(
            self,
            outputs: np.array,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            img_title: str = None
    ) -> list:
        """
        :param outputs: np array that contains the outputs for the cv_img
        :param cv_img: cv image
        :param fp: float precision on the score precentage. e.g. fp=2: 0.1231231352353 -> 12.31%
        :param ack: if True: print meta data and detections
        :param tabs: if ack True: tabs for print
        :param img_title: if ack True: title for print
        :return: list of dicts:
        dict is a detection of pose
            each has items:
                'joint_names_list':  - all joint names like in the config
                'joint_ids_list': - all joint ids like in the config
                'joint_x_y_list': - if joint found: it's x,y values
                'joint_z_list': - if joint found: it's z value
                'score_percentages_list': - if joint found: it's confidence in 0-100%,
        """

        if ack:
            title_suffix = '' if img_title is None else '{} '.format(img_title)
            title = '{} detection on image {}{}:'.format(self.model_name, title_suffix, cv_img.shape)
            print('{}{}'.format(tabs * '\t', title))
            print('{}Meta_data:'.format(tabs * '\t'))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(outputs, 'outputs')))
            print('{}Detections:'.format(tabs * '\t'))

        detections = []  # each detection is a set of joint
        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        net_h, net_w = outputs.shape[1], outputs.shape[2]

        for pose_id in range(1):  # currently supports 1 pose
            detection_d = {
                'joint_names_list': [],
                'joint_ids_list': [],
                'joint_x_y_list': [],
                'score_percentages_list': [],
            }

            for joint_id, joint_name in self.joint_names.items():
                detection_d['joint_names_list'].append(joint_name)
                detection_d['joint_ids_list'].append(joint_id)
                probMap = outputs[joint_id, :, :]  # confidence map.
                minVal, score_frac, minLoc, point = cv2.minMaxLoc(probMap)  # Find global maxima of the probMap.
                # Scale the point to fit on the original image
                x = int((img_w * point[0]) / net_w)
                y = int((img_h * point[1]) / net_h)
                score_percentage = round(score_frac * 100, fp)

                if self.model_cfg['threshold'] <= score_frac <= 1.0 and joint_name in self.allowed_joint_names:
                    detection_d['joint_x_y_list'].append([x, y])
                    detection_d['score_percentages_list'].append(score_percentage)
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)

                if ack:
                    d_msg = '{}\tpose {}: {}({}): xy={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['score_percentages_list'][-1]))
            detections.append(detection_d)
        return detections
