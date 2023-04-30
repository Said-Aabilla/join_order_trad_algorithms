SELECT COUNT(*) FROM question AS q, site AS s, tag_question AS tq, tag AS t WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('stackoverflow') AND t.name IN ('blade', 'html5-audio', 'specflow', 't4') AND q.score >= 0 AND q.score <= 5;