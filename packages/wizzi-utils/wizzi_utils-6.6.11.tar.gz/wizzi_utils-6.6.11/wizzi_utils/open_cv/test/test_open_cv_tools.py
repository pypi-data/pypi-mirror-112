from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.socket import socket_tools as st
from wizzi_utils.pyplot import pyplot_tools as pyplt
import numpy as np
import os
# noinspection PyPackageRequirements
import cv2

LOOP_TESTS = 50
BLOCK_MS_NORMAL = 2000  # 0 to block
ITERS_CAM_TEST = 10  # 0 to block


def load_img_from_web(name: str, ack: bool = True) -> np.array:
    f = mtt.IMAGES_INPUTS
    url = mtt.IMAGES_D[name]
    suffix = 'jpg'  # default
    # if '.webm' in url:
    #     suffix = 'webm'
    dst = '{}/{}.{}'.format(f, name, suffix)

    if not os.path.exists(dst):
        if not os.path.exists(f):
            mt.create_dir(f)
        success = st.download_file(url, dst)
        if not success:
            mt.exception_error('download failed - creating random img', real_exception=False)
            img = mt.np_random_integers(size=(240, 320, 3), low=0, high=255)
            img = img.astype('uint8')
            cvt.save_img(dst, img)

    img = cvt.load_img(path=dst, ack=ack)
    return img


def get_vid_from_web(name: str) -> str:
    f = mtt.VIDEOS_INPUTS
    url = mtt.VIDEOS_D[name]
    suffix = 'mp4'  # default
    if '.webm' in url:
        suffix = 'webm'
    dst = '{}/{}.{}'.format(f, name, suffix)

    if not os.path.exists(dst):
        if not os.path.exists(f):
            mt.create_dir(f)
        success = st.download_file(url, dst)
        if not success:
            mt.exception_error('download failed - creating random img', real_exception=False)
            dst = None

    return dst


def get_cv_version_test():
    mt.get_function_name(ack=True, tabs=0)
    cvt.get_cv_version(ack=True, tabs=1)
    return


