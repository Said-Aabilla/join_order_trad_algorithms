SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('mathematica') AND t.name IN ('dynamic', 'evaluation', 'export', 'fitting', 'front-end', 'graphics3d', 'image-processing', 'import', 'linear-algebra', 'manipulate', 'probability-or-statistics', 'programming', 'special-functions', 'symbolic') AND q.score >= 1 AND q.score <= 10