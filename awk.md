## postgre-SQL
设置千分位分隔符`\pset numericlocale` `SELECT TO_CHAR(76543210.98, '999G999G990D00')  --G 被描述为:组分隔符(使用区域设置)`
## Doris
千分位分隔符`show builtin functions like 'money_format'\g`
## linux 查看信号
`diff -y <(awk 'FNR==NR{a[$2]=$1} FNR!=NR{print a[$0],$0}' <(kill -l | xargs -n 2) <(compgen -A signal) ) <(nl -v0 -s') ' -w1 <(compgen -A signal))`
`compgen -A signal | nl -v0 -s'^' -w2 | awk -F'^' '{if ($1%5 == 0 && $i <= 32) {printf "%s) %s\n",$1,$2} else if ($i > 32 && $1%5==2) {printf "%s) %s\n",$1,$2} else {printf "%s) %s^",$1,$2}}' | column -t -s'^'`
## linux 源码
内核定义的退出码  /usr/src/kernels/3.10.0-693.21.1.el7.x86_64/include/uapi/asm-generic/errno{-base,}.h  ## errno 或者  error
## column
右对齐  `echo -e '12 15\n2 5'| column -t -N'col1,col2' -R'col1,col2' # 高版本 column 的右对齐，低版本 printf 指定长度`
## awk 行列互转
```bash
# awk 处理文本：行转列       ? : 三元表达式   awk: cmd. line:1: (FILENAME=- FNR=3) fatal: not enough arguments to satisfy format string
awk '{for(i=1;i<=NF;i++)a[NR,i]=$i}END{for(j=1;j<=NF;j++)for(k=1;k<=NR;k++)printf k==NR?a[k,j] RS:a[k,j] FS}'   ## j<NF 这个NF是最后一行的NF个数，会打印不全
awk '{LEN=LEN<NF?NF:LEN;for(i=1;i<=NF;i++){a[NR,i]=$i}}END{for(j=1;j<=LEN;j++)for(k=1;k<=NR;k++)printf k==NR?a[k,j] RS:a[k,j] FS}'
awk '{LEN=LEN<NF?NF:LEN;for(i=1;i<=NF;i++){a[NR,i]=$i}}END{for(j=1;j<=LEN;j++)for(k=1;k<=NR;k++)printf "%s",k==NR?a[k,j] RS:a[k,j] FS}'   ## 字段值中包含 %s 会提示：参数数量少于格式数量
awk -F, '{LEN=LEN<NF?NF:LEN;for(i=1;i<=NF;i++){a[NR,i]=$i;CL=(NR==1 && CL<length($i))?length($i):CL}}END{for(k=2;k<=NR;k++)for(j=1;j<=LEN;j++){printf j==1?"*************************** "k-1". row ***************************"RS:"";printf "%"CL"s: %s",a[1,j],a[k,j]RS }}'   ## 行转列 像数据库一样 \x 一样
#                    列转行       ? : 三元表达式
awk '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}' 
awk '{LEN=LEN<NF?NF:LEN;for(i=0;++i<=NF;){a[i]=a[i]?a[i] FS $i:$i}}END{for(i=0;i++<LEN;)print a[i]}' 
## sql表格式输出
function output_sql_format(){     separator="${1}";     shift;     if [ "$#" -eq 0 ];then         local lines="";         while IFS= read -r line; do             lines+="$line"$'\n';         done;         local tabstr="${lines%$'\n'*}";     else         tabstr="$*";     fi;     field_cnt=`echo "${tabstr}" | head -1 | awk -F"${separator}" '{print NF}'`;     _segment=$(printf "+#%.0s" `seq $field_cnt`;echo -n '+');     echo "${tabstr}" | sed -E -e "s#^#|#g" -e "s%${separator}|$%#|%g" -e "1,+1 i ${_segment}" -e "$ a ${_segment}" |column -s '#' -t |  awk '{if($0 ~ /^+/){gsub(" ","-",$0)} print $0}'; }

echo 'citycode,anylizetime,timestamp,stbid,programurl,sessionid,deviceid,terminalip,servicetype,totalrequest,local_404_cnt,local_4_5xx_cnt,up_4_5xx_cnt,hit_cnt,clip_cnt,miss_cnt,over_dl_cnt,over_res_cnt,avg_speed(kb/s),repeat_ts_cnt,ts_exceeded_interval_cnt,m3u8_exceeded_interval_cnt,no_ts_num,tssecond3,timestamp_format,haveplay,haveplay3,errresult
0573,2024-05-15 16:41:00,2024-05-09 19:45:35,00420100300400402106acbb61aa6eed,http://tx.flv.huya.com/src/78941969-2592787562-11135937784265572352-2914030356-10057-A-0-1-imgplus.flv?uid=1467319296272&uuid=1467319296272&wsSecret=64c26c03f2da180736eca7cabdba6a92&wsTime=663cae7e&ctype=huya_adr_tv&sphdcdn=al_7-tx_3-js_3-ws_7-bd_2-hw_2&sphdDC=huya&sphd=264_*-265_*&exsphd=264_500|264_2000|264_4000|264_8000|264_10000|264_15000|&fs=gctex&ratio=2000&u=1464778952867&ver=1&t=2&seqid=1569486883,NULL,NULL,NULL,NULL,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2024-05-09 19:30:00.00,1,0,2
0573,2024-05-15 16:41:00,2024-05-09 22:32:32,00420100100422d021453485110f0cab,http://hwltc.tv.cdn.zj.chinamobile.com/PLTV/88888888/224/3221231270/235855194.smil/index.m3u8?fmt=ts2hls&rrsip=hwltc.tv.cdn.zj.chinamobile.com&zoneoffset=0&servicetype=1&icpid=&limitflux=-1&limitdur=-1&tenantId=8601&accountinfo=%7E%7EV2.0%7Er6aGiq3YUmM0vFITwBWptA908a480609d97af82287da6e52478861%7EbkQb8QsW1mgGmT_NQSpvuMTWYlVqYAnlQWsabv-_iwXViRlutH6NA9jmVOBoevSm8f79f428a3c3b151a5ce787eb8f01b2d%7EExtInfoXDbFMH8X2FXepIGj25xiIge13364c549dc5084a6fd1fad3cfab7d0%3A20240423161213%3AUTC%2C10001299866796%2C223.94.210.123%2C20240423161213%2C30CP230120170215351600%2C10001299866796%2C-1%2C0%2C1%2C%2C%2C2%2C600000439142%2C%2C%2C2%2C10000213512142%2C0%2C10000213539927%2C00420100100422D021453485110F0CAB%2C%2C%2C2%2C1%2C235855194%2CEND&GuardEncType=2&USERID=73330003263607&STBID=00420100100422D021453485110F0CAB&profileid=main,RR4594820240423231551068137,3913510019,223.94.210.5,2,7809,0,0,0,7809,2716,0,0,0,12522.189985909745,1,0,0,204,19,2024-05-09 22:30:00.00,1,1,0' | awk -F, '{LEN=LEN<NF?NF:LEN;for(i=1;i<=NF;i++){a[NR,i]=$i;CL=(NR==1 && CL<length($i))?length($i):CL}}END{for(k=2;k<=NR;k++)for(j=1;j<=LEN;j++){printf j==1?"*************************** "k-1". row ***************************"RS:"";printf "%"CL"s: %s",a[1,j],a[k,j]RS }}'

echo 'citycode,anylizetime,timestamp,stbid,programurl,sessionid,deviceid,terminalip,servicetype,totalrequest,local_404_cnt,local_4_5xx_cnt,up_4_5xx_cnt,hit_cnt,clip_cnt,miss_cnt,over_dl_cnt,over_res_cnt,avg_speed(kb/s),repeat_ts_cnt,ts_exceeded_interval_cnt,m3u8_exceeded_interval_cnt,no_ts_num,tssecond3,timestamp_format,haveplay,haveplay3,errresult
0573,2024-05-15 16:41:00,2024-05-09 19:45:35,00420100300400402106acbb61aa6eed,http://tx.flv.huya.com/src/78941969-2592787562-11135937784265572352-2914030356-10057-A-0-1-imgplus.flv?uid=1467319296272&uuid=1467319296272&wsSecret=64c26c03f2da180736eca7cabdba6a92&wsTime=663cae7e&ctype=huya_adr_tv&sphdcdn=al_7-tx_3-js_3-ws_7-bd_2-hw_2&sphdDC=huya&sphd=264_*-265_*&exsphd=264_500|264_2000|264_4000|264_8000|264_10000|264_15000|&fs=gctex&ratio=2000&u=1464778952867&ver=1&t=2&seqid=1569486883,NULL,NULL,NULL,NULL,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2024-05-09 19:30:00.00,1,0,2
0573,2024-05-15 16:41:00,2024-05-09 22:32:32,00420100100422d021453485110f0cab,http://hwltc.tv.cdn.zj.chinamobile.com/PLTV/88888888/224/3221231270/235855194.smil/index.m3u8?fmt=ts2hls&rrsip=hwltc.tv.cdn.zj.chinamobile.com&zoneoffset=0&servicetype=1&icpid=&limitflux=-1&limitdur=-1&tenantId=8601&accountinfo=%7E%7EV2.0%7Er6aGiq3YUmM0vFITwBWptA908a480609d97af82287da6e52478861%7EbkQb8QsW1mgGmT_NQSpvuMTWYlVqYAnlQWsabv-_iwXViRlutH6NA9jmVOBoevSm8f79f428a3c3b151a5ce787eb8f01b2d%7EExtInfoXDbFMH8X2FXepIGj25xiIge13364c549dc5084a6fd1fad3cfab7d0%3A20240423161213%3AUTC%2C10001299866796%2C223.94.210.123%2C20240423161213%2C30CP230120170215351600%2C10001299866796%2C-1%2C0%2C1%2C%2C%2C2%2C600000439142%2C%2C%2C2%2C10000213512142%2C0%2C10000213539927%2C00420100100422D021453485110F0CAB%2C%2C%2C2%2C1%2C235855194%2CEND&GuardEncType=2&USERID=73330003263607&STBID=00420100100422D021453485110F0CAB&profileid=main,RR4594820240423231551068137,3913510019,223.94.210.5,2,7809,0,0,0,7809,2716,0,0,0,12522.189985909745,1,0,0,204,19,2024-05-09 22:30:00.00,1,1,0' | output_sql_format ,

echo 'citycode,anylizetime,timestamp,stbid,programurl,sessionid,deviceid,terminalip,servicetype,totalrequest,local_404_cnt,local_4_5xx_cnt,up_4_5xx_cnt,hit_cnt,clip_cnt,miss_cnt,over_dl_cnt,over_res_cnt,avg_speed(kb/s),repeat_ts_cnt,ts_exceeded_interval_cnt,m3u8_exceeded_interval_cnt,no_ts_num,tssecond3,timestamp_format,haveplay,haveplay3,errresult
0573,2024-05-15 16:41:00,2024-05-09 19:45:35,00420100300400402106acbb61aa6eed,http://tx.flv.huya.com/src/78941969-2592787562-11135937784265572352-2914030356-10057-A-0-1-imgplus.flv?uid=1467319296272&uuid=1467319296272&wsSecret=64c26c03f2da180736eca7cabdba6a92&wsTime=663cae7e&ctype=huya_adr_tv&sphdcdn=al_7-tx_3-js_3-ws_7-bd_2-hw_2&sphdDC=huya&sphd=264_*-265_*&exsphd=264_500|264_2000|264_4000|264_8000|264_10000|264_15000|&fs=gctex&ratio=2000&u=1464778952867&ver=1&t=2&seqid=1569486883,NULL,NULL,NULL,NULL,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2024-05-09 19:30:00.00,1,0,2
0573,2024-05-15 16:41:00,2024-05-09 22:32:32,00420100100422d021453485110f0cab,http://hwltc.tv.cdn.zj.chinamobile.com/PLTV/88888888/224/3221231270/235855194.smil/index.m3u8?fmt=ts2hls&rrsip=hwltc.tv.cdn.zj.chinamobile.com&zoneoffset=0&servicetype=1&icpid=&limitflux=-1&limitdur=-1&tenantId=8601&accountinfo=%7E%7EV2.0%7Er6aGiq3YUmM0vFITwBWptA908a480609d97af82287da6e52478861%7EbkQb8QsW1mgGmT_NQSpvuMTWYlVqYAnlQWsabv-_iwXViRlutH6NA9jmVOBoevSm8f79f428a3c3b151a5ce787eb8f01b2d%7EExtInfoXDbFMH8X2FXepIGj25xiIge13364c549dc5084a6fd1fad3cfab7d0%3A20240423161213%3AUTC%2C10001299866796%2C223.94.210.123%2C20240423161213%2C30CP230120170215351600%2C10001299866796%2C-1%2C0%2C1%2C%2C%2C2%2C600000439142%2C%2C%2C2%2C10000213512142%2C0%2C10000213539927%2C00420100100422D021453485110F0CAB%2C%2C%2C2%2C1%2C235855194%2CEND&GuardEncType=2&USERID=73330003263607&STBID=00420100100422D021453485110F0CAB&profileid=main,RR4594820240423231551068137,3913510019,223.94.210.5,2,7809,0,0,0,7809,2716,0,0,0,12522.189985909745,1,0,0,204,19,2024-05-09 22:30:00.00,1,1,0' | awk -F, '{LEN=LEN<NF?NF:LEN;for(i=0;++i<=NF;){a[i]=a[i]?a[i] FS $i:$i}}END{for(i=0;i++<LEN;)print a[i]}'
```