def imread_imwrite_test():
    mt.get_function_name(ack=True, tabs=0)
    name = mtt.SO_LOGO
    img = load_img_from_web(name)

    f = mtt.IMAGES_INPUTS
    url = mtt.IMAGES_D[name]
    dst_path = '{}/{}'.format(f, os.path.basename(url).replace('.png', '_copy.png'))

    cvt.save_img(dst_path, img, ack=True)
    img_loaded = cvt.load_img(dst_path, ack=True)
    print(mt.to_str(img_loaded, '\timg_copy'))
    mt.delete_file(dst_path, ack=True)
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def list_to_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    img_list = img.tolist()
    print(mt.to_str(img_list, '\timg_list'))
    img = cvt.list_to_cv_image(img_list)
    print(mt.to_str(img, '\timg'))
    # mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def display_open_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    print('\tVisual test: stack overflow logo')
    loc = (70, 200)  # move to X,Y
    resize = 1.7  # enlarge to 170%
    cvt.display_open_cv_image(
        img=img,
        ms=1,  # not blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    loc = pyplt.Location.TOP_RIGHT.value  # move to top right corner
    resize = 1.7  # enlarge to 170%
    cvt.display_open_cv_image(
        img=img,
        ms=BLOCK_MS_NORMAL,  # blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def display_open_cv_image_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    loc = (70, 200)  # move to X,Y
    resize = 1.7  # enlarge to 170%
    title = 'stack overflow logo moved to {} and re-sized to {} - {} iterations'.format(loc, resize, LOOP_TESTS)
    print('\tVisual test: {}'.format(title))
    for i in range(LOOP_TESTS):
        cvt.display_open_cv_image(
            img=img,
            ms=1,  # not blocking
            title=title,
            loc=loc,  # start from x =70 y = 0
            resize=resize
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def resize_opencv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img1 = load_img_from_web(mtt.SO_LOGO)
    img2 = img1.copy()
    img3 = img1.copy()

    cvt.display_open_cv_image(
        img=img1,
        ms=1,
        title='img1',
        loc=pyplt.Location.TOP_LEFT.value,
        resize=1.6,
        header='resize to 160%',
        save_path=None,
    )
    cvt.display_open_cv_image(
        img=img2,
        ms=BLOCK_MS_NORMAL,
        title='img2',
        loc=pyplt.Location.CENTER_LEFT.value,
        resize=(400, 200),
        header='resize to (400, 200)',
        save_path=None,
    )
    cv2.destroyAllWindows()

    # no full-screen
    cvt.display_open_cv_image(
        img=img3,
        ms=BLOCK_MS_NORMAL,
        title='img3',
        loc=pyplt.Location.BOTTOM_LEFT.value,
        resize='fs',
        header='resize to full-screen',
        save_path=None,
    )
    cv2.destroyAllWindows()
    return


def move_cv_img_x_y_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    options = [(0, 0), (100, 0), (0, 100), (150, 150), (400, 400), (250, 350)]
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for x_y in options:
        title = 'move to ({})'.format(x_y)
        cv2.imshow(title, img)
        cvt.move_cv_img_x_y(title, x_y)
    cv2.waitKey(BLOCK_MS_NORMAL)
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def move_cv_img_by_str_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    options = pyplt.Location.get_location_list_by_rows()
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for where_to in options:
        title = 'move to {}'.format(where_to)
        cv2.imshow(title, img)
        cvt.move_cv_img_by_str(img, title, where=where_to)
    cv2.waitKey(BLOCK_MS_NORMAL)
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def unpack_list_imgs_to_big_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    gray = cvt.BGR_img_to_gray(img)
    big_img = cvt.unpack_list_imgs_to_big_image(
        imgs=[img, gray, img],
        grid=(2, 2)
    )
    title = 'stack overflow logo 2x2(1 empty)'
    print('\tVisual test: {}'.format(title))
    cvt.display_open_cv_image(
        img=big_img,
        ms=BLOCK_MS_NORMAL,  # blocking
        title=title,
        loc=(0, 0),
        resize=None
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def display_open_cv_images_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    title = '2x1 grid'
    print('\tVisual test: {}'.format(title))
    loc1 = (0, 0)
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=1,  # blocking
        title='{} loc={}'.format(title, loc1),
        loc=loc1,
        resize=1.5,
        grid=(2, 1),
        header='{} loc={}'.format(title, loc1),
    )
    loc2 = pyplt.Location.BOTTOM_CENTER.value
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=BLOCK_MS_NORMAL,  # blocking
        title='{} loc={}'.format(title, loc2),
        loc=loc2,
        resize=None,
        grid=(2, 1),
        header='{} loc={}'.format(title, loc1),
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def display_open_cv_images_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    loc = (70, 200)  # move to X,Y
    title = 'stack overflow logo moved to {} - {} iterations'.format(loc, LOOP_TESTS)
    print('\tVisual test: {}'.format(title))
    for i in range(LOOP_TESTS):
        cvt.display_open_cv_images(
            imgs=[img, img],
            ms=1,  # blocking
            title=title,
            loc=loc,
            resize=None,
            grid=(2, 1),
            header=None
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def gray_to_BGR_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    print(mt.to_str(img, '\timgRGB'))
    gray = cvt.BGR_img_to_gray(img)
    print(mt.to_str(img, '\timg_gray'))
    img = cvt.gray_scale_img_to_BGR_form(gray)
    print(mt.to_str(img, '\timgRGB'))
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def BGR_img_to_RGB_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    imgBGR1 = load_img_from_web(mtt.SO_LOGO)
    print(mt.to_str(imgBGR1, '\timgBGR'))
    imgRGB = cvt.BGR_img_to_RGB(imgBGR1)
    print(mt.to_str(imgRGB, '\timgRGB'))
    imgBGR2 = cvt.RGB_img_to_BGR(imgRGB)
    print(mt.to_str(imgBGR2, '\timgBGR2'))

    cvt.display_open_cv_images(
        imgs=[imgBGR1, imgRGB, imgBGR2],
        ms=BLOCK_MS_NORMAL,  # blocking
        title='imgBGR1, imgRGB, imgBGR2',
        loc=pyplt.Location.CENTER_CENTER,
        resize=None,
        grid=(3, 1),
        header='compare'
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def CameraWu_test(type_cam: str):
    WITH_SLEEP = False
    ports = [0, 1, 13]
    cams = []
    for port in ports:
        cam = cvt.CameraWu.open_camera(port=port, type_cam=type_cam)
        if cam is not None:
            cams.append(cam)

    for cam in cams:
        title = 'CameraWu_test({}) on port {}'.format(cam.type_cam, cam.port)
        fps = mt.FPS(summary_title=title)
        for i in range(ITERS_CAM_TEST):
            fps.start()
            success, cv_img = cam.read_img()
            if WITH_SLEEP:
                mt.sleep(1)

            if success:
                cvt.display_open_cv_image(
                    img=cv_img,
                    ms=1,
                    title=title,
                    loc=pyplt.Location.CENTER_CENTER,
                    resize=None,
                    header='{}/{}'.format(i + 1, ITERS_CAM_TEST)
                )
            fps.update()
        fps.finalize()
    cv2.destroyAllWindows()
    return


def CameraWu_cv2_test():
    mt.get_function_name(ack=True, tabs=0)
    CameraWu_test(type_cam='cv2')
    return


def CameraWu_acapture_test():
    mt.get_function_name(ack=True, tabs=0)
    CameraWu_test(type_cam='acapture')
    return


def CameraWu_imutils_test():
    mt.get_function_name(ack=True, tabs=0)
    CameraWu_test(type_cam='imutils')
    return


def add_text_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.HORSES)
    cvt.add_text(img, header='test text', pos=(100, 100), text_color='r', with_rect=True, bg_color='y', bg_font_scale=2)
    cvt.add_text(img, header='test text', pos=(100, 200), text_color='black', with_rect=True, bg_color='b',
                 bg_font_scale=1)
    cvt.display_open_cv_image(img, ms=BLOCK_MS_NORMAL, loc=pyplt.Location.CENTER_CENTER.value)
    cv2.destroyAllWindows()
    return


def add_header_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.HORSES)

    cvt.add_header(img, header='TOP_LEFT', loc=pyplt.Location.TOP_LEFT.value,
                   text_color='lime', with_rect=True, bg_color='azure', bg_font_scale=1)
    cvt.add_header(img, header='BOTTOM_LEFT', loc=pyplt.Location.BOTTOM_LEFT.value,
                   text_color='fuchsia', with_rect=True, bg_color='black', bg_font_scale=2)
    cvt.add_header(img, header='TOP_RIGHT', loc=pyplt.Location.TOP_RIGHT.value, x_offset=180,
                   text_color='darkorange', with_rect=True, bg_color='azure', bg_font_scale=1)
    cvt.add_header(img, header='BOTTOM_RIGHT', loc=pyplt.Location.BOTTOM_RIGHT.value, x_offset=120,
                   text_color='aqua', with_rect=True, bg_color='black', bg_font_scale=2)
    cvt.display_open_cv_image(img, title='all headers', ms=1, loc=pyplt.Location.TOP_LEFT.value)

    img = load_img_from_web(mtt.DOG)
    cvt.display_open_cv_image(
        img,
        title='built in header',
        ms=BLOCK_MS_NORMAL,
        loc=pyplt.Location.TOP_RIGHT.value,
        header='direct header into display_open_cv_image'
    )
    cv2.destroyAllWindows()
    return


def Mp4_creator_test():
    mt.get_function_name(ack=True, tabs=0)
    # now open video file
    vid_name = mtt.DOG1
    video_path = get_vid_from_web(name=vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path), real_exception=False)
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        out_dims = cvt.get_dims_from_cap(cap)
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
        print('\tvid size is {}'.format(out_dims))
    else:
        mt.exception_error('cap is closed.', real_exception=False)
        return

    out_dir = '{}/create_mp4_test'.format(mtt.VIDEOS_OUTPUTS)
    mt.create_dir(out_dir)
    out_fp = '{}/{}_output.mp4'.format(out_dir, vid_name)

    mp4_creator = cvt.Mp4_creator(
        out_full_path=out_fp,
        out_fps=20.0,
        out_dims=out_dims
    )
    print(mp4_creator)

    for i in range(video_total_frames):
        success, frame = cap.read()
        if i % int(video_total_frames / 10) != 0:  # s
            # do only 10 frames
            continue
        print('\tframe {}/{}:'.format(i + 1, video_total_frames))
        # print('\t\t{}'.format(mt.to_str(frame)))
        if success:
            cvt.add_header(
                frame,
                header='create_mp4_test frame {}/{}'.format(i + 1, video_total_frames),
                loc=pyplt.Location.BOTTOM_LEFT.value,
                text_color=pyplt.get_random_color(),
                bg_color=pyplt.get_random_color(),
            )
            cvt.display_open_cv_image(frame, ms=1, title=vid_name, loc=None,
                                      header='{}/{}'.format(i + 1, video_total_frames))
            mp4_creator.add_frame(frame, ack=True, tabs=2)

    cap.release()
    mp4_creator.finalize()
    cv2.destroyAllWindows()
    return


def get_aspect_ratio_test():
    mt.get_function_name(ack=True, tabs=0)
    cv_img_fake = np.zeros(shape=(480, 640, 3))
    img_h, img_w = cv_img_fake.shape[0], cv_img_fake.shape[1]
    new_h = 192
    resize_dims = cvt.get_aspect_ratio_w(img_w=img_w, img_h=img_h, new_h=new_h)
    print('\timage size={} and new_h={}: new dims should be {}'.format(cv_img_fake.shape, new_h, resize_dims))

    new_w = 192
    resize_dims = cvt.get_aspect_ratio_h(img_w=img_w, img_h=img_h, new_w=new_w)
    print('\timage size={} and new_w={}: new dims should be {}'.format(cv_img_fake.shape, new_w, resize_dims))
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    get_cv_version_test()
    imread_imwrite_test()
    list_to_cv_image_test()
    display_open_cv_image_test()
    display_open_cv_image_loop_test()
    resize_opencv_image_test()
    move_cv_img_x_y_test()
    move_cv_img_by_str_test()
    unpack_list_imgs_to_big_image_test()
    display_open_cv_images_test()
    display_open_cv_images_loop_test()
    gray_to_BGR_and_back_test()
    BGR_img_to_RGB_and_back_test()
    add_header_test()
    add_text_test()
    CameraWu_cv2_test()
    CameraWu_acapture_test()
    CameraWu_imutils_test()
    Mp4_creator_test()
    get_aspect_ratio_test()
    print('{}'.format('-' * 20))
    return
