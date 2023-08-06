from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.models import models_configs as cfg
from wizzi_utils.models import BaseModel
from wizzi_utils.models import object_detection as od
from wizzi_utils.models import pose_detection as pd
import numpy as np
import os
# noinspection PyPackageRequirements
import cv2

IMAGE_MS = 5000
CAM_FRAMES = 3
VID_X_FRAMES_CV = 80
VID_X_FRAMES_TFL = 20
KEEP_ASPECT_RATIO = True


def __get_od_dict(op: int = 1):
    if op == 1:
        od_solo = {
            'model_names': ['coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'],
            'dis_size': (640, 480),
            'grid': (1, 1),
        }
        od_meta_dict = od_solo
    elif op == 2:
        od_dual = {
            'model_names': [
                'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29',
                # 'yolov4_tiny'
                'yolov4'
            ],
            'dis_size': (640 * 2, 480),
            'grid': (1, 2),
        }
        od_meta_dict = od_dual
    elif op == 3:
        od_all_models = {
            'model_names': od.get_object_detection_models(ack=False),
            'dis_size': 'fs',
            'grid': (5, 6),
        }
        od_meta_dict = od_all_models
    else:
        od_meta_dict = None
    return od_meta_dict


def __get_pd_dict(op: int = 1):
    if op == 1:
        pd_solo = {
            'model_names': ['pose_landmark_lite'],
            # 'model_names': ['pose_landmark_full'],
            # 'model_names': ['pose_landmark_heavy'],
            # 'model_names': ['posenet'],
            # 'model_names': ['openpose_pose_mpi'],
            # 'model_names': ['openpose_pose_coco'],
            # 'model_names': ['openpose_pose_coco_multi'],
            # 'model_names': ['body25'],
            # 'model_names': ['hand_pose'],
            'dis_size': (640, 480),
            'grid': (1, 1),
        }
        pd_meta_dict = pd_solo
    elif op == 2:
        pd_dual = {
            'model_names': [
                'pose_landmark_full',
                # 'posenet'
                # 'openpose_pose_coco'
                'openpose_pose_coco_multi'
            ],
            'dis_size': (640 * 2, 480),
            'grid': (1, 2),
        }
        pd_meta_dict = pd_dual
    elif op == 3:
        all_models_names = pd.get_pose_detection_models(ack=False)
        # remove hand pose - not the same work
        all_models_names.remove('hand_pose')
        pd_all_models = {
            'model_names': all_models_names,
            'dis_size': 'fs',
            'grid': (2, 4),
        }
        pd_meta_dict = pd_all_models
    else:
        pd_meta_dict = None
    return pd_meta_dict


def _get_models(model_names: list, keep_aspect_ratio: bool = True, img_h: int = -1, img_w: int = -1) -> list:
    models = []
    for model_name in model_names:
        if BaseModel.model_name_valid(model_name):
            model_cfg = cfg.MODELS_CONFIG[model_name]
            m_save_dir = '{}/{}/{}'.format(mtt.MODELS, cfg.MODELS_CONFIG[model_name]['job'], model_name)
            if model_cfg['model_type'] == cfg.ModelType.OdCvNormal.value:
                model = od.Cv2OdModel(
                    save_load_dir=m_save_dir,
                    model_name=model_name,
                )
            elif model_cfg['model_type'] == cfg.ModelType.OdTflNormal.value:
                model = od.TflOdModel(
                    save_load_dir=m_save_dir,
                    model_name=model_name,
                )
            elif model_cfg['model_type'] == cfg.ModelType.PdCvNormal.value:
                model = pd.Cv2PdModel(
                    save_load_dir=m_save_dir,
                    model_name=model_name,
                )
            elif model_cfg['model_type'] == cfg.ModelType.PdTflNormal.value:
                model = pd.TflPdModel(
                    save_load_dir=m_save_dir,
                    model_name=model_name,
                    # allowed_joint_names=['nose', 'leftEyeInside', 'leftEye']
                )
            elif model_cfg['model_type'] == cfg.ModelType.PdTflPoseNet.value:
                model = pd.TflPdModelPoseNet(
                    save_load_dir=m_save_dir,
                    model_name=model_name,
                )
            elif model_cfg['model_type'] == cfg.ModelType.PdCvCocoMulti.value:
                if keep_aspect_ratio and 'in_dims' in model_cfg:
                    in_dims_w, in_dims_h = model_cfg['in_dims']
                    # in_dims = cvt.get_aspect_ratio_w(img_w=img_w, img_h=img_h, new_h=in_dims_h)
                    in_dims = cvt.get_aspect_ratio_h(img_w=img_w, img_h=img_h, new_w=in_dims_w)
                else:
                    in_dims = None
                model = pd.Cv2PdModelCocoMultiPoses(
                    save_load_dir=m_save_dir,
                    model_name=model_name,
                    # allowed_joint_names=['Nose', 'Neck', 'RShoulder', 'LShoulder', 'RHip', 'RKnee', 'LHip', 'LKnee',
                    #                      'LAnkle', 'RAnkle']
                    allowed_joint_names=[
                        "Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
                        "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle"
                    ],
                    # device='gpu'
                    in_dims=in_dims,
                    min_p_valid_joints=0.3
                )
            else:
                model = None
                mt.exception_error('model type not found')
                exit(-1)
            print(model.to_string(tabs=1))
            models.append(model)
    return models


