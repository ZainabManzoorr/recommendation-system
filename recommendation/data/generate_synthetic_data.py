
import numpy as np

def generate_measurements():
    data = []
    np.random.seed(42)

    def generate_row(body_type, gender):
        height = np.random.uniform(150, 175) if gender == 'Female' else np.random.uniform(160, 185)
        weight = np.random.uniform(50, 70) if gender == 'Female' else np.random.uniform(65, 85)

        if body_type == 'Hourglass':
            chest = np.random.uniform(85, 95)
            hips = chest + np.random.uniform(-2, 2)
            waist = np.random.uniform(60, 68)
            shoulder = chest + np.random.uniform(-1, 1)

        elif body_type == 'Pear':
            hips = np.random.uniform(95, 105)
            chest = hips - np.random.uniform(5, 10)
            waist = np.random.uniform(65, 72)
            shoulder = chest - np.random.uniform(0, 2)

        elif body_type == 'Apple':
            chest = np.random.uniform(95, 105)
            waist = np.random.uniform(80, 90)
            hips = chest - np.random.uniform(5, 8)
            shoulder = chest + np.random.uniform(0, 3)

        elif body_type == 'Rectangle':
            chest = np.random.uniform(80, 90)
            waist = chest - np.random.uniform(0, 3)
            hips = chest + np.random.uniform(-2, 2)
            shoulder = chest + np.random.uniform(-2, 2)

        elif body_type == 'Inverted Triangle':
            shoulder = np.random.uniform(100, 110)
            chest = shoulder - np.random.uniform(2, 5)
            hips = chest - np.random.uniform(5, 8)
            waist = hips - np.random.uniform(5, 8)

        sleeve = np.random.uniform(55, 60) if gender == 'Female' else np.random.uniform(58, 64)

        return {
            "gender": gender,
            "height": round(height, 2),
            "weight": round(weight, 2),
            "chest": round(chest, 2),
            "waist": round(waist, 2),
            "hips": round(hips, 2),
            "shoulder": round(shoulder, 2),
            "sleeve": round(sleeve, 2),
            "body_type": body_type
        }

    female_body_types = ['Hourglass', 'Pear', 'Apple', 'Rectangle']
    male_body_types = ['Apple', 'Rectangle', 'Inverted Triangle']

    for body_type in female_body_types:
        for _ in range(40):
            data.append(generate_row(body_type, 'Female'))

    for body_type in male_body_types:
        for _ in range(40):
            data.append(generate_row(body_type, 'Male'))

    return data
