python -m PyInstaller main.py ^
--onefile ^
--noconfirm ^
--contents-directory . ^
--hidden-import tensorflow_io ^
--add-data .\model\model_800;.\model\model_800 ^
--add-data .\*.qml;. ^
--paths .\build_dlls ^
--add-binary %LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.10_*^
\LocalCache\local-packages\Python310\site-packages\scipy\linalg\_fblas.cp310-win_amd64.dll.a;. ^
--add-binary %LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.10_*^
\LocalCache\local-packages\Python310\site-packages\tensorflow_io\python\ops\*.so;^
.\tensorflow_io\python\ops ^
