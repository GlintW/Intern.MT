#### name_table
```sql
-- ----------------------------
-- Table structure for name_table
-- ----------------------------
DROP TABLE IF EXISTS `name_table`;
CREATE TABLE `name_table` (
  `no` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of name_table
-- ----------------------------
INSERT INTO `name_table` VALUES ('1', 'aa');
INSERT INTO `name_table` VALUES ('2', 'bb');
INSERT INTO `name_table` VALUES ('3', 'cc');
```

|no|name|
|---|---|
|1|aa|
|2|bb|
|3|cc|


#### score_table
```sql
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for score_table
-- ----------------------------
DROP TABLE IF EXISTS `score_table`;
CREATE TABLE `score_table` (
  `no` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of score_table
-- ----------------------------
INSERT INTO `score_table` VALUES ('1', '100');
INSERT INTO `score_table` VALUES ('3', '80');
INSERT INTO `score_table` VALUES ('4', '50');
```

|no|score|
|---|---|
|1|100|
|3|80|
|4|50|


#### left join
```sql
SELECT * FROM `name_table`
LEFT JOIN score_table
ON name_table.`no` = score_table.`no`
ORDER BY name_table.`no`;
```
|no|name|no1|score|
|---|---|---|---|
|1|aa|1|100|
|2|bb|null|null|	
|3|cc|3|80|
#### right join
```sql
SELECT * FROM `name_table`
RIGHT JOIN score_table
ON name_table.`no` = score_table.`no`
ORDER BY score_table.`no`;
```
|no|name|no1|score|
|---|---|---|---|
|1|aa|1|100|
|3|cc|3|80|
|null|null|4|50|
#### inner join
```sql
SELECT * FROM `name_table`
INNER JOIN score_table
ON name_table.`no` = score_table.`no`;
```
|no|name|no1|score|
|---|---|---|---|
|1|aa|1|100|
|3|cc|3|80|
#### full join (mysql不支持, 需分别left和right关联后再union)
```sql
SELECT * FROM `name_table`
LEFT JOIN score_table
ON name_table.`no` = score_table.`no`
UNION 
SELECT * FROM `name_table`
RIGHT JOIN score_table
ON name_table.`no` = score_table.`no`
```
|no|name|no1|score|
|---|---|---|---|
|1|aa|1|100|
|2|bb|null|null|	
|3|cc|3|80|
|null|null|4|50|
