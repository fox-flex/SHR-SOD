from pathlib import Path
from tqdm.auto import tqdm
import cv2
import time
import matplotlib.pyplot as plt
import segmentation_refinement as refine
import torch
import numpy as np



def add_mask_transparency(image_, mask_):
    mask_vis_ = np.zeros_like(image_)
    mask_vis_[:,:] = (0, 255, 255)
    mask_vis_ = cv2.bitwise_and(mask_vis_, mask_vis_, mask=mask_)
    res = cv2.addWeighted(mask_vis_, 1, image_, 1, 0, None)
    return res


class Refiner:
    def __init__(self, device='cuda:0', fast=False, L=900):
        self.fast = fast
        self.L = L
        self.refiner = refine.Refiner(device=device)
    
    def refine(self, img, mask):
        mask = cv2.threshold(mask.copy(), 25, 255, cv2.THRESH_BINARY)[1]
        mask_ref = self.refiner.refine(img, mask, fast=self.fast, L=self.L)
        mask_ref = cv2.threshold(mask_ref, 1, 255, cv2.THRESH_BINARY)[1]
        return mask_ref


dir_data = Path('./DatasetDM/data_gen/sod_UHRSD_4')
dir_img = dir_data / 'image'
dir_mask = dir_data / 'mask'
dir_mask_th = dir_data / 'mask_th'
dir_mask_vis = dir_data / 'mask_vis'
dir_mask_ref = dir_data / 'mask_ref'
dir_mask_ref_vis = dir_data / 'mask_ref_vis'
dir_vis = dir_data / 'vis'

for dir_path in dir_mask_th, dir_mask_ref, dir_mask_vis, dir_mask_ref_vis, dir_vis:
    dir_path.mkdir(parents=True, exist_ok=True)

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
# refiner = refine.Refiner(device=device) # device can also be 'cpu'4
refiner = Refiner(device=device)


imgs = sorted(dir_img.glob('*'))
masks = sorted(dir_mask.glob('*'))
for path_img, path_mask in tqdm(zip(imgs, masks), total=len(imgs), desc='Refining masks'):
    name = path_mask.name
    img = cv2.imread(str(path_img))
    
    mask = cv2.imread(str(path_mask), cv2.IMREAD_GRAYSCALE)
    mask = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)[1]

    mask_ref = refiner.refine(img, mask)
    mask_ref = cv2.threshold(mask_ref, 1, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(str(dir_mask_ref / name), mask_ref)

    cv2.imwrite(str(dir_mask_th / name), mask)

    viss = []
    for mask, vis_dir in zip(
        (mask, mask_ref),
        (dir_mask_vis, dir_mask_ref_vis),
    ):
        vis = add_mask_transparency(img.copy(), mask)
        viss.append(vis)
        cv2.imwrite(str(vis_dir / name), vis)
    
    mask_vis = np.hstack([img] + viss)
    cv2.imwrite(str(dir_vis / name), mask_vis)
