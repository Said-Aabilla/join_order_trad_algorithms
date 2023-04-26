SELECT COUNT(DISTINCT (q1.id))
FROM site AS s,
     post_link AS pl,
     question AS q1,
     question AS q2,
     comment AS c1,
     comment AS c2,
     tag AS t,
     tag_question AS tq1,
     tag_question AS tq2
WHERE s.site_name = 'german'
  AND pl.site_id = s.site_id
  AND pl.site_id = q1.site_id
  AND pl.post_id_from = q1.id
  AND pl.site_id = q2.site_id
  AND pl.post_id_to = q2.id
  AND c1.site_id = q1.site_id
  AND c1.post_id = q1.id
  AND c2.site_id = q2.site_id
  AND c2.post_id = q2.id
  AND c1.date > c2.date
  AND t.name IN ('ruby', 'html')
  AND t.id = tq1.tag_id
  AND t.site_id = tq1.site_id
  AND t.id = tq2.tag_id
  AND t.site_id = tq1.site_id
  AND t.site_id = pl.site_id
  AND tq1.site_id = q1.site_id
  AND tq1.question_id = q1.id
  AND tq2.site_id = q2.site_id
  AND tq2.question_id = q2.id