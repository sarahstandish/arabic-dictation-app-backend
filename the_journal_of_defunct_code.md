Old, nonworking, or experimental code snippets from the project

words = Word.query.filter(Word.unvoweled_word.like('%ا%')).all() # works
words = Word.query.filter(Word.unvoweled_word.contains('ا')).all() # works
words = Word.query.filter(not_(Word.unvoweled_word.contains('ا'))).all() # works
words = Word.query.filter(Word.unvoweled_word.contains('ا'), Word.unvoweled_word.contains('ب')).all() # works
words = Word.query.filter(not_(Word.unvoweled_word.contains('ا')), not_(Word.unvoweled_word.contains('ب'))).all() # works, each 'contains' must be canceled separately
words = Word.query.filter(Word.unvoweled_word.contains('ا', 'ب')).all() # does not work
words = Word.query.filter(Word.unvoweled_word.like('%[ا-ب]%')).all() # does not work
words = Word.query.filter(Word.unvoweled_word.like('%(ا|ب)%')).all() # does not work
sql_query = sqlalchemy.text("select * from words where unvoweled_word not similar to '%(\u0623)%'") # worked

# SQL queries tried
`select * from words where unvoweled_word like '%ب%';` success
`select * from words where unvoweled_word like '%ب%' and unvoweled_word like '%ت%';` success
`select * from words where unvoweled_word like '%ب%' and unvoweled_word like '%ت%' and unvoweled_word like '%ث%';` success
`select * from words where unvoweled_word like '%ب%ت%ث%';` failed, zero rows returned; maybe this is stating the order
`select * from words where unvoweled_word like '%ب%ث%';` successful only in a limited sense, this only returned strings with the letters in this order
`select * from words where unvoweled_word like '%ب% || %ث%';` unsuccessful, zero rows
`select * from words where unvoweled_word like '%ب || ث%';` unsuccessful, zero rows
`select * from words where unvoweled_word like '%[ا-ب]%';` unsuccessful, zero rows
`select * from words where unvoweled_word like '%[اب]%';` unsuccessful, zero rows
`select * from words where unvoweled_word like '%[ا]%';` unsuccessful, zero rows
`select * from words where unvoweled_word like '[ا]%';` unsuccessful, zero rows
`select * from words where unvoweled_word similar to '%ا%';` successful
`select * from words where unvoweled_word not similar to '%ا%';` successful
`select * from words where unvoweled_word similar to '%(ا|ب)%';` successful
`select * from words where unvoweled_word not similar to '%(ا|ب)%';` successful!!
`select * from words where unvoweled_word not similar to '%(ا|ب|ت)%';` successful!!
`select * from words where unvoweled_word like '%(ا|ب)%';` # unsuccessful

# Possible query patterns for Flask/Postgres
Found in https://docs.sqlalchemy.org/en/14/orm/query.html
`q = session.query(User).filter(User.name.like('e%'))`
`sqlalchemy.orm.Query.params(*args, **kwargs)` Not sure if I could use this to simplify the query?
Performing multiple queries and then finding the union:
  `q1 = sess.query(SomeClass).filter(SomeClass.foo=='bar')`
  `q2 = sess.query(SomeClass).filter(SomeClass.bar=='foo')`
  `q3 = q1.union(q2)`
  Would I need to perform multiple queries and then find the union?
It seems like it would make more sense to filter out the unwanted letters, than to filter for the wanted letters, given than I don't necessarily want only those letters...but at least I know that it would make sense in the future, if I have a "must use" letter, it would be easy to select for it.
`sqlalchemy.sql.expression.ColumnOperators.contains(other, **kwargs)`
`Note.query.filter(Note.message.match("%somestr%")).all()` (from https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement)
`Model.query.filter(Model.columnName.contains('sub_string'))` or 
`Model.query.filter(not_(Model.columnName.contains('sub_string')))` from https://stackoverflow.com/questions/4926757/sqlalchemy-query-where-a-column-contains-a-substring
