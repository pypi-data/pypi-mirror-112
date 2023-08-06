# %% 导入包
import os
import shutil
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
import glob
import cv2
import os
import sys
# %% 分割训练和测试函数
def sperate_train_test(labels_filename,taskNameDir,dataset_dir, test_ratio):
    test_save = taskNameDir + '/test/'
    train_save = taskNameDir + '/train/'
    labels_save = taskNameDir + '/label.txt'
    reading = np.loadtxt(labels_filename, str, delimiter='\t')

    if not os.path.exists(test_save):
        os.makedirs(test_save)
    if not os.path.exists(train_save):
        os.makedirs(train_save)
    test_size = [0] * len(reading)
    train_size = [0] * len(reading)

    test_txt = open(taskNameDir + '/test.txt', 'w')  # 'a':write in the end
    train_txt = open(taskNameDir + '/train.txt', 'w')  # 'w':clear txt and write
    size = [0] * len(reading)
    for m in range(0, len(dataset_dir)):
        for k in range(0, len(reading)):
            folder = dataset_dir[m] + '/' + reading[k] + '/'
            if not os.path.exists(folder):
                continue
            # print folder
            ls_all = os.listdir(folder)
            #print("ls_all: ", ls_all)
            size[k] = len(ls_all)
            # print size[k]8
            l = np.arange(0, size[k])
            np.random.shuffle(l)
            # print l
            test_size[k] = int(test_ratio * size[k])  # define test data size, 20% of whole data
            train_size[k] = size[k] - test_size[k]
            print("label: ", os.path.join(test_save, reading[k]), "train_size:",
                  train_size[k]," test_size:",test_size[k])

            for j in range(0, test_size[k]):
                ind = l[j]
                path = folder + ls_all[ind]
                save_name = ls_all[ind]
                save_folder = os.path.join(test_save, reading[k])
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                shutil.copyfile(path, save_folder + '/' + save_name)
            for j in range(test_size[k], size[k]):
                ind = l[j]
                path = folder + ls_all[ind]
                save_name = ls_all[ind]
                save_folder = os.path.join(train_save, reading[k])
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                shutil.copyfile(path, save_folder + '/' + save_name)

    test_txt.close()
    print("Done!")


