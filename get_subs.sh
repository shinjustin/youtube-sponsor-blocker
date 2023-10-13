for ID in $(cat videos.txt)
do
    echo $ID
    youtube_transcript_api "$ID" --format webvtt > subs/$ID.vtt --exclude-manually-created
done
