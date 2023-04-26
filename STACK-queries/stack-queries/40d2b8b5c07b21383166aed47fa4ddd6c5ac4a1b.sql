SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('stats') AND t.name IN ('autocorrelation', 'descriptive-statistics', 'expected-value', 'experiment-design', 'interaction', 'interpretation', 'mean', 'optimization', 'pdf', 'poisson-distribution', 'random-variable', 'simulation', 'spss', 'survival', 'terminology') AND q.view_count >= 10 AND q.view_count <= 1000