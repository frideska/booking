from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import SportsGroup, Membership, Invitation
from .forms import NewInvitationForm


@login_required
def group_index(request, slug):
    return redirect('group_members', slug=slug)


@login_required
def members(request, slug):
    group = get_object_or_404(SportsGroup, slug=slug)
    invitations = Invitation.objects.filter(group=group.pk)
    members = Membership.objects.filter(group=group.pk)
    return render(request, 'groups/members.html', {
        'group': group,
        'members': members,
        'total_members': len(members),
        'total_invitations': len(invitations),
        'slug': slug,
        'active_tab': 'members',

    })

@login_required
def invitations(request, slug):
    group = get_object_or_404(SportsGroup, slug=slug)
    invitations = Invitation.objects.filter(group=group.pk)
    members = Membership.objects.filter(group=group.pk)
    return render(request, 'groups/invitations.html', {
        'group': group,
        'invitations': invitations,
        'total_invitations': len(invitations),
        'total_members': len(members),
        'slug': slug,
        'active_tab': 'invitations',
    })


@login_required
def invite_member(request, slug):
    groups = SportsGroup.objects.filter(slug=slug)
    if (len(groups) != 1):
        raise Http404("Group does not exist")
    group = groups[0]

    if request.method == 'POST':
        form = NewInvitationForm(request.POST, slug=slug)
        if form.is_valid():
            invitation = form.save()
            # TODO: change to redirect to 'group_invitations'
            return redirect('group_members', slug=slug)
    else:
        form = NewInvitationForm(slug=slug)

    # render group form
    return render(request, 'groups/invite_member.html', {
        'group': group,
        'slug': slug,
        'form': form,
    })


def list_groups(request):
    return render(request, 'groups/list_groups.html')