def od_run(
        model: (od.TflOdModel, od.Cv2OdModel),
        cv_img: np.array,
        fps: mt.FPS = None,
        with_tf: bool = False,
        with_sub: bool = False
):
    if fps is not None:
        fps.start()
    detections = model.detect_cv_img(cv_img, ack=False)
    if fps is not None:
        fps.update(ack_progress=True, tabs=1, with_title=True)
    if with_tf:
        detections = model.add_traffic_light_to_detections(
            detections,
            traffic_light_p={
                'up': 0.2,
                'mid': 0.3,
                'down': 0.4
            }
        )
    if with_sub:
        detections = model.add_sub_sub_image_to_detection(
            detections,
            cv_img=cv_img,
            bbox_image_p={
                'x_left_start': 0.2,
                'x_left_end': 0.8,
                'y_top_start': 0,
                'y_top_end': 0.5,
            },
        )
    model.draw_detections(
        detections,
        colors_d={
            'label_bbox': 'black',  # if draw_labels - text bg color
            'text': 'white',  # if draw_labels - text bg color
            'sub_image': 'blue',  # if draw_sub_image - sub image bbox color
            'default_bbox': 'red',  # bbox over the detection
            'person_bbox': 'black',  # custom color per class person
            'dog_bbox': 'lime',  # custom color per class dog
            'cat_bbox': 'magenta',  # custom color per class cat
        },
        cv_img=cv_img,
        draw_labels=True,
        draw_tl_image=with_tf,
        draw_sub_image=with_sub,
    )
    return


def pd_run(
        model: (pd.TflPdModel, pd.Cv2PdModel, pd.TflPdModelPoseNet),
        cv_img: np.array,
        fps: mt.FPS = None,
        with_sub: bool = False
):
    if fps is not None:
        fps.start()
    # detections = model.detect_cv_img(cv_img, ack=True)  # TODO comment out
    detections = model.detect_cv_img(cv_img, ack=False)
    if fps is not None:
        fps.update(ack_progress=True, tabs=1, with_title=True)
    if with_sub:
        detections = model.add_sub_sub_image_to_detection(
            detections,
            cv_img=cv_img,
            bbox_image_p={
                'x_left_start': 0.2,
                'x_left_end': 0.8,
                'y_top_start': 0,
                'y_top_end': 0.5,
            },
        )
    model.draw_detections(
        detections,
        colors_d={
            'bbox_c': 'blue',
            'sub_image_c': 'black',
            'text_c': 'black',
            # 'joint_colors': 'red',
            # 'edge_c': 'yellow',
        },
        cv_img=cv_img,
        draw_joints=True,
        draw_labels=True,
        draw_edges=True,
        draw_bbox=True,
        draw_sub_image=with_sub,
    )
    return


