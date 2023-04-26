SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('gaming') AND t.name IN ('achievements', 'diablo-3', 'pokemon-go', 'starcraft-2', 'xbox-360') AND q.score >= 1 AND q.score <= 10