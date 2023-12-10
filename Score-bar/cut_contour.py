import cv2

image = cv2.imread('image_2.jpg')
original_image = image.copy()
# 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 阈值处理图像
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# 得到二值图像
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 设定边缘距离阈值,用于排除原图像边缘检测出来的边界
edge_threshold = 2
# 初始化最小边框信息，用于记录最终切割边框
min_x, min_y, max_w, max_h = float('inf'), float('inf'), 0, 0
# 找到不靠近图像边缘的所有轮廓的最小边框范围
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # 检查边框是否靠近图像边缘，如果是则跳过此边框
    if x > edge_threshold and y > edge_threshold and x + w < image.shape[1] - edge_threshold and y + h < image.shape[0] - edge_threshold:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_w = max(max_w, x + w)
        max_h = max(max_h, y + h)
# 确保坐标为整数
min_x, min_y, max_w, max_h = int(min_x), int(min_y), int(max_w), int(max_h)
# 检查裁剪后图像宽度是否满足条件
if max_w - min_x >= 1490:
    cropped_image = original_image[min_y - 5:max_h + 5, min_x:max_w]
else:
    left_distance = min_x  # 距离左边缘的距离
    right_distance = original_image.shape[1] - max_w  # 距离右边缘的距离
    if left_distance < right_distance:
        # 从左边开始裁剪
        cropped_image = original_image[min_y - 5:max_h + 5, min_x:min_x + 1493]
    else:
        # 从右边开始裁剪
        cropped_image = original_image[min_y - 5:max_h + 5, max_w - 1493:max_w]

#cv2.imwrite("cut_102.jpg", cropped_image)

# 显示最终裁剪的图像
cv2.imshow('Final Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
