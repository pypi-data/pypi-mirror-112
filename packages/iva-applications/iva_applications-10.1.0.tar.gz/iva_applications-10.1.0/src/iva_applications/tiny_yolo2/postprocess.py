"""Postprocessing utils for Tiny YOLO2."""
from typing import Dict
import numpy as np
from iva_applications.yolo2.postprocess import CLASS_NAMES, ANCHORS
from iva_applications.yolo2.postprocess import yolo_head, yolo_eval


def get_postprocessed_predictions(predictions: Dict[str, np.ndarray], image_shape: tuple,
                                  confidence_threshold: float = .5, iou_threshold: float = .5,
                                  fmap_size: int = 19) -> tuple:
    """Convert output convolution tensor to final scores, boxes, classes."""
    anchors = np.array(ANCHORS)
    predictions = predictions['conv2d_9/BiasAdd:0']
    yolo_outputs = yolo_head(predictions, anchors, fmap_size, len(CLASS_NAMES))

    out_scores, out_boxes, out_classes = yolo_eval(yolo_outputs, image_shape,
                                                   confidence_threshold=confidence_threshold,
                                                   iou_threshold=iou_threshold)
    return out_scores, out_boxes, out_classes
