from sqldb import db, Student_details

#creates all the tables
db.create_all()

#create the role objects
user_johnmicheal = Student_details('2015030171704', 'Johnmicheal', 'Uzendu', 500, 'Computer Engineering')
user_ezinne = Student_details('2013030170111', 'Ezinne', 'Uzendu', 600, 'Medicine')
user_uche = Student_details('2019030171222', 'Uchechukwu', 'Uzendu', 100, 'Accountancy')


#add details and commit to db
db.session.add_all([user_ezinne, user_johnmicheal, user_uche])
db.session.commit()

print(user_johnmicheal.regnumber)

