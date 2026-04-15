#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片水印/Logo添加脚本
根据 logos 文件夹内部的子文件夹自动识别 logo 位置并添加到图片对应角落，同时按比例添加边距及自适应缩放Logo，保留原图并保存到新文件夹
"""

import os
from PIL import Image, ImageOps

# 尝试导入 pillow_heif 来支持原生读取 HEIC 格式
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("警告: 未检测到 pillow-heif 库，如果需要处理苹果 HEIC 照片，请先运行: pip install pillow-heif")

# ================= 全局配置区 =================
# 边距比例：决定了 Logo 距离图片边缘的距离。
# 例如 0.03 表示距离边缘为原图较长边的 3%
MARGIN_RATIO = 0.04

# Logo 宽度占比：决定了计算出来的 Logo 在当前照片中的绝对缩放比例。
# 分别配置四个角的缩放比例，例如 0.20 表示宽度占据原图较长边的 20%。
LOGO_SCALE_RATIO = {
    'up_left_corner': 0.10,
    'up_right_corner': 0.20,
    'low_left_corner': 0.20,
    'low_right_corner': 0.20
}
# ==============================================

def add_watermark(original_image_path, logos_dict, output_path):
    """
    将相应的logo添加到原图指定角落
    
    参数:
        original_image_path: 原图路径
        logos_dict: 字典形式的logo路径，key为角落名称，value为logo路径
        output_path: 输出图片路径
    """
    # 打开原图
    original = Image.open(original_image_path)
    # 应用EXIF旋转信息，将图片在像素层面旋转到正确方向
    original = ImageOps.exif_transpose(original).convert('RGBA')
    
    # 获取原图尺寸
    orig_width, orig_height = original.size
    
    # 按照比例动态计算相对基准长度（取宽和高较长的一边，避免因为特别细长的原图导致logo发生诡异形变）
    base_length = max(orig_width, orig_height)
    
    # 计算实际边距像素（统一使用较长边作为基准）
    margin = int(base_length * MARGIN_RATIO)
    margin_x = margin
    margin_y = margin
    
    # 创建一个与原图大小相同的透明图层
    watermark_layer = Image.new('RGBA', (orig_width, orig_height), (0, 0, 0, 0))
    
    # 遍历需要添加的logo并贴到对应的位置
    for corner, logo_path in logos_dict.items():
        logo = Image.open(logo_path).convert('RGBA')
        
        # 获取当前角落的缩放比例，如果没有配置则默认使用 0.20
        current_scale_ratio = LOGO_SCALE_RATIO.get(corner, 0.20)
        
        # 让每个 Logo 的宽度占据当前基准长度的固定百分比
        target_logo_width = int(base_length * current_scale_ratio)
        # 依靠该目标宽度得到缩放比例系数，按此缩放高度以防止发生形变拉伸
        scale_ratio = target_logo_width / float(logo.size[0])
        target_logo_height = int(logo.size[1] * scale_ratio)
        
        # 如果缩放后的尺寸大于 0 才进行缩放，避免报错
        if target_logo_width > 0 and target_logo_height > 0:
            logo = logo.resize((target_logo_width, target_logo_height), Image.Resampling.LANCZOS)
        
        if corner == 'up_left_corner':
            x, y = margin_x, margin_y
        elif corner == 'up_right_corner':
            x, y = orig_width - target_logo_width - margin_x, margin_y
        elif corner == 'low_left_corner':
            x, y = margin_x, orig_height - target_logo_height - margin_y
        elif corner == 'low_right_corner':
            x, y = orig_width - target_logo_width - margin_x, orig_height - target_logo_height - margin_y
        else:
            continue
            
        watermark_layer.paste(logo, (x, y), logo)
    
    # 将水印图层合成到原图上
    result = Image.alpha_composite(original, watermark_layer)
    
    # 如果原图不是RGBA格式，需要转换回去
    if original.mode != 'RGBA':
        result = result.convert(original.mode)
    else:
        # 保持RGBA格式
        result = result
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 根据输出文件扩展名保存
    if output_path.lower().endswith('.png'):
        result.save(output_path, 'PNG')
    elif output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        # 如果原图是RGBA，转换为RGB
        if result.mode == 'RGBA':
            rgb_result = Image.new('RGB', result.size, (255, 255, 255))
            rgb_result.paste(result, mask=result.split()[3])  # 使用alpha通道作为mask
            rgb_result.save(output_path, 'JPEG', quality=95)
        else:
            result.save(output_path, 'JPEG', quality=95)
    else:
        result.save(output_path)


def main():
    # 定义路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, 'put_your_images_here')
    output_dir = os.path.join(script_dir, 'get_results_here')
    logos_dir = os.path.join(script_dir, 'logos')
    
    corner_dirs = [
        'up_left_corner', 'up_right_corner',
        'low_left_corner', 'low_right_corner'
    ]
    
    # 查找所有角对应的logo
    logos_dict = {}
    for corner in corner_dirs:
        corner_path = os.path.join(logos_dir, corner)
        if os.path.isdir(corner_path):
            # 找到该文件夹下第一个图片文件作为logo
            for f in os.listdir(corner_path):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    logos_dict[corner] = os.path.join(corner_path, f)
                    print(f"找到 [{corner}] 对应的 logo: {f}")
                    break
    
    if not logos_dict:
        print(f"错误：在 {logos_dir} 的各角落子文件夹中未找到任何 logo 文件。")
        return
    
    # 检查图片文件夹是否存在
    if not os.path.exists(image_dir):
        print(f"错误：找不到待处理的图片文件夹 {image_dir}")
        return
    
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图片格式 (加入了HEIF/HEIC)
    supported_formats = ('.png', '.jpg', '.jpeg', '.heic', '.heif')
    
    # 遍历图片文件夹中的所有图片
    processed_count = 0
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(supported_formats):
            original_path = os.path.join(image_dir, filename)
            
            # 如果原图是 HEIC/HEIF 格式，为了分享和各大平台的广泛兼容性，生成的图片强制保存为 JPG
            output_filename = filename
            if filename.lower().endswith(('.heic', '.heif')):
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}.jpg"
                
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                # 打开图片获取尺寸日志打印
                with Image.open(original_path) as img:
                    img_orientated = ImageOps.exif_transpose(img)
                    width, height = img_orientated.size
                
                print(f"正在处理: {filename} ({width}x{height})")
                add_watermark(original_path, logos_dict, output_path)
                processed_count += 1
                print(f"✓ 完成: {filename}")
            except Exception as e:
                print(f"✗ 处理 {filename} 时出错: {str(e)}")
    
    print(f"\n处理完成！共处理 {processed_count} 张图片")
    print(f"输出目录: {output_dir}")

if __name__ == '__main__':
    main()