## lftp

```bash
## 上传任务，保证10s上传未完成就取消任务
lftp -u user,passwd sftp://127.1:22 <<EOF
set net:limit-rate 1M
lcd /media/vdb1/crt_download
cd /media/vdb1/mr_jar/
at now + 10sec -- 'echo fail ; kill 1 ; rm alter_add_partiton.sql' &
(put alter_add_partiton.sql;mv alter_add_partiton.sql alter_add_partiton.sql_ok;local mv alter_add_partiton.sql alter_add_partiton.sql_ok;kill 0;echo ok) &
fg 1
fg 0
exit 

EOF
```

## openssl

`openssl x509 -noout -in /insecure/ca.pem  -text #openssl 查看证书信息`

## go 性能测试工具

> go性能测试工具  报错问题    http://0.0.0.0:11111/ui
> go tool pprof -http 0.0.0.0:11111 http://178.18.201.103:16807/debug/pprof/heap
> 	Failed to open connection to "session" message bus: Unable to autolaunch a dbus-daemon without a $DISPLAY for X11
> 	Error: no DISPLAY environment variable specified
>
> eval `dbus-launch --sh-syntax`
> X11Forwarding yes   ==>   /etc/ssh/sshd_config          systemctl restart sshd
> export  DISPLAY="127.0.0.1:10.0"
> /usr/bin/Xvfb :99 -ac -screen 0 1024x768x8 & export DISPLAY=":99"

