import cv2
import os
import mediapipe as mp
from pathlib import Path

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def analyze_pose(image_path):
    """
    Analyzes the pose in the given image and returns key points and instructions.
    """
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return "No pose detected."

    # Extract key points
    landmarks = results.pose_landmarks.landmark

    # Example: Identify hand and leg positions
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_leg = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_leg = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

    # Generate instructions (example logic)
    instructions = []
    if left_hand.y < right_hand.y:
        instructions.append("Raise your left hand higher than your right hand.")
    else:
        instructions.append("Raise your right hand higher than your left hand.")

    if left_leg.y < right_leg.y:
        instructions.append("Step forward with your left leg.")
    else:
        instructions.append("Step forward with your right leg.")

    return " ".join(instructions)

def analyze_folder(folder_path):
    """
    Analyzes all images in a folder and generates instructions for each dance move.
    """
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    instructions = {}

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        instructions[image_file] = analyze_pose(image_path)

    return instructions

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing dance move pictures: ").strip()

    if not os.path.exists(folder_path):
        print("The specified folder does not exist.")
    else:
        results = analyze_folder(folder_path)
        
        # Save or print the results
        output_path = Path(folder_path) / "dance_instructions.txt"
        with open(output_path, "w") as f:
            for image_name, instruction in results.items():
                f.write(f"{image_name}: {instruction}\n")

        print(f"Instructions have been saved to {output_path}")
