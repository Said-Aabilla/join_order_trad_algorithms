SELECT acc.location, COUNT(*) FROM site AS s, so_user AS u1, question AS q1, answer AS a1, tag AS t1, tag_question AS tq1, badge AS b, account AS acc WHERE s.site_id = q1.site_id AND s.site_id = u1.site_id AND s.site_id = a1.site_id AND s.site_id = t1.site_id AND s.site_id = tq1.site_id AND s.site_id = b.site_id AND q1.id = tq1.question_id AND q1.id = a1.question_id AND a1.owner_user_id = u1.id AND t1.id = tq1.tag_id AND b.user_id = u1.id AND acc.id = u1.account_id AND s.site_name IN ('askubuntu', 'math') AND t1.name IN ('11.10', '12.10', 'compactness', 'dependencies', 'determinant', 'euclidean-geometry', 'graphing-functions', 'internet', 'network-manager', 'power-series', 'predicate-logic', 'python', 'scripts', 'triangles', 'virtualbox') AND q1.score >= 0 AND q1.score <= 0 AND u1.upvotes >= 10 AND u1.upvotes <= 1000000 AND b.name IN ('Announcer', 'Caucus', 'Citizen Patrol', 'Commentator', 'Constituent', 'Excavator', 'Famous Question', 'Good Answer', 'Good Question', 'Notable Question', 'Student', 'Supporter', 'Teacher', 'Yearling') GROUP BY acc.location ORDER BY COUNT(*) DESC LIMIT 100