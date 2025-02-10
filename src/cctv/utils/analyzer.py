from abc import ABC, abstractmethod

import cv2
import numpy as np
from joblib import load


class AbstractImageAnalazer(ABC):
    @abstractmethod
    def analyse_image(self, image: cv2.typing.MatLike) -> bool: ...


class SimpleImageAnalazer(AbstractImageAnalazer):
    clf = load("./cctv/utils/models/simple_analyzer_v1.joblib")

    @classmethod
    def analyse_image(cls, image: cv2.typing.MatLike) -> bool:
        res = [func(image) for func in cls._funcs]
        return cls.clf.predict([res])

    @staticmethod
    def _calculate_laplacian_variance(image):
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Compute the Laplacian (second derivative)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)

        # Variance of the Laplacian gives a measure of sharpness
        variance = laplacian.var()

        return variance

    @staticmethod
    def _detect_edges(image):
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Use Canny Edge Detection
        edges = cv2.Canny(blurred_image, 50, 150)

        # Count the number of edges
        edge_count = np.sum(edges > 0)

        return edge_count

    @staticmethod
    def _analyze_color_histogram(image):
        # Convert image to HSV color space for better light and saturation analysis
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Compute the histogram for the saturation channel (index 1)
        hist = cv2.calcHist([hsv_image], [1], None, [256], [0, 256])

        # Normalize the histogram
        hist = hist / hist.sum()

        # Calculate the standard deviation (how spread out the colors are)
        saturation_variance = np.var(hist)

        return saturation_variance

    @staticmethod
    def _detect_noise(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean, stddev = cv2.meanStdDev(gray)
        return stddev[0][0]

    @staticmethod
    def _detect_compression_artifacts(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dct = cv2.dct(np.float32(gray))

        # Analyze the DCT coefficients, e.g., check mean value
        mean_dct = np.mean(dct)
        return mean_dct

    _funcs = [
        _detect_edges,
        _calculate_laplacian_variance,
        _analyze_color_histogram,
        _detect_noise,
        _detect_compression_artifacts,
    ]
