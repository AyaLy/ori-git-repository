# 从零开始学习shell脚本
# grep 命令
# -H：显示文件名

fmt_sql(){ separator="${1}"; shift; if [ "$#" -eq 0 ];then local lines=""; while IFS= read -r line; do lines+="$line"$'\n'; done; local tabstr="${lines%$'\n'*}"; else tabstr="$*"; fi; field_cnt=`echo "${tabstr}" | head -1 | awk -F"${separator}" '{print NF}'`; _segment=$(printf "+#%.0s" `seq $field_cnt`;echo -n '+'); echo "${tabstr}" | sed -E -e "s#^#|#g" -e "s%${separator}|$%#|%g" -e "1,+1 i ${_segment}" -e "$ a ${_segment}" |column -s '#' -t |  awk '{if($0 ~ /^+/){gsub(" ","-",$0)} print $0}'; }
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show frontends\G' | grep -E 'Host|IsMaster|Alive|Version' | awk '{a[$1]=a[$1]==""?"-"$2:a[$1]",-"$2} END {print a["Host:"];print a["IsMaster:"];print a["Alive:"];print a["Version:"]}' | awk -F, '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}' | sed '1i Host,IsMaster,Alive,Version' | fmt_sql ,
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show backends\G' | grep -E 'Host|Alive|Version' | awk '{a[$1]=a[$1]==""?"-"$2:a[$1]",-"$2} END {print a["Host:"];print a["Alive:"];print a["Version:"]}' | awk -F, '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}' | sed '1i Host,Alive,Version' | fmt_sql ,
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show frontends' | sed 's/\t/^/g' | awk -v OFS=',' -F'^' 'NR==1 {for (i=1;i<=NF;i++) if ($i ~ /Host|IsMaster|Alive|Version/) a[$i]=i; n=asort(a, idx)} {for (i=1; i<=n; i++) printf i==1?"%s":",%s",$(idx[i]);print ""}' | fmt_sql ,
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show backends' | sed 's/\t/^/g' | awk -v OFS=',' -F'^' 'NR==1 {for (i=1;i<=NF;i++) if ($i ~ /Host|Alive|Version/) a[$i]=i; n=asort(a, idx)} {for (i=1; i<=n; i++) printf i==1?"%s":",%s",$(idx[i]);print ""}' | fmt_sql ,
ps -o lstart,pid,comm `pgrep -f 'doris_be|DorisFE'` | awk -vOFS='@' 'function _trim(line,start,end){ if (end == "") {str = substr(line, start+1)} else {str = substr(line, start+1, end-start-1)};gsub(/^ +| +$/,"",str);return str; } NR==1 {a=index($0,"STARTED")+7;b=index($0,"PID")+3} {print _trim($0,0,a),_trim($0,a,b),_trim($0,b)}' | fmt_sql '@'
ps -o lstart,pid,comm,cmd `pgrep -f 'doris_be|DorisFE'` | awk -vOFS='@' 'function _trim(line,start,end){ if (end == "") {str = substr(line, start+1)} else {str = substr(line, start+1, end-start-1)};gsub(/^ +| +$/,"",str);return str; } NR==1 {a=index($0,"STARTED")+7;b=index($0,"PID")+3;c=index($0,"CMD")} {print _trim($0,0,a),_trim($0,a,b),_trim($0,b,c),_trim($0,c-1,c+141)}' | fmt_sql '@' ## 命令太长了不好看，就用c+141限制140个字符，后续优化方向 根据当前终端的column进行输出（,c+141可去掉）

ps -o lstart,pid,comm,cmd `pgrep -f 'doris_be|DorisFE'` | awk -vOFS='@' 'function _trim(line,start,end){ if (end == "") {str = substr(line, start+1)} else {str = substr(line, start+1, end-start-1)};gsub(/^ +| +$/,"",str);return str; } NR==1 {a=index($0,"STARTED")+7;b=index($0,"PID")+3;c=index($0,"CMD")} {print _trim($0,0,a),_trim($0,a,b),_trim($0,b,c),_trim($0,c-1)}' | awk -F'@' '{LEN=LEN<NF?NF:LEN;for(i=1;i<=NF;i++){a[NR,i]=$i;CL=(NR==1 && CL<length($i))?length($i):CL}}END{for(k=2;k<=NR;k++)for(j=1;j<=LEN;j++){printf j==1?"*************************** "k-1". row ***************************"RS:"";printf "%"CL"s: %s",a[1,j],a[k,j]RS }}'



