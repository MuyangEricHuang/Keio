#!/bin/sh

usage_exit() {
    echo "Usage: qtop [-n node] [-u user] -c -h" 1>&2
    echo "-n node : Show information of only this node" 1>&2
    echo "-u user : Show information of only this user" 1>&2
    echo "-c      : Do not show job information" 1>&2
    echo "-q      : Show qued jobs" 1>&2
    echo "-h      : Show this help" 1>&2
    exit 1
}

while getopts n:u:cqh OPT
do
  case $OPT in
      n ) FLG_NODE="TRUE" ; NODE="$OPTARG" ;;
      u ) FLG_USER="TRUE" ; USER="$OPTARG" ;;
      c ) FLG_CORE="TRUE" ; USER="$OPTARG" ;;
      q ) FLG_QUE="TRUE" ;;
      h ) usage_exit ;;
  esac
done

USERSHORT=$(cut -c-11 <<< ${USER})
#echo ${USERSHORT}

while :
do
    clear
    echo -e "\e[36m"
    echo -e "============================================================================================="
    echo -e "kingTop for ${USER} - Updated : "`date`
    echo -e "-------------------------------------------------------------------------------------------"

    ## Node Information
    echo -e "Node\tLoadAve\tMemory Usage                                             %Mem  RemainingMem"
    echo -e "-------------------------------------------------------------------------------------------\e[m"

    if [[ ${FLG_NODE} = "TRUE" ]] ;
    then
 pbsnodes | grep -e '^k' -e "     status" | perl -ne 'chomp if /^k/; print $_' | perl -lane '$core = shift @F; foreach $b( @F ){ $b =~ /loadave\=([0-9\.]+)[\w\d\=\,\.]+availmem\=(\d+)kb[\w\d\=\,\.]+totmem=(\d+)kb/; ($loadave,$availmem,$totalmem) = ($1, $2,$3);}  $memusage = $availmem > 1 ? (100-$availmem/214755604*100)/2 : 0; $memlength = "|" x int($memusage); $nonmemlength=" " x (50-int($memusage)); $loadave2 = $loadave > 28 ? "\e[31m".$loadave."\e[m" : $loadave > 10 ? "\e[33m".$loadave."\e[\m" : "\e[m".$loadave."\e[m";  print join("\t", ($core, $loadave2, "[".$memlength.$nonmemlength."] ".sprintf("%7.2f",$memusage*2)."%: ".sprintf("%06.2fG",$availmem/1000/1000)))' | grep ${NODE}
    else
 pbsnodes | grep -e '^k' -e "     status" | perl -ne 'chomp if /^k/; print $_' | perl -lane '$core = shift @F; foreach $b( @F ){ $b =~ /loadave\=([0-9\.]+)[\w\d\=\,\.]+availmem\=(\d+)kb[\w\d\=\,\.]+totmem=(\d+)kb/; ($loadave,$availmem,$totalmem) = ($1, $2,$3);}  $memusage = $availmem > 1 ? (100-$availmem/214755604*100)/2 : 0; $memlength = "|" x int($memusage); $nonmemlength=" " x (50-int($memusage)); $loadave2 = $loadave > 28 ? "\e[31m".$loadave."\e[m" : $loadave > 10 ? "\e[33m".$loadave."\e[m" : "\e[32m".$loadave."\e[m"; if($memusage*2>90 ) {$memcol = "\e[31m"; } elsif( $memusage*2>30 ) { $memcol = "\e[33m"; } else { $memcol = "\e[32m";} print join("\t", ("\e[36m".$core."\e[m", $loadave2, "[".$memcol.$memlength.$nonmemlength."\e[m"."] ".$memcol.sprintf("%7.2f",$memusage*2)."%  ".sprintf("%11.2fG",$availmem/1000/1000)))."\e[m"'
    fi
