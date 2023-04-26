SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('stackoverflow') AND t.name IN ('android-layout', 'angular', 'google-chrome', 'haskell', 'ios', 'java', 'language-agnostic', 'linux', 'maven', 'pandas', 'python-3.x', 'rest', 'ruby-on-rails', 'string', 'unit-testing') AND q.favorite_count >= 5 AND q.favorite_count <= 5000