def od_or_pd_Model_image_test(
        cv_img: np.array,
        model_names: list,
        ms: int = cvtt.BLOCK_MS_NORMAL,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    mt.get_function_name(ack=True, tabs=0)
    orig_shape = '{}'.format(cv_img.shape)
    cv_imgs_post = []
    img_h, img_w = cv_img.shape[0], cv_img.shape[1]
    models = _get_models(model_names, keep_aspect_ratio=KEEP_ASPECT_RATIO, img_w=img_w, img_h=img_h)

    for model in models:
        cv_img_clone = cv_img.copy()
        fps = mt.FPS(summary_title='{}'.format(model.model_name))
        if isinstance(model, (od.Cv2OdModel, od.TflOdModel)):
            od_run(model, cv_img_clone, fps=fps, with_tf=True, with_sub=True)
        elif isinstance(model, (pd.Cv2PdModel, pd.TflPdModel, pd.TflPdModelPoseNet)):
            pd_run(model, cv_img_clone, fps=fps, with_sub=True)

        cvt.add_header(cv_img_clone, header=model.model_name, loc=pyplt.Location.BOTTOM_LEFT.value, bg_font_scale=1)
        cvt.add_header(cv_img_clone, header='{:.2f} FPS'.format(fps.get_fps()), loc=pyplt.Location.TOP_RIGHT.value,
                       x_offset=190, text_color='r', with_rect=False, bg_font_scale=1)

        cv_imgs_post.append(cv_img_clone)
    cvt.display_open_cv_images(
        cv_imgs_post,
        ms=ms,
        title=orig_shape,
        loc=pyplt.Location.CENTER_CENTER.value,
        grid=grid,
        resize=dis_size,
        header=None,
        save_path=None
    )
    cv2.destroyAllWindows()
    return


def _od_or_pd_Model_cam_test(
        cam: (cv2.VideoCapture, cvt.CameraWu),
        model_names: list = None,
        max_frames: int = CAM_FRAMES,
        work_every_x_frames: int = 1,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    if isinstance(cam, cv2.VideoCapture):
        img_w, img_h = cvt.get_dims_from_cap(cam)
    else:
        img_w, img_h = cvt.get_dims_from_cap(cam.cam)
    if len(model_names) == 1:
        mp4_out_dir = '{}/{}/{}'.format(mtt.VIDEOS_OUTPUTS, mt.get_function_name(), model_names[0])
        if not os.path.exists(mp4_out_dir):
            mt.create_dir(mp4_out_dir)
        out_fp = '{}/{}_detected.mp4'.format(mp4_out_dir, 'cam')
        out_dims = (img_w, img_h)
        mp4 = cvt.Mp4_creator(
            out_full_path=out_fp,
            out_fps=20.0,
            out_dims=out_dims
        )
        print(mp4)
    else:
        mp4 = None

    models = _get_models(model_names, keep_aspect_ratio=KEEP_ASPECT_RATIO, img_w=img_w, img_h=img_h)
    fps_list = [mt.FPS(summary_title='{}'.format(model.model_name)) for model in models]
    for i in range(max_frames):
        if isinstance(cam, cv2.VideoCapture):
            success, cv_img = cam.read()
        else:
            success, cv_img = cam.read_img()
        if i % work_every_x_frames != 0:  # s
            # do only x frames
            continue
        cv_imgs_post = []
        if success:
            for model, fps in zip(models, fps_list):
                cv_img_clone = cv_img.copy()
                if isinstance(model, (od.Cv2OdModel, od.TflOdModel)):
                    od_run(model, cv_img_clone, fps=fps, with_tf=False, with_sub=False)
                elif isinstance(model, (pd.Cv2PdModel, pd.TflPdModel)):
                    pd_run(model, cv_img_clone, fps=fps, with_sub=False)

                cvt.add_header(cv_img_clone, header=model.model_name, loc=pyplt.Location.BOTTOM_LEFT.value,
                               bg_font_scale=1)
                cvt.add_header(cv_img_clone, header='{:.2f} FPS'.format(fps.get_fps()),
                               loc=pyplt.Location.TOP_RIGHT.value, x_offset=190, text_color='r', with_rect=False,
                               bg_font_scale=1)
                cv_imgs_post.append(cv_img_clone)
            if mp4 is not None:
                mp4.add_frame(cv_imgs_post[0])
        cvt.display_open_cv_images(
            cv_imgs_post,
            ms=1,
            title='cam 0',
            loc=pyplt.Location.CENTER_CENTER.value,
            grid=grid,
            resize=dis_size,
            header='{}/{}'.format(i + 1, max_frames),
            save_path=None
        )
    for fps in fps_list:
        fps.finalize()
    if mp4 is not None:
        mp4.finalize()
    cv2.destroyAllWindows()
    return


def od_or_pd_Model_cam_test(
        model_names: list = None,
        max_frames: int = CAM_FRAMES,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    mt.get_function_name(ack=True, tabs=0)
    cam = cvt.CameraWu.open_camera(port=0, type_cam='cv2')

    if cam is not None:
        _od_or_pd_Model_cam_test(
            cam=cam,
            model_names=model_names,
            max_frames=max_frames,
            work_every_x_frames=1,
            dis_size=dis_size,
            grid=grid,
        )
    return


def od_or_pd_Model_video_test(
        model_names: list,
        vid_path: str,
        work_every_x_frames: int = 1,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    mt.get_function_name(ack=True, tabs=0)
    cam = cv2.VideoCapture(vid_path)
    if cam is not None:
        _od_or_pd_Model_cam_test(
            cam=cam,
            model_names=model_names,
            max_frames=cvt.get_frames_from_cap(cam),
            work_every_x_frames=work_every_x_frames,
            dis_size=dis_size,
            grid=grid,
        )
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))

    od_image_test = True
    od_cam_test = False
    od_vid_test = False
    pd_image_test = True
    pd_cam_test = False
    pd_vid_test = False

    # od.get_object_detection_models(ack=True)
    # pd.get_pose_detection_models(ack=True)
    # exit(-12)
    od_meta_dict = __get_od_dict(op=1)
    pd_meta_dict = __get_pd_dict(op=1)

    # OBJECT DETECTION TESTS
    if od_image_test:
        cv_img = cvtt.load_img_from_web(mtt.DOG, ack=False)
        od_or_pd_Model_image_test(
            cv_img=cv_img,
            model_names=od_meta_dict['model_names'],
            ms=IMAGE_MS,
            dis_size=od_meta_dict['dis_size'],
            grid=od_meta_dict['grid'],
        )
    if od_cam_test:
        od_or_pd_Model_cam_test(
            model_names=od_meta_dict['model_names'],
            max_frames=CAM_FRAMES,
            dis_size=od_meta_dict['dis_size'],
            grid=od_meta_dict['grid'],
        )
    if od_vid_test:
        # vid_path = cvtt.get_vid_from_web(name=mtt.DOG1)
        vid_path = cvtt.get_vid_from_web(name=mtt.WOMAN_YOGA)
        od_or_pd_Model_video_test(
            model_names=od_meta_dict['model_names'],
            vid_path=vid_path,
            work_every_x_frames=VID_X_FRAMES_CV,
            dis_size=od_meta_dict['dis_size'],
            grid=od_meta_dict['grid'],
        )
    # POSE DETECTION TESTS
    if pd_image_test:
        # cv_img = cvtt.load_img_from_web(mtt.FACES, ack=False)
        # cv_img = cvtt.load_img_from_web(mtt.HAND, ack=False)  # if testing 'hand_pose', use HAND image
        cv_img = cvtt.load_img_from_web(mtt.F_MODEL, ack=False)
        # cv_img = cvt.load_img(path='{}/Input2/77.jpg'.format(mtt.IMAGES_PATH))
        # cv_img = cvt.load_img(path='{}/Input2/cam1_0.jpg'.format(mtt.IMAGES_PATH))

        od_or_pd_Model_image_test(
            cv_img=cv_img,
            model_names=pd_meta_dict['model_names'],
            ms=0,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    if pd_cam_test:
        od_or_pd_Model_cam_test(
            model_names=pd_meta_dict['model_names'],
            max_frames=CAM_FRAMES,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    if pd_vid_test:
        vid_path = cvtt.get_vid_from_web(name=mtt.WOMAN_YOGA)
        od_or_pd_Model_video_test(
            model_names=pd_meta_dict['model_names'],
            vid_path=vid_path,
            work_every_x_frames=VID_X_FRAMES_TFL,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )

    print('{}'.format('-' * 20))
    return
