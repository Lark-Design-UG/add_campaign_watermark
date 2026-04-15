# Add Campaign Watermark

[中文](#中文) | [English](#english)

---

<h2 id="中文">中文</h2>

这是一个用于给图片批量添加水印/Logo 的 Python 脚本。它能够根据 `logos` 文件夹内的子文件夹自动识别 Logo 位置，并将其按比例自适应缩放到原图的对应角落，同时保留原图并将处理后的图片保存到新文件夹中。

### 第一次使用指南

#### 1. 环境准备
确保你的电脑上安装了 Python 3。然后通过 `requirements.txt` 安装必要的依赖库：

```bash
pip install -r requirements.txt
```

如果提示找不到 pip，请尝试使用：

```bash
pip3 install -r requirements.txt
```

#### 2. 准备文件目录
脚本依赖特定的文件夹结构来工作，请在脚本所在的目录下确保存在以下文件夹：

*   `put_your_images_here/`：把你需要加水印的**原图**放在这里。
*   `logos/`：存放你的 Logo 文件。该文件夹下包含四个子文件夹，代表图片的四个角落：
    *   `up_left_corner/`（左上角）
    *   `up_right_corner/`（右上角）
    *   `low_left_corner/`（左下角）
    *   `low_right_corner/`（右下角）
    *   *你只需要在需要显示 Logo 的对应角落文件夹中放入 Logo 图片（`.png` 格式最佳，支持透明背景）。*

#### 3. 配置参数（可选）
你可以使用文本编辑器打开 `add_watermark.py`，在脚本顶部的 **全局配置区** 修改缩放比例和边距：

*   `MARGIN_RATIO`：控制 Logo 距离边缘的距离（基于原图较长边的比例）。
*   `LOGO_SCALE_RATIO`：分别控制四个角 Logo 的相对大小（基于原图较长边的比例）。
*   `OUTPUT_FORMAT`：选择导出图片的格式，可选 `'jpg'` 或 `'png'`（默认为 `'jpg'`）。

#### 4. 运行脚本
在终端或命令行中，进入脚本所在的目录，运行：

```bash
python add_watermark.py
```

如果提示找不到 python，请尝试使用：

```bash
python3 add_watermark.py
```

处理完成的图片会自动保存在自动创建的 `get_results_here/` 文件夹中。

---

<h2 id="english">English</h2>

This is a Python script for batch adding watermarks/logos to images. It automatically identifies the logo position based on the subfolders within the `logos` directory, adaptively scales and places them in the corresponding corners of the original images, and saves the processed images to a new folder while preserving the originals.

### First Time Setup & Usage

#### 1. Environment Setup
Make sure Python 3 is installed on your computer. Then install the required dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### 2. Prepare Directory Structure
The script relies on a specific folder structure. Please ensure the following folders exist in the same directory as the script:

*   `put_your_images_here/`: Place the **original images** you want to watermark in this folder.
*   `logos/`: Contains your logo files. Inside this folder, there should be four subfolders representing the four corners:
    *   `up_left_corner/`
    *   `up_right_corner/`
    *   `low_left_corner/`
    *   `low_right_corner/`
    *   *Simply place your logo image (preferably `.png` with a transparent background) into the subfolder corresponding to the corner where you want it to appear.*

#### 3. Configuration (Optional)
You can open `add_watermark.py` with a text editor and adjust the scaling and margin ratios in the **Global Configuration Section** at the top:

*   `MARGIN_RATIO`: Controls the distance of the logo from the edge (based on the proportion of the image's longest side).
*   `LOGO_SCALE_RATIO`: Separately controls the relative size of the logos in the four corners (based on the proportion of the image's longest side).
*   `OUTPUT_FORMAT`: Choose the export format for the images, either `'jpg'` or `'png'` (defaults to `'jpg'`).

#### 4. Run the Script
Open your terminal or command prompt, navigate to the script's directory, and run:

```bash
python add_watermark.py
# If 'python' is not found, try using:
# python3 add_watermark.py
```

The processed images will be automatically saved in the `get_results_here/` folder, which will be created automatically if it doesn't exist.
