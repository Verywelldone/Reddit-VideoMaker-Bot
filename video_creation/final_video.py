from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeAudioClip,
    CompositeVideoClip,
)
from utils.console import print_step
import re


W, H = 1080, 1920


def make_final_video(number_of_clips, unparsed_video):
    print_step("Creating the final video 🎥")
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)

    old_video_title = re.sub("[!@#$%^&*()[]{};:,.<>?\|`~-=_+]/", "", unparsed_video)
    video_title = ''.join(ch for ch in old_video_title if ch.isalnum())

    background_clip = (
        VideoFileClip("assets/mp4/clip.mp4")
        .without_audio()
        .resize(height=H)
        .crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    )
    # Gather all audio clips
    audio_clips = []
    for i in range(0, number_of_clips):
        audio_clips.append(AudioFileClip("assets/{}/mp3/{}.mp3".format(video_title,i)))
    audio_clips.insert(0, AudioFileClip("assets/{}/mp3/title.mp3".format(video_title)))
    audio_concat = concatenate_audioclips(audio_clips)
    audio_composite = CompositeAudioClip([audio_concat])

    # Gather all images
    image_clips = []
    for i in range(0, number_of_clips):
        imgsPath = "assets/{}/comment_{}.png".format(video_title,i)
        image_clips.append(
            ImageClip(imgsPath)
            .set_duration(audio_clips[i + 1].duration)
            .set_position("center")
            .resize(width=W - 100),
        )
    image_clips.insert(
        0,
        ImageClip("assets/{}/title.png".format(video_title))
        .set_duration(audio_clips[0].duration)
        .set_position("center")
        .resize(width=W - 100),
    )
    image_concat = concatenate_videoclips(image_clips).set_position(
        ("center", "center")
    )
    image_concat.audio = audio_composite
    final = CompositeVideoClip([background_clip, image_concat])
    finalFileName = "assets/{}/{}.mp4".format(video_title,video_title)
    final.write_videofile(
        finalFileName, fps=30, audio_codec="aac", audio_bitrate="192k"
    )

   

    for i in range(0, number_of_clips):
        pass
 

   