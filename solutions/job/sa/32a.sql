SELECT MIN(lt.link) AS link_type,
       MIN(t1.title) AS first_movie,
       MIN(t2.title) AS second_movie
  FROM movie_keyword AS mk JOIN keyword AS k ON mk.keyword_id = k.id JOIN title AS t1 ON t1.id = mk.movie_id JOIN movie_link AS ml ON ml.movie_id = t1.id JOIN title AS t2 ON ml.linked_movie_id = t2.id JOIN link_type AS lt ON lt.id = ml.link_type_id WHERE k.keyword = '10,000-mile-club';