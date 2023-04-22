SELECT COUNT(*)
FROM
site as s,
so_user as u1,
question as q1,
answer as a1,
tag as t1,
tag_question as tq1,
badge as b,
account as acc
WHERE
s.site_id = q1.site_id
AND s.site_id = u1.site_id
AND s.site_id = a1.site_id
AND s.site_id = t1.site_id
AND s.site_id = tq1.site_id
AND s.site_id = b.site_id
AND q1.id = tq1.question_id
AND q1.id = a1.question_id
AND a1.owner_user_id = u1.id
AND t1.id = tq1.tag_id
AND b.user_id = u1.id
AND acc.id = u1.account_id
AND (s.site_name in ('gamedev','judaism','security','softwareengineering','travel'))
AND (t1.name in ('2d','air-travel','encryption','halacha','minhag','network','parshanut-torah-comment','php','shabbat','transit','uk','unity','usa','visas'))
AND (q1.score >= 1)
AND (q1.score <= 10)
AND (u1.reputation >= 0)
AND (u1.reputation <= 10)
AND (b.name in ('Autobiographer','Editor','Informed','Student'))
