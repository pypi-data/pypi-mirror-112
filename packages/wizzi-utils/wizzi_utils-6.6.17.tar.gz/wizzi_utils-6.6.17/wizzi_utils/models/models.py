import numpy as np
import os
import abc
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.socket import socket_tools as st
from wizzi_utils.models import models_configs as cfg


class BaseModel:
    def __init__(self, save_load_dir: str, model_name: str):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name from models_config.py
        see:
        class_Models_test()
        """
        self.model_name = model_name
        self.local_path = save_load_dir
        if not os.path.exists(save_load_dir):
            mt.create_dir(save_load_dir, ack=False)
        return

    @staticmethod
    def model_name_valid(model_name: str) -> bool:
        if model_name not in cfg.MODELS_CONFIG:
            err = 'model {} not found in MODELS_CONFIG. options: {}'
            mt.exception_error(err.format(model_name, list(cfg.MODELS_CONFIG.keys())), real_exception=False)
            valid = False
        else:
            valid = True
        return valid

    @staticmethod
    def model_type_valid(model_type: str, model_type_needed: str) -> bool:
        if model_type not in model_type_needed:
            err = 'model type is {} but {} needed'.format(model_type, model_type_needed)
            mt.exception_error(err, real_exception=False)
            valid = False
        else:
            valid = True
        return valid

    @staticmethod
    def _download_if_needed(local_path: str, url_dict: dict) -> None:
        if not os.path.exists(local_path):
            download_style = url_dict['download_style']
            url = url_dict['url']
            if download_style == cfg.DownloadStyle.Direct.value:
                st.download_file(url=url, dst_path=local_path)
            elif download_style in [cfg.DownloadStyle.Tar.value, cfg.DownloadStyle.Zip.value]:
                root_d = os.path.dirname(local_path)
                comp_path = '{}/compressed.{}'.format(root_d, download_style)
                st.download_file(url=url, dst_path=comp_path)  # download compressed
                extracted_folder = '{}/ex'.format(root_d)
                if mt.is_windows():
                    extracted_folder = mt.full_path_no_limit(extracted_folder)

                mt.extract_file(src=comp_path, dst_folder=extracted_folder,
                                file_type=download_style)  # extract
                target_file_in_tar = url_dict['file_to_look']
                # find target file
                target_files = mt.find_files_in_folder(dir_path=extracted_folder, file_suffix=target_file_in_tar)
                if len(target_files) != 1:
                    err_msg = 'not found or found more than 1 target file in downloaded folder: {}'.format(target_files)
                    mt.exception_error(err_msg, real_exception=False)
                    exit(-1)
                mt.move_file(file_src=target_files[0], file_dst=local_path)  # move file

                mt.delete_file(file=comp_path)  # clean up tar\zip
                mt.delete_dir_with_files(dir_path=extracted_folder)  # clean up extracted_folder
        return

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
