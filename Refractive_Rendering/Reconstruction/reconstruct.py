import os, argparse, glob
import numpy as np
import cv2
from scipy.misc import imread, imsave
from skimage.measure import compare_ssim
import psnr
import fastaniso
import utils as utils

parser = argparse.ArgumentParser()
parser.add_argument('--input_root', default='../Images')
parser.add_argument('--rgb_dir', default='RGBs')
parser.add_argument('--ref_dir', default='Refs')
parser.add_argument('--mask_dir', default='Masks')
parser.add_argument('--flow_dir', default='Flows')
parser.add_argument('--final_dir', default='Reconstructs')
parser.add_argument('--smoothing', default=False, action='store_true')
parser.add_argument('--cal_loss', default=False, action='store_true')
args = parser.parse_args()


def setupDirList():
    if args.input_root == '':
        raise Exception('Input root not defined')
    print('[Input root]: %s' % (args.input_root))
    print('[Dir list]: %s' % (args.dir_list))

    args.dir_list = os.path.join(args.input_root, args.dir_list)
    dir_list = utils.readList(args.dir_list)
    if args.max_images > 0:
        dir_list = dir_list[:args.max_images]
    return dir_list


def convertMask(mask):
    mask = np.sum(mask, axis=2)
    mask = 1 - (mask == 0)
    mask = mask.astype(float)
    mask = np.expand_dims(mask, 2).repeat(3, 2)

    return mask


def loadData(image_id):
    if type(image_id) != str:
        image_id = str(image_id)
    flow_name = os.path.join(args.input_root, args.flow_dir, image_id + '_flow.flo')
    in_name = os.path.join(args.input_root, args.rgb_dir, image_id + '.jpg')
    bg_name = os.path.join(args.input_root, args.ref_dir, image_id + '_ref.jpg')
    mask_name = os.path.join(args.input_root, args.mask_dir, image_id + '_mask.png')
    flow = utils.readFloFile(flow_name).astype(float)
    in_img = imread(in_name).astype(float)
    bg_img = imread(bg_name).astype(float)
    mask = imread(mask_name).astype(int)
    mask = convertMask(mask)

    final_prefix = os.path.join(args.input_root, args.final_dir, image_id)
    fcolor = utils.flowToColor(flow)
    imsave(final_prefix + '_fcolor.jpg', fcolor)
    h, w, c = in_img.shape

    return {'in': in_img, 'bg': bg_img, 'mask': mask, 'flow': flow,
            'fcolor': fcolor, 'h': h, 'w': w, 'name': final_prefix}


def renderFinalImg(ref, warped, mask):
    final = mask * warped + (1 - mask) * ref

    return final


def warpImage(ref, flow, grid_x, grid_y):
    h, w = grid_x.shape
    flow_x = np.clip(flow[:, :, 1] + grid_x, 0, w - 1)
    flow_y = np.clip(flow[:, :, 0] + grid_y, 0, h - 1)
    flow_x, flow_y = cv2.convertMaps(flow_x.astype(np.float32), flow_y.astype(np.float32), cv2.CV_32FC2)
    warped_img = cv2.remap(ref, flow_x, flow_y, cv2.INTER_LINEAR)
    return warped_img


def computeError(img1, img2):
    img_psnr = psnr.psnr(img1, img2)
    gt_y = cv2.cvtColor(cv2.cvtColor(img1.astype(np.uint8), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2YCR_CB)[:, :, 0]
    pred_y = cv2.cvtColor(cv2.cvtColor(img2.astype(np.uint8), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2YCR_CB)[:, :, 0]
    img_ssim = compare_ssim(gt_y, pred_y, gaussian_weight=True)
    return img_psnr, img_ssim


def smoothingMask(mask):
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    return mask


def smoothingFlow(flow):
    flow[:, :, 0] = fastaniso.anisodiff(flow[:, :, 0], niter=9)
    flow[:, :, 1] = fastaniso.anisodiff(flow[:, :, 1], niter=9)
    return flow


def smoothingRho(rho, mask):
    rho[mask < 0.2] = 1
    rho = cv2.GaussianBlur(rho, (5, 5), 0)
    return rho


def smoothingEstimation(data, grid_x, grid_y):
    smooth = {}
    smooth['mask'] = smoothingMask(data['mask'])
    smooth['flow'] = smoothingFlow(data['flow'])
    smooth['flow'][(smooth['mask'] < 0.2)[:, :, 0:2]] = 0
    smooth['fcolor'] = utils.flowToColor(smooth['flow'])
    smooth['warped'] = warpImage(data['bg'], smooth['flow'], grid_x, grid_y)
    smooth['final'] = renderFinalImg(data['bg'], smooth['warped'], smooth['mask'])

    results = {}
    out = ['mask', 'fcolor', 'final']
    for i, name in enumerate(out):
        key = '%s' % (name)
        if name in ['mask', 'rho']:
            results.update({key: smooth[name] * 255})
        else:
            results.update({key: smooth[name]})
    utils.saveResultsSeparate(data['name'] + "_smooth", results)


def reconstructImages(image_ids):
    print('Total number of images: %d' % len(image_ids))
    loss = {'psnr': 0, 'ssim': 0, 'psnr_bg': 0, 'ssim_bg': 0}
    for idx, image_id in enumerate(image_ids):
        data = loadData(image_id)
        h, w = data['h'], data['w']
        print('[%d/%d], size %dx%d' % (idx, len(image_ids), h, w))

        # Reconstructed Input Image with the estimated matte and background image
        grid_x = np.tile(np.linspace(0, w - 1, w), (h, 1)).astype(float)
        grid_y = np.tile(np.linspace(0, h - 1, h), (w, 1)).T.astype(float)
        data['warped'] = warpImage(data['bg'], data['flow'], grid_x, grid_y)
        data['final'] = renderFinalImg(data['bg'], data['warped'], data['mask'])
        imsave(data['name'] + '_final.jpg', data['final'])

        # Background Error
        if args.cal_loss:
            p, s = computeError(data['bg'], data['in'])
            print('\t BG psnr: %f, ssim: %f' % (p, s))
            loss['psnr_bg'] += p
            loss['ssim_bg'] += s

            # TOM-Net Error
            p, s = computeError(data['final'], data['in'])
            loss['psnr'] += p
            loss['ssim'] += s
            print('\t TOMNet psnr: %f, ssim: %f' % (p, s))

        # Smoothing Environment Matte
        if args.smoothing:
            smoothingEstimation(data, grid_x, grid_y)
    if args.cal_loss:
        print('******* Finish Testing Dir: %s' % args.input_root)
        with open(os.path.join(args.input_root, 'Log'), 'w') as f:
            f.write('Input_root: %s\n' % (args.input_root))
            for k in loss.keys():
                print('[%s]: %f' % (k, loss[k] / len(image_ids)))
                f.write('[%s]: %f\n' % (k, loss[k] / len(image_ids)))


if __name__ == '__main__':
    image_ids = utils.getImageIds(os.path.join(args.input_root, args.rgb_dir))
    utils.makeFile(os.path.join(args.input_root, args.final_dir))
    reconstructImages(image_ids)