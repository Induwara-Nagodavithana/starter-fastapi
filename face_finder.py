import face_recognition

class FaceFinder:
    def __init__(self):
        # Load the jpg files into numpy arrays
        biden_image = face_recognition.load_image_file("E:/New Batch/Student Rec/face_rec_sever/src/biden.jpg")
        obama_image = face_recognition.load_image_file("E:/New Batch/Student Rec/face_rec_sever/src/obama.jpg")

        # Get the face encodings for each face in each image file
        # Since there could be more than one face in each image, it returns a list of encodings.
        # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
        try:
            biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
            obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()

        self.known_faces = [
            biden_face_encoding,
            obama_face_encoding
        ]

        self.known_faces_name = [
            "biden",
            "obama"
        ]

    def recognise_face(self, image):

        unknown_face_image = face_recognition.load_image_file(image)

        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_face_image)[0]
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            return False

        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        results = face_recognition.compare_faces(self.known_faces, unknown_face_encoding)
        for index, val in enumerate(results):
            if val:
                return self.known_faces_name[index]
            
        return False
    
    def save_face(self, image, name):

        unknown_face_image = face_recognition.load_image_file(image)

        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_face_image)[0]
            self.known_faces.append(unknown_face_encoding)
            self.known_faces_name.append(name)
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            return False
        return True
        


if __name__ == '__main__':
    reid = FaceFinder()