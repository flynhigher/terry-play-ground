from django import template

register = template.Library()

def show_judge(judge, myjudge, user_logged_in):
    return {"judge": judge, "myjudge": myjudge, "user_logged_in": user_logged_in}
register.inclusion_tag("judge_item.html")(show_judge)

def show_judge_short(judge):
    return {"judge": judge}
register.inclusion_tag("judge_short.html")(show_judge_short)