## tcpdump

> ----关于 tcp  tcpdump
> 每行 4 字节bytes 32位 bits，前 5 行 20 字节bytes 为Basic TCP Headers，前6行 24 字节bytes为 TCP Headers
>  0                            15                              31 
> -----------------------------------------------------------------
> |          source port          |       destination port        |
> -----------------------------------------------------------------
> |                        sequence number                        |
> -----------------------------------------------------------------
> |                     acknowledgment number                     |
> -----------------------------------------------------------------
> |  HL   | rsvd  |C|E|U|A|P|R|S|F|        window size            |
> -----------------------------------------------------------------
> |         TCP checksum          |       urgent pointer          |
> -----------------------------------------------------------------
> |                       Option                                  |
> -----------------------------------------------------------------
> |                       Data                                    |
> -----------------------------------------------------------------
> 源端口和目的端口字段
>     TCP源端口（Source Port）：源计算机上的应用程序的端口号，占 16 位。
>     TCP目的端口（Destination Port）：目标计算机的应用程序端口号，占 16 位。
> 序列号字段
>     CP序列号（Sequence Number）：占 32 位。它表示本报文段所发送数据的第一个字节的编号。在 TCP 连接中，所传送的字节流的每一个字节都会按顺序编号。当SYN标记不为1时，这是当前数据分段第一个字母的序列号；如果SYN的值是1时，这个字段的值就是初始序列值（ISN），用于对序列号进行同步。这时，第一个字节的序列号比这个字段的值大1，也就是ISN加1。
> 确认号字段
>     TCP 确认号（Acknowledgment Number，ACK Number）：占 32 位。它表示接收方期望收到发送方下一个报文段的第一个字节数据的编号。其值是接收计算机即将接收到的下一个序列号，也就是下一个接收到的字节的序列号加1。
> 数据偏移字段
>     TCP 首部长度（Header Length）：数据偏移是指数据段中的“数据”部分起始处距离 TCP 数据段起始处的字节偏移量，占 4 位。其实这里的“数据偏移”也是在确定 TCP 数据段头部分的长度，告诉接收端的应用程序，数据从何处开始。
> 保留字段
>     保留（Reserved）：占 4 位。为 TCP 将来的发展预留空间，目前必须全部为 0。
> 标志位字段
>     CWR（Congestion Window Reduce）：拥塞窗口减少标志，用来表明它接收到了设置 ECE 标志的 TCP 包。并且，发送方收到消息之后，通过减小发送窗口的大小来降低发送速率。
>     ECE（ECN Echo）：用来在 TCP 三次握手时表明一个 TCP 端是具备 ECN 功能的。在数据传输过程中，它也用来表明接收到的 TCP 包的 IP 头部的 ECN 被设置为 11，即网络线路拥堵。
>     URG（URGent）：表示本报文段中发送的数据是否包含紧急数据。URG=1 时表示有紧急数据。当 URG=1 时，后面的紧急指针字段才有效。
>     ACK（ACKnowledgment）：表示前面的确认号字段是否有效。ACK=1 时表示有效。只有当 ACK=1 时，前面的确认号字段才有效。TCP 规定，连接建立后，ACK 必须为 1。
>     PSH（PuSH）：告诉对方收到该报文段后是否立即把数据推送给上层。如果值为 1，表示应当立即把数据提交给上层，而不是缓存起来。
>     RST（ReSeT）：表示是否重置连接。如果 RST=1，说明 TCP 连接出现了严重错误（如主机崩溃），必须释放连接，然后再重新建立连接。
>     SYN（SYNchronization）：在建立连接时使用，用来同步序号。当 SYN=1，ACK=0 时，表示这是一个请求建立连接的报文段；当 SYN=1，ACK=1 时，表示对方同意建立连接。SYN=1 时，说明这是一个请求建立连接或同意建立连接的报文。只有在前两次握手中 SYN 才为 1。
>     FIN（FINish）：标记数据是否发送完毕。如果 FIN=1，表示数据已经发送完成，可以释放连接。
> 窗口大小字段
>     窗口大小（Window Size）：占 16 位。它表示从 Ack Number 开始还可以接收多少字节的数据量，也表示当前接收端的接收窗口还有多少剩余空间。该字段可以用于 TCP 的流量控制。
> TCP 校验和字段
>     校验位（TCP Checksum）：占 16 位。它用于确认传输的数据是否有损坏。发送端基于数据内容校验生成一个数值，接收端根据接收的数据校验生成一个值。两个值必须相同，才能证明数据是有效的。如果两个值不同，则丢掉这个数据包。Checksum 是根据伪头 + TCP 头 + TCP 数据三部分进行计算的。
> 紧急指针字段
>     紧急指针（Urgent Pointer）：仅当前面的 URG 控制位为 1 时才有意义。它指出本数据段中为紧急数据的字节数，占 16 位。当所有紧急数据处理完后，TCP 就会告诉应用程序恢复到正常操作。即使当前窗口大小为 0，也是可以发送紧急数据的，因为紧急数据无须缓存。
> 可选项字段
>     选项（Option）：长度不定，但长度必须是 32bits 的整数倍。

