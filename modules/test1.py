"""
광원제거 + filter2d test

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('C:/SGM_AI/42Brick/img/creator/twn246.jpg', cv2.IMREAD_COLOR)
img_YUV = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)    
y = img_YUV[:,:,0]

rows = y.shape[0]    
cols = y.shape[1]

### illumination elements와 reflectance elements를 분리하기 위해 log를 취함
imgLog = np.log1p(np.array(y, dtype='float') / 255) # y값을 0~1사이로 조정한 뒤 log(x+1)
 
### frequency를 이미지로 나타내면 4분면에 대칭적으로 나타나므로 
### 4분면 중 하나에 이미지를 대응시키기 위해 row와 column을 2배씩 늘려줌
M = 2*rows + 1
N = 2*cols + 1
 
### gaussian mask 생성 sigma = 10
sigma = 10
(X, Y) = np.meshgrid(np.linspace(0, N-1, N), np.linspace(0, M-1, M)) # 0~N-1(and M-1) 까지 1단위로 space를 만듬
Xc = np.ceil(N/2) # 올림 연산
Yc = np.ceil(M/2)
gaussianNumerator = (X - Xc)**2 + (Y - Yc)**2 # 가우시안 분자 생성
 
### low pass filter와 high pass filter 생성
LPF = np.exp(-gaussianNumerator / (2*sigma*sigma))
HPF = 1 - LPF

LPF_shift = np.fft.ifftshift(LPF.copy())
HPF_shift = np.fft.ifftshift(HPF.copy())
img_FFT = np.fft.fft2(imgLog.copy(), (M, N))
img_LF = np.real(np.fft.ifft2(img_FFT.copy() * LPF_shift, (M, N)))
img_HF = np.real(np.fft.ifft2(img_FFT.copy() * HPF_shift, (M, N)))

### 각 LF, HF 성분에 scaling factor를 곱해주어 조명값과 반사값을 조절함
gamma1 = 1.5
gamma2 = 2.5
img_adjusting = gamma1*img_LF[0:rows, 0:cols] + gamma2*img_HF[0:rows, 0:cols]
 
### 조정된 데이터를 이제 exp 연산을 통해 이미지로 만들어줌
img_exp = np.expm1(img_adjusting) # exp(x) + 1
img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp)) # 0~1사이로 정규화
img_out = np.array(255*img_exp, dtype = 'uint8') # 255를 곱해서 intensity값을 만들어줌

img_YUV[:,:,0] = img_out

### 마지막으로 YUV에서 Y space를 filtering된 이미지로 교체해주고 RGB space로 converting
result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
val = 100
array = np.full(result.shape, (val, val, val), dtype=np.uint8)
res_img = cv2.add(result, array)


# 커널 생성(대상이 있는 픽셀을 강조)
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

# 커널 적용 
image_sharp = cv2.filter2D(res_img, -1, kernel)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_sharp = cv2.cvtColor(image_sharp, cv2.COLOR_BGR2RGB)




fig, ax = plt.subplots(1,2, figsize=(10,5))
ax[0].imshow(image, cmap='gray')
ax[0].set_title ('Original Image')
ax[1].imshow(image_sharp, cmap='gray')
ax[1].set_title('homomorphic filter + Sharp Image')
plt.show()