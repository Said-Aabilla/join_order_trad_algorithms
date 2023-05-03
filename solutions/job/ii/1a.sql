SELECT MIN(mc.note)           AS production_note,
       MIN(t.title)           AS movie_title,
       MIN(t.production_year) AS movie_year
FROM info_type AS it
         JOIN movie_info_idx AS mi_idx ON it.id = mi_idx.info_type_id
         JOIN movie_companies AS mc ON mc.movie_id = mi_idx.movie_id
         JOIN company_type AS ct ON ct.id = mc.company_type_id
         JOIN title AS t ON t.id = mc.movie_id And t.id = mi_idx.movie_id
WHERE ct.kind = 'production companies'
  AND it.info = 'top 250 rank'
  AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%'
  AND (mc.note LIKE '%(co-production)%' OR mc.note LIKE '%(presents)%');