#### 自动拆分 列数不一样的行 进行分段格式化
fmt_sql () { separator="${1}"; shift; if [ "$#" -eq 0 ]; then local lines=""; while IFS= read -r line; do lines+="$line"$'\n'; done; local tabstr="${lines%$'\n'*}"; else tabstr="$*"; fi; unset idxs; for _el in `echo "$tabstr" | awk -F, '{nfc=nfc==""?NF:nfc;printf NF==nfc?"":NR-1" ";nfc=NF} END {print NR}'`; do idxs=${idxs:-1}; _txt=`echo "$tabstr" | sed -n "$idxs,$_el p"`; idxs=$((_el+1)); field_cnt=`echo "${_txt}" | head -1 | awk -F"${separator}" '{print NF}'`; _segment=$(printf "+#%.0s" `seq $field_cnt`;echo -n '+'); echo "${_txt}" | sed -E -e "s#^#|#g" -e "s%${separator}|$%#|%g" -e "1,+1 i ${_segment}" -e "$ a ${_segment}" | column -s '#' -t | awk '{if($0 ~ /^+/){gsub(" ","-",$0)} print $0}'; done }
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show frontends\G' | grep -E 'Host|IsMaster|Alive|Version' | awk '{a[$1]=a[$1]==""?"-"$2:a[$1]",-"$2} END {print a["Host:"];print a["IsMaster:"];print a["Alive:"];print a["Version:"]}' | awk -F, '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}' | sed '1i Host,IsMaster,Alive,Version' | fmt_sql ,
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show backends\G' | grep -E 'Host|Alive|Version' | awk '{a[$1]=a[$1]==""?"-"$2:a[$1]",-"$2} END {print a["Host:"];print a["Alive:"];print a["Version:"]}' | awk -F, '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}' | sed '1i Host,Alive,Version' | fmt_sql ,
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show frontends' | sed 's/\t/^/g' | awk -v OFS=',' -F'^' 'NR==1 {for (i=1;i<=NF;i++) if ($i ~ /Host|IsMaster|Alive|Version/) a[$i]=i; n=asort(a, idx)} {for (i=1; i<=n; i++) printf i==1?"%s":",%s",$(idx[i]);print ""}' | fmt_sql ,
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show backends' | sed 's/\t/^/g' | awk -v OFS=',' -F'^' 'NR==1 {for (i=1;i<=NF;i++) if ($i ~ /Host|Alive|Version/) a[$i]=i; n=asort(a, idx)} {for (i=1; i<=n; i++) printf i==1?"%s":",%s",$(idx[i]);print ""}' | fmt_sql ,
ps -o lstart,pid,comm `pgrep -f 'doris_be|DorisFE'` | awk -vOFS='@' 'function _trim(start,end){ if (end == "") {str = substr($0, start+1)} else {str = substr($0, start+1, end-start-1)};gsub(/^ +| +$/,"",str);return str; } NR==1 {a=index($0,"STARTED")+7;b=index($0,"PID")+3} {print _trim(0,a),_trim(a,b),_trim(b)}' | fmt_sql '@'
ps -o lstart,pid,comm,cmd `pgrep -f 'doris_be|DorisFE'` | awk -vOFS='@' 'function _trim(start,end){ if (end == "") {str = substr($0, start+1)} else {str = substr($0, start+1, end-start-1)};gsub(/^ +| +$/,"",str);return str; } NR==1 {a=index($0,"STARTED")+7;b=index($0,"PID")+3;c=index($0,"CMD")} {print _trim(0,a),_trim(a,b),_trim(b,c),_trim(c-1,c+141)}' | fmt_sql '@' ## 命令太长了不好看，就用c+141限制140个字符，后续优化方向 根据当前终端的column进行输出（,c+141可去掉）
ps -o lstart,pid,comm,cmd `pgrep -f 'doris_be|DorisFE'` | awk -vOFS='@' 'function _trim(start,end){ if (end == "") {str = substr($0, start+1)} else {str = substr($0, start+1, end-start-1)};gsub(/^ +| +$/,"",str);return str; } NR==1 {a=index($0,"STARTED")+7;b=index($0,"PID")+3;c=index($0,"CMD")} {print _trim(0,a),_trim(a,b),_trim(b,c),_trim(c-1)}' | awk -F'@' '{LEN=LEN<NF?NF:LEN;for(i=1;i<=NF;i++){a[NR,i]=$i;CL=(NR==1 && CL<length($i))?length($i):CL}}END{for(k=2;k<=NR;k++)for(j=1;j<=LEN;j++){printf j==1?"*************************** "k-1". row ***************************"RS:"";printf "%"CL"s: %s",a[1,j],a[k,j]RS }}'
### BE/FE 二合一
/home/mr/mysql-5.7.22-linux-glibc2.12-x86_64/bin/mysql -uadmin -P9030 -h168.58.211.215 -e 'show frontends;show backends;' | sed 's/\t/^/g' | awk -v OFS=',' -F'^' '$0~/^Name|^BackendId/ {delete a;for (i=1;i<=NF;i++) if ($i ~ /Host|IsMaster|Alive|Version/) a[$i]=i; n=asort(a, idx)} {for (i=1; i<=n; i++) printf i==1?"%s":",%s",$(idx[i]);print ""}' | fmt_sql ,



fmt_sql () 
{ 
    separator="${1}";
    shift;
    if [ "$#" -eq 0 ]; then
        local lines="";
        while IFS= read -r line; do
            lines+="$line"'
';
        done;
        local tabstr="${lines%
*}";
    else
        tabstr="$*";
    fi;
    unset idxs;
    for _el in `echo "$tabstr" | awk -F, '{nfc=nfc==""?NF:nfc;printf NF==nfc?"":NR-1" ";nfc=NF} END {print NR}'`;
    do
        idxs=${idxs:-1};
        _txt=`echo "$tabstr" | sed -n "$idxs,$_el p"`;
        idxs=$((_el+1));
        field_cnt=`echo "${_txt}" | head -1 | awk -F"${separator}" '{print NF}'`;
        _segment=$(printf "+#%.0s" `seq $field_cnt`;echo -n '+');
        echo "${_txt}" | sed -E -e "s#^#|#g" -e "s%${separator}|$%#|%g" -e "1,+1 i ${_segment}" -e "$ a ${_segment}" | column -s '#' -t | awk '{if($0 ~ /^+/){gsub(" ","-",$0)} print $0}';
    done
}




