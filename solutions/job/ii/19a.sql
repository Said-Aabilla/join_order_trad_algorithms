SELECT MIN(n.name) AS voicing_actress,
       MIN(t.title) AS voiced_movie
  FROM movie_info AS mi JOIN cast_info AS ci ON mi.movie_id = ci.movie_id JOIN movie_companies AS mc ON mc.movie_id = mi.movie_id And  mc.movie_id = ci.movie_id JOIN company_name AS cn ON cn.id = mc.company_id JOIN info_type AS it ON it.id = mi.info_type_id JOIN title AS t ON t.id = mi.movie_id And  t.id = ci.movie_id And  t.id = mc.movie_id JOIN role_type AS rt ON rt.id = ci.role_id JOIN name AS n ON n.id = ci.person_id JOIN aka_name AS an ON n.id = an.person_id And  ci.person_id = an.person_id JOIN char_name AS chn ON chn.id = ci.person_role_id WHERE ci.note IN ('(voice)', '(voice: Japanese version)', '(voice) (uncredited)', '(voice: English version)') AND cn.country_code = '[us]' AND it.info = 'release dates' AND (mc.note LIKE '%(USA)%' OR mc.note LIKE '%(worldwide)%') AND (mi.info LIKE 'Japan:%200%' OR mi.info LIKE 'USA:%200%') AND n.gender = 'f' AND n.name LIKE '%Ang%' AND rt.role = 'actress' AND t.production_year BETWEEN 2005 AND 2009;