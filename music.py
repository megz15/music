import PySimpleGUI as sg
sg.theme('DarkBlack1')

if sg.popup('Select a mode:',custom_text=('Create','Read'),no_titlebar=True,grab_anywhere=True)=='Read':
    taal,tempo = '',0
    notes,sharp_flat,octave = [],[],[]
    music_path = sg.popup_get_file('Choose your music file:',title='Select file',file_types=(('Music Text Files','.mus'),))

    music_file = open(music_path)
    for i in music_file:
        if i[0]=='#':
            continue
        elif i[:4]=='INFO':
            taal = i[10:i.rfind('\t')].title()
            tempo = i[i.index('Tempo=')+6:]
        elif i[:10]=='Sharp_Flat':
            sharp_flat = i[11:i.rfind(',')+2].split(',')
        elif i[:6]=='Octave':
            octave = i[7:i.rfind(',')+2].split(',')
        elif i[:5]=='Notes':
            notes = i[6:].split(',')

    #===DEFINE_TAALS===#
    if taal=='Teentaal':
        za,zb = 16,[4,8,12,16]
    elif taal=='Dadra':
        za,zb = 6,[3,6]
    elif taal=='Ektaal':
        za,zb = 12,[2,4,6,8,10,12]
    elif taal=='Rupak':
        za,zb = 7,[3,5,7]

    label_notes = {}
    count=0
    for i in range(len(notes)):
        a = notes[i]
        if int(octave[i])==0:
            pass
        elif int(octave[i])==1:
            a+='\u0307'
        elif int(octave[i])==-1:
            a+='\u0323'
        if i!=0 and (i)%za==0:
            count+=1
        for j in range(len(zb)):
            if i in (zb[j]+za*0,zb[j]+za*1,zb[j]+za*2,zb[j]+za*3,zb[j]+za*4,zb[j]+za*5,zb[j]+za*6):
                try:
                    label_notes[count].append(sg.VerticalSeparator())
                except KeyError:
                    pass
        try:
            if sharp_flat[i]=='n':
                label_notes[count].append(sg.Text(a,font='Cousine'))
            elif sharp_flat[i]=='`':
                label_notes[count].append(sg.Text(a,text_color='lime green',font='Cousine'))
            elif sharp_flat[i]=='_':
                label_notes[count].append(sg.Text(a,text_color='dark orange',font='Cousine'))
        except KeyError:
            label_notes[count] = []
            label_notes[count].append(sg.Text(a,font='Cousine'))
        
    layout = [[sg.Text('Taal: '+taal+'\tTempo: '+str(tempo))]]
    layout.extend(list(label_notes.values()))
    window_r = sg.Window(music_path.rstrip('.mus')[music_path.rfind('/')+1:].title(),layout)
    while True:
        event,values = window_r.read()
        if event == sg.WIN_CLOSED:
            break
    window_r.close()
else:
    taal = sg.popup_get_text('Enter a taal: ',title='Set Taal').title()
    rows = int(sg.popup_get_text('Enter number of rows: ',title='Rows'))
    tempo = int(sg.popup_get_text('Enter a tempo: ',title='Set Tempo'))
    f_name = sg.popup_get_text('Enter file name: ',title='Set File Name')
    
    #===DEFINE_TAALS===#
    if taal=='Teentaal':
        za,zb = 16,[4,8,12,16]
    elif taal=='Dadra':
        za,zb = 6,[3,6]
    elif taal=='Ektaal':
        za,zb = 12,[2,4,6,8,10,12]
    elif taal=='Rupak':
        za,zb = 7,[3,5,7]
    
    input_notes = {}
    count=0
    for i in range(rows):
        for i in range(za):
            for j in range(len(zb)):
                if i in (zb[j]+za*0,zb[j]+za*1,zb[j]+za*2,zb[j]+za*3,zb[j]+za*4,zb[j]+za*5,zb[j]+za*6):
                    input_notes[count].append(sg.VerticalSeparator())
            try:
                input_notes[count].append(sg.InputText(size=(4,1)))
            except KeyError:
                input_notes[count]=[]
                input_notes[count].append(sg.InputText(size=(4,1)))
        count+=1
    col = list(input_notes.values())
    
    layout = [[sg.Text('Taal: '+taal+'\tTempo: '+str(tempo))],
              [sg.Text()],[sg.Column(col)],
              [sg.Text()],[sg.Button('Save File'),sg.Button('Exit')]]
    
    window_c = sg.Window(f_name,layout)
    while True:
        event,values = window_c.read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        if event=='Save File':
            octave,sharp_flat,notes = [],[],[]
            for i in list(values.values()):
                
                a=i
                if i.find('+')!=-1:
                    octave.append(i[i.find('+'):])
                    a = i[:i.find('+')]
                elif i.find('-')!=-1:
                    octave.append(i[i.find('-'):])
                    a = i[:i.find('-')]
                else:
                    octave.append('0')
                
                if i.find("'")!=-1:
                    sharp_flat.append('`')
                    a = i[:i.find("'")]
                elif i.find(',')!=-1:
                    sharp_flat.append('_')
                    a = i[:i.find(',')]
                else:
                    sharp_flat.append('n')
                notes.append(a)
                sharp_flat.append(',')
                octave.append(',')
                notes.append(',')
            del octave[-1],sharp_flat[-1],notes[-1]

            f_c = open(f_name+'.mus','w')
            f_c.writelines(['#'+f_name+'\nINFO'+'\t'+'Taal='+str(taal)+'\t'+'Tempo='+str(tempo)+'\nSharp_Flat='])
            f_c.writelines(sharp_flat)
            f_c.writelines('\nOctave=')
            f_c.writelines(octave)
            f_c.writelines('\nNotes=')
            f_c.writelines(notes)
            f_c.close()
    window_c.close()