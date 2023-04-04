import cv2

# 读取图片
img = cv2.imread('./output/007.png')

# 裁剪左半边图片
left_img = img[:, :img.shape[1]//2]

# 保留右半边图片并保留原始颜色通道
right_img = img[:, img.shape[1]//2:]

# 保存图片
cv2.imwrite('left_half.png', left_img)
cv2.imwrite('right_half.png', right_img)
