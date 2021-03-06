import os
import string
import pytesseract

def dicttostr(dictionary):
    dictionary=str(dictionary)
    dictionary=dictionary.replace("[('", '')
    dictionary=dictionary.replace("',)]", '')
    return(dictionary)

def find(search, section, segment, jsonarg, what): #search = looking for; section=segment; jsonarg=json objected loaded; segment=greater segment
    # fobj = open('test2.json',) open json
    # test = json.load(fobj) set obj
    # name,tid =find('Brent', 'name', 'data', 'test', 'tid') [test[data[name[bren]]]]. returns 
  for dict in jsonarg[segment]:
    if dict[section] == search:
      name = dict['name']
     # print('Name', dict['name'])
     # print('Id', dict['tid'])
     # print('Attribue', dict['x'])
     # print('now the return values')
      return name, dict[what]
    else : continue

def clearwindow():
  clear= lambda:os.system('cls')
  clear()

#binarize images

def binarize(image_to_transform, threshold):
    output_image=image_to_transform.convert("L")
    for x in range(output_image.width):
        for y in range(output_image.height):
            if output_image.getpixel((x,y))< threshold:
                output_image.putpixel( (x,y), 0 )
            else:
                output_image.putpixel( (x,y), 255 )
    return output_image

#ocr comparison vs word file

def comparison(graphic):
  eng_dict=[]
  with open ("words_alpha.txt", "r") as f:
      data=f.read()
      eng_dict=data.split("\n")

  for i in range(150,170):
      # lets binarize and convert this to s tring values
      strng=pytesseract.image_to_string(binarize(graphic,i))
      # We want to remove non alphabetical characters, like ([%$]) from the text, here's
      # a short method to do that
      # first, lets convert our string to lower case only
      strng=strng.lower()
      import string
      comparison=''
      for character in strng:
          if character in string.ascii_lowercase:
              comparison=comparison+character
      # finally, lets search for comparison in the dictionary file
      if comparison in eng_dict:
          # and print it if we find it
          return(comparison)