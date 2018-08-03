# Flight_Augmented_Data_Aircraft
Augments aircraft data such as type and alt over the image as it flies past

This is very experimental.

Requires Requests, Opencv2, imutils.

The Aircraft Haar Cascade can do with work. Lots of work. Its very sensitive so if anyone has one thats better please update it!

Run both files at the same time. One grabs data, the other overlays it onto the webcam image if it recognises a plane.

The information is taken as the most likely aircraft and as such may not be correct. This can be improved by change the search distance.

Given as is so have fun!
