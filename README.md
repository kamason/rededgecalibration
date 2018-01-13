# MicaSense RedEdge Imagery - Radiometric Calibration
This directory contains Python code for radiometrically calibrating MicaSense RedEdge Imagery. This code utilizes the Python tools from MicaSense for firmware versions later than 2.1.0, and also includes a script for processing images with earlier firmware. The images should first be converted to absolute radiance and then to reflectance using the Empirical Line Calibration method (i.e. ELC). The ELC method requires images of a calibration target before (and preferably also after) each flight. Calibration targets must take up more than 50 pixels in the image and should be relatively centered.

For more information on how to use this code, please email: kmaso270@gmail.com
