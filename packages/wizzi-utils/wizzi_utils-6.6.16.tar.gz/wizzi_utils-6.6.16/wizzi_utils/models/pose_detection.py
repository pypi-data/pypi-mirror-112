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
        'bbox_c': 'blue',
        'sub_image_c': 'darkorange',
        'text_c': 'white',
    }
    NOT_FOUND_VALUE = -1
    NOT_FOUND_PAIR = [NOT_FOUND_VALUE, NOT_FOUND_VALUE]

    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            allowed_joint_names: list = None,
            min_p_valid_joints: float = 0.3,
    ):
        super().__init__(save_load_dir=save_load_dir, model_name=model_name)
        if not self.model_name_valid(model_name):
            exit(-1)
        self.model_cfg = cfg.MODELS_CONFIG[model_name]
        self.joint_names = self.model_cfg['joint_names']
        self.pairs_indices = self.model_cfg['pairs_indices']
        # grab default colors and convert to bgr
        self.pairs_indices_colors = [pyplt.get_BGR_color(c) for c in self.model_cfg['pairs_indices_colors']]
        self.joint_colors = [pyplt.get_BGR_color(c) for c in self.model_cfg['joint_colors']]
        self.allowed_joint_names = list(
            self.joint_names.values()) if allowed_joint_names is None else allowed_joint_names
        self.min_p_valid_joints = min_p_valid_joints
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
            draw_joints: bool = True,
            draw_labels: bool = False,
            draw_edges: bool = False,
            draw_bbox: bool = False,
            draw_sub_image: bool = False
    ) -> None:
        """
        :param detections: output of self.classify_cv_img()
        :param colors_d: colors in str form:
            bbox_c: bbox color
            sub_image_c: sub image color
            text_c: text color
            joints_c: str or list of size self.joint_names. if None - has default in cfg
            edge_c: str or list of size self.pairs_indices. if None - has default in cfg
            e.g. colors_d={
                    'bbox_c': 'blue'
                    'sub_image_c': 'black'
                    'text_c': 'black',
                    'joints_c': str or list of size self.joint_names. if None - has default in cfg
                    'edge_c': str or list of size self.pairs_indices. if None - has default in cfg
                },
        :param cv_img: the same that was given input to self.classify_cv_img()
        :param draw_joints: draw joints
        :param draw_labels: draw joint ids (valid if draw_joints True)
        :param draw_edges: draw edges between joints
        :param draw_bbox: draw bbox around poses
        :param draw_sub_image: draw sub image from the bbox around the poses
        :return:
        """
        if colors_d is None:
            colors_d = self.DEFAULT_COLOR_DICT

        for detection in detections:  # each detection is a pose
            names = detection['joint_names_list']
            ids = detection['joint_ids_list']
            xys = detection['joint_x_y_list']
            # zs = detection['joint_z_list'] if 'joint_z_list' in detection else [self.NOT_FOUND_VALUE] * len(names)
            scores = detection['score_percentages_list']
            pose_bbox = detection['bbox']
            bbox_sub_image_d = detection['bbox_sub_image'] if 'bbox_sub_image' in detection else None

            if draw_bbox:  # DRAW BBOX
                color_bgr = pyplt.get_BGR_color(colors_d['bbox_c'])
                pt1 = (pose_bbox['x0'], pose_bbox['y0'])
                pt2 = (pose_bbox['x1'], pose_bbox['y1'])
                cv2.rectangle(img=cv_img, pt1=pt1, pt2=pt2, color=color_bgr, thickness=2)

            if draw_sub_image and bbox_sub_image_d is not None:  # DRAW sub image
                color_bgr = pyplt.get_BGR_color(colors_d['sub_image_c'])
                pt1 = (bbox_sub_image_d['x0'], bbox_sub_image_d['y0'])
                pt2 = (bbox_sub_image_d['x1'], bbox_sub_image_d['y1'])
                cv2.rectangle(img=cv_img, pt1=pt1, pt2=pt2, color=color_bgr, thickness=1)  # sub image

            # DRAW EDGES: lines connecting the edges
            if draw_edges:
                if 'edge_c' in colors_d:
                    edges_colors = colors_d['edge_c']
                    if mt.is_str(edges_colors):  # 1 color for all
                        edges_colors = [pyplt.get_BGR_color(edges_colors)] * len(self.pairs_indices)
                    else:  # list of colors - must be in len(self.joint_names)
                        edges_colors = [pyplt.get_BGR_color(c) for c in edges_colors]
                else:  # take default colors
                    edges_colors = self.pairs_indices_colors
                for pair, bgr_c in zip(self.pairs_indices, edges_colors):
                    partA, partB = pair
                    if xys[partA] != self.NOT_FOUND_PAIR and xys[partB] != self.NOT_FOUND_PAIR:
                        cv2.line(cv_img, pt1=tuple(xys[partA]), pt2=tuple(xys[partB]), color=bgr_c, thickness=2)

            # DRAW JOINTS: circle and joint id if asked
            if draw_joints:
                text_color_str = colors_d['text_c']
                if 'joint_colors' in colors_d:
                    joints_colors = colors_d['joint_colors']
                    if mt.is_str(joints_colors):  # 1 color for all
                        joints_colors = [pyplt.get_BGR_color(joints_colors)] * len(self.joint_names)
                    else:  # list of colors - must be in len(self.joint_names)
                        joints_colors = [pyplt.get_BGR_color(c) for c in joints_colors]
                else:  # take default colors
                    joints_colors = self.joint_colors

                for name, jid, xy, score, bgr_c in zip(names, ids, xys, scores, joints_colors):
                    if xy != self.NOT_FOUND_PAIR:
                        cv2.circle(cv_img, center=tuple(xy), radius=5, color=bgr_c, thickness=-1)
                        if draw_labels:
                            label_xy = (xy[0] - 5, xy[1])
                            label = '{}'.format(jid)
                            cvt.add_text(cv_img, header=label, pos=label_xy, text_color=text_color_str, with_rect=False,
                                         bg_font_scale=2)
        return

    @staticmethod
    def get_bbox_dict(joint_x_y_list: list) -> dict:
        x0, y0, x1, y1 = np.inf, np.inf, -1, -1
        for x_y in joint_x_y_list:
            if x_y != PdBaseModel.NOT_FOUND_PAIR:
                x, y = x_y
                if x0 > x:
                    x0 = x
                elif x1 < x:
                    x1 = x
                if y0 > y:
                    y0 = y
                elif y1 < y:
                    y1 = y

        # check bbox valid:
        if 0 <= x0 < x1 and 0 <= y0 < y1:
            bbox = {
                #  pt1 = (x0, y0)  # obj frame top left corner
                #  pt2 = (x1, y1)  # obj frame bottom right corner
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
            }
        else:
            bbox = None
        return bbox

    @staticmethod
    def add_sub_sub_image_to_detection(
            detections: list,
            cv_img: np.array,
            bbox_image_p: dict,
            ack: bool = False,
            tabs: int = 1
    ) -> list:
        """
        :param detections:
        :param cv_img:
        :param bbox_image_p: dict that specify how much from the bbox to save
                bbox_image_p = {  # all bbox
                    'x_left_start': 0,
                    'x_left_end': 1,
                    'y_top_start': 0,
                    'y_top_end': 1,
                }
                bbox_image_p = {  # sub bbox
                    'x_left_start': 0.2,  x left: start from 20% of the image
                    'x_left_end': 0.9, x right: end at 90%
                    'y_top_start': 0.2, y top: start at 20%
                    'y_top_end': 0.6, y bottom: end at 60%
                }
        :param ack: print sub image dict
        :param tabs:
        :return: for each detection in detections: add entry 'bbox_sub_image' with a dict with keys image,x0,x1,y0,y1
                    if you imshow - you will get the bbox of the detection (according to bbox_image_p)
        """
        if ack:
            print('{}bbox_sub_image of {} detections:'.format(tabs * '\t', len(detections)))
        for pose_i, detection_d in enumerate(detections):
            # label = detection_d['label']
            # confidence = detection_d['score_percentage']
            bbox = detection_d['bbox']
            x0, x1 = bbox['x0'], bbox['x1']
            y0, y1 = bbox['y0'], bbox['y1']

            y_dist = y1 - y0
            x_dist = x1 - x0
            # prepare sub sub image (a part of the bbox)
            # the origin is left - top. (x0,y0) is top left. (x1,y1) is bottom right
            sub_y0 = int(y0 + bbox_image_p['y_top_start'] * y_dist)
            sub_y1 = int(y0 + bbox_image_p['y_top_end'] * y_dist)
            sub_x0 = int(x0 + bbox_image_p['x_left_start'] * x_dist)
            sub_x1 = int(x0 + bbox_image_p['x_left_end'] * x_dist)

            if 0 <= sub_x0 < sub_x1 and 0 <= sub_y0 < sub_y1:
                detection_d['bbox_sub_image'] = {
                    'image': cv_img[sub_y0:sub_y1, sub_x0:sub_x1].tolist(),
                    'x0': sub_x0,
                    'y0': sub_y0,
                    'x1': sub_x1,
                    'y1': sub_y1,
                }
                # cvt.display_open_cv_image(detection_d['bbox_sub_image']['image'])
            else:
                detection_d['bbox_sub_image'] = None

            if ack:
                string = '{}\tbbox_sub_image of pose {}:'.format(tabs * '\t', pose_i)
                bbox_sub = detection_d['bbox_sub_image']
                if bbox_sub is not None:
                    string += ' x0={} y0={} x1={} y1={} '.format(bbox_sub['x0'], bbox_sub['y0'], bbox_sub['x1'],
                                                                 bbox_sub['y1'])
                    string += '{}'.format(mt.to_str(np.array(bbox_sub['image']), title='sub_img'))
                    print(string)
                else:
                    print('{} is None'.format(string))
        return detections


