SELECT COUNT(DISTINCT(acc.display_name)) FROM account AS acc, so_user AS u, badge AS b1, badge AS b2 WHERE acc.website_url <> '' AND acc.id = u.account_id AND b1.site_id = u.site_id AND b1.user_id = u.id AND b1.name = 'Custodian' AND b2.site_id = u.site_id AND b2.user_id = u.id AND b2.name = 'Sheriff' AND b2.date > b1.date