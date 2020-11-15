# -*- coding: utf-8 -*-
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import sys
from random import *
from pathlib import Path
#import Image

def PositionTextes(PositionBuque):

    les_pos = []
    if PositionBuque == 0:
        y_en_cours = 0
    else :
        y_en_cours = 200
    for i in range(5):
        largeur=randint(10,250)
        
        if PositionBuque==0:
            hauteur=randint(0,100)
        else:
            hauteur=randint(280,890)
        les_pos.append((largeur,hauteur+y_en_cours))
        y_en_cours += 150
        
    return les_pos


les_buques = []
f = open("buques.csv", "r")
tbuques = f.readline()
buques = f.readlines()

buques_traitees = []
for buque_i in buques:
    
    buque_t = []
    fams = buque_i.split(';')[0]
    surbuque = buque_i.split(';')[1]
    buque_t.append(fams + '.jpg')
    #buque_t.append(surbuque)

    haut_bas = buque_i.split(';')[2]

    if haut_bas != '':
        haut_bas = int(haut_bas)
    else:
        haut_bas = 1
    
    if haut_bas == 1:
        
        buque_t.append(str(surbuque) + ' ' + fams)
        buque_t.append('')
    else :
        
        buque_t.append('')
        buque_t.append(str(surbuque) + ' ' + fams)

    texts = []
    

    positions_textes = PositionTextes(haut_bas)
    
    for i in range(3,8):
        
        texts_i = []
        
        text_rigolo_i = buque_i.split(';')[i].strip()
        texts_i.append(text_rigolo_i)

        
        
       
##        superpositionDetectee = True
##        while superpositionDetectee:
##            superpositionDetectee = False
##            Pos_temoraire = PositionTextes(haut_bas)
##            for yi in y_deja_pose:
##                if (Pos_temoraire[1] > yi-90) and (Pos_temoraire[1] < yi+90):
##                    superpositionDetectee = True
##                    #print('Ah, on refait')
##            
##        y_deja_pose.append(Pos_temoraire[1])     
##        
        texts_i.append(positions_textes[i-3])
        texts.append(texts_i)
        
    buque_t.append(texts)
    buques_traitees.append(buque_t)
    les_buques.append(fams + '.jpg')

def ChoixCouleur ():
    Couleurs=((227,40,40),(223,119,35),(233,218,35),(73,235,33),(29,226,237),(31,118,239),(247,21,213))
    CouleurChoisie=Couleurs[randint(0,len(Couleurs)-1)]
    cc = 90 #constraste_ constour
    CouleurContour=(max(0,CouleurChoisie[0]-cc),max(0,CouleurChoisie[1]-cc),max(0,CouleurChoisie[2]-cc))

    return [CouleurChoisie,CouleurContour]



def make_meme(topString, bottomString, filename, petits_textes):

    img = Image.open('source/'+filename)
    imageSize = img.size

    # find biggest font size that works
    fontSize = 200
    font = ImageFont.truetype("fonts/impact.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    
    while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
        fontSize = fontSize - 1
        font = ImageFont.truetype("fonts/impact.ttf", fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)


    #print (fontSize)
    
    # find top centered position for top text
    topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
    topTextPositionY = 45 - fontSize/3
    topTextPosition = (topTextPositionX, topTextPositionY)

    
    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1] + 30 - fontSize/2
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    draw = ImageDraw.Draw(img)

    print('On trace les contours de la surbuque')
    
    # draw outlines
    # there may be a better way
    outlineRange = int(fontSize/15)
    for x in range(-outlineRange, outlineRange+1):
            for y in range(-outlineRange, outlineRange+1):
                    draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
                    draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)
    print('On place le texte du haut et du bas')
    
    draw.text(topTextPosition, topString, (255,255,255), font=font)
    draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

    fontSize = 80
    police_petits_textes = 'fonts/clunsois.ttf'
    font_petit = ImageFont.truetype(police_petits_textes, 80)
    #On place les texts rigolos
    couleurs_choisis = []
    for text_rigolo in petits_textes:
        
        print(text_rigolo)

        longeur_phrase = len(text_rigolo[0])

        if longeur_phrase < 10:
            fontSize = 130
            font_petit = ImageFont.truetype(police_petits_textes, 130)
        elif longeur_phrase < 15:
            fontSize = 110
            font_petit = ImageFont.truetype(police_petits_textes, 110)
        elif longeur_phrase < 20:
            fontSize = 90
            font_petit = ImageFont.truetype(police_petits_textes, 90)
        elif longeur_phrase < 30:
            fontSize = 70
            font_petit = ImageFont.truetype(police_petits_textes, 70)
        elif longeur_phrase < 35:
            fontSize = 50
            font_petit = ImageFont.truetype(police_petits_textes, 50)
        else:
            fontSize = 40
            font_petit = ImageFont.truetype(police_petits_textes, 40)

        
        TextPosition = text_rigolo[1]
        String = text_rigolo[0]
        color = ChoixCouleur()
        while color[0] in couleurs_choisis:
            print('couleur deja utilisee')
            color = ChoixCouleur()
    
        couleurs_choisis.append(color[0])
        
        #print(color)

        outlineRange = int(fontSize/15)
        for x in range(-outlineRange, outlineRange+1):
            for y in range(-outlineRange, outlineRange+1):
                    draw.text((TextPosition[0]+x, TextPosition[1]+y), String, color[1], font=font_petit)
                         
        draw.text(TextPosition, String, color[0] , font=font_petit)
    
    img.save('output/' + filename)


photos_manquantes = []
for i in range(len(buques_traitees)):
    my_file = Path("source/" + str(buques_traitees[i][0]))
    if my_file.is_file():
        output_file = Path("output/" + str(buques_traitees[i][0]))
        if output_file.is_file():
            print('Fichier ignoré. La sortie existe déjà : ' + str(output_file))
        else:
            print(str(my_file) + ' existe. Création du meme') # file exists
            make_meme(buques_traitees[i][1],buques_traitees[i][2],buques_traitees[i][0],buques_traitees[i][3])
    else:
        print(str(my_file) + ' n\'existe pas. Il faut trouver la photo')
        photos_manquantes.append(str(my_file))




    
