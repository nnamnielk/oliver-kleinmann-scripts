#!/bin/bash

#defaults
##Set your var defaults here




#process optional args

PARAMS=""

while (( "$#" )); do
  case "$1" in
    -t|--two_parts)
      Part2=$2
      shift 2
      ;;
    -b|--some_boolean)
      some_boolean=1
      shift 1
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done



# set positional arguments in their proper place eval set -- "$PARAMS"
eval set -- "$PARAMS"




if [ $# -ne 1 ] ; then

cat <<EOF;

usage: $0  /path/to/dir/with/pdfs

runs ghostscript tp remove active content


EOF

exit 1

fi



#there is a more profresh why to get this part
MYDIR=`dirname $0`
MYDIR=`cd $MYDIR; pwd`



set -e
set -u
set -o pipefail
set -x


DIR=$1




#timestamp=`date "+%Y%m%d.%H%M%S"`
#export LOG_DIR=$LOG_DIR/$myname.$timestamp
#mkdir -p $LOG_DIR
#echo “logging to $LOG_DIR”


for x in `find $DIR -type f`; do
  if file $x | grep PDF; then
	echo processing $x
    dirname="$(dirname $x)"
    leftside="${x%.pdf}"
    pdf2ps $x "$dirname/$leftside.ps"
    ps2pdf "$dirname/$leftside.ps" clean_${x}
    rm -f "$dirname/$leftside.ps"
  fi
done



echo $0 done
