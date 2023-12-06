import os
import subprocess
import json

class Semi2:
    # EXERCISE 1:
    def generate_macroblocks_video(input_path, output_path):
        # Run FFMpeg command to generate video with macroblocks and motion vectors
        base_name, ext = os.path.splitext(os.path.basename(input_path))
        command = f"ffmpeg -hide_banner -flags2 +export_mvs -i {input_path} -vf codecview=mv=pf+bf+bb -an {output_path}"
        subprocess.run(command, shell=True, check=True)

    # EXERCISE 2:
    def create_new_bbb_container(input_path, output_cut, output_mono, output_stereo, output_aac, output_final):

        #Cut BBB into 50 seconds only video.
        os.system(f'ffmpeg -i {input_path} -t 50 -c:v copy -c:a copy {output_cut}')

        #Export BBB(50s) audio as MP3 mono track.
        os.system(f'ffmpeg -i {output_cut} -vn -ac 1 -ab 128k {output_mono}')

        #Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        os.system(f'ffmpeg -i {output_cut} -vn -q:a 5 {output_stereo}')

        #Export BBB(50s) audio in AAC codec
        os.system(f'ffmpeg -i {output_cut} -vn -c:a aac {output_aac}')

        #Packaging everything in a .mp4:
        os.system(f'ffmpeg -i {output_cut} -i {output_mono} -i {output_stereo} -i {output_aac} -c:v copy -c:a copy {output_final}')

    # EXERCISE 3:
    def count_tracks(input_path):

        result = subprocess.run(f'ffprobe -v error -show_entries stream=index,codec_name,codec_type -of json {input_path}',shell=True,check=True,capture_output=True,text=True)

        # Access the stdout attribute of the CompletedProcess object
        stracks = result.stdout

        # Load the JSON data from the string
        json_data = json.loads(stracks)

        # Check if json_data has 'streams' property and get its length
        num_tracks = len(json_data.get('streams', []))
        print(f'The container contains {num_tracks} track(s).')


if __name__ == "__main__":
    # EXERCISE 1:
    input = "BigBuckBunny.mp4"
    output = "Macroblocks.mp4"
    Semi2.generate_macroblocks_video(input, output)

    # EXERCISE 2:
    input_path = "BBB.mp4"
    output_cut = "BBB_50s.mp4"
    output_mono = "BBB_50s_mono.mp3"
    output_stereo = "BBB_50s_stereo.mp3"
    output_aac = "BBB_aac.aac"
    output_final = "BBB_final.mp4"
    Semi2.create_new_bbb_container(input_path, output_cut, output_mono, output_stereo, output_aac, output_final)

    # EXERCISE 3:
    track_count = Semi2.count_tracks(output_final)

    #EXERCISE 5:
    from Subtitles import Subtitles
    video_processor = Subtitles(
        '/home/laiamarinello/Documents/Semi2_Codification/BigBuckBunny.mp4',
        '/home/laiamarinello/Documents/Semi2_Codification/TheSmashingPumpkins.srt'
    )
    video_processor.integrate_subtitles('/home/laiamarinello/Documents/Semi2_Codification/BigBuckBunny_Subtitled.mp4')

    #EXERCISE 6:
    from YuvHistogram import YuvHistogram 
    input_video_path = "BigBuckBunny.mp4"
    output_video_path = "/home/laiamarinello/Documents/Semi2_Codification/BBBB_Histogram.mp4"

    yuv_histogram_processor = YuvHistogram(input_video_path, output_video_path)
    yuv_histogram_processor.integrate_yuv_histogram()