import os
import shutil


class SplitTrainingTestingValidation:

    def do_split(self, training_percentage=0.8, testing_percentage=0.1, image_and_txt_directory=None,
                 image_and_txt_result_directory=None):
        if training_percentage is None or training_percentage > 1 or training_percentage < 0 or testing_percentage is None or testing_percentage > 1 or testing_percentage < 0 or (
                testing_percentage + training_percentage) > 1:
            raise Exception("training_percentage or testing_percentage is illegal.")
        if image_and_txt_directory is None or image_and_txt_result_directory is None:
            raise Exception("image_and_txt_directory and image_and_txt_result_directory must be exist.")
        if not os.path.exists(image_and_txt_directory):
            raise Exception("image_and_txt_directory is not exist.")
        """
        training_percentage = 0.8
        testing_percentage = 0.15
        validating_percentage = 1 - training_percentage - testing_percentage
        image_and_txt_directory = r'/home/wwl/mypython/myworkspace/vialearning/mwds'
        image_and_txt_result_directory = r'/home/wwl/mypython/myworkspace/vialearning/mwdsresult1'
        """

        xml_files = os.listdir(image_and_txt_directory)
        xml_files_list = list()
        for xml_name in xml_files:
            print(xml_name)
            if str(xml_name).find(".txt") < 0:
                continue
            xml_files_list.append(xml_name)
        all_number = xml_files_list.__len__()
        training_number = int(training_percentage * all_number)
        testing_number = int(testing_percentage * all_number)
        validation_number = all_number - training_number - testing_number
        print(training_number)
        print(testing_number)
        print(validation_number)
        list1 = xml_files_list[0:training_number]
        list2 = xml_files_list[training_number:testing_number + training_number]
        list3 = xml_files_list[testing_number + training_number:]
        print(list1.__len__())
        print(list2.__len__())
        print(list3.__len__())
        dir1 = "images"
        dir2 = "labels"
        dir3 = "train"
        dir4 = "test"
        dir5 = "val"
        d1 = os.path.join(image_and_txt_result_directory, dir1, dir3)
        d2 = os.path.join(image_and_txt_result_directory, dir1, dir4)
        d3 = os.path.join(image_and_txt_result_directory, dir1, dir5)
        d4 = os.path.join(image_and_txt_result_directory, dir2, dir3)
        d5 = os.path.join(image_and_txt_result_directory, dir2, dir4)
        d6 = os.path.join(image_and_txt_result_directory, dir2, dir5)
        for d in [d1, d2, d3, d4, d5, d6]:
            if not os.path.exists(d):
                os.makedirs(d)
        for temp in list1:
            img_name = temp.replace(".txt", ".jpg")
            txt_name = temp.replace(".txt", ".txt")

            srcImage = os.path.join(image_and_txt_directory, img_name)
            srcTxt = os.path.join(image_and_txt_directory, txt_name)

            dstImage = os.path.join(d1, img_name)
            dstTxt = os.path.join(d4, txt_name)
            shutil.copy(srcImage, dstImage)
            shutil.copy(srcTxt, dstTxt)
        for temp in list2:
            img_name = temp.replace(".txt", ".jpg")
            txt_name = temp.replace(".txt", ".txt")

            srcImage = os.path.join(image_and_txt_directory, img_name)
            srcTxt = os.path.join(image_and_txt_directory, txt_name)

            dstImage = os.path.join(d2, img_name)
            dstTxt = os.path.join(d5, txt_name)
            shutil.copy(srcImage, dstImage)
            shutil.copy(srcTxt, dstTxt)
        for temp in list3:
            img_name = temp.replace(".txt", ".jpg")
            txt_name = temp.replace(".txt", ".txt")

            srcImage = os.path.join(image_and_txt_directory, img_name)
            srcTxt = os.path.join(image_and_txt_directory, txt_name)

            dstImage = os.path.join(d3, img_name)
            dstTxt = os.path.join(d6, txt_name)
            shutil.copy(srcImage, dstImage)
            shutil.copy(srcTxt, dstTxt)


if __name__ == '__main__':
    splitTrainingTestingValidation = SplitTrainingTestingValidation()
    splitTrainingTestingValidation.do_split(image_and_txt_directory='/home/wwl/mypython/myworkspace/vialearning/mwds',
                                            image_and_txt_result_directory='/home/wwl/mypython/myworkspace/vialearning/mwdsresult1')
