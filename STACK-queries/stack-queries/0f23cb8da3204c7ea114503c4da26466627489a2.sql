SELECT COUNT(*) FROM tag AS t, site AS s, question AS q, tag_question AS tq WHERE t.site_id = s.site_id AND q.site_id = s.site_id AND tq.site_id = s.site_id AND tq.question_id = q.id AND tq.tag_id = t.id AND s.site_name IN ('physics') AND t.name IN ('atomic-physics', 'differentiation', 'electric-current', 'heisenberg-uncertainty-principle', 'inertial-frames', 'material-science', 'nuclear-physics', 'quantum-electrodynamics', 'reflection', 'soft-question', 'solid-state-physics', 'tensor-calculus', 'torque', 'universe') AND q.score >= 0 AND q.score <= 5