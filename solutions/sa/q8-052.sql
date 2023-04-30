SELECT COUNT(DISTINCT(q1.id)) FROM comment AS c1, tag AS t, comment AS c2, tag_question AS tq1, site AS s, question AS q2, question AS q1, post_link AS pl, tag_question AS tq2 WHERE s.site_name = 'german' AND pl.site_id = s.site_id AND pl.site_id = q1.site_id AND pl.post_id_from = q1.id AND pl.site_id = q2.site_id AND pl.post_id_to = q2.id AND c1.site_id = q1.site_id AND c1.post_id = q1.id AND c2.site_id = q2.site_id AND c2.post_id = q2.id AND c1.date > c2.date AND t.name IN ('string', 'spring') AND t.id = tq1.tag_id AND t.site_id = tq1.site_id AND t.id = tq2.tag_id AND t.site_id = tq1.site_id AND t.site_id = pl.site_id AND tq1.site_id = q1.site_id AND tq1.question_id = q1.id AND tq2.site_id = q2.site_id AND tq2.question_id = q2.id