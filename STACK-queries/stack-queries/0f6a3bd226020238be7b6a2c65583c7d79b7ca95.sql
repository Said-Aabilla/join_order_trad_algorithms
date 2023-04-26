SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('stackoverflow') AND t.name IN ('bar-chart', 'converter', 'firemonkey', 'gradient', 'grouping', 'gruntjs', 'inversion-of-control', 'keras', 'marshalling', 'message-queue', 'plist', 'sql-injection', 'submit', 'trigonometry', 'user-input') AND q.score >= 0 AND q.score <= 1000