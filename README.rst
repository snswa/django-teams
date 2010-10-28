==============
 django-teams
==============


This app provides a hierarchical team structure, built for use on a social
action website.

The first versions focus on the following model.  Future versions may add
some capability for customizable roles other than "member" and "manager".


Example hierarchy
=================

Given this hierarchy of teams:

- org

  - org.alpha

  - org.beta

    - org.beta.x

  - org.gamma

    - org.gamma.y

    - org.gamma.z

If a user is a member of a team, they are de facto members of all ancester and
descendant teams. If a user were a member of org.gamma above, they would also
be de facto members of org, org.gamma.y, and org.gamma.z, but not any of the
other org.* teams.

If a user is a manager of a team, they are de fact managers of all descendant
teams.  If a user were a manager of org.beta above, they would also be de
facto manager of org.beta.x, but not org or any other team.
