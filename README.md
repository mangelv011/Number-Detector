
# Number-Detector


Number-Detector is a computer vision project for real-time detection and recognition of numbers from images and video streams, using color segmentation and template matching. It also features an interactive password mechanism based on detected digits.


## How It Works

- **Camera Streaming:** Uses Picamera2 to stream video, display FPS, and show detected numbers.
- **Image Segmentation:** Segments green regions in images to isolate numbers using HSV color space and morphological operations.
- **Number Extraction:** Finds contours in segmented images, crops the region containing the number, and resizes it for template matching.
- **Template Matching:** Compares the cropped image against digit templates (`images/cropped_images/0.png` to `9.png`) to identify the detected number.
- **Password Mechanism:** Users interactively build a 4-digit password from detected numbers. The password can be checked, reset, or modified via console commands:
    - Press `d` to save the current detected digit to the password.
    - Press `r` to delete the last digit from the password.
    - Press `c` to check if the entered password matches the correct password.
    - If correct, you can reset the password interactively.


## Main Scripts & Project Structure

- `src/main.py`: Main application logic, camera stream, password interaction.
- `src/number_detector.py` & `intermediate_images.py`: Image processing, segmentation, contour detection, template matching.
- `src/calibrate.py`: Camera calibration functions.
- `images/`: Templates, raw, cropped, and test images.

## Usage

1. **Prepare Images:** Place digit templates in `images/cropped_images/` and test images in `images/test_images/`.
2. **Run the Main Script:**
   ```powershell
   python src/main.py
   ```
3. **Interact:** Use the console to save detections, delete digits, or check the password.
4. Place your images in the appropriate folders under `images/`. Use the provided scripts in `src/` to calibrate, process, and detect numbers in your images.

## Example Workflow

- The camera captures an image.
- The green region is segmented and cropped.
- The cropped image is matched against digit templates.
- The detected digit is displayed and can be added to a password.
- Users interact with the console to build and verify a password using detected digits.

## Contributors

- Miguel Angel Vallejo ([GitHub](https://github.com/mangelv011))
- Guzmán Perez ([GitHub](https://github.com/Guso12345678))

## License

This project is licensed under the MIT License.




