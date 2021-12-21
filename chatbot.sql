/* version 1.0 */

/* create table */
create table chatbot(
  request varchar2(100),
  rule varchar2(100),
  response varchar2(100)
)

/* insert column */
insert into chatbot (request, rule, response) values ('너의 이름은?',	'너|이름',	'저는 자비스라고 합니다.');
insert into chatbot (request, rule, response) values ('네 이름을 말해줘',	'네|이름|말해',	'저는 자비스라고 합니다');
insert into chatbot (request, rule, response) values ('네 이름이 뭐니?',	'네|이름|뭐',	'저는 자비스라고 합니다');
insert into chatbot (request, rule, response) values ('놀러가고 싶다',	'놀러|싶',	'가끔씩 휴식하는 것도 좋죠');
insert into chatbot (request, rule, response) values ('느그 아부지 뭐하시노',	'느그|아부지|뭐하',	'우리 아부지 건달입니다');
insert into chatbot (request, rule, response) values ('말귀좀 알아듣는다?',	'말귀|알아듣는다',	'다행이네요. 열심히 배우고 있어요',);
insert into chatbot (request, rule, response) values ('맛저해',	'맛저해',	'맛저하세요~');
insert into chatbot (request, rule, response) values ('맛점해',	'맛점해',	'맛점하세요~');
insert into chatbot (request, rule, response) values ('메리크리스마스',	'메리|크리',	'메리~ 크리스마스~');
insert into chatbot (request, rule, response) values ('면접에서 떨어졌어',	'면접|떨어',	'다음엔 꼭 붙을 수 있을거에요');
insert into chatbot (request, rule, response) values ('무슨 말인지 모르겠어',	'무슨|말|모르',	'죄송해요 학습이 덜 됐나봐요');
insert into chatbot (request, rule, response) values ('뭐해?',	'뭐해',	'그냥 있어요');
insert into chatbot (request, rule, response) values ('아 월요일이 다가온다',	'월요일|다가',	'월요병이 심한가봐요');
insert into chatbot (request, rule, response) values ('안녕',	'안녕',	'안녕하세요');
insert into chatbot (request, rule, response) values ('영화 추천해줘',	'영화|추천',	'아이언맨 시리즈와 어벤져스 시리즈를 보세요');
insert into chatbot (request, rule, response) values ('1조 멤버 알려줘',	'1조|멤버|알려',	'1조원은 강재균,이성찬,정훈오,김기환 입니다');
insert into chatbot (request, rule, response) values ('ㅋㅋㅋ',	'ㅋㅋㅋ',	'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ');
insert into chatbot (request, rule, response) values ('서울 맛집 알려줘',	'서울|맛집',	'서울 맛집 입니다.');


/* 추가 insert 구문 예비용 */
insert into chatbot (request, rule, response) values ();
