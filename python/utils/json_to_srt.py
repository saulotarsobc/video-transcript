import json

import datetime


def format_time(seconds):
    """
    Formats the given number of seconds into a string representation in the format HH:MM:SS,MMM.

    Args:
        seconds (float): The number of seconds to be formatted.

    Returns:
        str: The formatted time string in the format HH:MM:SS,MMM.

    Example:
        >>> format_time(123.456)
        '02:03:45,456'
    """
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds / 60)
    seconds %= 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)

    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def to_str(json_data):
    """
    Converts a JSON data structure representing a transcript into a string in the .srt format.

    Args:
        json_data (dict): The JSON data structure representing the transcript. It should have a "segments" key
            containing a list of dictionaries, each representing a segment of the transcript. Each segment should
            have a "start" key (float) representing the start time of the segment, an "end" key (float) representing
            the end time of the segment, and a "text" key (str) representing the text of the segment.

    Returns:
        str: The transcript in .srt format.

    Example:
        >>> json_data = {
        ...     "segments": [
        ...         {"start": 0.0, "end": 5.0, "text": "Hello world!"},
        ...         {"start": 5.0, "end": 10.0, "text": "How are you?"}
        ...     ]
        ... }
        >>> to_str(json_data)
        '1\n00:00:00,000 --> 00:00:05,000\nHello world!\n\n2\n00:00:05,000 --> 00:00:10,000\nHow are you?\n\n'
    """
    srt_content = ""
    segments = json_data.get("segments", [])
    segment_id = 1

    for segment in segments:
        start_time = segment.get("start", 0.0)
        end_time = segment.get("end", 0.0)
        text = segment.get("text", "")

        # Format start and end times into HH:MM:SS,MMM
        start_time_formatted = format_time(start_time)
        end_time_formatted = format_time(end_time)

        # Construct the subtitle block in .srt format
        srt_content += f"{segment_id}\n"
        srt_content += f"{start_time_formatted} --> {end_time_formatted}\n"
        srt_content += f"{text}\n\n"

        segment_id += 1

    return srt_content.strip()


def write_srt(srt_content, filename):
    """
    Write the given `srt_content` to a file with the specified `filename`.

    Parameters:
        srt_content (str): The content to be written to the file.
        filename (str): The name of the file to write the content to.

    Returns:
        None
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(srt_content)


def json_to_srt(json_data, filename):
    """
    Converts a JSON data structure representing a transcript into a string in the .srt format
    and saves it to a file.

    Args:
        json_data (dict): The JSON data structure representing the transcript. It should have a "segments"
            key containing a list of dictionaries, each representing a segment of the transcript. Each segment
            should have a "start" key (float) representing the start time of the segment, an "end" key (float)
            representing the end time of the segment, and a "text" key (str) representing the text of the segment.
        filename (str): The name of the file to save the transcription in.

    Returns:
        None
    """
    # Open the file in write mode, with UTF-8 encoding
    with open(f'./temp/transcriptions/{filename}/transcription.srt', "w", encoding="utf-8") as f:
        # Convert the JSON data structure to the .srt format
        data = to_str(json_data)
        # Write the .srt data to the file
        f.write(data)
    # Print a message indicating that the transcription has been saved
    print(
        f'Saved transcription in ./temp/transcriptions/{filename}/transcription.srt!')
