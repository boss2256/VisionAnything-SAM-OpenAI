# VisionAnything-SAM-OpenAI

![VisionAnything-SAM-OpenAI](https://miro.medium.com/v2/resize:fit:640/format:webp/0*oY5iH4bwb4JhZ2N_.png)

A real-time image segmentation application using the Segment Anything Model (SAM) and deep learning to assist in children's cognitive development by identifying everyday objects.

## Description

VisionAnything-SAM-OpenAI is designed to provide a new learning experience for children during the beginning of cognitive training and development. This application uses the Segment Anything Model (SAM) and deep learning techniques to identify and segment everyday objects in real-time, aiding in children's cognitive development.

## Features

- **Real-time Image Segmentation**: Utilizes the Segment Anything Model (SAM) for accurate image segmentation.
- **Child-Friendly Interface**: Designed to be intuitive and easy to use for children.
- **Mobile-Friendly**: Compatible with both Android and iOS devices.
- **Audio and Visual Feedback**: Announces identified objects both visually and audibly to aid visually impaired users.
- **Scalable**: Can be extended to include more categories of objects in the future.

## Requirements

To run this application, you need to set an environment variable `API_KEY` with your own OpenAI API key.

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/boss2256/VisionAnything-SAM-OpenAI.git
    cd VisionAnything-SAM-OpenAI
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set the environment variable for the API key:
    ```bash
    export API_KEY='your_openai_api_key'  # On Windows use `set API_KEY=your_openai_api_key`
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. **Login**: Users can register and login to the application.
2. **Upload or Capture Image**: Users can upload images or capture photos using their mobile device.
3. **Image Segmentation**: The application will segment the image and provide a confidence score for the detected objects.

## Web Application

Access the application [here](https://visionanything-f611522951e1.herokuapp.com/).

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0). See the [LICENSE](LICENSE) file for details.
