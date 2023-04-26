SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('stackoverflow') AND t.name IN ('action', 'applet', 'curl', 'cygwin', 'html-table', 'http-headers', 'jdbc', 'plugins', 'processing', 'sap', 'shell', 'uicollectionview', 'variadic-templates', 'xhtml') AND q.view_count >= 10 AND q.view_count <= 1000