```bash
for i in {1..1000};do echo $((RANDOM>>9));done | awk '{yy[$1]++} END {for (i in yy) {print i,yy[i]}}' | sort -k1,1n  ##15-9=6 2^6=0~63
dd if=/dev/zero of=/data2/lftpTestTransferFile.dd bs=10K count=$((RANDOM>>9))  ##15-9=6 2^6=0~63
lftp -u user,passwd sftp://${remote_ip}:22:/data2 <<EOF
set net:limit-rate 10K
lcd /data2
mput -c lftpTestTransferFile.dd
exit 
EOF
tcpdump -s 0 -i eth0 -vnn dst host ${remote_ip} and dst port 22 -c 100    抓包连接到 168.58.202.181:22 的 sftp 或者 ssh 的包
tcpdump version 4.9.2
libpcap version 1.9.0-PRE-GIT (with TPACKET_V3)
OpenSSL 1.1.1o  NSDL FIPS 16 May 2022
Usage: tcpdump [-aAbdDefhHIJKlLnNOpqStuUvxX#] [ -B size ] [ -c count ]
                [ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
                [ -i interface ] [ -j tstamptype ] [ -M secret ] [ --number ]
                [ -Q in|out|inout ]
                [ -r file ] [ -s snaplen ] [ --time-stamp-precision precision ]
                [ --immediate-mode ] [ -T type ] [ --version ] [ -V file ]
                [ -w file ] [ -W filecount ] [ -y datalinktype ] [ -z postrotate-command ]
                [ -Z user ] [ expression ]
    -w         写入文件
    -r         读取文件
```