# %% 数据增强
def img_aug(src_base_folder, dst_base_folder,single_class_img_num):
    sometimes = lambda aug: iaa.Sometimes(0.5, aug)
    # Define our sequence of augmentation steps that will be applied to every image.
    seq = iaa.Sequential(
        [
            # Apply the following augmenters to most images.
            #
            # iaa.Fliplr(0.5), # horizontally flip 50% of all images
            # iaa.Flipud(0.2), # vertically flip 20% of all images

            # crop some of the images by 0-10% of their height/width
            sometimes(iaa.Crop(percent=(0, 0.1))),

            # Apply affine transformations to some of the images
            # - scale to 80-120% of image height/width (each axis independently)
            # - translate by -20 to +20 relative to height/width (per axis)
            # - rotate by -45 to +45 degrees
            # - shear by -16 to +16 degrees
            # - order: use nearest neighbour or bilinear interpolation (fast)
            # - mode: use any available mode to fill newly created pixels
            #         see API or scikit-image for which modes are available
            # - cval: if the mode is constant, then use a random brightness
            #         for the newly created pixels (e.g. sometimes black,
            #         sometimes white)
            sometimes(iaa.Affine(
                scale={"x": (0.95, 1.05), "y": (0.95, 1.05)},
                translate_percent={"x": (0, 0), "y": (0, 0)},
                rotate=(-3, 3),
                shear=(-16, 16),
                order=[0, 1],
                cval=(0, 0),
                mode='constant'
            )),

            #
            # Execute 0 to 5 of the following (less important) augmenters per
            # image. Don't execute all of them, as that would often be way too
            # strong.
            #
            iaa.SomeOf((0, 5),
                [
                    # Convert some images into their superpixel representation,
                    # sample between 20 and 200 superpixels per image, but do
                    # not replace all superpixels with their average, only
                    # some of them (p_replace).
                    # sometimes(
                    #     iaa.Superpixels(
                    #         p_replace=(0, 1.0),
                    #         n_segments=(20, 200)
                    #     )
                    # ),

                    # Blur each image with varying strength using
                    # gaussian blur (sigma between 0 and 3.0),
                    # average/uniform blur (kernel size between 2x2 and 7x7)
                    # median blur (kernel size between 3x3 and 11x11).
                    iaa.OneOf([
                        iaa.GaussianBlur((0, 1.0)),
                        iaa.AverageBlur(k=(2, 3)),
                        iaa.MedianBlur(k=(3, 5)),
                    ]),

                    # Sharpen each image, overlay the result with the original
                    # image using an alpha between 0 (no sharpening) and 1
                    # (full sharpening effect).
                    iaa.Sharpen(alpha=(0, 1.0), lightness=(0.92, 1.15)),

                    # Same as sharpen, but for an embossing effect.
                    # iaa.Emboss(alpha=(0, 1.0), strength=(0, 2.0)),

                    # Search in some images either for all edges or for
                    # directed edges. These edges are then marked in a black
                    # and white image and overlayed with the original image
                    # using an alpha of 0 to 0.7.
                    # sometimes(iaa.OneOf([
                    #     iaa.EdgeDetect(alpha=(0, 0.7)),
                    #     iaa.DirectedEdgeDetect(
                    #         alpha=(0, 0.7), direction=(0.0, 1.0)
                    #     ),
                    # ])),

                    # Add gaussian noise to some images.
                    # In 50% of these cases, the noise is randomly sampled per
                    # channel and pixel.
                    # In the other 50% of all cases it is sampled once per
                    # pixel (i.e. brightness change).
                    iaa.AdditiveGaussianNoise(
                        loc=0, scale=(0.0, 0.001*255), per_channel=0.5
                    ),

                    # Either drop randomly 1 to 10% of all pixels (i.e. set
                    # them to black) or drop them on an image with 2-5% percent
                    # of the original size, leading to large dropped
                    # rectangles.
                    # iaa.OneOf([
                    #     iaa.Dropout((0.01, 0.1), per_channel=0.5),
                    #     iaa.CoarseDropout(
                    #         (0.03, 0.15), size_percent=(0.02, 0.05),
                    #         per_channel=0.2
                    #     ),
                    # ]),

                    # Invert each image's channel with 5% probability.
                    # This sets each pixel value v to 255-v.
                    # iaa.Invert(0.05, per_channel=True), # invert color channels

                    # Add a value of -10 to 10 to each pixel.
                    iaa.Add((-2, 2), per_channel=0.5),

                    # Change brightness of images (50-150% of original value).
                    iaa.Multiply((0.95, 1.05), per_channel=0.5),

                    # Improve or worsen the contrast of images.
                    iaa.ContrastNormalization((0.9, 1.5), per_channel=0.5),

                    # Convert each image to grayscale and then overlay the
                    # result with the original with random alpha. I.e. remove
                    # colors with varying strengths.
                    # iaa.Grayscale(alpha=(0.0, 1.0)),

                    # In some images move pixels locally around (with random
                    # strengths).
                    # sometimes(
                    #     iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)
                    # ),

                    # In some images distort local areas with varying strength.
                    # sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05)))
                ],
                # do all of the above augmentations in random order
                random_order=True
            )
        ],
        # do all of the above augmentations in random order
        random_order=True
  )

    class_labels = os.listdir(src_base_folder)
    for class_label in class_labels:
        src_folder = os.path.join(src_base_folder,class_label)
        dst_folder = os.path.join(dst_base_folder,class_label)

        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        img_list = glob.glob(src_folder+'/*.jpg')
        img_list=[i.replace('\\','/') for i in img_list]
        images=[]
        for i in img_list:
            img=cv2.imread(i)
            height,width,channel=img.shape
            max_len = width
            if height > max_len:
                max_len = height
            img2 = np.zeros((max_len,max_len,3),np.uint8)
            rows_start = int((max_len - height)/2)
            rows_end = rows_start + height
            cols_start = int((max_len - width)/2)
            cols_end = cols_start + width
            img2[rows_start:rows_end,cols_start:cols_end] = img
            # cv2.imshow('img2',img2)
            # cv2.waitKey(10)
            # cv2.destroyAllWindows()



            images.append(img)#保持原图比例，不进行方形扩增
            # images.append(img2)#进行原图扩增

        # # 测试图片转换为方形
        # for i in range(len(images)):
        #     save_folder = dst_folder
        #     img_name=img_list[i][img_list[i].rindex('/')+1:img_list[i].rindex('.')]
        #     cv2.imwrite(save_folder+'/'+img_name+'.jpg',images[i])
        
        # 增强算法
        # single_class_img_num = 2000
        aug_num = int(single_class_img_num / len(images)) + 1
        if aug_num>500:
            aug_num=500
        count  = 0
        for num in range(aug_num):
            ia.seed(100000*(num+1))
            images_aug = seq.augment_images(images=images)
            for i in range(len(images_aug)):
                img_name=img_list[i][img_list[i].rindex('/')+1:img_list[i].rindex('.')]
                # folder = img_list[i][0:img_list[i].rindex('/')]
                # save_folder = dst_folder  + folder[folder.rindex('/')+1:]
                save_folder = dst_folder

                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                cv2.imwrite(save_folder+'/'+img_name+'_'+str(num)+'.jpg',images_aug[i])
                count+=1
                if num ==0:
                    cv2.imwrite(save_folder+'/'+img_name+'.jpg',images[i])
                    count+=1
                
                if count >= single_class_img_num:
                    break


    print("done img aug!")

