# bestof

## Installation and Running

The pip installation command is:

```py
pip install bestOf==0.0.51
```

To run bestOf, simply type: "bestOf" (without the quotes) and watch the magic.

## Summary

BestOf is an application designed to curate and cleanse large image libraries from events where several similar photos are often taken. Users simply upload all the relevant images, and BestOf returns an intuitive menu displaying their images organized into a grid layout. Each row of the grid represents a group, indicating that all images in a particular row are very similar in nature. The first image in each row is the recommended and default selected image, and at the end of the process, the user can download all selected images (having the option to select of the non-recommended ones if they so choose).

## How it Works

The process by which BestOf analyzes images has 3 major steps. First, it performs image similarity analysis by converting each image into a feature vector using a deep neural network. These feature vectors are used to compute cosine similarities and intelligently group images into sets. Second, it scores each image on default parameters. These parameters are attributes of the subjects in the image - namely whether they are blinking or cropped. An image is deemed better if a greater percentage of subjects are both not blinking and fully visible in the image. These attributes are identified via CNNs trained for these two tasks. The third step of the process is analyzing user-selected criteria. The user has the option to enable analysis of lighting, subject centering, sharpness, and resolution. They are also able to rank this criteria according to their preferences. BestOf creates a score that takes into account all enabled features, weighting them by the user defined rankings. This is combined with the default parameter score to give each image an official BestOf score that is then used to select the recommended image in each group.

## GitHub Repository

https://github.com/apangasa/bestof
