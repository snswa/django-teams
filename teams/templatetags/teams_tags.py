from django import template
from django.template import NodeList, Variable, VariableDoesNotExist

from featureflipper.models import Feature


register = template.Library()


@register.tag
def teammember(parser, token):
    try:
        tag_name, team = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{0} tag requires a single argument'.format(token.contents.split()[0]))
    end_tag = 'endteammember'
    non_tag = 'nonmember'
    nodelist_member = parser.parse((non_tag, end_tag))
    token = parser.next_token()
    if token.contents == non_tag:
        nodelist_nonmember = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_nonmember = NodeList()
    return TeamMemberNode(team, nodelist_member, nodelist_nonmember)


class TeamMemberNode(template.Node):

    def __init__(self, team, nodelist_member, nodelist_nonmember):
        self.team = Variable(team)
        self.nodelist_member = nodelist_member
        self.nodelist_nonmember = nodelist_nonmember

    def render(self, context):
        try:
            team = self.team.resolve(context)
        except VariableDoesNotExist:
            is_member = False
        else:
            user = context.get('user')
            if not user.is_authenticated:
                is_member = False
            else:
                is_member = team.user_is_member(user)
        if is_member:
            return self.nodelist_member.render(context)
        else:
            return self.nodelist_nonmember.render(context)
