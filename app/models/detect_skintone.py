import cv2
import numpy as np
import mediapipe as mp
from sklearn.cluster import KMeans

mp_face_mesh = mp.solutions.face_mesh

# Sample landmarks for cheeks and forehead
SAMPLE_POINTS = [
    234, 93, 132,   
    454, 323, 361,  
    10, 338, 297    
]

def classify_skin_tone(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        return {"status": "error", "message": "image-not-found"}

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_rgb)
        if not results.multi_face_landmarks:
            return {"status": "error", "message": "no-face-detected"}

        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = image.shape
        skin_pixels = []

        patch_size = 5  

        for idx in SAMPLE_POINTS:
            lm = face_landmarks.landmark[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            for dx in range(-patch_size, patch_size + 1):
                for dy in range(-patch_size, patch_size + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        skin_pixels.append(image[ny, nx])

        if not skin_pixels:
            return {"status": "error", "message": "no-skin-pixels"}

        # KMeans to find dominant skin color
        kmeans = KMeans(n_clusters=1, n_init=10)
        kmeans.fit(np.array(skin_pixels))
        dominant_color = kmeans.cluster_centers_[0].astype(int)
        b, g, r = dominant_color.tolist()  
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

        return {
            "status": "success",
            "skin_tone": {
                "skin_tone": label_skin_tone((r, g, b)),
                "rgb": [r, g, b],
                "hex": hex_color
            }
        }

def label_skin_tone(rgb_color):
    r, g, b = rgb_color
    brightness = (r + g + b) / 3

    if brightness > 200:
        return "fair"
    elif brightness > 170:
        return "light"
    elif brightness > 140:
        return "medium"
    elif brightness > 110:
        return "olive"
    elif brightness > 80:
        return "brown"
    else:
        return "dark"
