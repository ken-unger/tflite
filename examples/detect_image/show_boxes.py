import cv2 as cv
import sys
if __name__ == '__main__':
   
   testimg = sys.argv[1]
   dets = sys.argv[2]  
   label = sys.argv[3]  
   saveimg = 'prediction.jpg'
   img = cv.imread(testimg)

   label_list=[]
   fp=open(label,'r')
   for line in fp:
       label_list.append(line.split('\n')[0])
   fp.close()

   fp=open(dets,'r')
   for line in fp:
       classes = int(line.split(',')[0])
       left = line.split(',')[1]
       right = line.split(',')[2]
       up = line.split(',')[3]
       bottom = line.split(',')[4]
       print('{},{},{},{},{}'.format(label_list[classes-1],left,right,up,bottom))
       cv.rectangle(img, (int(left), int(up)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
       cv.putText(img, '{}'.format(label_list[classes-1]),
                    (int(left), int(up) - 5),
                    cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)


   fp.close()
   cv.imwrite(saveimg, img)
   