## 网络丢包

>https://zhuanlan.zhihu.com/p/502027581
>网络丢包情形概览
>硬件网卡丢包
>	Ring Buffer溢出
>		ethtool -S ens4f1 | grep rx_fifo
>		解决方案：修改网卡eth0接收与发送硬件缓存区大小
>			$ ethtool -G ens4f1 rx 4096 tx 4096
>	网卡端口协商丢包
>		ethtool -S ens4f1 | grep errors
>		主要查看网卡和上游网络设备协商速率和模式是否符合预期
>		解决方案：
>			1 重新自协商： ethtool -r eth1/eth0;
>			2 如果上游不支持自协商，可以强制设置端口速率：
>			ethtool -s eth1 speed 1000 duplex full autoneg off
>	网卡流控丢包
>		ethtool -S eth1 | grep control
>		rx_flow_control_xon是在网卡的RX Buffer满或其他网卡内部的资源受限时，给交换机端口发送的开启流控的pause帧计数。对应的，tx_flow_control_xoff是在资源可用之后发送的关闭流控的pause帧计数
>		ethtool -a eth1
>		解决方案：关闭网卡流控
>			ethtool -A ethx autoneg off //自协商关闭
>			ethtool -A ethx tx off //发送模块关闭
>			ethtool -A ethx rx off //接收模块关闭
>	报文mac地址丢包
>		tcpdump 抓包
>		arp 抓包
>	其他网卡异常丢包
>		网卡firmware版本
>		网线接触不良
>			ethtool -S eth0 | grep rx_crc_errors
>		报文长度丢包
>			ethtool -S eth1|grep length_errors
>网卡驱动丢包
>	驱动溢出丢包
>		cat /proc/net/softnet_stat
>以太网链路层丢包
>网络IP层丢包
>传输层UDP/TCP丢包
>应用层socket丢包

