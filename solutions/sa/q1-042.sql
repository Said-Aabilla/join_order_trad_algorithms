SELECT COUNT(*) FROM site AS s, question AS q, tag_question AS tq, tag AS t WHERE s.site_name = 'stackoverflow' AND t.name = 'rowid' AND t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id