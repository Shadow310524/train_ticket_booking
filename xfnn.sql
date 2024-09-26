use train_ticket_booking;
create table ticket_details(username varchar(30),train_id int,train_name varchar(30),departure varchar(30),arrival varchar(30),departure_time time,arrival_time time,duration time,dateoftravel date,selected_seat_class varchar(30));
select * from ticket_details;