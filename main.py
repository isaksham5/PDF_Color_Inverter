from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import PIL.ImageOps    
import img2pdf
import os
import time
from tkinter import filedialog
from pathlib import Path
import cv2
import keyboard
import numpy
import win32print
import win32ui
import win32api

os.system('set OPENCV_LOG_LEVEL=OFF')
ImgSelected=False
Collage_paths=[]
path_images=[]
path_inverted_image=[]
path_uninverted_image=[]
down_path=str(Path.home())+"\\Downloads\\"


PIL.Image.MAX_IMAGE_PIXELS = 5*1024 * 1024 * 1024 // 4 // 3
def printer(file_path):
    try:
        win32api.ShellExecute(0, "printto", file_path , None, ".", 0)
        print('Print Command sent to printer Successfully')
    except:
        print("Unable to Print, Check Printer Connection")
    
def Keyboard():
    c=keyboard.read_key()
    time.sleep(0.1)
    keyboard.send('backspace')
    time.sleep(1)
    return c
def newpage():
    page = numpy.zeros((3508,2480,3), numpy.uint8)
    page[:,:,0]=255
    page[:,:,1]=255
    page[:,:,2]=255
    w_initial=50
    return page,w_initial
def SnippetMaker(path,page):
    im=cv2.imread(path)
    image = cv2.resize(im, (1075, 586))
    roi=cv2.selectROI('Select Required Area',image)
    croppedim=image[int(roi[1]):int(roi[1]+roi[3]),
                    int(roi[0]):int(roi[0]+roi[2])]
    width=int((int(roi[3]))*2.2)
    length=int((int(roi[2]))*2.2)
    snippet=cv2.resize(croppedim, (length, width))
    return snippet, length, width

def SnippetPaster(fname, path, w_initial, page_no, page):
    snippet,Length,width = SnippetMaker(path,page)
    if 3500-(w_initial+width)<0:
        cv2.imwrite(down_path+'Inverted\\Collage_'+fname+f'_page{page_no}.jpg',page)
        Collage_paths.append(down_path+'Inverted\\Collage_'+fname+f'_page{page_no}.jpg')
        page,w_initial=newpage()
        page_no+=1
    else:
        pass
    page[w_initial:w_initial+width,50:50+Length]=snippet
    w_initial=w_initial+(50+width)
    return page_no, page, w_initial
def Question_Collage_Maker(fname,filepaths):
    
    page_no=1
    page,w_initial=newpage()
    c=1
    for path in filepaths:
        try:
            page_no, page, w_initial=SnippetPaster(fname, path, w_initial, page_no, page)
            print(f'Snippet Count={c}       \t\t\t.',end='\r')
            c+=1
        except Exception as e:
            pass
    else:
        print()
        cv2.destroyAllWindows()
        cv2.imwrite(down_path+'Inverted\\Collage_'+fname+f'_page{page_no}.jpg',page)
        Collage_paths.append(down_path+'Inverted\\Collage_'+fname+f'_page{page_no}.jpg')
        Collage_PDF_Path=down_path+'Inverted_PDF\\Ques_Collage_'+fname+'.pdf'
        with open(Collage_PDF_Path,"wb") as f:
            f.write(img2pdf.convert(Collage_paths))
        print(name, " - Question Collage PDF Saved Successfully\t\t\t.")
    return Collage_paths, Collage_PDF_Path
        