> https://support.huawei.com/enterprise/zh/knowledge/EKB1001622131
> 查看网口及类型
> 	netstat -i | column -t
> 查看网卡的驱动版本和FW版本
> 	ethtool -i bond0 
> 通过ethtool或/proc/net/dev可以查看因Ring Buffer满而丢弃的包统计，在统计项中以fifo标识
> 	ethtool -S ens4f0 | grep rx_fifo
> 	cat /proc/net/dev | sed 's/|/ |/g' | column -t 
>     cat /proc/net/dev | sed -e '1{s/|/ |/g;s/Receive/- - - Receive - - -/;s/Transmit/- - - Transmit - - -/}' -e '2{s/|/ |/g}' | column -t 
> 查看 ens4f0 网卡 Ring Buffer 最大值和当前设置
> 	ethtool -g  ens4f0
> 查看网卡丢包统计
> 	ethtool -S ens4f1
> 	ethtool -S ens4f1 | grep errors
> 查看网卡配置状态
> 	ethtool ens4f1 
> 查看流控统计
> 	ethtool -S ens4f1 | grep control
> 查看网络流控配置
> 	ethtool -a eth1

mount 流程 
https://www.cnblogs.com/wahaha02/p/4504688.html
mount过程就是初始化对象的过程。这其中包括上层（vfs层、页缓存层、通用块层）的回调接口的注册，从设备中获取相关信息（super block， master node，log，orphan， index node），初始化ubifs_info、TNC、LPT等内部对象，并对ubifs各区（默认不检查main区的index node，因为有log区的日志，一般情况下不需要扫描所有的index tree）、journal head、lpt head等进行校验、检查、修复、更新，创建后台进程等。可以看出，mount中包含了检查和修复过程，所以ubifs并没有提供额外的修复工具，这一点区别于vfat、ext3等文件系统。

文件系统 orphan inode 机制
https://oenhan.com/fs-orphan-inode-analysis


nc -v -z 117.128.7.227 4506  ## 类似 telnet 查看 端口 是否可以连通

如果在 /etc/bashrc 或 ~/.bashrc 中有echo等输出语句, 则无法远程用scp, sftp 传文件

unset aa ; echo ${aa:-yes} ; echo $aa       yes 
unset aa ; echo ${aa:=yes} ; echo $aa       yes yes
unset aa ; echo ${aa:?yes} ; echo $aa       -bash: aa: yes
unset aa ; echo ${aa:+yes} ; echo $aa       
unset aa ; aa=no ; echo ${aa:-yes} ; echo $aa       no no
unset aa ; aa=no ; echo ${aa:?yes} ; echo $aa       no no
unset aa ; aa=no ; echo ${aa:=yes} ; echo $aa       no no
unset aa ; aa=no ; echo ${aa:+yes} ; echo $aa       yes no

## 安装yum-utils
```bash
$ yum -y install yum-utils
$ yum -y install yum-download
--- No.1
# 下载 ansible 全量依赖包
$ repotrack ansible
--- No.2
# 下载 ansible 依赖包
$ yumdownloader --resolve --destdir=/tmp ansible
--- No.3
# 下载 ansible 依赖包
$ yum -y install ansible --downloadonly --downloaddir=/tmp

# 离线安装
$ rpm -Uvh --force --nodeps *.rpm
```

https://zhuanlan.zhihu.com/p/676834467
kernel/ ---- Linux内核的核心代码，包含了3.2小节所描述的进程调度子系统，以及和进程调度相关的模块。
mm/ ---- 内存管理子系统（3.3小节）。
fs/ ---- VFS子系统（3.4小节）。
net/ ---- 不包括网络设备驱动的网络子系统（3.5小节）。
ipc/ ---- IPC（进程间通信）子系统。
arch// ---- 体系结构相关的代码，例如arm, x86等等。
arch//mach- ---- 具体的machine/board相关的代码。
arch//include/asm ---- 体系结构相关的头文件。
arch//boot/dts ---- 设备树（Device Tree）文件。
init/ ---- Linux系统启动初始化相关的代码。
block/ ---- 提供块设备的层次。
sound/ ---- 音频相关的驱动及子系统，可以看作“音频子系统”。
drivers/ ---- 设备驱动（在Linux kernel 3.10中，设备驱动占了49.4的代码量）。
lib/ ---- 实现需要在内核中使用的库函数，例如CRC、FIFO、list、MD5等。
crypto/ ----- 加密、解密相关的库函数。
security/ ---- 提供安全特性（SELinux）。
virt/ ---- 提供虚拟机技术（KVM等）的支持。
usr/ ---- 用于生成initramfs的代码。
firmware/ ---- 保存用于驱动第三方设备的固件。
samples/ ---- 一些示例代码。
tools/ ---- 一些常用工具，如性能剖析、自测试等。
Kconfig, Kbuild, Makefile, scripts/ ---- 用于内核编译的配置文件、脚本等。
COPYING ---- 版权声明。
MAINTAINERS ----维护者名单。
CREDITS ---- Linux主要的贡献者名单。
REPORTING-BUGS ---- Bug上报的指南。
Documentation, README ---- 帮助、说明文档。

