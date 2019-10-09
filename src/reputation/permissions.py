from rest_framework.permissions import BasePermission, SAFE_METHODS


class RuleBasedPermission(BasePermission):
    class Meta:
        abstract = True

    def has_permission(self, request, view):
        if self.is_read_only_request(request):
            return True
        return self.satisfies_rule(request)

    def is_read_only_request(self, request):
        return request.method in SAFE_METHODS

    def satisfies_rule(self, request):
        raise NotImplementedError


class CreateDiscussionThread(RuleBasedPermission):
    message = 'Not enough reputation to create thread.'

    def satisfies_rule(self, request):
        return request.user.reputation >= 1


class CreateDiscussionComment(RuleBasedPermission):
    message = 'Not enough reputation to create comment.'

    def satisfies_rule(self, request):
        return request.user.reputation >= 1


class CreatePaper(RuleBasedPermission):
    message = 'Not enough reputation to upload paper.'

    def satisfies_rule(self, request):
        return request.user.reputation >= 1


class UpvoteDiscussionComment(RuleBasedPermission):
    message = 'Not enough reputation to upvote comment.'

    def satisfies_rule(self, request):
        return request.user.reputation >= 1


class UpvoteDiscussionThread(RuleBasedPermission):
    message = 'Not enough reputation to upvote thread.'

    def satisfies_rule(self, request):
        return request.user.reputation >= 1


class UpvotePaper(RuleBasedPermission):
    message = 'Not enough reputation to upvote paper.'

    def satisfies_rule(self, request):
        return request.user.reputation >= 1
