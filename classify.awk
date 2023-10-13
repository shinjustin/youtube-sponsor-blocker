NR > 1 {
    curr = substr($0, 3)
    if(prev_label != $1) {
        print prev_label "," segment
        segment = ""
        prev_label = $1
        }
}
{
    prev = substr($0, 3)
    prev_label = $1
    segment = segment " " prev
}
END {
    print prev_label "," segment
}