https://blog.csdn.net/u013457167/article/details/79196306
https://zhuanlan.zhihu.com/p/641039869
/usr/src/kernels/3.10.0-693.21.1.el7.x86_64/include/uapi/asm-generic/errno{-base,}.h  ## errno 或者  error
EPERM	1	Operation not permitted	操作不允许
ENOENT	2	No such file or directory	没有这样的文件或目录
ESRCH	3	No such process	没有这样的过程
EINTR	4	Interrupted system call	系统调用被中断
EIO	    5	I/O error	I/O错误

man proc  关于/proc的信息
https://luoguochun.cn/post/2014-07-28-process-information-pseduo-file-system/
/proc/[pid]/auxv    包含ELF解析信息（ELF就是Linux系统二进制可执行文件的文件格式），auxv 是 AUXiliary Vector简写。每个条目的格式就是:一个unsigned longID加上一个unsigned long数值。这个AUXV是什么意思呢？ 我们可以通过加上LD_SHOW_AUXV=1 程序名可以获取具体的数值:
    LD_SHOW_AUXV=1 /bin/sh  ### /usr/src/kernels/3.10.0-693.21.1.el7.x86_64/include/uapi/linux/auxvec.h

显示什么类型的手册，由 man 和命令中间的数字决定，目前共有 9 个 man 支持的数字。
数字	说明
1	可执行程序或 Shell 命令
2	系统调用（内核提供的函数）
3	库调用
4	特殊文件（通常位于 /dev 目录）
5	文件格式和约定（比如 /etc/passwd）
6	游戏
7	杂项（包和一些约定）Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7)
8	系统管理命令（通常是 root 用户执行的命令）
9	内核相关的文件 Kernel routines [Non standard]
系统调用 
https://zhuanlan.zhihu.com/p/344311940

valgrind -s  --tool=memcheck --leak-check=full --show-reachable=yes --trace-children=yes --log-file=./xielou_check.log  ./mem_xielou.sh
awk -F'=' '{print NR,$3,$0}' xielou_check.log | sort -k2,2 -k1,1n > xielou_check.log_awk
https://cloud.tencent.com/developer/ask/sof/116359549
http://blog.chinaunix.net/uid-29494093-id-4743981.html
通过内存泄露检测，和bash相关代码和原理分析，问题产生的原因简单如下：
1、实际的内存泄露并不是被调用的后台进程自身产生的，泄露之处在于bash，bash调用后台命令，后台命令执行结束后，自身占用的资源(包括内存)应 该是成功回收的(bash中应该考虑了SIGCHLD信号的处理)，但问题关键在于：bash自己会为每一个后台子进程创建一个数据结构，用于保存后台进 程的返回值，否则bash中就无法了解后台子进程的退出状态了，这在一些情况下，确实是需要了解的。所以，泄露的内存就在这个数据结构上，如果不用 wait，那么每个后台子进程对应的数据结构就无法回收。
2、理论上，泄露的数据结构应该很小，不会产生大的影响，但是另一个关键在于glibc的堆实现，如果死循环中不断的创建后台子进程，那就不断的会有相应 的数据结构分配，而其占用的内存很可能顶在了堆顶，我们知道，如果堆顶的内存不能回收，那么堆顶之下的内存也是不能回收的，所以由于该数据结构的泄露，可 能导致更大的内存泄露。经过分析故障当时bash进程的堆分布情况，确实可以确认这一点。
综上，这个问题由于bash和glibc和脚本用法共同导致。

ELF LSB 逆向 反编译 https://52sbl.cn/discussion/25926.html    /bin/ls
https://zhuanlan.zhihu.com/p/347262004
命令	说明
readelf -h	读取ELF文件头
readelf -S	查看段的属性
readelf -s	查看符号表
objdump -h	查看段的属性
objdump -s	将所有段的内容以十六进制打印出来
objdump -d	将所有包含的指令反汇编
objdump -r	查看重定位段

段名	说明
.text	代码段。存放可执行文件的指令，这部分区域在程序运行前就已经确定。通过 objdump -s -d 查看
.data	数据段。保存已经初始化（非零初始化）的全局变量和静态局部变量
.bss	bss段。未初始化（零初始化）的全局变量和静态局部变量保存在bss段，准确来说.bss段为他们预留了位置，等到最终链接时在分配到.bss段（具体和编译器有关）
.rodata	只读数据段。存放的是只读数据，一般是程序里面的只读变量(const修饰的变量)和字符串变量（printf 的格式化字符也算）
.comment	存放的是编译器的版本信息
.symtab	符号表段。用来定位、重定位程序中符号定义和引用的信息，简单的理解就是符号表记录了该文件中的所有符号，所谓的符号就是经过修饰了的函数名或者变量名，不同的编译器有不同的修饰规则。
.shstrtab	字符串表段。存放着所有符号的名称字符串
.dynamic	动态链接信息。