# %% 生成CNN数据
def genaraterCNN(augPicDir,folder_base,labels_filename,cnn_dataset_dir, taskNameDir):
    folder_base=folder_base+'/'
    subfolder = [augPicDir]
    if augPicDir == 'train_aug':
        test_ratio = 0
    elif augPicDir == 'test_aug':
        test_ratio = 1
    else:
        print('Which type is your dataset? Please check the date type.')
        return
    s_folder = cnn_dataset_dir
    test_save = folder_base +s_folder + '/test_aug/'
    train_save = folder_base +s_folder + '/train_aug/'
    labels_save = folder_base+s_folder+'/label.txt'
    reading = np.loadtxt(labels_filename, str, delimiter='\t')

    if not os.path.exists(test_save):
        os.makedirs(test_save)
    if not os.path.exists(train_save):
        os.makedirs(train_save)

    shutil.copyfile(labels_filename,labels_save)



    test_size = [0]*len(reading)
    train_size = [0]*len(reading)
    if test_ratio != 0:
        test_txt = open(folder_base +s_folder+'/test.txt', 'w')#'a':write in the end
    if test_ratio !=1:
        train_txt = open(folder_base +s_folder+'/train.txt', 'w')#'w':clear txt and write
    size = [0]*len(reading)
    for m in range(0,len(subfolder)):
        for k in range(0,len(reading)):
            folder = folder_base + taskNameDir + '/' + subfolder[m] + '/' + reading[k] + '/'
        if not os.path.exists(folder):
            continue
        #print folder
        ls_all =  os.listdir(folder)
        size[k] = len(ls_all)
        #print size[k]
        l = np.arange(0, size[k])
        np.random.shuffle(l)
        # print l
        test_size[k] = int(test_ratio * size[k])    # define test data size, 20% of whole data
        train_size[k] = size[k] - test_size[k]

        print("label: ", os.path.join(test_save, reading[k]), "train_size:",
                    train_size[k]," test_size:",test_size[k])
        
        for j in range(0, test_size[k]):
            ind = l[j]
            path = folder + ls_all[ind]
            save_name = "aa"+'_' + reading[k]+'_'+ls_all[ind]
            save_folder = os.path.join(test_save, reading[k])
            shutil.copyfile(path,test_save +save_name)
            test_txt.writelines(save_name+' '+str(k)+'\n')
            # f.writelines(save_name+' '+reading[k]+'\n') # write image's name and label
        

        for j in range(test_size[k], size[k]):
            ind = l[j]
            path = folder + ls_all[ind]

            save_name = "aa"+'_' + reading[k]+'_'+ls_all[ind]
            save_folder = os.path.join(train_save, reading[k])
            shutil.copyfile(path,train_save +save_name)
            train_txt.writelines(save_name+' '+str(k)+'\n')


def caffe_pipeline(dataset_dir, cnn_dataset_dir = 'cnn_data',\
    taskNameDir = 'number_base',clean_tmp_dir=True,\
    aug_train_pictures=500,aug_test_pictures=None,test_ratio = 0.1):
    '''整理分类数据到当前目录下
    Args:
        dataset_dir: 包含
        cnn_dataset_dir: 生成的cnn数据结果
        aug_train_pictures: 增强后的待训练图片总量
        aug_test_pictures: 增强后的测试图片数量, 默认不增强
        test_ratio: 测试图片占比
    '''
    labelList = ['0','1','2','3','4','5','6','7','8','9']
    
    if not os.path.exists(taskNameDir):
        os.mkdir(taskNameDir)
    # 把label写入label.txt
    labels_filename = os.path.join(taskNameDir,"label.txt")
    #labels_filename = taskNameDir+"/label.txt"
    print('labels_filename: ',labels_filename)
    file_write_obj = open(labels_filename, 'w')
    for label in labelList:
        file_write_obj.writelines(label)
        file_write_obj.write('\n')
    file_write_obj.close()

    # %% 分割数据
    print('labels_filename: ',taskNameDir, '\ntaskNameDir: ',taskNameDir, '\ndataset_dir: ',dataset_dir)
    sperate_train_test(labels_filename,taskNameDir,[dataset_dir], test_ratio)
    img_aug(taskNameDir+'/train',taskNameDir+'/train_aug', aug_train_pictures)
    if aug_test_pictures:
        img_aug(taskNameDir+'/test',taskNameDir+'/test_aug', aug_test_pictures)
    genaraterCNN('train_aug',sys.path[0],labels_filename,cnn_dataset_dir, taskNameDir)
    genaraterCNN('test_aug',sys.path[0],labels_filename,cnn_dataset_dir, taskNameDir)
    if clean_tmp_dir:
        try:
            shutil.rmtree(taskNameDir)
        except OSError as e:
            print("Error: %s : %s" % (taskNameDir, e.strerror))


