#### 1. 安装hadoop


##### 1) 下载 
> https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz  


##### 2) 解压并配置环境变量
hadoop和jdk路径不能包含空格(建议使用jdk8)  

配置环境变量 `HADOOP_HOME`  
path中增加 `%HADOOP_HOME%\bin`  


##### 3) 安装winutils（仅当使用windows时需要）
因为hadoop原本只能运行在linux环境下, 所以需要安装winutils
winutils的版本需要和下载的hadoop版本一致
> 下载 https://github.com/cdarlint/winutils 
> 解压并覆盖在bin目录下  

##### 4) 配置修改
> etc/hadoop/core-site.xml  
```xml
<configuration>
	<property>
       <name>fs.default.name</name>
       <value>hdfs://0.0.0.0:9000</value>
   </property>
</configuration>
```

> etc/hadoop/mapred-site.xml
```xml
<configuration>
	<property>
       <name>mapreduce.framework.name</name>
       <value>yarn</value>
   </property>
</configuration>
```

> etc/hadoop/hdfs-site.xml
```xml
<configuration>
	<!-- 这个参数设置为1，因为是单机版hadoop -->
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
	<property> 
     <name>dfs.permissions</name> 
     <value>false</value> 
  </property>
   <property>
       <name>dfs.namenode.name.dir</name>
       <value>/hadoop/data/namenode</value>
   </property>
   <property>
		<name>fs.checkpoint.dir</name>
		<value>/hadoop/data/snn</value>
	</property>
	<property>
		<name>fs.checkpoint.edits.dir</name>
		<value>/hadoop/data/snn</value>
	</property>
	   <property>
       <name>dfs.datanode.data.dir</name>
       <value>/hadoop/data/datanode</value>
   </property>
</configuration>
```

> etc/hadoop/yarn-site.xml
```xml
<configuration>
<!-- Site specific YARN configuration properties -->
	<property>
    	<name>yarn.nodemanager.aux-services</name>
    	<value>mapreduce_shuffle</value>
   </property>
   <property>
      	<name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>  
		<value>org.apache.hadoop.mapred.ShuffleHandler</value>
   </property>
</configuration>
```

> etc/hadoop/hadoop-env.cmd  
> 修改`JAVA_HOME`， 例如：
```
export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jre/"
```

#### 2. 启动hadoop

* 新建用户，例如"bigdata"  
```
groupadd bigdata
useradd bigdata -g bigdata
```

* 生成免密登录的公钥并配置
```
ssh-keygen
cat /home/bigdata/.ssh/id_rsa.pub >> /home/bigdata/.ssh/authorized_keys  
```

* 初始化namenode  
```
hdfs namenode -format  
```

* 启动  
```
start-all.cmd  
```

* 查看集群所有节点状态  
> http://127.0.0.1:8088/cluster

* 文件管理  
> http://127.0.0.1:9870/dfshealth.html#tab-overview

* mapper & reducer 
```
echo a a a b b c | python C:\Users\cc\Desktop\mapper.py | python C:\Users\cc\Desktop\reducer.py
```

```
hadoop jar E:\hadoop-3.1.2\share\hadoop\tools\lib\hadoop-streaming-3.1.2.jar -file C:\Users\cc\Desktop\mapper.py -file C:\Users\cc\Desktop\reducer.py -mapper "python mapper.py" -reducer "python reducer.py" -input /demo.txt -output /output
```

#### 3. 安装hive

* 下载
> https://hive.apache.org/downloads.html  

配置环境变量 `HIVE_HOME`  
path中增加 `%HIVE_HOME%\bin`  

* 安装derby（仅当使用derby时需要）
> https://db.apache.org/derby/derby_downloads.html

配置环境变量 `DERBY_HOME`  
path中增加 `%DERBY_HOME%\bin` 

* 配置修改
> hive-site.xml  
```xml
<configuration>
    <property>
      <name>javax.jdo.option.ConnectionURL</name>
      <value>jdbc:derby:/usr/local/hive/metastore_db;databaseName=metastore_db;create=true</value>
    </property>

    <property>
      <name>javax.jdo.option.ConnectionDriverName</name>
      <value>org.apache.derby.jdbc.EmbeddedDriver</value>
    </property>

    <property>
      <name>hive.metastore.warehouse.dir</name>
      <value>/usr/local/hive/warehouse</value>
    </property>
</configuration>
```

* 创建默认derby db schema
```
schematool -initSchema -dbType derby
```

* 使用hive  
```
$ cd
$ hive
hive> show tables;
OK
Time taken: 0.803 seconds
```

#### 4. wordcount使用HQL
```
$ cat 1.txt 2.txt 3.txt 
pobby is a glint girl.
pobby is a cute girl.
pobby is my lovely sister.
```

