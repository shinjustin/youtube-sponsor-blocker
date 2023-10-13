NR > 1 {

curr = substr($0, 3)
    if(prev_label != $1){
        label = 1
        }
    else {
        label = 0
        }
    printf("%s, %s\n",label,curr)
}
{
    prev_label = $1
    }
