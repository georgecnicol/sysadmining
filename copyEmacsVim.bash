#!/usr/bin/bash
# George Nicol
# Feb 4, 2015

# copies emacs and vimrc files from /path/vmNameA/home/$user to
# /path/vmNameB/test/$user. This happens on the NFS server.
# The instructor had requested those things be available to the
# students during their in class code testing

hmpath="/path/vmNameA/home/"
tspath="/path/vmNameB/test/"
file=studentDirs.temp

ls $hmpath >> $file

while read line
do
        # copy an emacs dir if it exists
        studentDir=$line
        if [[ -d $hmpath$studentDir/emacs.d && -d $tspath/$studentDir ]]
        then
                cp -rp $hmpath$studentDir/.emacs.d $tspath/$studentDir
        fi

        # copy a vim dir if it exists
        if [[ -d $hmpath$studentDir/.vim && -d $tspath/$studentDir ]]
        then
                cp -rp $hmpath$studentDir/.vim $tspath/$studentDir
        fi

        # copy an emacs config file if it exists
        if [[ -e $hmpath$studentDir/.vimrc && -d $tspath/$studentDir ]]
        then
                cp -p $hmpath$studentDir/.vimrc $tspath/$studentDir
        fi

        # copy a vimrc file if it exists
        if [[ -e $hmpath$studentDir/.emacs && -d $tspath/$studentDir ]]
        then
                cp -p $hmpath$studentDir/.emacs $tspath/$studentDir
        fi

done<$file
rm $file