```
hive> create table wordcount(rowdata string);

hive> load data local inpath '/home/bigdata/tmp/1.txt' into table wordcount;
Loading data to table cc.wordcount
OK
Time taken: 3.344 seconds

hive> load data local inpath '/home/bigdata/tmp/2.txt' into table wordcount;
Loading data to table cc.wordcount
OK
Time taken: 0.32 seconds

hive> load data local inpath '/home/bigdata/tmp/3.txt' into table wordcount;
Loading data to table cc.wordcount
OK
Time taken: 0.177 seconds

hive> select * from wordcount;
OK
pobby is a glint girl.
pobby is a cute girl.
pobby is my lovely sister.
Time taken: 1.563 seconds, Fetched: 3 row(s)

hive> SELECT explode(split(rowdata, ' ')) AS word FROM wordcount;
OK
pobby
is
a
glint
girl.
pobby
is
a
cute
girl.
pobby
is
my
lovely
sister.
Time taken: 0.887 seconds, Fetched: 15 row(s)

hive> SELECT word, count(1) as cnts FROM (select replace(word, '.', '') as word from (SELECT explode(split(rowdata, ' ')) AS word FROM wordcount) t_tmp) t_tmp2 GROUP BY word ORDER BY cnts desc; 
OK
pobby   3
is      3
girl    2
a       2
sister  1
my      1
lovely  1
glint   1
cute    1
Time taken: 49.149 seconds, Fetched: 9 row(s)
```

#### 5. 结果存到HBase

* 下载  
> http://hbase.apache.org/downloads.html  

配置环境变量 `HBASE_HOME`  
path中增加 `%HBASE_HOME%\bin` 

* 配置修改
> hbase-site.xml  
```xml
<configuration>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://localhost:9000/hbase</value>
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/usr/local/hbase/data</value>
    </property>
    <property>
        <name>hbase.master.info.port</name>
        <value>60010</value>
    </property>
    <property>
        <name>hbase.unsafe.stream.capability.enforce</name>
        <value>false</value>
    </property>
</configuration>
```

HIVE与HBASE的通信通过hive-hbase-handler-*.jar实现  
```
cp -arf hive-hbase-handler-3.1.1.jar /usr/local/hbase/lib/
```

* 使用  

在hive中建立结果表
```
hive> CREATE TABLE word_count_result(key string, value int) STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key,cf1:val") TBLPROPERTIES ("hbase.table.name" = "word_count_result", "hbase.mapred.output.outputtable" = "word_count_result");
```
在hive结果表中插入mapred数据
```
hive> insert overwrite table word_count_result SELECT word, count(1) as cnts FROM (select replace(word, '.', '') as word from (SELECT explode(split(rowdata, ' ')) AS word FROM wordcount) t_tmp) t_tmp2 GROUP BY word ORDER BY cnts desc;
```

在hbase中查看数据
```
hbase(main):031:0> list
TABLE                                                                                                                                                                      
word_count_result                                                                                                                                                          
2 row(s)
Took 0.0073 seconds                                                                                                                                                        
=> ["word_count_result"]

hbase(main):030:0> describe 'word_count_result'
Table word_count_result is ENABLED                                                                                                                                         
word_count_result                                                                                                                                                          
COLUMN FAMILIES DESCRIPTION                                                                                                                                                
{NAME => 'cf1', VERSIONS => '1', EVICT_BLOCKS_ON_CLOSE => 'false', NEW_VERSION_BEHAVIOR => 'false', KEEP_DELETED_CELLS => 'FALSE', CACHE_DATA_ON_WRITE => 'false', DATA_BLO
CK_ENCODING => 'NONE', TTL => 'FOREVER', MIN_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', CACHE_INDEX_ON_WRITE => 'false', IN_MEMORY => 'false', CACHE_
BLOOMS_ON_WRITE => 'false', PREFETCH_BLOCKS_ON_OPEN => 'false', COMPRESSION => 'NONE', BLOCKCACHE => 'true', BLOCKSIZE => '65536', METADATA => {'CACHE_DATA_IN_L1' => 'fals
e'}}                                                                                                                                                                       

1 row(s)

QUOTAS                                                                                                                                                                     
0 row(s)
Took 0.0604 seconds

hbase(main):035:0> t.scan
ROW                                         COLUMN+CELL                                                                                                                    
 a                                          column=cf1:val, timestamp=1562120408200, value=2                                                                               
 cute                                       column=cf1:val, timestamp=1562120408200, value=1                                                                               
 girl                                       column=cf1:val, timestamp=1562120408200, value=2                                                                               
 glint                                      column=cf1:val, timestamp=1562120408200, value=1                                                                               
 is                                         column=cf1:val, timestamp=1562120408200, value=3                                                                               
 lovely                                     column=cf1:val, timestamp=1562120408200, value=1                                                                               
 my                                         column=cf1:val, timestamp=1562120408200, value=1                                                                               
 pobby                                      column=cf1:val, timestamp=1562120408200, value=3                                                                               
 sister                                     column=cf1:val, timestamp=1562120408200, value=1                                                                               
9 row(s)
Took 0.0187 seconds

```

------

#### 6. 完整bash_profile示例
```
export HADOOP_HOME="/usr/local/hadoop"
export HIVE_HOME="/usr/local/hive"
export DERBY_HOME="/usr/local/derby"
export HBASE_HOME="/usr/local/hbase"
export CLASSPATH=$CLASSPATH:${HADOOP_HOME}/lib/*:.
export CLASSPATH=$CLASSPATH:${HIVE_HOME}/lib/*:.
export CLASSPATH=$CLASSPATH:${DERBY_HOME}/lib/derby.jar:$DERBY_HOME/lib/derbytools.jar
PATH=${JAVA_HOME}/bin:${HADOOP_HOME}/bin:${HIVE_HOME}/bin:${DERBY_HOME}/bin:${HBASE_HOME}/bin:$PATH:$HOME/.local/bin:$HOME/bin
export PATH
```

------