def rotation(img):
    # 获取输入图像的信息，生成旋转操作所需的参数（padding: 指定零填充的宽度； canter: 指定旋转的轴心坐标）
    h, w = img.shape[:2]
    padding = (w - h) // 2
    center = (w // 2, w // 2)

    # 在原图像两边做对称的零填充，使得图片由矩形变为方形
    img_padded = np.zeros(shape=(w, w, 3), dtype=np.uint8)
    img_padded[padding:padding+h, :, :] = img

    # cv2.imshow("", img_padded)
    # cv2.waitKey(1000)
    # cv2.imwrite("./img_padded.jpg", img_padded)

    # 逆时针-90°(即顺时针90°)旋转填充后的方形图片
    M = cv2.getRotationMatrix2D(center, -90, 1)
    rotated_padded = cv2.warpAffine(img_padded, M, (w, w))

    # cv2.imshow("", rotated_padded)
    # cv2.waitKey(1000)
    # cv2.imwrite("./rotated_padded.jpg", rotated_padded)

    # 从旋转后的图片中截取出我们需要的部分，作为最终的输出图像
    output = rotated_padded[:, padding:padding+h, :]
    return output


if __name__ == "__main__":
    
    print(os.getcwd())
    #os.chdir('../video')
    print(os.getcwd())
    folder = '/mnt/d/DataSet/CarPlate/carplate-detection/video/business'  # 'video/door-light-fy'
    save_folder = '/mnt/d/DataSet/CarPlate/carplate-detection/video/business/out/'  # "video/video-out/door-light-fy/"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    all_avis = os.listdir(folder)
    all_avis.sort()
    avis_size = len(all_avis)   

    c=1
    d=1
    for i in range(0,avis_size):
        print(all_avis[i])
        save_folder2 =save_folder+str(i+0)+'/'
        if not os.path.exists(save_folder2):
            os.makedirs(save_folder2)
        vc = cv2.VideoCapture(folder +'/'+ all_avis[i]) #读入视频文件 
        if vc.isOpened(): #判断是否正常打开 
            rval , frame = vc.read() 
        else: 
            rval = False
        timeF = 10 #视频帧计数间隔频率 
        while rval:  #循环读取视频帧 
            rval, frame = vc.read()
            # try:
            #     frame = rotation(frame)
            # except AttributeError:
            #     print("Error: 图片为空")
            #     continue
            # else:
            #     print("Rotation frame")
                #print(frame.shape[0])
            if(c%timeF == 0): #每隔timeF帧进行存储操作 
                # print("c= ",c)
                # rows = frame.shape[ls0] 
                # cols = frame.shape[1]
                # M=cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),270,1)
                # dst = cv2.warpAffine(frame,M,(cols,rows))
                #trans_img = cv2.transpose(frame)
                #dst = cv2.flip(trans_img,1)
                (file, ext) = os.path.splitext(all_avis[i])
                # cv2.imwrite(save_folder2 + file +' '+str(int(c/timeF)).zfill(5) + '.jpg',frame) #文件夹名+空格+时间戳
                cv2.imwrite(save_folder2 + str(d).zfill(7) + '.jpg',frame)  # 存储为图像 以数字为序
                #cv2.imwrite(save_folder2 + str(int(c/timeF)) + '.jpg',dst)  # 存储为图像  
                d = d + 1
            c = c + 1
            #cv2.waitKey(1) 
        vc.release() 
    print('Done!')

if __name__ == '__main__':
    dataset_dir = '/mnt/f/DataSet/Number/Number-base'
    caffe_pipeline(dataset_dir,aug_train_pictures=200,aug_test_pictures=10)