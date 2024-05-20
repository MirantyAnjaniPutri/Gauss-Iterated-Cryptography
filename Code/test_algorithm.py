import numpy as np
import cv2
import time
import math
from skimage.metrics import peak_signal_noise_ratio as psnr

class TestAlgorithm:
    # Uji UACI
    def uaci(image1,image2):
        pixel1=image1.load()
        pixel2=image2.load()
        width,height=image1.size
        value=0.0
        for y in range(0,height):
            for x in range(0,width):
                value=(abs(pixel1[x,y][0]-pixel2[x,y][0])/255)+value

        value=(value/(width*height))*100
        return value

    # Uji NPCR
    def rateofchange(height,width,pixel1,pixel2,matrix,i):
        for y in range(0,height):
            for x in range(0,width):
                #print(x,y)
                if pixel1[x,y][i] == pixel2[x,y][i]:
                    matrix[x,y]=0
                else:
                    matrix[x,y]=1
        return matrix

    def sumofpixel(height,width,pixel1,pixel2,ematrix,i):
        matrix=TestAlgorithm.rateofchange(height,width,pixel1,pixel2,ematrix,i)
        psum=0
        for y in range(0,height):
            for x in range(0,width):
                psum=matrix[x,y]+psum
        return psum

    def npcrv(image1, image2):
        width, height = image1.size
        pixel1 = image1.load()
        pixel2 = image2.load()
        ematrix = np.empty([width, height])
        per = (
            (
                (TestAlgorithm.sumofpixel(height, width, pixel1, pixel2, ematrix, 0) / (height * width)) * 100
            ) + (
                (TestAlgorithm.sumofpixel(height, width, pixel1, pixel2, ematrix, 1) / (height * width)) * 100
            ) + (
                (TestAlgorithm.sumofpixel(height, width, pixel1, pixel2, ematrix, 2) / (height * width)) * 100
            )
        ) / 3
        return per


    def psnr(image1, image2):
        # Convert images to numpy arrays
        img1 = np.array(image1)
        img2 = np.array(image2)

        # Calculate MSE (Mean Squared Error)
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return float('inf')  # PSNR is infinite if there is no noise (mse is 0)

        # Calculate RMSE (Root Mean Squared Error)
        rmse = math.sqrt(mse)
        if rmse <= 0:
            raise ValueError("RMSE should be positive to calculate PSNR")

        # Calculate PSNR
        psnr_value = 20 * math.log10(255.0 / rmse)
        return psnr_value