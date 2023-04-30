SELECT COUNT(DISTINCT(acc.display_name)) FROM so_user AS u1, site AS s1, tag_question AS tq1, account AS acc, question AS q1, tag AS t1, answer AS a1 WHERE s1.site_name = 'drupal' AND t1.name = 'theming' AND t1.site_id = s1.site_id AND q1.site_id = s1.site_id AND tq1.site_id = s1.site_id AND tq1.question_id = q1.id AND tq1.tag_id = t1.id AND a1.site_id = q1.site_id AND a1.question_id = q1.id AND a1.owner_user_id = u1.id AND a1.site_id = u1.site_id AND a1.creation_date >= q1.creation_date AND acc.id = u1.account_id