#    echo -e "\e[36m-------------------------------------------------------------------------------------------"
    echo -e "\e[36m=============================================================================================\e[m"

    if [[ ${FLG_CORE} = "TRUE" ]];
    then
 sleep 30
 continue
    fi

    ## Job information
    perl -e 'print "\e[36mNode\t".sprintf("%5s", "Core")."\t".sprintf("%12s", "User")."\t".sprintf("%16s","ScriptName")."\t".sprintf("%12s","JobID")."\tElap Time\n"'
    echo -e "---------------------------------------------------------------------------------\e[m"
    if [[ ${FLG_NODE} = "TRUE" ]] ;
    then
 if [[ ${FLG_USER} = "TRUE" ]] ;
 then
     qstat -n1 | perl -slane 'next if @F[9] ne "R"; ($a,$b) = (split /\//,@F[11]); $c=int((split /\:/,@F[10])[0]); if ($c>20){$timecol="\e[31m"} elsif($c>15){$timecol="\e[33m";} else {$timecol="\e[32m";} if( @F[1] eq $user ) {$usercol="\e[35m";} else {$usercol="\e[34m";} print join("\t", ("\e[36m".$a."\t".sprintf("%5s",$b)."\e[m", $usercol.sprintf("%12s",@F[1]), sprintf("%16s",@F[3]), @F[0]."\e[m", $timecol.@F[10]."\e[m"))' -- -user=${USERSHORT} | sort -k1,2n | grep ${USERSHORT} | grep ${NODE}
 else
     qstat -n1 | perl -slane 'next if @F[9] ne "R"; ($a,$b) = (split /\//,@F[11]); $c=int((split /\:/,@F[10])[0]); if ($c>20){$timecol="\e[31m"} elsif($c>15){$timecol="\e[33m";} else {$timecol="\e[32m";} if( @F[1] eq $user ) {$usercol="\e[35m";} else {$usercol="\e[34m";} print join("\t", ("\e[36m".$a."\t".sprintf("%5s",$b)."\e[m", $usercol.sprintf("%12s",@F[1]), sprintf("%16s",@F[3]), @F[0]."\e[m", $timecol.@F[10]."\e[m"))' -- -user=${USERSHORT} | sort -k1,2n | grep ${NODE}
 fi
    else
 if [[ ${FLG_USER} = "TRUE" ]] ;
 then
     qstat -n1 | perl -slane 'next if @F[9] ne "R"; ($a,$b) = (split /\//,@F[11]); $c=int((split /\:/,@F[10])[0]); if ($c>20){$timecol="\e[31m"} elsif($c>15){$timecol="\e[33m";} else {$timecol="\e[32m";} if( @F[1] eq $user ) {$usercol="\e[35m";} else {$usercol="\e[34m";} print join("\t", ("\e[36m".$a."\t".sprintf("%5s",$b)."\e[m", $usercol.sprintf("%12s",@F[1]), sprintf("%16s",@F[3]), @F[0]."\e[m", $timecol.@F[10]."\e[m"))' -- -user=${USERSHORT} | sort -k1,2n | grep ${USERSHORT}
 else
     qstat -n1 | perl -slane 'next if @F[9] ne "R"; ($a,$b) = (split /\//,@F[11]); $c=int((split /\:/,@F[10])[0]); if ($c>20){$timecol="\e[31m"} elsif($c>15){$timecol="\e[33m";} else {$timecol="\e[32m";} if( @F[1] eq $user ) {$usercol="\e[35m";} else {$usercol="\e[34m";} print join("\t", ("\e[36m".$a."\t".sprintf("%5s",$b)."\e[m", $usercol.sprintf("%12s",@F[1]), sprintf("%16s",@F[3]), @F[0]."\e[m", $timecol.@F[10]."\e[m"))' -- -user=${USERSHORT} | sort -k1,2n
 fi
    fi
    echo -e "\e[36m=============================================================================================\e[m"

    if [[ ${FLG_QUE} = "TRUE" ]] ;
    then
 echo -e "\e[36mUser\t\tJob\tNumCore\e[m";
 echo -e "\e[36m---------------------------------------------------------------------------------\e[m"
 qstat -n | perl -slane 'next unless @F[9] eq "Q";  if( @F[1] eq $user ) {$usercol="\e[35m";} else {$usercol="\e[34m";}; print $usercol.join("\t", (@F[1],@F[3],@F[6]))."\e[m";'  -- -user=${USERSHORT}
 echo -e "\e[36m=============================================================================================\e[m"
    fi

    if [[ ${FLG_NODE} = "TRUE" ]] ;
    then
 echo "# -n "${NODE}
    fi
    if [[ ${FLG_USER} = "TRUE" ]] ;
    then
 echo "# -u "${USER}
    fi
 #   echo -e "# Press c-c to stop."
    sleep 15
done
