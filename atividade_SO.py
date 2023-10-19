import threading
import numpy as np
import cv2  # Biblioteca OpenCV para leitura de imagens

# Função para calcular as bordas na direção x
def calculate_Gx(image, Gx):
    M, N = len(image), len(image[0])
    for i in range(1, M - 2):
        for j in range(1, N - 2):
            Gx[i][j] = abs(image[i+1][j-1] + image[i+1][j] + image[i+1][j+1] - image[i-1][j-1] - image[i-1][j] - image[i-1][j+1])
            if G[i][j] < 0: G[i][j] = 0
            if G[i][j] > 255: G[i][j] = 255

# Função para calcular as bordas na direção y
def calculate_Gy(image, Gy):
    M, N = len(image), len(image[0])
    for i in range(1, M - 2):
        for j in range(1, N - 2):
            Gy[i][j] = abs(image[i-1][j+1] + image[i][j+1] + image[i+1][j+1] - image[i-1][j-1] - image[i][j-1] - image[i+1][j-1])
            if G[i][j] < 0: G[i][j] = 0
            if G[i][j] > 255: G[i][j] = 255

# Função para calcular a imagem de saída G
def calculate_G(image, G, Gx, Gy):
    M, N = len(image), len(image[0])
    for i in range(1, M-1):
        for j in range(1, N-1):
            G[i][j] = Gx[i][j] + Gy[i][j]
            if G[i][j] > 255: G[i][j] = 255

# Leitura da imagem em nível de cinza usando OpenCV
image = cv2.imread('coins.png', cv2.IMREAD_GRAYSCALE)

# Defina M e N com as dimensões da imagem
M, N = image.shape

# Crie as matrizes Gx, Gy e G para as imagens de bordas
Gx = np.zeros((M, N), dtype=np.uint8)
Gy = np.zeros((M, N), dtype=np.uint8)
G = np.zeros((M, N), dtype=np.uint8)

# Crie as threads para calcular Gx e Gy
thread_Gx = threading.Thread(target=calculate_Gx, args=(image, Gx))
thread_Gy = threading.Thread(target=calculate_Gy, args=(image, Gy))

# Inicie as threads
thread_Gx.start()
thread_Gy.start()

# Aguarde a conclusão das threads
thread_Gx.join()
thread_Gy.join()

# Calcule a imagem de saída G
calculate_G(image, G, Gx, Gy)

# Salve a imagem de saída G
cv2.imwrite('edge_image.png', G)

# Exiba a imagem de saída G
cv2.imshow('Edge Image', G)
cv2.waitKey(0)
cv2.destroyAllWindows()

