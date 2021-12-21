/* version 1.0 */

/* create table */
create table navermapcoordinate(
  area varchar2(100),
  lat float,
  lng float
)

/* insert column */
insert into navermapcoordinate (area, lat, lng) values ('서울','37.5557776885486','126.985070087077');
insert into navermapcoordinate (area, lat, lng) values ('춘천','37.8913193660305','127.735243066563');
insert into navermapcoordinate (area, lat, lng) values ('울릉도','37.4899660054861','130.93944212844');
insert into navermapcoordinate (area, lat, lng) values ('강릉','37.7249865587184','128.859629245075');
insert into navermapcoordinate (area, lat, lng) values ('백령도','37.9621401000847','124.657579803005');
insert into navermapcoordinate (area, lat, lng) values ('대전','36.3806654031377','127.41984913426');
insert into navermapcoordinate (area, lat, lng) values ('청주','36.6267556309948','127.496515899621');
insert into navermapcoordinate (area, lat, lng) values ('대구','35.8638923944849','128.574044241117');
insert into navermapcoordinate (area, lat, lng) values ('전주','35.8309974443219','127.142023264096');
insert into navermapcoordinate (area, lat, lng) values ('광주','35.206603946237','126.866098962607');
insert into navermapcoordinate (area, lat, lng) values ('부산','35.2015657945284','129.058064836969');
insert into navermapcoordinate (area, lat, lng) values ('제주','33.4149082547921','126.795593265549');


/* 추가 insert 구문 예비용 */
insert into navermapcoordinate (area, lat, lng) values ();
