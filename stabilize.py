import os
import shutil
import time
import pymiere
from pymiere import wrappers

import sys
import re

debug = False #this disables copying etc and restores the files to the original positions

# input_folder = "/Users/andrewke/Desktop/100D Test/to_stabilise"
# output_folder = "/Users/andrewke/Desktop/100D Test/stabilised"
# completed_folder="/Users/andrewke/Desktop/100D Test/completed"

#if no argument is used
input_folder = "/Volumes/Elements/test"

#if argument is used, set it as input folder
if len(sys.argv) == 2:
    input_folder = sys.argv[1]
    print("1st arguemnt", input_folder)


subfolders = ["Stabilised", "Original files"]
# subfolders = ["Original files"]

# Create subfolders
for subfolder in subfolders:
    subfolder_path = os.path.join(input_folder, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

output_folder = os.path.join(input_folder,"Stabilised")
completed_folder = os.path.join(input_folder,"Original files")

new_clip = "/Users/andrewke/Desktop/100D Test/M26-1041_2.8K_waist quite a bit of shake.mov"

preset = "/Users/andrewke/Documents/Adobe/Adobe Media Encoder/22.0/Presets/hevc10 80mbps.epr"

# to_stabilize = True
to_render = True
to_import = True
move_source_after_stabilize = True






print("running python script")

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
        # print(display_name)
        # print(property.getValue())
        
        if display_name == "Smoothness":
            property.setValue(smoothness, True)  # 1 means update gui

        #set to position, scale, rotation
        elif display_name == "Method":
            property.setValue(1, True)

        # elif display_name == "Advanced":
        #     isDetailedAnalysis=True #detailed analysis is the first option in the advanced menu. set isDetailedAnalysis to true, so on next loop, detailed analysis is turned on
        # elif isDetailedAnalysis:
        #     property.setValue(True, True)  # a bit too slow
        #     isDetailedAnalysis = False

    return




mov_files = []

for file in os.listdir(input_folder):
    if file.lower().endswith('.mov') or file.lower().endswith('.mp4'):
        file_path = os.path.join(input_folder, file)
        mov_files.append((file_path, os.path.splitext(file)[0]))
        file_extension = os.path.splitext(file)[1]


if len(mov_files) == 0:
    print("no files found, exiting")

for file_path, file_name in mov_files:
    print("-" * 30)
    print("File path:", file_path)
    print("File name:", file_name)

    # outputPath = "/Users/andrewke/Downloads/out.mp4"
    outputPath = output_folder + "/" + file_name+".mp4"

    
    # #move source files to different folder
    new_source_path = os.path.join(completed_folder, file_name+".mov")
    # shutil.move(file_path, new_source_path)

    


    # time.sleep(999)

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






    



    #import clip
    rootBin = project.rootItem
    if to_import: project.importFiles([file_path], True, rootBin, False)



    # #insert clip
    items = project.rootItem.findItemsMatchingMediaPath(file_path, ignoreSubclips=False)  
    clip1=items[0]
    # project.activeSequence.videoTracks[0].insertClip(items[0], 0)





    project.createNewSequenceFromClips(clip1.name, [clip1], rootBin);

    # Open Sequences in Premiere Pro if none are active
    if not sequence_active:
        sequences = wrappers.list_sequences()
        for seq in sequences:
            project.openSequence(sequenceID=seq.sequenceID)
        # Set the first Sequence in the list as the active Sequence
        project.activeSequence = sequences[0]

    sequence = project.activeSequence













    #read video metadata
    text = project.activeSequence.videoTracks[0].clips[0].projectItem.getProjectMetadata()
    # print(text)

    res_match = re.search(r'VideoInfo(.{4,12})', text)

    #find resolution from video metadata
    match = re.search(r'VideoInfo(.{4,12})', text)
    # print(match.group(1))
    video_width = int(res_match.group(1)[1:5])
    print(video_width)

    video_height = int(res_match.group(1)[8:12])
    print(video_height)

    clip_fps = float(re.search(r'MediaTimebase(.{4,7})', text).group(1)[1:])
    print(clip_fps)

    if clip_fps > 46:
        print("skipping stabilisation")
        pymiere.objects.app.project.saveAs("/Users/andrewke/Desktop/100D Test/Untitled 5.prproj")  

        pymiere.objects.app.project.closeDocument()


        

        outputPath = output_folder + "/" + file_name+file_extension
        shutil.copy(file_path, outputPath)


        if move_source_after_stabilize:
            new_source_path = os.path.join(completed_folder, file_name+file_extension)
            shutil.move(file_path, new_source_path)




        continue
    # else:
        # outputPath = output_folder + "/" + file_name+".mp4"



    # time.sleep(999)

    # if video_width == 2880:
    #     fps = 23.985
    #     fps_setting = 110
    # elif video_width == 4800:
    #     fps = 23.983
    #     fps_setting = 110

    #set 23.976 in prpro. plan to skip stabilisation if clip is 56fps



    def closest_frame_rate(clip_fps):
        target_fps = [23.976, 24, 29.97, 30]
        closest_fps = None
        min_difference = float('inf')

        for target in target_fps:
            difference = abs(clip_fps - target)
            if difference < min_difference:
                min_difference = difference
                closest_fps = target

        return closest_fps

    closest_fps = closest_frame_rate(clip_fps)
    print("closest_fps",closest_fps)

    #https://github.com/Adobe-CEP/Samples/blob/master/PProPanel/jsx/PPRO/Premiere.jsx
    TIMEDISPLAY_24Timecode = 100
    TIMEDISPLAY_25Timecode = 101
    TIMEDISPLAY_2997DropTimecode = 102
    TIMEDISPLAY_2997NonDropTimecode = 103
    TIMEDISPLAY_30Timecode = 104
    TIMEDISPLAY_50Timecode = 105
    TIMEDISPLAY_5994DropTimecode = 106
    TIMEDISPLAY_5994NonDropTimecode = 107
    TIMEDISPLAY_60Timecode = 108
    TIMEDISPLAY_Frames = 109
    TIMEDISPLAY_23976Timecode = 110
    TIMEDISPLAY_16mmFeetFrames = 111
    TIMEDISPLAY_35mmFeetFrames = 112
    TIMEDISPLAY_48Timecode = 113
    TIMEDISPLAY_AudioSamplesTimecode = 200
    TIMEDISPLAY_AudioMsTimecode = 201



    if closest_fps == 23.976:
        print("choosing fps preset")
        fps_preset = TIMEDISPLAY_23976Timecode
    elif closest_fps == 24:
        fps_preset = TIMEDISPLAY_24Timecode
    elif closest_fps == 29.97:
        fps_preset = TIMEDISPLAY_2997DropTimecode
    elif closest_fps == 30:
        fps_preset = TIMEDISPLAY_30Timecode


    print(fps_preset, type(fps_preset))



    #set sequence resolution
    oldSettings = sequence.getSettings()
    oldSettings.videoFrameHeight = video_height
    oldSettings.videoFrameWidth = video_width
    print(oldSettings.videoDisplayFormat)
    print(type(oldSettings.videoDisplayFormat))
    # oldSettings.videoDisplayFormat = fps_setting #doesnt work
    # oldSettings.videoDisplayFormat = fps_preset
    sequence.setSettings(oldSettings)


    app = pymiere.objects.app
    active_sequence = app.project.activeSequence

    active_sequence.projectItem.setOverrideFrameRate(30) #doesnt work



    # if active_sequence:
    #     current_seq_settings = active_sequence.getSettings()
    #     if current_seq_settings:
    #         # old_vid_setting = current_seq_settings.videoDisplayFormat
    #         # time_as_text = active_sequence.getPlayerPosition().getFormatted(current_seq_settings.videoFrameRate, active_sequence.videoDisplayFormat)

    #         # current_seq_settings.videoDisplayFormat = old_vid_setting + 1
    #         # if current_seq_settings.videoDisplayFormat > pymiere.constants.TIMEDISPLAY_48Timecode:
    #         current_seq_settings.videoDisplayFormat = fps_preset

    #         active_sequence.setSettings(current_seq_settings)
    #         # pymiere.PPP.updateEventPanel(f"Changed timecode display format for '{active_sequence.name}'.")






    # List all videos clips in the active Sequence
    clips = wrappers.list_video(project.activeSequence)

    # Convert timebase in ticks per second to Frame Per Second (FPS)
    fps = 1/(float(project.activeSequence.timebase)/wrappers.TICKS_PER_SECONDS)
    print("Sequence as a framerate of {} fps".format(fps))

    # Select the first video clip in the Timeline
    clips[0].setSelected(True, True)




    videoTrack = sequence.videoTracks[0]
    clip = videoTrack.clips[0]

    

    



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



    #add warp stabilizer. if video is too short, stabilisation might fail and script is stuck. TODO filter for short videos?
    qclip.addVideoEffect(pymiere.objects.qe.project.getVideoEffectByName("Warp Stabilizer"))
    smoothness = 2
    applyEffectProperties(getComponentByDisplayName(clip.components, effectName))

    

    while not sequence.isDoneAnalyzingForVideoEffects():
        time.sleep(1)  # Sleep for 1 second



    # time.sleep(99999)
    
    export_path = os.path.join(output_folder, file_name)+".mp4"  # path of the exported file

    if to_render:
        result = sequence.exportAsMediaDirect(
            export_path,
            preset,  # path of the export preset file
            pymiere.objects.app.encoder.ENCODE_ENTIRE  # what part of the sequence to export. Others are: ENCODE_IN_TO_OUT or ENCODE_WORKAREA
        )

    #avoid making changes to original prproj. closeDocument() saves the file by default
    pymiere.objects.app.project.saveAs("/Users/andrewke/Desktop/100D Test/Untitled 5.prproj")  

    pymiere.objects.app.project.closeDocument()

    # if debug:
    #     os.remove(export_path)
    #     shutil.move(new_source_path,file_path)

    # time.sleep(999999999)

    if move_source_after_stabilize:
        shutil.move(file_path, new_source_path)




sys.tracebacklimit = 0
