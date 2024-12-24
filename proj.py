import cv2
import numpy as np

def grade_bubble_sheet(image_path, answer_key):
  
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,  
        param1=50,
        param2=30,    
        minRadius=15, 
        maxRadius=30  
    )
    
    score = 0  
    results = {}  
    
    if circles is not None:
        circles = np.uint16(np.around(circles[0, :])) 
        circles = sorted(circles, key=lambda c: (c[1], c[0]))

        rows = []
        row = [circles[0]]
        for i in range(1, len(circles)):
            if abs(circles[i][1] - row[-1][1]) < 20:  
                row.append(circles[i])
            else:
                rows.append(row)
                row = [circles[i]]
        rows.append(row)

        for question_number, row in enumerate(rows, start=1):
            row = sorted(row, key=lambda c: c[0])  
            selected_options = []

            for i, circle in enumerate(row):
                x, y, radius = circle
                bubble_roi = thresh[y-radius:y+radius, x-radius:x+radius]

                filled_ratio = cv2.countNonZero(bubble_roi) / (np.pi * radius**2)
                if filled_ratio > 0.6:  
                    selected_options.append(chr(65 + i))  

            results[question_number] = selected_options
            correct_answer = answer_key.get(question_number, None)
            print(f"Question {question_number}:")
            print(f"  Detected Bubbles: {selected_options}")
            print(f"  Correct Answer: {correct_answer}")

            if len(selected_options) > 1:
                print("  Grading: Multiple answers filled. -0.5 penalty.")
                score -= 0.5
            elif not selected_options:
                print("  Grading: No answer provided. -0.5 penalty.")
                score -= 0.5
            else:
                detected_answer = selected_options[0]
                if detected_answer == correct_answer:
                    print(f"  Grading: Correct! +1 point.")
                    score += 1
                else:
                    print(f"  Grading: Incorrect! -0.5 penalty.")
                    score -= 0.5

    for circle in circles:
        x, y, radius = circle
        bubble_roi = thresh[y-radius:y+radius, x-radius:x+radius]
        filled_ratio = cv2.countNonZero(bubble_roi) / (np.pi * radius**2)

        color = (0, 255, 0) if filled_ratio > 0.6 else (0, 0, 255) 
        cv2.circle(image, (x, y), radius, color, 2)

    cv2.imshow("Graded Bubble Sheet", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return score, results

image_path = "C:/Projects/cv/filled10mcq.png"

answer_key = {i: 'A' for i in range(1, 11)}  # all answers are 'A'

score, results = grade_bubble_sheet(image_path, answer_key)
print(f"Final Score: {score}")
print("Detailed Results:", results)
