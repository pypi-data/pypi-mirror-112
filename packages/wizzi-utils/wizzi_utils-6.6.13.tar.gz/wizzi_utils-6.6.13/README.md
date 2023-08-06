# Package wizzi utils:  
## Installation: 
```bash
pip install wizzi_utils 
```
## Usage
```python
import wizzi_utils as wu # imports all that is available
print(wu.version()) 
wu.test_all_modules()  # run all tests in all modules(packages)
```
* The above import will give you access to all functions and tests in wizzi_utils.<br/>
* Other than misc_tools, it's the user's responsibility to install the requirements to sub packages such
as torch, tensorflow and so on.
* For convenience, the wizzi_utils imports all it can from the sub packages, therefore
only the one import above is enough.
* Every function is covered by a test(usually the 'func_name'_test()). Use this to see how the 
function works and also to copy paste the signature.
```markdown
from wizzi_utils import algorithms as algs  
# access wu.algs.func() or wu.algs.test.func() 
from wizzi_utils import coreset as cot
from wizzi_utils import google as got
from wizzi_utils import json as jt
from wizzi_utils import open_cv as cvt
from wizzi_utils import pyplot as pyplt
from wizzi_utils import socket as st
from wizzi_utils import torch as tt
from wizzi_utils import tensorflow as tft
from wizzi_utils import tflite as tflt
```

###  misc_tools & misc_tools_test
'pip install wizzi_utils' made sure you'll have everything needed installed so they should be fully working,
so there is no namespace for misc_tools module(direct access from wu)<br/>
```python
import wizzi_utils as wu


def main():
    # all functions in misc_tools & misc_tools_test are imported to wizzi_utils
    print(wu.to_str(var=2, title='my_int'))  # notice only wu namespace

    # direct access to the misc_tools module
    print(wu.misc_tools.to_str(var=2, title='my_int'))  # not needed but possible

    wu.test.test_all()  # runs all tests in misc_tools_test.py
    wu.test.to_str_test()  # runs only to_str_test
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```

### All other packages
Other packages, e.g. torch_tools, will work only if you have all the dependencies written in the init file of the module
or by calling wu.wizzi_utils_requirements()

