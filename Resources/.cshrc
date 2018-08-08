########################################################################
#
# Filname : .cshrc
#
# Private .cshrc 
#
# This file should be copied to the users HOME directory 
#
########################################################################
#
set ext=cshrc
set LoginPath=/adm/login
#
# Set personal configuration here.
# Read the file /adm/login/VarHelp.cshrc for information.
#========================================================
# 
#
# DO NOT CHANGE THIS LINE
source $LoginPath/DEFAULT.$ext
#
# Personal variables after this line :
#========================================================
#
#setenv PRINTER grb3u
# 
#if ( $?prompt == 0 || $?VUE != 0 ) exit
#
# Personal aliases after this line :
#========================================================
setenv ACTIVE /project/RCP/active/fluent/
setenv TMP $ACTIVE/TMP
setenv RC $ACTIVE/Atle_Resources
setenv FLUENT_ARCH lnx86
#source /prog/sdpsoft/env.csh                  # not sure if this should be active...
source /project/res/SDP_cshrc                  # "geriljavirksomhet under radaren..." Per Arne Slotte. should still be active according to Hove 15/6-18
source /project/res/komodo/stable/enable.csh   # komodo as of june 2018 (Joakim Hove - Yammer 15/6-18)
source $HOME/.mycshrc
#source /prog/LSF/conf/cshrc.lsf # included by John Hybertsen to be able to start eclipse from unix shell
#
#
#
# NO CHANGES AFTER THIS LINE
source $LoginPath/END.$ext
