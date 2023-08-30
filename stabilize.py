"""
This demo show basic interactions with Premiere Pro using the Pymiere library.
It will display some info about the currently opened project in Premiere Pro and an action in the timeline.
Before running this script make sure that you have a Premiere project opened with at least a sequence.
"""


new_clip = "/Users/andrewke/Desktop/100D Test/M26-1041_2.8K_waist quite a bit of shake.mov"
#to run environment
# source /Users/andrewke/Documents/Pymiere/pymiere/bin/activate

# to_stabilize = True
to_render = True
to_import = True

import time
import pymiere
from pymiere import wrappers


import pymiere  
project_path = "/Users/andrewke/Desktop/100D Test/Untitled 4.prproj"
# create new empty project  
# pymiere.objects.app.newProject(project_path)  # from Premiere 2020  
# pymiere.objects.qe.newProject(project_path)  # before Premiere 2020  
# open existing project  
pymiere.objects.app.openDocument(project_path)  
# save project  
# pymiere.objects.app.project.save()  
# pymiere.objects.app.project.saveAs(project_path)  
# close project  



project = pymiere.objects.app.project


# sequence = project.createNewSequence("Sequence 01","0")




# Check for an open project
project_opened, sequence_active = wrappers.check_active_sequence(crash=False)
if not project_opened:
    raise ValueError("please open a project")


# Open Sequences in Premiere Pro if none are active
if not sequence_active:
    sequences = wrappers.list_sequences()
    for seq in sequences:
        project.openSequence(sequenceID=seq.sequenceID)
    # Set the first Sequence in the list as the active Sequence
    project.activeSequence = sequences[0]



sequence = project.activeSequence



import re



#import clip
rootBin = project.rootItem
if to_import: project.importFiles([new_clip], True, rootBin, False)




items = project.rootItem.findItemsMatchingMediaPath(new_clip, ignoreSubclips=False)  






#insert clip
project.activeSequence.videoTracks[0].insertClip(items[0], 0)

text = project.activeSequence.videoTracks[0].clips[0].projectItem.getProjectMetadata()
# info= text.child(0).child(0).child('premierePrivateProjectMetaData:Column.Intrinsic.VideoInfo')
# alert(info);

print(text)

match = re.search(r'VideoInfo(.{4,12})', text)

print(match.group(1))
video_width = int(match.group(1)[1:5])
print(video_width)

video_height = int(match.group(1)[8:12])
print(video_height)

# if video_width == 2880:
#     fps = 23.985
#     fps_setting = 110
# elif video_width == 4800:
#     fps = 23.983
#     fps_setting = 110

#set 23.976 in prpro. plan to skip stabilisation if clip is 56fps

oldSettings = sequence.getSettings()
oldSettings.videoFrameHeight = video_height
oldSettings.videoFrameWidth = video_width
# oldSettings.videoDisplayFormat = fps_setting #doesnt work
sequence.setSettings(oldSettings)



# dstTicks =  0

# clipToInsert = first_clip

# video_track.insertClip(clipToInsert, dstTicks)






# List all videos clips in the active Sequence
clips = wrappers.list_video(project.activeSequence)

# Convert timebase in ticks per second to Frame Per Second (FPS)
fps = 1/(float(project.activeSequence.timebase)/wrappers.TICKS_PER_SECONDS)
print("Sequence as a framerate of {} fps".format(fps))

# Select the first video clip in the Timeline
clips[0].setSelected(True, True)




videoTrack = sequence.videoTracks[0]
clip = videoTrack.clips[0]

# clip.addVideoEffect(qe.project.getVideoEffectByName("Warp Stabilizer"))#error

def getComponentByDisplayName(components, name):
    for component in components:
        if name == component.displayName:
            return component
    return None


def applyEffectProperties(component):
    if not component:
        print("not component")
        return
    
    print("adding warp stabilizer effect")
    isDetailedAnalysis=False
    
    for property in component.properties:
        display_name = property.displayName
        print(display_name)
        print(property.getValue())
        
        if display_name == "Smoothness":
            property.setValue(smoothness, True)  # 1 means update gui
        elif display_name == "Advanced":
            isDetailedAnalysis=True #detailed analysis is the first option in the advanced menu
        # elif isDetailedAnalysis:
        #     property.setValue(True, True)  # a bit too slow
        #     isDetailedAnalysis = False

    return



if not sequence_active:
    sequences = wrappers.list_sequences()
    for seq in sequences:
        project.openSequence(sequenceID=seq.sequenceID)
    # Set the first Sequence in the list as the active Sequence
    project.activeSequence = sequences[0]


effectName = "Warp Stabilizer"
qsequence = pymiere.objects.qe.project.getSequenceAt(0)
# qsequence = sequence
qclip = qsequence.getVideoTrackAt(0).getItemAt(0)



print("qclip",qclip)




qclip.addVideoEffect(pymiere.objects.qe.project.getVideoEffectByName("Warp Stabilizer"))
smoothness = 2
applyEffectProperties(getComponentByDisplayName(clip.components, effectName))



while not sequence.isDoneAnalyzingForVideoEffects():
    time.sleep(1)  # Sleep for 1 second



# time.sleep(99999)
outputPath = "/Users/andrewke/Downloads/out.mp4"


if to_render:
    result = sequence.exportAsMediaDirect(
        outputPath,  # path of the exported file
        "/Users/andrewke/Documents/Adobe/Adobe Media Encoder/22.0/Presets/hevc10.epr",  # path of the export preset file
        pymiere.objects.app.encoder.ENCODE_ENTIRE  # what part of the sequence to export. Others are: ENCODE_IN_TO_OUT or ENCODE_WORKAREA
    )

pymiere.objects.app.project.saveAs("/Users/andrewke/Desktop/100D Test/Untitled 5.prproj")  

pymiere.objects.app.project.closeDocument()