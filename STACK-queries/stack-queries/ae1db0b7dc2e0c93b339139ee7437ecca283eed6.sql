SELECT t1.name, COUNT(*) FROM site AS s, so_user AS u1, question AS q1, answer AS a1, tag AS t1, tag_question AS tq1 WHERE q1.owner_user_id = u1.id AND a1.question_id = q1.id AND a1.owner_user_id = u1.id AND s.site_id = q1.site_id AND s.site_id = a1.site_id AND s.site_id = u1.site_id AND s.site_id = tq1.site_id AND s.site_id = t1.site_id AND q1.id = tq1.question_id AND t1.id = tq1.tag_id AND s.site_name IN ('pt') AND t1.name IN ('angular', 'asp.net', 'c++', 'delphi', 'laravel', 'node.js', 'orientação-a-objetos', 'postgresql', 'python-3.x', 'query', 'regex', 'string', 'winforms', 'wordpress', 'xml') AND q1.view_count >= 10 AND q1.view_count <= 1000 AND u1.upvotes >= 0 AND u1.upvotes <= 1 GROUP BY t1.name