column 格式化 输出类似sql表格的样式  当 第一个参数为0时，从标准输出读取，当为其他值时 读取剩下的所有位置参数
function column_table(){
    if [ "$1" == "0" ];then
        local lines=""
        while IFS= read -r line; do
            lines+="$line"$'\n'
        done
        local tabstr="${lines%$'\n'*}"
    else
        shift
        tabstr="$*"
    fi
    field_cnt=`echo "${tabstr}" | head -1 | awk '{print NF}'`
    _segment=$(printf "+#%.0s" `seq $field_cnt`;echo -n '+')
    echo "${tabstr}" | sed -E -e "s#^#|#g" -e "s%\s+|$%#|%g" -e "1,+1 i ${_segment}" -e "$ a ${_segment}" |column -s '#' -t |  awk '{if($0 ~ /^+/){gsub(" ","-",$0)} print $0}'
}


' '   UTF-8编码是\x3d\x3d\x3e    \xc2\xa0    Non-breaking space，用于阻止在此处自动换行和阻止多个空格被压缩成一个
## 多线程
```bash
Multi-threaded.sh
#!/bin/bash
THREAD_NUM=3
TMP_FILE="/tmp/$$.fifo"
echo 'ulimit -n: '`ulimit -n` 
trap "exec 6>&-;exec 6<&-;exit 0" 2     #脚本运行过程中，如果接收到信号2(Ctrl+C)中断命令，则关闭文件描述符6的读写，并正常退出
 
mkfifo ${TMP_FILE}  #创建有名管道
exec 6<>${TMP_FILE} #创建文件描述符，文件描述符可使用3-(n-1)，n取值范围：ulimit -n。以读写(<,读；>,写)方式绑定TMP_FILE管道文件。标识对文件描述符6的所有操作等同于对管道文件TMP_FILE的操作
rm -rf ${TMP_FILE}  #为什么不直接使用管道文件？因为管道的一个重要特性：读写必须同时存在，缺失某个操作，另一个操作就会滞留。绑定文件描述符（读、写绑定）正好解决了这个问题
 
for ((J=1;J<=${THREAD_NUM};J++)) #向管道中中输入THREAD_NUM个并发数量的空行。为什么写入空行而不是字符？那是因为管道文件的读取是以行为单位。
do
    echo >&6
done
 
START_TIME=`date +%s`
 
for ((I=1;I<=12;I++))
do 
    read -u6 #从管道中读取行，每次读一行。每读一次就会减少一个空行，直到管道中没有回车符，所有行读取完毕后执行挂起，实现线程数量控制。
    {
        echo "${I}: success" ; sleep 2
        echo >&6    #任务在后台执行结束后，向文件描述符中写入一个空行。如果不在向描述符中写入空行，当后台放入THREAD_NUM个任务之后，由于描述符中没有可读取的空行，会导致read -u6停顿。
    }&
done
wait
 
STOP_TIME=`date +%s`
echo "TIME: $(expr ${STOP_TIME} - ${START_TIME})"
 
exec 6>&-
exec 6<&-
```
## curl
>curl -k -s -w "http_code:"%{http_code}"\ntime_namelookup:"%{time_namelookup}"\ntime_connect:"%{time_connect}"\ntime_appconnect:"%{time_appconnect}"\ntime_redirect:"%{time_redirect}"\ntime_pretransfer:"%{time_pretransfer}"\ntime_starttransfer:"%{time_starttransfer}"\ntime_total:"%{time_total}"\nspeed_download:"%{speed_download}"\n" -H "Content-Type: application/json" -XGET 'baidu.com'
http_code:           响应码
time_namelookup：    DNS 域名解析的时间，就是把 https://zhihu.com 转换成 ip 地址的过程
time_connect：       TCP 连接建立的时间，就是三次握手的时间
time_appconnect：    SSL/SSH 等上层协议建立连接的时间，比如 connect/handshake 的时间
time_redirect：      从开始到最后一个请求事务的时间
time_pretransfer：   从请求开始到响应开始传输的时间
time_starttransfer： 从请求开始到第一个字节将要传输的时间
time_total：         这次请求花费的全部时间
-w：从文件中读取要打印信息的格式  与 -i 冲突
-o /dev/null：把响应的内容丢弃，因为我们这里并不关心它，只关心请求的耗时情况
-s：不要打印进度条，去掉所有状态
--insecure --anyauth -u 安全相关