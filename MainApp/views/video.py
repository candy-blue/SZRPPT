import ffmpeg

# 输入和输出文件的路径
# 图片路径
input_image_path = r'D:\pythonProject save\SZRPPT\static\123.jpg'
# 原视频路径
input_video_path = r'D:\pythonProject save\SZRPPT\static\321.mp4'
# 视频人像部分的掩码视频路径
mask_video_path = r'D:\pythonProject save\SZRPPT\static\322.mp4'
# 输出路径
output_video_path = r'D:\pythonProject save\SZRPPT\static\999.mp4'
output_mask_path = r'D:\pythonProject save\SZRPPT\static\masked_output.mp4'
looped_mask_path = r'D:\pythonProject save\SZRPPT\static\looped_mask.mp4'
overlayed_background_path = r'D:\pythonProject save\SZRPPT\static\overlayed_background.mp4'


# 提取人像部分
ffmpeg.input(mask_video_path).output(output_mask_path, c='copy').run(overwrite_output=True)

# 将人像与背景图片叠加
ffmpeg.input(output_mask_path).filter('loop', loop=1, size=1).output(looped_mask_path).run(overwrite_output=True)
ffmpeg.input(input_image_path).input(looped_mask_path).filter('overlay').output(overlayed_background_path).run(overwrite_output=True)

# 合并原视频的其余部分
ffmpeg.input(input_video_path).input(overlayed_background_path).output(output_video_path, shortest=None).run(overwrite_output=True)
