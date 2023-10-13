NR > 1 {

curr = substr($0, 3)
    if((prev_label+$1)/2 != $1) {
        label = 1
        }
    else {
        label = 0
        }
    printf "%s,%s,%s\n",label,prev,curr
}
{
    prev = substr($0, 3)
    prev_label = $1
    }