```python
import wizzi_utils as wu


def main():
    wu.wizzi_utils_requirements()  # will print all packages names and their requirements

    # access to a function in the torch module (must install torch and torchvision)
    print(wu.tt.to_str(var=3, title='my_int'))  # notice wu and tt namespaces. tt for torch tools

    # access to a function in the matplotlib module(must install matplotlib and mpl_toolkits)
    print(wu.pyplt.get_RGB_color(color_str='r'))

    # access to a module test
    wu.algs.test.test_all()  # all tests in algorithm module
    wu.pyplt.test.plot_3d_iterative_dashboard_test()  # specific test in pyplot module
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```  
### Examples:
```python
import wizzi_utils as wu


def main():
    wu.wizzi_utils_requirements()
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```
```text
C:\Users\GiladEiniKbyLake\.conda\envs\wu\python.exe D:/workspace/2021wizzi_utils/temp/wu_test.py
--------------------------------------------------------------------------------
main_wrapper:
* Run started at 29-05-2021 18:25:19
* Python Version 3.6.8 |Anaconda, Inc.| (default, Feb 21 2019, 18:30:04) [MSC v.1916 64 bit (AMD64)]
* Interpreter: C:\Users\GiladEiniKbyLake\.conda\envs\wu\python.exe
* wizzi_utils Version 6.3.3
* Working Dir: D:\workspace\2021wizzi_utils\temp
* Computer Name: XXXX
* Computer Mac: AA:BB:CC:DD:EE:FF
* CPU Info: AMD64, Physical cores 4, Total cores 8, Frequency 3601.00Mhz, CPU Usage 15.9%
* Physical Memory: C: Total 232.33 GB, Used 186.69 GB(80.40%), Free 45.64 GB, D: Total 931.39 GB, Used 490.31 GB(52.60%), Free 441.07 GB, E: PermissionError: [WinError 21] The device is not ready: 'E'
* RAM: Total 15.94 GB, Used 5.1 GB(32.0%), Available 10.83 GB 
* Computer ipv4: 111.111.1.1
* CUDA Version: v9.1
* PyTorch Version 1.1.0 - cuda detected ? True
* TensorFlow Version 1.12.0 - GPU detected ? True
* TFLite Version 2.5.0
* OpenCv Version 4.5.1
* Seed was initialized to 42
Function <function main at 0x0000022C883B1EA0> started:
--------------------------------------------------------------------------------
Requirements per package:
	To use a test of a package, must install all package requirements
--------------------------------------------------------------------------------
Package misc(misc_tools.py, namespace: mt):
	pip install py7zr # to use 7z compress and extract
	test_misc_tools.py(namespace: mt.test):
		None
--------------------------------------------------------------------------------
Package algorithms(algorithms.py, namespace: alg):
	pip install sklrean
	test_algorithms.py(namespace: alg.test):
		Sub Package: pyplot
--------------------------------------------------------------------------------
Package coreset(coreset_tools.py, namespace: cot):
	None
	test_coreset_tools.py(namespace: cot.test):
		None
--------------------------------------------------------------------------------
Package google(google_tools.py, namespace: got):
	*** see instructions in order to use written in class google_handler docstring
	pip install pydrive
	test_google_tools.py(namespace: got.test):
		Sub Package: socket
--------------------------------------------------------------------------------
Package json(json_tools.py, namespace: jt):
	None
	test_json_tools.py(namespace: jt.test):
		None
--------------------------------------------------------------------------------
Package open_cv(open_cv_tools.py, namespace: cvt):
	pip install opencv-python
	Sub Package: pyplot
	test_open_cv_tools.py(namespace: cvt.test):
		Sub Package: socket
		Sub Package: open_cv
--------------------------------------------------------------------------------
Package pyplot(pyplot_tools.py, namespace: pyplt):
	pip install matplotlib
	pip install mpl_toolkits
	pip install torch # for compare_images_multi_sets_squeezed()
	test_pyplot_tools.py(namespace: pyplt.test):
		pip install torch # for compare_images_multi_sets_squeezed_test()
		Sub Package: open_cv # also the test
--------------------------------------------------------------------------------
Package socket(socket_tools.py, namespace: st):
	None
	test_socket_tools.py(namespace: st.test):
		Sub Package: json
--------------------------------------------------------------------------------
Package torch(torch_tools.py, namespace: tt):
	torch options:
		pip install torch # cpu
		pip install torch==1.1.0 torchvision==0.3.0 -f https://download.pytorch.org/whl/cu90/torch_stable.html # gpu(cuda 9 and 9.1)
		all options: https://pytorch.org/get-started/locally/
		** may need to uninstall numpy and re-install
	pip install torchvision
	test_torch_tools.py(namespace: tt.test):
		None
--------------------------------------------------------------------------------
Package tensorflow(tensorflow_tools.py, namespace: tft):
	tensorflow options:
		pip install tensorflow # cpu only
		pip install tensorflow-gpu==1.12 # gpu cuda 9.1
		pip install tensorflow-gpu # gpu cuda>=10
		all options: https://stackoverflow.com/questions/50622525/which-tensorflow-and-cuda-version-combinations-are-compatible
	test_tensorflow_tools.py(namespace: tft.test):
		None
--------------------------------------------------------------------------------
Package tflite(tflite_tools.py, namespace: tflt):
	tensorflow options:
		pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime # windows 10
	test_tflite_tools.py(namespace: tflt.test):
		None
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Total run time 0:00:01

Process finished with exit code 0
```
```python
import wizzi_utils as wu


def main():
    # mt package - main package
    wu.test.to_str_test()
    wu.test.add_color_test()
    wu.test.get_time_stamp_test()
    wu.test.get_time_stamp_test()
    wu.test.save_load_npz_test()
    wu.test.shuffle_np_arrays_test()
    wu.test.save_load_pkl_test()
    wu.test.nCk_test()
    wu.test.get_base_file_and_function_name_test()
    wu.test.file_or_folder_size_test()
    wu.test.classFPS_test()
    # alg package
    wu.algs.test.find_centers_test()
    # pyplt package
    wu.pyplt.test.move_figure_by_str_test()
    wu.pyplt.test.plot_2d_many_figures_iterative_test()
    wu.pyplt.test.plot_3d_iterative_dashboard_test()
    wu.pyplt.test.compare_images_sets_test()
    wu.pyplt.test.compare_images_multi_sets_squeezed_test()  # if you have torch, torchvision
    # cvt package
    wu.cvt.test.move_cv_img_by_str_test()
    wu.cvt.test.unpack_list_imgs_to_big_image_test()
    # st package
    wu.st.test.download_file_test()    
    # tt package
    wu.tt.test.count_keys_test()
    wu.tt.test.to_str_test()
    wu.tt.test.save_load_tensor_test()
    wu.tt.test.OptimizerHandler_test()
    wu.tt.test.shuffle_tensors_test()
    wu.tt.test.count_keys_test()
    wu.tt.test.get_torch_version_test()
    wu.tt.test.save_load_model_test()
    wu.tt.test.model_summary_test()
    
    # got package - first do the instructions
    wu.got.test.upload_delete_image_test()
    return


if __name__ == '__main__':
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
```     
    