def PDF_Inverter(name,fullpath):
    print("Processing", name,end='\r')
    if not os.path.exists(down_path+"Inverted"):
        os.mkdir(down_path+"Inverted")
    if not os.path.exists(down_path+"UnInverted"):
        os.mkdir(down_path+"UnInverted")
    if not os.path.exists(down_path+"Inverted_PDF"):
        os.mkdir(down_path+"Inverted_PDF")
    try:    
        images = convert_from_path(fullpath)
    except ValueError:
        print("Specified File Does Not Exist, Please Try Again\t\t")
        exit()
    
    list_of_inverted_img_path=[]
    list_of_uninverted_img_path=[]

    if not c:
        for i in range(len(images)):
            uninverted_img_path=down_path+'UnInverted\\' + name \
                                 + ' page'+ "{:03d}".format(i+1) +'.jpg'
            images[i].save(uninverted_img_path, 'JPEG')
            a1 = cv2.imread(uninverted_img_path)
            a=cv2.bitwise_not(a1)
            inverted_img_path=down_path+'Inverted\\' + name \
                               + ' page'+ "{:03d}".format(i+1) +'.jpg'
            if p and q:
                invimg=SelectedImgInverter(uninverted_img_path)
                cv2.destroyAllWindows()
                cv2.imwrite(uninverted_img_path,invimg)
                a = cv2.bitwise_not(invimg)
                cv2.imwrite(inverted_img_path,a)
                list_of_inverted_img_path.append(inverted_img_path)

            elif p:
                invimg=SelectedImgInverter(uninverted_img_path)
                cv2.destroyAllWindows()
                cv2.imwrite(uninverted_img_path,invimg)
            elif q:
                cv2.imwrite(inverted_img_path,a)
                list_of_inverted_img_path.append(inverted_img_path)
            else:
                list_of_uninverted_img_path.append(uninverted_img_path)
            
    else:
        for i in range(len(images)):
            b = PIL.ImageOps.invert(images[i])
            #Enhancing Brightness
            enhancer = ImageEnhance.Brightness(b)
            b = enhancer.enhance(1.4)
            #Enhancing Contrast
            enhancer = ImageEnhance.Contrast(b)
            b = enhancer.enhance(1.3)
            #Saving uninverted image
            a = PIL.ImageOps.invert(b)
            uninverted_img_path=down_path+'UnInverted\\' + name \
                                 + ' page'+ "{:03d}".format(i+1) +'.jpg'
            a.save(uninverted_img_path, 'JPEG')
            inverted_img_path=down_path+'Inverted\\' + name + ' page'+ "{:03d}".format(i+1) +'.jpg'
            if p and q:
                invimg=SelectedImgInverter(uninverted_img_path)
                cv2.imwrite(uninverted_img_path,invimg)
                a = cv2.bitwise_not(invimg)
                cv2.imwrite(inverted_img_path,a)
                list_of_inverted_img_path.append(inverted_img_path)
            elif p:
                invimg=SelectedImgInverter(uninverted_img_path)
                cv2.imwrite(uninverted_img_path,invimg)
                list_of_uninverted_img_path.append(uninverted_img_path)

            elif q:
                a=cv2.imread(uninverted_img_path)
                invimg = cv2.bitwise_not(a)
                cv2.imwrite(inverted_img_path,invimg)
                list_of_inverted_img_path.append(inverted_img_path)

            else:
                list_of_uninverted_img_path.append(uninverted_img_path)
    
    path=down_path+"Inverted_PDF\\Inverted_" + name+'.pdf'
    with open(path,"wb") as f:
        if q:
            f.write(img2pdf.convert(list_of_inverted_img_path))
            print(name, " - Inverted PDF Saved Successfully\t\t\t.")
        else:
            f.write(img2pdf.convert(list_of_uninverted_img_path))
            print(name, " - PDF Saved Successfully\t\t\t.")
    return list_of_inverted_img_path, list_of_uninverted_img_path

def SelectedImgInverter(path):
    im=cv2.imread(path)
    image = cv2.resize(im, (1075, 586))

    try:
        roi=cv2.selectROI('Select Required Area',image)
        croppedim=image[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]
        a = cv2.bitwise_not(croppedim)
        image[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]=a
        image = cv2.resize(image, (3556, 2000))
        cv2.destroyAllWindows()
        return image
    except:
        return im


filepaths=filedialog.askopenfilenames(initialdir=\
                                     down_path[:-1], title="Select PDFs to Invert or Images to PDF",\
                                     filetypes=(("All Files","*.*"),("PDF Files","*.pdf"), ("PNG Files", "*.png"), ("JPEG Files","*.jpeg")\
                                                ,("JPG Files","*.jpg")))

    

