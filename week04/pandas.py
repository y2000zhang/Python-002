# 1. SELECT * FROM data;
data

# 2. SELECT * FROM data LIMIT 10;
data[0:10]

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
data["id"]

# 4. SELECT COUNT(id) FROM data;
data["id"].count()

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
data[(data["id"] < 1000) & (data["age"] > 30)]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
table1.groupby('id').aggregate({'order_id': pd.Series.nunique})

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(table1, table2, on='id', how='inner')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([table1, table2])

# 9. DELETE FROM table1 WHERE id=10;
table1.drop(table1[table1["id"].isin([10])].index).reset_index()  # table1不改变实际结构
table1.drop(table1[table1["id"].isin([10])].index, axis=0, inplace=True)  # table1改变实际结构

# 10. ALTER TABLE table1 DROP COLUMN column_name;
table1.drop('A', axis=1)  # table1不改变实际结构
table1.drop('A', axis=1, inplace=True)  # table1改变实际结构

