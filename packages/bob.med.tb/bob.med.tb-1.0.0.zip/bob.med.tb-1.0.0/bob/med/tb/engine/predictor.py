#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import csv
import shutil

import PIL
import numpy
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec

import torch
import torchvision.transforms.functional as VF
from torchvision import transforms

from ..utils.grad_cams import GradCAM

import logging

logger = logging.getLogger(__name__)

colors = [[(47, 79, 79), "Cardiomegaly"], 
            [(255, 0, 0), "Emphysema"], 
            [(0, 128, 0), "Pleural effusion"], 
            [(0, 0, 128), "Hernia"], 
            [(255, 84, 0), "Infiltration"],
            [(222, 184, 135), "Mass"],
            [(0, 255, 0), "Nodule"],
            [(0, 191, 255), "Atelectasis"],
            [(0, 0, 255), "Pneumothorax"],
            [(255, 0, 255), "Pleural thickening"],
            [(255, 255, 0), "Pneumonia"],
            [(126, 0, 255), "Fibrosis"],
            [(255, 20, 147), "Edema"],
            [(0, 255, 180), "Consolidation"]]

def run(model, data_loader, name, device, output_folder, grad_cams=False):
    """
    Runs inference on input data, outputs HDF5 files with predictions

    Parameters
    ---------
    model : :py:class:`torch.nn.Module`
        neural network model (e.g. pasa)

    data_loader : py:class:`torch.torch.utils.data.DataLoader`

    name : str
        the local name of this dataset (e.g. ``train``, or ``test``), to be
        used when saving measures files.

    device : str
        device to use ``cpu`` or ``cuda:0``

    output_folder : str
        folder where to store output prediction and model
        summary

    grad_cams : bool
        if we export grad cams for every prediction (must be used along
        a batch size of 1 with the DensenetRS model)

    Returns
    -------

    all_predictions : list
        All the predictions associated with filename and groundtruth

    """
    
    output_folder = os.path.join(output_folder, name)
    
    logger.info(f"Output folder: {output_folder}")
    os.makedirs(output_folder, exist_ok=True)

    logger.info(f"Device: {device}")

    logfile_name = os.path.join(output_folder, "predictions.csv")
    logfile_fields = (
        "filename",
        "likelihood",
        "ground_truth"
    )

    if os.path.exists(logfile_name):
        backup = logfile_name + "~"
        if os.path.exists(backup):
            os.unlink(backup)
        shutil.move(logfile_name, backup)

    if grad_cams:
        grad_folder = os.path.join(output_folder, "cams")
        logger.info(f"Grad cams folder: {grad_folder}")
        os.makedirs(grad_folder, exist_ok=True)

    with open(logfile_name, "a+", newline="") as logfile:
        logwriter = csv.DictWriter(logfile, fieldnames=logfile_fields)

        logwriter.writeheader()

        model.eval()  # set evaluation mode
        model.to(device)  # set/cast parameters to device

        # Setup timers
        start_total_time = time.time()
        times = []
        len_samples = []

        all_predictions = []

        for samples in tqdm(
            data_loader, desc="batches", leave=False, disable=None,
        ):

            names = samples[0]
            images = samples[1].to(
                device=device, non_blocking=torch.cuda.is_available()
            )
            
            # Gradcams generation
            allowed_models = ["DensenetRS"]
            if grad_cams and model.name in allowed_models:
                gcam = GradCAM(model=model)
                probs, ids = gcam.forward(images)

                # To store signs overlays
                cams_img = dict()

                # Top k number of radiological signs for which we generate cams
                topk = 1

                for i in range(topk):

                    # Keep only "positive" signs
                    if probs[:, [i]] > 0.5:

                        # Grad-CAM
                        b = ids[:, [i]]
                        gcam.backward(ids=ids[:, [i]])
                        regions = gcam.generate(target_layer="model_ft.features.denseblock4.denselayer16.conv2")
                        
                        for j in range(len(images)):
                            
                            current_cam = regions[j, 0].cpu().numpy()
                            current_cam[current_cam < 0.75] = 0.0
                            current_cam[current_cam >= 0.75] = 1.0
                            current_cam = PIL.Image.fromarray(numpy.uint8(current_cam * 255) , 'L')
                            cams_img[b.item()] = [current_cam, round(probs[:, [i]].item(), 2)]

                if len(cams_img) > 0:

                    # Convert original image tensor into PIL Image
                    original_image = transforms.ToPILImage(mode='RGB')(images[0])

                    for sign_id, label_prob in cams_img.items():

                        label = label_prob[0]

                        # Create the colored overlay for current sign
                        colored_sign = PIL.ImageOps.colorize(
                            label.convert("L"), (0, 0, 0), colors[sign_id][0]
                        )

                        # blend image and label together - first blend to get signs drawn with a
                        # slight "label_color" tone on top, then composite with original image, to
                        # avoid loosing brightness.
                        retval = PIL.Image.blend(original_image, colored_sign, 0.5)
                        composite_mask = PIL.ImageOps.invert(label.convert("L"))
                        original_image = PIL.Image.composite(original_image, retval, composite_mask)

                    handles = []
                    labels = []
                    for i, v in enumerate(colors):
                        # If sign present on image
                        if cams_img.get(i) is not None:
                            handles.append(Rectangle((0,0),1,1, color = tuple((v/255 for v in v[0]))))
                            labels.append(v[1] + " (" + str(cams_img[i][1]) + ")")

                    gs = GridSpec(6,1)
                    fig = plt.figure(figsize = (10,11))
                    ax1 = fig.add_subplot(gs[:-1,:]) # For the plot
                    ax2 = fig.add_subplot(gs[-1,:])   # For the legend

                    ax1.imshow(original_image)
                    ax1.axis('off')
                    ax2.legend(handles,labels, mode='expand', ncol=3, frameon=False)
                    ax2.axis('off')
                    
                    original_filename = samples[0][0].split('/')[-1].split('.')[0]
                    cam_filename = os.path.join(grad_folder, original_filename + "_cam.png")
                    fig.savefig(cam_filename)

            with torch.no_grad():

                start_time = time.perf_counter()
                outputs = model(images)
                probabilities = torch.sigmoid(outputs)
                
                # necessary check for HED architecture that uses several outputs
                # for loss calculation instead of just the last concatfuse block
                if isinstance(outputs, list):
                    outputs = outputs[-1]

                # predictions = sigmoid(outputs)

                batch_time = time.perf_counter() - start_time
                times.append(batch_time)
                len_samples.append(len(images))

                logdata = (
                    ("filename", f"{names[0]}"),
                    ("likelihood", f"{torch.flatten(probabilities).data.cpu().numpy()}"),
                    ("ground_truth", f"{torch.flatten(samples[2]).data.cpu().numpy()}"),
                )

                logwriter.writerow(dict(k for k in logdata))
                logfile.flush()
                tqdm.write(" | ".join([f"{k}: {v}" for (k, v) in logdata[:4]]))

                # Keep prediction for relevance analysis
                all_predictions.append([
                        names[0], 
                        torch.flatten(probabilities).data.cpu().numpy(),
                        torch.flatten(samples[2]).data.cpu().numpy()
                        ])

        # report operational summary
        total_time = datetime.timedelta(seconds=int(time.time() - start_total_time))
        logger.info(f"Total time: {total_time}")

        average_batch_time = numpy.mean(times)
        logger.info(f"Average batch time: {average_batch_time:g}s")

        average_image_time = numpy.sum(numpy.array(times) * len_samples) / float(
            sum(len_samples)
        )
        logger.info(f"Average image time: {average_image_time:g}s")

        return all_predictions