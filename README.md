# ocv_detector
RU:  
этот скрипт загружает все необходимые параметры из конфигурационного файла и осуществляет поиск объекта в кадре при помощи каскада  
и библиотеки OpenCV 3.1  
Параметры конфигурационного файла:  
секция [general]  
camera - числовое значение 0...9 номер устройства источника видео (вебкамера например)  
brightness - уровень яркости  
contrast - контраст  
saturation - насыщеность  
gain - усиление  
framew - ширина картинки после захвата например можно сжать из 640 на 320  
frameh - высота картинки после захвата например можно сжать из 480 на 240  
cascades - количество каскадов которые будут использоваться  
showwindow - показывать окно с выводом картинки  
  
секция [cascade#]  
enabled - параметр указывающий на то будет ли использоваться данный каскадв работе скрипта  
file - имя файла каскада (если файл находится не в папке скрипта следует указать путь)  
shapecheck - включать ли проверку по форме фигуры (например вы ищите круглый дорожный знак, будут сначала захвачены все круглые предметы 
и переданы напроверку каскаду)  
shape - фигура для проверки функции shapecheck (пока реализована только одна круг)  
color - цвет рамки найденого объекта (green white red orange black blue)  
depth - толщина рамки  
scale - параметр функции detectmultiscale() размер  
neighbors - параметр функции detectmultiscale() сколько соседей должен иметь объект  
minsize_w - минимальная ширина объекта при поиске  
minsize_h - минимальная высота объекта при поиске  
maxsize_w - максимальнаяширина объекта припоиске  
maxsize_h - максимальная высота объекта припоиске  
include - подключаемый файл скрипта python 
action - выполнить действие при обнаружении объекта (не реализовано. взамен автоматически выполняется функция run() из файла include)  
description - описаниекаскада  
  
для запускавыполните команду в папке с файлом detector.py  
#./detector.py  
  
  
EN:  
this script loads all the necessary parameters from the configuration file and searches for the object  
in the frame using the cascade and the OpenCV 3.1 library.  
  
Configuration file options:
section [general]
camera - numeric value 0...9 the device number of the video source (webcam for example)
brightness - brightness level
contrast - contrast level
saturation - saturation level
gain - gain level
framew - width of picture after capture for example can be compressed from 640 to 320
frame-the height of the image after capture for example can be compressed from 480 to 240
cascades - number of cascades to be used
showwindow - show window with image output

section [cascade#]  
enabled - this parameter indicates whether to use Cascad the script  
file - name of the cascade file (if the file is not in the script folder, specify the path)  
shapecheck - to include verification in the form of a figure (for example you are looking for round traffic sign, will be first captured all circular objects  
and passed on to the cascade)  
shape - the shape to check the function shapecheck (so far implemented only one round)  
color - frame color of the found object (green white red orange black blue)  
depth - frame thickness  
scale - parameter of the detectmultiscale () function size  
neighbors - parameter of the detectmultiscale () function how many neighbors the object should have  
minsize_w - minimum width of the object when searching   
minsize_h - minimum height of the object when searching  
maxsize_w - maksimalnaya object pribojska  
maxsize_h - maximum height of the annotation object  
include - python script plug-in file   
action - to perform an action upon detection of an object (not implemented. instead, the run() function from the include file is executed automatically)  
description - description of the cascade  

to run the command, run the command in the file folder detector.py  
#./detector.py  
