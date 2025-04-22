import os
import matplotlib.pyplot as plt

print("1. Student grade")
print("2. Assignment statistics")
print("3. Assignment graph")
choice = input("Enter your selection: ")

student_names = []
student_ids = []

with open("data/students.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            sid = parts[-1]
            name = " ".join(parts[:-1])
            student_names.append(name)
            student_ids.append(sid)

assignment_names = []
assignment_ids = []
assignment_points = []

with open("data/assignments.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) == 3:
            assignment_names.append(parts[0])
            assignment_ids.append(parts[1])
            try:
                assignment_points.append(int(parts[2]))
            except ValueError:
                assignment_points.append(0)

all_submissions = []
submission_files = os.listdir("data/submissions")

for file in submission_files:
    with open(os.path.join("data/submissions", file), "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                try:
                    sid, aid, percent = parts
                    all_submissions.append((sid, aid, float(percent)))
                except ValueError:
                    continue

if choice == "1":
    name_input = input("What is the student's name: ")
    found = False
    student_index = -1

    for i in range(len(student_names)):
        if student_names[i].lower() == name_input.lower():
            found = True
            student_index = i
            break

    if not found:
        print("Student not found")
    else:
        sid = student_ids[student_index]
        total_earned = 0
        total_possible = 0

        for a in range(len(assignment_ids)):
            aid = assignment_ids[a]
            points = assignment_points[a]
            for sub in all_submissions:
                if sub[0] == sid and sub[1] == aid:
                    total_earned += (sub[2] / 100) * points
                    total_possible += points

        if total_possible > 0:
            grade = round((total_earned / total_possible) * 100)
            print(f"{grade}%")
        else:
            print("No submissions found")

elif choice == "2":
    assignment_input = input("What is the assignment name: ")
    found = False
    aid = ""
    for i in range(len(assignment_names)):
        if assignment_names[i].lower() == assignment_input.lower():
            found = True
            aid = assignment_ids[i]
            break

    if not found:
        print("Assignment not found")
    else:
        scores = []
        for sub in all_submissions:
            if sub[1] == aid:
                scores.append(sub[2])

        if len(scores) > 0:
            print("Min:", int(min(scores)), "%")
            print("Avg:", int(sum(scores) / len(scores)), "%")
            print("Max:", int(max(scores)), "%")
        else:
            print("No scores found")

elif choice == "3":
    assignment_input = input("What is the assignment name: ")
    found = False
    aid = ""
    for i in range(len(assignment_names)):
        if assignment_names[i].lower() == assignment_input.lower():
            found = True
            aid = assignment_ids[i]
            break

    if not found:
        print("Assignment not found")
    else:
        scores = []
        for sub in all_submissions:
            if sub[1] == aid:
                scores.append(sub[2])

        if len(scores) > 0:
            plt.hist(scores, bins=[0, 25, 50, 75, 100])
            plt.title("Scores for " + assignment_input)
            plt.xlabel("Score (%)")
            plt.ylabel("Number of Students")
            plt.show()
        else:
            print("No scores found")
