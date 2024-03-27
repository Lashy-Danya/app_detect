import tensorflow as tf
import cv2
import numpy as np


def non_max_suppression(detections, overlapThresh):
    if len(detections) == 0:
        return []
    
    boxes = np.array([[xmin, ymin, xmax, ymax, score]
                      for score, object_name, xmin, ymin, xmax, ymax in detections])
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
    sc = boxes[:,4]
    
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(sc)
    
    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        
        overlap = (w * h) / area[idxs[:last]]
        
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))
        
    return [detections[pick[i]] for i in range(len(pick))]


class TFLiteModel:
    def __init__(self, model_path) -> None:
        self.interpreter = tf.lite.Interpreter(model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __run_inference_for_single_image(self, image):
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()

        scores = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        boxes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[3]['index'])[0]

        return scores, boxes, classes
    
    def __run_inference_for_image_part(self, image, cutoff, class_name, ax0, ay0, ax1, ay1):
        detections = []
        im = image[ay0:ay1, ax0:ax1]

        im_resize = cv2.resize(im, (self.input_details[0]['shape'][2], self.input_details[0]['shape'][1]))
        im_resize = np.expand_dims(im_resize, axis=0)

        # Нормализация входных данных
        im_resize = np.float32(im_resize / 255)

        scores, boxes, classes = self.__run_inference_for_single_image(im_resize)

        h, w, _ = im.shape

        for i in range(len(scores)):
            if scores[i] > cutoff:
                ymin = int(boxes[i][0] * h)
                xmin = int(boxes[i][1] * w)
                ymax = int(boxes[i][2] * h)
                xmax = int(boxes[i][3] * w)

                object_id = int(classes[i])
                object_name = class_name.get(object_id, "Unknown")

                detections.append([scores[i], object_name, xmin + ax0, ymin + ay0, xmax + ax0, ymax + ay0])

        return detections


    def __run_inference_for_image_part_pcnt(self, image, cutoff, class_name, p_ax0=0, p_ay0=0, p_ax1=1, p_ay1=1):
        h, w, _ = image.shape
        max_x, max_y = w - 1, h - 1
        return self.__run_inference_for_image_part(image, cutoff, class_name,
                                            int(p_ax0 * max_x), int(p_ay0 * max_y),
                                            int(p_ax1 * max_x), int(p_ay1 * max_y))
    
    def __display_image_with_boxes(self, image, detections, p_x0=0, p_y0=0, p_x1=0, p_y1=0):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for score, name, xmin, ymin, xmax, ymax in detections:
            label = f"{name}: {score * 100:.2f}%"
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(ymin, label_size[1] + 10)
            cv2.rectangle(image,
                        (xmin, label_ymin - label_size[1] - 10),
                        (xmin + label_size[0], label_ymin + base_line - 10),
                        (255, 255, 255),
                        cv2.FILLED)
            cv2.putText(image, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        if p_x0 != 0 or p_y0 != 0 or p_x1 != 1 or p_y1 != 1:
            h, w, _ = image.shape
            max_x, max_y = w -1, h -1
            cv2.rectangle(image,
                        (int(p_x0 * max_x), int(p_y0 * max_y)),
                        (int(p_x1 * max_x), int(p_y1 * max_y)),
                        (0, 0, 255), 4)

        return image

    def do_sliding_window_inference(self, path_file, cutoff, class_name):
        image = cv2.imread(path_file)
        detections = self.__run_inference_for_image_part_pcnt(image, cutoff, class_name, 0, 0, 1, 1)

        if not detections:
            print("No detections found meeting the cutoff threshold.")
            return image

        boxes = [[xmin, ymin, xmax, ymax, score]
                 for score, object_name, xmin, ymin, xmax, ymax in detections]

        h, w, _ = image.shape

        a = np.array(boxes)
        mean_dx = int(np.mean(a[:,2] - a[:,0]))
        mean_dy = int(np.mean(a[:,3] - a[:,1]))

        step_x, step_y = mean_dx, mean_dy
        window_size = 4 * mean_dy
        detections = []
        y0 = 0
        while y0 < h - 1:
            x0 = 0
            while x0 < w - 1:
                x1, y1 = x0 + window_size, y0 + window_size
                detections += self.__run_inference_for_image_part(image, cutoff, class_name, x0, y0, x1, y1)
                x0 += step_y
            y0 += step_x
        
        detections = non_max_suppression(detections, 0.5)

        processed_image = self.__display_image_with_boxes(image, detections)

        return (processed_image, detections)
