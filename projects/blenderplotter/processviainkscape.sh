#!/bin/bash
/usr/local/bin/inkscape $PWD/$1 --verb EditSelectAll --verb SelectionSimplify --verb FileSave --verb FileQuit