for i in filepaths:
    path,name_ext=os.path.split(i)
    name,ext=os.path.splitext(name_ext)
    if ext==".pdf":
        print("Do you want to Invert the Entire PDF(y/n)",end='\r')
        b=Keyboard()
        time.sleep(1)
        q=False
        if b=='y':
            q=True
        print('Are Pagewise Edits Required(y/n)                                                        .',end='\r')
        a=Keyboard()
        time.sleep(0.1)
        keyboard.send('backspace')
        if a=='y':
            p=True
        else:
            p=False
        time.sleep(1)
        print('Do You Want To Enhance the PDF (y/n) :                                                        .', end='\r')
        n=Keyboard()
        time.sleep(0.1)
        keyboard.send('backspace')
        c=False
        if n=='y':
            c=True
        inv_img_path, uninv_img_path=PDF_Inverter(name,i)
        print('Do you want to make snippet collage(y/n)?                                                        .',end='\r')
        d=Keyboard()
        if d=='y':
            if q:
                Collage_Paths, Collage_PDF_Path=Question_Collage_Maker(name, inv_img_path)
            else:
                Collage_Paths, Collage_PDF_Path=Question_Collage_Maker(name, uninv_img_path)
            print("Snipper Collage Saved Successfully")
        time.sleep(1)

        print('Do you want to print snippet collage to default printer(y/n)?                                                        .',end='\r')
        p=Keyboard()

        if p=='y':
            print("Do you want to preview snippet collage(y/n)?                                                    .",end='\r')
            pr=Keyboard()
            if pr=='y':
                Page_No=1
                for path in Collage_Paths:
                    a=cv2.imread(path)
                    image = cv2.resize(a, (620, 877))
                    cv2.imshow(f'Page No.: {Page_No}',image)
                    cv2.waitKey(0)
                    Page_No+=1
                    cv2.destroyAllWindows()
                time.sleep(2)
                print('Press Enter to Start Printing                                                                       .',end='\r')
                n=Keyboard()
                time.sleep(0.1)
                if n=='enter':
                    printer(Collage_PDF_Path)
                    time.sleep(2)
                else:
                    print('Printing Cancelled')
                    keyboard.send('backspace')
            else:
                print('Press Enter to Start Printing                                                                       .',end='\r')
                n=Keyboard()
                time.sleep(0.1)
                if n=='enter':
                    printer(Collage_PDF_Path)
                    time.sleep(2)
                else:
                    print('Printing Cancelled',end='\r')
                    keyboard.send('backspace')
            time.sleep(1)
        else:
            pass
        print("Thankyou for Using the Program, Have a Nice Day                                             \t\t\t.")
    elif ext in [".png",".jpeg",".jpg"]:
        ImgSelected=True
        path_images.append(i)
    

if ImgSelected==True:
    name=input("Enter the Name of the PDF : ")
    if not os.path.exists(down_path+"Inverted_PDF"):
        os.mkdir(down_path+"Inverted_PDF")
    path_images.sort()
    path=down_path+"Inverted_PDF\\" + name+'.pdf'

    while True:
        choice=input("Do You Want To Invert It (y/n): ")
        print('Do You Want To Enhance the Images (y/n) \t\t\t: ',end='\r')
        c=Keyboard()
        if choice.lower()=="n":
            if c.lower()=='y':
                for i in range(len(path_images)):
                    a = Image.open(path_images[i])
                    #Enhancing Brightness
                    enhancer = ImageEnhance.Brightness(a)
                    a = enhancer.enhance(1.5)
                    #Enhancing Contrast
                    enhancer = ImageEnhance.Contrast(a)
                    a = enhancer.enhance(1.5)
                    uninverted_img_path=down_path+'UnInverted\\' + name + ' page'+ "{:03d}".format(i+1) +'.jpg'
                    #Saving UnInverted Image
                    a.save(uninverted_img_path, 'JPEG')
                    #Appending to the list for UnInverted Images
                    path_uninverted_image.append(uninverted_img_path)
                path_images=path_uninverted_image
                path=down_path+"Inverted_PDF\\UnInverted_" + name+'.pdf'
            with open(path,"wb") as f:
                f.write(img2pdf.convert(path_images))
            print(name,".pdf : PDF Saved Successfully! \nLocation : Download/Inverted_PDF\n\n")
            print('Do You Want To create Question Collage? (y/n) \t\t\t: ',end='\r')
            c=Keyboard()
            if c.lower()=="y":
                Question_Collage_Maker(name,path_uninverted_image)
            break
        elif choice.lower()=="y":
            for i in range(len(path_images)):
                img = Image.open(path_images[i])
                if c.lower()=='y':
                    #Enhancing Brightness
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.5)
                    #Enhancing Contrast
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.5)
                a = PIL.ImageOps.invert(img)
                inverted_img_path=down_path+'Inverted\\' + name + ' page'+ "{:03d}".format(i+1) +'.jpg'
                #Saving Inverted Image
                a.save(inverted_img_path, 'JPEG')
                #Appending to the list for Inverted Images
                path_inverted_image.append(inverted_img_path)
            path=down_path+"Inverted_PDF\\Inverted_" + name+'.pdf'
            with open(path,"wb") as f:
                f.write(img2pdf.convert(path_inverted_image))
            print("Inverted_"+name,".pdf : Saved Successfully! \t\t\t\nLocation : Download/Inverted_PDF",sep="")
            print('Do You Want To create Question Collage? (y/n) \t\t\t: ',end='\r')
            c=Keyboard()
            if c.lower()=="y":
                Question_Collage_Maker(name,path_inverted_image)

            break
        else:
            print("Wrong Input, Please Try Again")
time.sleep(2)