class TflPdModel(PdBaseModel):
    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            threshold: float = None,
            allowed_joint_names: list = None,
            min_p_valid_joints: float = 0.3,
            check_type: bool = True
    ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        :param threshold: only detection above this threshold will be pass first filter
        :param allowed_joint_names: joint_names to track from the joint_names of the model
        :param min_p_valid_joints:
            let x=min_p_valid_joints*len(allowed_joint_names)
            to keep a pose: we need max(x,2) joints found
        :param check_type:
        example:
        see:
        """
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, allowed_joint_names=allowed_joint_names,
                         min_p_valid_joints=min_p_valid_joints)
        if check_type and not self.model_type_valid(self.model_cfg['model_type'], cfg.ModelType.PdTflNormal.value):
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
        string += '\n\t{}{}'.format(tabs_s, mt.to_str(self.allowed_joint_names, 'allowed_joint_names'))
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
                'bbox': {}
            }
            valid_joints_found = 0  # max is len(self.allowed_joint_names)
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
                    valid_joints_found += 1
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['joint_z_list'].append(self.NOT_FOUND_VALUE)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)

                if ack:
                    d_msg = '{}\tpose {}: {}({}): xy={}, z={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['joint_z_list'][-1], detection_d['score_percentages_list'][-1]))
            min_joints_found_ok = valid_joints_found >= self.min_p_valid_joints * len(self.allowed_joint_names)
            pose_valid = min_joints_found_ok and valid_joints_found >= 2
            if pose_valid:  # minimum 2 regardless to self.min_p_valid_joints(which could be zero)
                detection_d['bbox'] = PdBaseModel.get_bbox_dict(detection_d['joint_x_y_list'])
                if detection_d['bbox'] is not None:
                    if ack:
                        print('{}\tbbox:{}'.format(tabs * '\t', detection_d['bbox']))
                    detections.append(detection_d)
                else:
                    if ack:
                        print('{}\tPose {} was dumped. bbox is None'.format(tabs * '\t', pose_id))
            else:
                if ack:
                    min_needed = max(self.min_p_valid_joints * len(self.allowed_joint_names), 2)
                    msg = '{}\tPose {} was dumped. It had valid_joints_found={} (min needed {})'
                    print(msg.format(tabs * '\t', pose_id, valid_joints_found, min_needed))
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
    def __init__(
            self,
            save_load_dir: str,
            model_name: str,
            threshold: float = None,
            allowed_joint_names: list = None,
            min_p_valid_joints: float = 0.3,
            check_type: bool = True
    ):
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, threshold=threshold,
                         allowed_joint_names=allowed_joint_names, min_p_valid_joints=min_p_valid_joints,
                         check_type=False)
        if check_type and not self.model_type_valid(self.model_cfg['model_type'], cfg.ModelType.PdTflPoseNet.value):
            exit(-1)
        return

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
                'bbox': {}
            }
            valid_joints_found = 0  # max is len(self.allowed_joint_names)
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
                    valid_joints_found += 1
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)

                if ack:
                    d_msg = '{}\tpose {}: {}({}): xy={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['score_percentages_list'][-1]))
            min_joints_found_ok = valid_joints_found >= self.min_p_valid_joints * len(self.allowed_joint_names)
            pose_valid = min_joints_found_ok and valid_joints_found >= 2
            if pose_valid:  # minimum 2 regardless to self.min_p_valid_joints(which could be zero)
                detection_d['bbox'] = PdBaseModel.get_bbox_dict(detection_d['joint_x_y_list'])
                if detection_d['bbox'] is not None:
                    if ack:
                        print('{}\tbbox:{}'.format(tabs * '\t', detection_d['bbox']))
                    detections.append(detection_d)
                else:
                    if ack:
                        print('{}\tPose {} was dumped. bbox is None'.format(tabs * '\t', pose_id))
            else:
                if ack:
                    min_needed = max(self.min_p_valid_joints * len(self.allowed_joint_names), 2)
                    msg = '{}\tPose {} was dumped. It had valid_joints_found={} (min needed {})'
                    print(msg.format(tabs * '\t', pose_id, valid_joints_found, min_needed))
        return detections


class Cv2PdModel(PdBaseModel):

    def __init__(self,
                 save_load_dir: str,
                 model_name: str,
                 allowed_joint_names: list = None,
                 min_p_valid_joints: float = 0.3,
                 threshold: float = None,
                 in_dims: tuple = None,
                 scalefactor: float = None,
                 mean: tuple = None,
                 swapRB: bool = None,
                 crop: bool = None,
                 check_type: bool = True,
                 device: str = 'cpu'
                 ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        :param allowed_joint_names: joint_names to track from the joint_names of the model
        :param min_p_valid_joints:
            let x=min_p_valid_joints*len(allowed_joint_names)
            to keep a pose: we need max(x,2) joints found
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
        super().__init__(save_load_dir=save_load_dir, model_name=model_name, allowed_joint_names=allowed_joint_names,
                         min_p_valid_joints=min_p_valid_joints)
        if check_type and not self.model_type_valid(self.model_cfg['model_type'], cfg.ModelType.PdCvNormal.value):
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

        # TODO Future
        if device == "cpu" or True:
            self.pose_net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
        elif device == "gpu":
            self.pose_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.pose_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

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
        # TODO check if it increase precision (set aspect ratio)
        # frameWidth = cv_img.shape[1]
        # frameHeight = cv_img.shape[0]
        # inHeight = 368
        # inWidth = int((inHeight / frameHeight) * frameWidth)
        # in_dims = (inWidth, inHeight)
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
                'bbox': {}
            }
            valid_joints_found = 0  # max is len(self.allowed_joint_names)
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
                    valid_joints_found += 1
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)

                if ack:
                    d_msg = '{}\tpose {}: {}({}): xy={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['score_percentages_list'][-1]))
            min_joints_found_ok = valid_joints_found >= self.min_p_valid_joints * len(self.allowed_joint_names)
            pose_valid = min_joints_found_ok and valid_joints_found >= 2
            if pose_valid:  # minimum 2 regardless to self.min_p_valid_joints(which could be zero)
                detection_d['bbox'] = PdBaseModel.get_bbox_dict(detection_d['joint_x_y_list'])
                if detection_d['bbox'] is not None:
                    if ack:
                        print('{}\tbbox:{}'.format(tabs * '\t', detection_d['bbox']))
                    detections.append(detection_d)
                else:
                    if ack:
                        print('{}\tPose {} was dumped. bbox is None'.format(tabs * '\t', pose_id))
            else:
                if ack:
                    min_needed = max(self.min_p_valid_joints * len(self.allowed_joint_names), 2)
                    msg = '{}\tPose {} was dumped. It had valid_joints_found={} (min needed {})'
                    print(msg.format(tabs * '\t', pose_id, valid_joints_found, min_needed))
        return detections


class Cv2PdModelCocoMultiPoses(Cv2PdModel):
    def __init__(self,
                 save_load_dir: str,
                 model_name: str,
                 allowed_joint_names: list = None,
                 min_p_valid_joints: float = 0.3,
                 threshold: float = None,
                 in_dims: tuple = None,
                 scalefactor: float = None,
                 mean: tuple = None,
                 swapRB: bool = None,
                 crop: bool = None,
                 check_type: bool = True,
                 device: str = 'cpu'
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
        # inWidth = int((inHeight / frameHeight) * frameWidth)
        super().__init__(
            save_load_dir=save_load_dir, model_name=model_name, allowed_joint_names=allowed_joint_names,
            min_p_valid_joints=min_p_valid_joints, threshold=threshold, in_dims=in_dims, scalefactor=scalefactor,
            mean=mean, swapRB=swapRB, crop=crop, check_type=False, device=device
        )
        if check_type and not self.model_type_valid(self.model_cfg['model_type'], cfg.ModelType.PdCvCocoMulti.value):
            exit(-1)

        self.pose_pairs_indices = self.pairs_indices
        self.pafs_pairs_indices = self.model_cfg['pafs_indices']
        return

    @staticmethod
    def extract_joint_locations(probMap: np.array, threshold: float, seq_id_start: int) -> (dict, int):
        """
        :param probMap: joint probMap of a joint in size (cv_img_width, cv_img_height)
        :param threshold:
        :param seq_id_start: used to give an id for each detection.
        :return: list of dicts: per joint detection in every pose - see self.joint_names
        """
        mapSmooth = cv2.GaussianBlur(src=probMap, ksize=(3, 3), sigmaX=0, dst=0)
        mapMask = np.uint8(mapSmooth > threshold)
        joint_data = {}

        # find the blobs
        contours, hierarchy = cv2.findContours(
            image=mapMask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE
        )[-2:]

        # for each blob find the maxima
        for i, cnt in enumerate(contours):
            blobMask = np.zeros(mapMask.shape)
            blobMask = cv2.fillConvexPoly(img=blobMask, points=cnt, color=1)
            maskedProbMap = mapSmooth * blobMask
            _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
            confidence = probMap[maxLoc[1], maxLoc[0]]  # float
            joint_data[seq_id_start + i] = {
                'xy': list(maxLoc),  # maxLoc is a xy - 2d list
                'score_frac': confidence
            }
        seq_id_end = seq_id_start + len(joint_data)
        return joint_data, seq_id_end

    def get_all_joints(self, outputs: np.array, cv_img: np.array, threshold: float) -> dict:
        """
        :param outputs: detection output
        :param cv_img: original image
        :param threshold: threshold
        :return:
        * seq_id is just a sequential running id to each joint found.
            e.g. we have 2 noses, 2 necks ...
                so nose 1 seq_id = 0
                so nose 2 seq_id = 1
                so neck 1 seq_id = 2
                and so on

        dict of joint_id to joint_datum_dict
            joint_datum_dict is a dict of seq_id to joint_data_dict
                joint_data_dict has 'xy' and 'score_frac'
        """
        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        all_joints_datum = {}
        seq_id = 0
        for joint_id, joint_name in self.joint_names.items():
            probMap = outputs[joint_id, :, :]  # probability map for this joint - multi detections
            probMap = cv2.resize(probMap, (img_w, img_h))
            # print(mt.to_str(probMap, '\t\tprobMap'))
            # cvt.display_open_cv_image(probMap, ms=0, title='probMap')  # you can actual image show this map
            joint_datum_dict, seq_id = Cv2PdModelCocoMultiPoses.extract_joint_locations(probMap, threshold, seq_id)
            all_joints_datum[joint_id] = joint_datum_dict

        # uncomment to see output
        # detected all joints but don't know which belongs to which person
        # print(mt.to_str(all_joints_datum, '\tall_joints_datum'))
        # for joint_id, joint_datum_dict in all_joints_datum.items():
        #     print('{}({})'.format(self.joint_names[joint_id], joint_id))
        #     for seq_id, joint_data_dict in joint_datum_dict.items():
        #         print('\tseq_id {}: {}'.format(seq_id, joint_data_dict))

        # uncomment to draw all joints
        # for joint_id, joint_datum_dict in all_joints_datum.items():  # all_joints_datum is a list of lists
        #     for seq_id, joint_data_dict in joint_datum_dict.items():
        #         cv2.circle(cv_img, joint_data_dict['xy'], 2, pyplt.get_BGR_color('blue'), -1, cv2.LINE_AA)
        # cvt.display_open_cv_image(cv_img, ms=1, title='cv_img - all joints')
        return all_joints_datum

    def join_joints_of_same_pose(self, output: np.array, all_joints_datum: dict, cv_img: np.array) -> dict:
        """
        :param output:
        :param all_joints_datum: see extract_joint_locations() output
            e.g. for joint_id == 0 (the nose), we have a list of noses found on image
        :param cv_img:
        :return:
            Find valid connections between the different joints of a all persons present:
            for pose_pair_indices in self.pose_pairs_indices: (key="pose_pair_indices[0]_pose_pair_indices[1]")
                valid_pairs_dict[key] = valid_pair_list
            e.g. go over each pose pair indices (the first is [1,0]: neck-nose):
                take the list of noses detected and the list of necks from all_joints_datum[0] and [1]
                now figure who is most likely to be connected to who
        """
        img_h, img_w = cv_img.shape[0], cv_img.shape[1]
        valid_pairs_dict = {}
        n_interp_samples = 10
        paf_score_th = 0.1
        conf_th = 0.7
        # loop for every POSE_PAIR and see which seq_idA is connected to seq_idB
        for k, (pose_pair_indices, pafs_pair_indices) in enumerate(
                zip(self.pose_pairs_indices, self.pafs_pairs_indices)):
            joint_id_1, joint_id_2 = pose_pair_indices
            # Find the key points for the first and second limb
            candidatesA = all_joints_datum[joint_id_1]
            candidatesB = all_joints_datum[joint_id_2]
            key = '{}_{}'.format(joint_id_1, joint_id_2)
            paf_idx_1, paf_idx_2 = pafs_pair_indices

            # A->B constitute a limb
            pafA = output[paf_idx_1]
            pafB = output[paf_idx_2]
            pafA = cv2.resize(pafA, (img_w, img_h))
            pafB = cv2.resize(pafB, (img_w, img_h))

            # If key points for the joint-pair is detected
            # check every joint in candidatesA with every joint in candidatesB
            # Calculate the distance vector between the two joints
            # Find the PAF values at a set of interpolated points between the joints
            # Use the above formula to compute a score to mark the connection valid

            if len(candidatesA) != 0 and len(candidatesB) != 0:
                valid_pairs = []
                for seq_idA, candidateA in candidatesA.items():
                    xy_i = np.array(candidateA['xy'])
                    best_seq_idB = -1
                    maxScore = -1
                    for seq_idB, candidateB in candidatesB.items():
                        xy_j = np.array(candidateB['xy'])
                        d_ij = xy_j - xy_i  # Find d_ij
                        norm = np.linalg.norm(d_ij)
                        if norm:
                            d_ij = d_ij / norm
                            interp_coord = list(zip(  # Find p(u)
                                np.linspace(xy_i[0], xy_j[0], num=n_interp_samples),
                                np.linspace(xy_i[1], xy_j[1], num=n_interp_samples)
                            ))

                            paf_interp = []
                            for xy in interp_coord:  # Find L(p(u))
                                xy_r = np.round(xy).astype(np.int)
                                paf_interp.append([pafA[xy_r[1], xy_r[0]], pafB[xy_r[1], xy_r[0]]])

                            paf_scores = np.dot(paf_interp, d_ij)  # Find E
                            avg_paf_score = sum(paf_scores) / len(paf_scores)

                            # Check if the connection is valid
                            # If the fraction of interpolated vectors aligned with PAF
                            # is higher then threshold -> Valid Pair
                            if (len(np.where(paf_scores > paf_score_th)[0]) / n_interp_samples) > conf_th:
                                if avg_paf_score > maxScore:
                                    maxScore = avg_paf_score
                                    best_seq_idB = seq_idB
                    # Append the connection to the list
                    if best_seq_idB != -1:
                        valid_pairs.append([seq_idA, best_seq_idB])

                # Append the detected connections to the global list
                valid_pairs_dict[key] = valid_pairs
            else:  # If no valid pairs are detected - save joints_pair_index
                # mt.exception_error('No Connection : k = {}'.format(k), real_exception=False)
                valid_pairs_dict[key] = []
        # uncomment for output
        # print(mt.to_str(valid_pairs_dict, '\tvalid_pairs_dict', chars='all'))
        # for pose_pair_indices, valid_pairs in valid_pairs_dict.items():
        #     p1, p2 = pose_pair_indices.split('_')
        #     p1, p2 = int(p1), int(p2)
        #     print('\t\tconnection of {}({}) to {}({})'.format(self.joint_names[p1], p1, self.joint_names[p2], p2))
        #     print('\t\t\tseq_ids list {}'.format(valid_pairs))
        return valid_pairs_dict

    def separate_poses(self, valid_pairs_dict: dict):
        """
        :param valid_pairs_dict:
        :return:
        using the valid_pairs_dict - separate poses
        e.g we have 2 poses (not mandatory all joints found on both poses)
        first pose_pairs_indices is 1,2 which is neck to RShoulder
        so an example to a valid pair in valid_pairs_dict['1_2']:
            connection of Neck(1) to RShoulder(2)
                seq_ids list [[1, 3], [2, 4]]
            all_joints_datum[joint_id='1'][seq_id='1'] is the 1st Neck
            all_joints_datum[joint_id='1'][seq_id='2'] is the 2nd Neck
            all_joints_datum[joint_id='2'][seq_id='3'] is the 1st RShoulder
            all_joints_datum[joint_id='2'][seq_id='4'] is the 2nd RShoulder

        """
        poses = []

        for pose_pair in self.pose_pairs_indices:
            poseAid, poseBid = pose_pair
            key = '{}_{}'.format(poseAid, poseBid)
            valid_pairs = valid_pairs_dict[key]  # x seq_ids of connected joints for this pose_pair (e.g. neck to nose)

            if len(valid_pairs) > 0:
                valid_pairs = np.array(valid_pairs)
                seq_ids1 = valid_pairs[:, 0]  # take first joint seq_ids
                seq_ids2 = valid_pairs[:, 1]  # take second joint seq_ids

                for seq_id1, seq_id2 in zip(seq_ids1, seq_ids2):
                    person_idx = -1
                    for j, pose in enumerate(poses):
                        if pose[poseAid] == seq_id1:
                            person_idx = j
                            break
                    if person_idx != -1:
                        poses[person_idx][poseBid] = seq_id2

                    # new person found
                    elif person_idx == -1:
                        row = -1 * np.ones(len(self.joint_names))
                        row[poseAid] = seq_id1
                        row[poseBid] = seq_id2
                        poses.append(row)
        poses = np.array(poses, dtype=np.int)
        return poses

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

        all_joints_datum = self.get_all_joints(outputs, cv_img, self.model_cfg['threshold'])
        valid_pairs_dict = self.join_joints_of_same_pose(outputs, all_joints_datum, cv_img)
        poses = self.separate_poses(valid_pairs_dict)
        if ack:
            print('{}\t{}'.format(tabs * '\t', mt.to_str(all_joints_datum, 'all_joints_datum', chars=300)))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(valid_pairs_dict, 'valid_pairs_dict')))
            print('{}\t{}'.format(tabs * '\t', mt.to_str(poses, 'poses')))
            print('{}Detections:'.format(tabs * '\t'))

        # cvt.display_open_cv_image(cv_img, ms=1, title='cv_img - all joints')

        detections = []  # each detection is a set of joints
        for pose_id, pose in enumerate(poses):
            if ack:
                print('{}\t{}'.format(tabs * '\t', mt.to_str(pose, 'pose {}'.format(pose_id))))
            detection_d = {
                'joint_names_list': [],
                'joint_ids_list': [],
                'joint_x_y_list': [],
                'score_percentages_list': [],
                'bbox': {}
            }
            valid_joints_found = 0  # max is len(self.allowed_joint_names)
            for joint_id, joint_name in self.joint_names.items():
                detection_d['joint_names_list'].append(joint_name)
                detection_d['joint_ids_list'].append(joint_id)
                seq_id = pose[joint_id]

                if seq_id != self.NOT_FOUND_VALUE:
                    joint_d = all_joints_datum[joint_id][seq_id]
                    x, y = joint_d['xy']
                    score_frac = joint_d['score_frac']

                    if self.model_cfg['threshold'] <= score_frac <= 1.0 and joint_name in self.allowed_joint_names:
                        score_percentage = round(score_frac * 100, fp)
                        detection_d['joint_x_y_list'].append([x, y])
                        detection_d['score_percentages_list'].append(score_percentage)
                        valid_joints_found += 1
                    else:
                        detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                        detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)
                else:
                    detection_d['joint_x_y_list'].append(self.NOT_FOUND_PAIR)
                    detection_d['score_percentages_list'].append(self.NOT_FOUND_VALUE)
                if ack:
                    d_msg = '{}\t\tpose {}: {}({}): xy={}, score=({}%)'
                    print(d_msg.format(tabs * '\t', pose_id, joint_name, joint_id, detection_d['joint_x_y_list'][-1],
                                       detection_d['score_percentages_list'][-1]))

            min_joints_found_ok = valid_joints_found >= self.min_p_valid_joints * len(self.allowed_joint_names)
            pose_valid = min_joints_found_ok and valid_joints_found >= 2
            if pose_valid:  # minimum 2 regardless to self.min_p_valid_joints(which could be zero)
                detection_d['bbox'] = PdBaseModel.get_bbox_dict(detection_d['joint_x_y_list'])
                if detection_d['bbox'] is not None:
                    if ack:
                        print('{}\tbbox:{}'.format(tabs * '\t', detection_d['bbox']))
                    detections.append(detection_d)
                else:
                    if ack:
                        print('{}\tPose {} was dumped. bbox is None'.format(tabs * '\t', pose_id))
            else:
                if ack:
                    min_needed = max(self.min_p_valid_joints * len(self.allowed_joint_names), 2)
                    msg = '{}\tPose {} was dumped. It had valid_joints_found={} (min needed {})'
                    print(msg.format(tabs * '\t', pose_id, valid_joints_found, min_needed))
        return detections
