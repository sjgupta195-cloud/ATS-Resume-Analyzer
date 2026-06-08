from semantic_match import semantic_similarity


def smart_skill_match(
        resume_skills,
        jd_skills,
        threshold=0.65
):

    matched = []

    for jd_skill in jd_skills:

        for resume_skill in resume_skills:

            score = semantic_similarity(
                jd_skill,
                resume_skill
            )

            if score >= threshold:
                if jd_skill not in matched:
                    matched.append(jd_skill)
                
                break

    return matched
