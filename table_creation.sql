create database yet_another_split;

use yet_another_split;

create table users (

user_id int primary key auto_increment,
first_name varchar(255) not null,
last_name varchar(255) not null,
email varchar(255) not null,
created_at datetime default current_timestamp

);

create table friends (

user_id int not null,
friend_user_id int not null,
added_at datetime default current_timestamp,
foreign key (user_id) references users(user_id),
foreign key (friend_user_id) references users(user_id)	


);

create table expenses (

expense_id int primary key auto_increment,
added_by int not null,
expense_description varchar(255) not null,
amount decimal(10, 2) not null,
foreign key (added_by) references users(user_id)

);

create table splits(

expense_id int not null,
user_id int not null,
amountper_person decimal(10, 2) not null,
foreign key (expense_id) references expenses(expense_id),
foreign key (user_id) references users(user_id)


);
