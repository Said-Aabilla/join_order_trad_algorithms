SELECT COUNT(DISTINCT (acc.id))
FROM account AS acc,
     site AS s,
     so_user AS u,
     question AS q,
     post_link AS pl,
     tag AS t,
     tag_question AS tq
WHERE s.site_name = 'stackoverflow'
  AND s.site_id = q.site_id
  AND pl.site_id = q.site_id
  AND pl.post_id_to = q.id
  AND t.name = 'regex-group'
  AND t.site_id = q.site_id
  AND q.creation_date > '2016-01-01'
  AND tq.site_id = t.site_id
  AND tq.tag_id = t.id
  AND tq.question_id = q.id
  AND q.owner_user_id = u.id
  AND q.site_id = u.site_id
  AND u.reputation > 112
  AND acc.id = u.account_id
  AND acc.website_url <> ''