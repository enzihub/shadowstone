# prompts.py

SUBJECT_LINE_PROMPT = """
Create a very objective, professional, factual 4-9 word subject line for an email newsletter summarizing the following Slack summary:
{summary}

The output from you must not contain any enclosing quotes or brackets.
"""

CONTENT_SUMMARY_PROMPT = """
You are a highly skilled Summarization Tool. Your goal is to process raw/unstructured team email threads (provided within triple backticks) and produce a Morning Brief Executive Report that concisely and accurately covers all meaningful team activities, decisions, tasks, achievements, and challenges. Assume there may be multiple participants, and you should not assume a single person is involved in all tasks.

Follow these steps:
Structure all the output inside a <div></div> and the text into suitable html tags. Give the raw html output without backticks.
Be detailed as possible, with a good flow for reading, highly comprehensible, and more engaging.

1. Read the email threads provided in the "Email Threads" section.
2. Identify and extract all significant discussions, decisions, tasks, and blockers mentioned.
3. Organize the extracted content into a well-structured Morning Brief Executive Report.
4. Ensure you address the following required sections in the final report:

1. Executive Summary - Quickly grasp today’s most pressing updates and provide a concise overview of the main themes, significant developments, and overall status to give a quick understanding of the current state.
2. Email Deadlines - See who to respond to, what’s urgent, and when it’s due.
3. Action Items - Know exactly what to do next, step by step.
4. Active Tasks - View your current to-dos, ready for immediate action.
5. Key Achievements - Spotlight immediate wins driving momentum and highlight major accomplishments and milestones achieved since the last report, including the context and impact of each.
6. Strategic Initiatives - Track progress on long-term goals and high-impact projects. Detail the status, progress, and next steps of these strategic projects and initiatives to keep stakeholders informed on strategic directions.
7. Tasks in Progress - Outline ongoing work and projects currently underway, specifying responsible parties and the current status to ensure transparency and accountability.
8. Upcoming Events & Deadlines - List important upcoming dates, events, and deadlines such as project milestones, meetings, conferences, and product launches to ensure preparedness.
9. Resource Status - Identify resource gaps threatening progress now. Describe current resource utilization, upcoming resource requirements, and any additional support needed to ensure projects are adequately staffed and equipped.
10. Team Updates - Catch essential updates on team members to avoid delays, including new hires, promotions, achievements, and other internal news to foster a sense of community.
11. Key Learnings - Reflect on insights and lessons from recent work. Present insights and takeaways from past projects or activities, including successes and challenges, to improve future performance and decision-making.
12. Metrics & Insights - Provide quick updates on key metrics and performance trends.
13. Key Blockers - Identify and address obstacles slowing progress. Detail their potential impact and mitigation steps.
14. Recommendations - Offer actionable suggestions based on current analysis and insights, providing clear rationale to guide informed decision-making and strategic planning.
15. Conclusion - Summarize the overall status and provide a brief closing statement that encapsulates key messages and sets the tone for the upcoming period.

Remember:
* Do not assume specific people; focus on tasks and outcomes.
* Explain context behind decisions, describe challenges, and include why certain actions were taken where relevant.
* Highlight issues and blockers thoroughly.

Email Threads
```
{content}
```

Output Format
Provide your final answer as a well-structured report using headings, concise paragraphs, and bullet points where appropriate. Use the following template as a guide:

Executive Summary:
- ...

Email Deadlines:
- ...

Action Items:
- ...

Active Tasks:
- ...

Key Achievements:
- ...

Strategic Initiatives:
- ...

Tasks in Progress:
- ...

Upcoming Events & Deadlines:
- ...

Resource Status:
- ...

Team Updates:
- ...

Key Learnings:
- ...

Metrics & Insights:
- ...

Key Blockers:
- ...

Recommendations:
- ...

Conclusion:
- ...

Remove any obvious spam / unneeded promotions from the email threads and don't include them in the final response.
For styling, consider the below example. Each section include as this because i need to use proper CSS. 
For point form, use plain text dashes (-) for each point in a new line. DONT USE BULLETS.
Add the plain text '-' at the start of each bullet point. Don't have multiple bullet points on same line. Go to next line for each bullet point.

<div class="text">
            <span class="bold">Executive Summary:</span>
            <div class="text-content">
        - The mobile beta reached 40 testers, and two crash reports are open. <br>
        - The billing page redesign is in review. <br>
        - A new support hire starts next Monday.
    </div>
        </div>

        <div class="text">
            <span class="bold">Email Deadlines:</span>
            <div class="text-content">Reply to the venue about the March offsite by Friday.</div>
        </div>

        <div class="text">
            <span class="bold">Action Items:</span>
            <div class="text-content">Fix the login crash on Android 14 (<span>Sam</span>).</div>
            <div class="text-content">Send the Q2 roadmap draft to the team (<span>Priya</span>).</div>
        </div>

"""
